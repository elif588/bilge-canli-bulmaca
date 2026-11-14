import asyncio
import json
import logging
import os
from typing import Set

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from TikTokLive import TikTokLiveClient
from TikTokLive.events import CommentEvent, GiftEvent, LikeEvent, ConnectEvent, DisconnectEvent

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("bilge-live")

app = FastAPI(title="BİLGE Canlı Bulmaca API", version="1.0.0")

# The browser game is hosted on this GitHub Pages origin.
ALLOWED_ORIGINS = {
    "https://elif588.github.io",
    "http://localhost",
    "http://127.0.0.1",
}

connected_sockets: Set[WebSocket] = set()
active_client = None
active_username = None
client_task = None
client_lock = asyncio.Lock()


async def broadcast(payload: dict) -> None:
    message = json.dumps(payload, ensure_ascii=False)
    stale = []
    for socket in list(connected_sockets):
        try:
            await socket.send_text(message)
        except Exception:
            stale.append(socket)
    for socket in stale:
        connected_sockets.discard(socket)


@app.get("/")
async def root():
    return {"service": "BILGE Canli Bulmaca", "status": "ok", "websocket": "/ws"}


@app.get("/health")
async def health():
    return JSONResponse({"ok": True, "tiktok_connected": bool(active_client and getattr(active_client, 'connected', False)), "username": active_username})


async def start_tiktok(username: str) -> None:
    global active_client, active_username, client_task

    async with client_lock:
        if active_client is not None and active_username == username and client_task and not client_task.done():
            await broadcast({"type": "status", "text": "● TIKTOK BAĞLANTISI ZATEN AÇIK"})
            return

        if active_client is not None:
            try:
                await active_client.stop()
            except Exception:
                logger.exception("Previous TikTok client stop failed")
            active_client = None
            active_username = None

        client = TikTokLiveClient(unique_id=username)
        active_client = client
        active_username = username

        @client.on(ConnectEvent)
        async def on_connect(event: ConnectEvent):
            logger.info("TikTok connected: @%s", username)
            await broadcast({"type": "connected", "username": username})

        @client.on(DisconnectEvent)
        async def on_disconnect(event: DisconnectEvent):
            logger.info("TikTok disconnected: @%s", username)
            await broadcast({"type": "status", "text": "● TIKTOK BAĞLANTISI KESİLDİ"})

        @client.on(CommentEvent)
        async def on_comment(event: CommentEvent):
            user = getattr(event.user, "nickname", None) or getattr(event.user, "unique_id", "İzleyici")
            await broadcast({"type": "comment", "user": str(user), "text": str(event.comment)})

        @client.on(LikeEvent)
        async def on_like(event: LikeEvent):
            # TikTok may batch multiple likes into one event; use its count field.
            count = int(getattr(event, "count", 1) or 1)
            await broadcast({"type": "like", "count": count})

        @client.on(GiftEvent)
        async def on_gift(event: GiftEvent):
            # Ignore intermediate frames of streakable gifts; count the completed streak once.
            gift = getattr(event, "gift", None)
            if gift is None:
                return
            gift_type = getattr(gift, "type", None)
            streaking = bool(getattr(event, "streaking", False))
            if gift_type == 1 and streaking:
                return
            user = getattr(event.user, "nickname", None) or getattr(event.user, "unique_id", "İzleyici")
            gift_name = getattr(gift, "name", None) or "Hediye"
            diamonds = int(getattr(gift, "diamond_count", 0) or 0)
            await broadcast({"type": "gift", "user": str(user), "gift": str(gift_name), "diamonds": diamonds})

        await broadcast({"type": "status", "text": "● TIKTOK'A BAĞLANILIYOR"})

        async def runner():
            try:
                await client.start()
            except Exception as exc:
                logger.exception("TikTok connection failed")
                await broadcast({"type": "status", "text": "● TIKTOK BAĞLANTISI KURULAMADI"})
                await broadcast({"type": "error", "message": str(exc)[:240]})

        client_task = asyncio.create_task(runner())


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    origin = websocket.headers.get("origin")
    if origin and origin not in ALLOWED_ORIGINS:
        await websocket.close(code=1008)
        return

    await websocket.accept()
    connected_sockets.add(websocket)
    await websocket.send_text(json.dumps({"type": "status", "text": "● SUNUCUYA BAĞLANDI"}, ensure_ascii=False))

    try:
        while True:
            raw = await websocket.receive_text()
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                continue

            if data.get("type") == "connect":
                username = str(data.get("username", "")).strip().lstrip("@").replace(" ", "")
                if not username or len(username) > 50:
                    await websocket.send_text(json.dumps({"type": "error", "message": "Geçerli bir TikTok kullanıcı adı gir."}, ensure_ascii=False))
                    continue
                await start_tiktok(username)
            elif data.get("type") == "ping":
                await websocket.send_text(json.dumps({"type": "pong"}))
    except WebSocketDisconnect:
        connected_sockets.discard(websocket)
    except Exception:
        connected_sockets.discard(websocket)
        logger.exception("Browser WebSocket error")


@app.on_event("shutdown")
async def shutdown_event():
    global active_client
    if active_client is not None:
        try:
            await active_client.stop()
        except Exception:
            logger.exception("TikTok client shutdown failed")
