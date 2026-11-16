import json
import asyncio
from pathlib import Path
from aiohttp import web
from config import Config
from queue_manager import (
    TIER_FREE, TIER_BENI_SEV, TIER_DONAT, TIER_CAY,
    TIER_KARISIK, TIER_DERIN_ASK, TIER_KADER
)

def get_local_ip():
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

class OverlayServer:
    def __init__(self, orchestrator=None):
        self.orchestrator = orchestrator
        self.app = web.Application()
        self.websockets = set()
        self.base_dir = Path(__file__).resolve().parent / "web_overlay"
        self._setup_routes()

    def set_orchestrator(self, orchestrator):
        self.orchestrator = orchestrator

    def _setup_routes(self):
        self.app.router.add_get("/ws", self.websocket_handler)
        self.app.router.add_get("/api/status", self.api_status)
        self.app.router.add_post("/api/test_comment", self.api_test_comment)
        self.app.router.add_post("/api/test_gift", self.api_test_gift)
        self.app.router.add_post("/api/set_voice_provider", self.api_set_voice_provider)
        self.app.router.add_post("/api/update_tiktok_user", self.api_update_tiktok_user)
        self.app.router.add_post("/api/toggle_tiktok", self.api_toggle_tiktok)
        
        self.app.router.add_static("/audio", Config.AUDIO_DIR)
        self.app.router.add_static("/", self.base_dir)

    async def api_status(self, request):
        if not self.orchestrator:
            return web.json_response({"status": "ready", "queue_size": 0, "tiktok_connected": False})
        
        local_ip = get_local_ip()
        pub_url = getattr(self.orchestrator, 'public_url', None)
        return web.json_response({
            "status": "running" if self.orchestrator.is_running else "stopped",
            "tiktok_user": Config.TIKTOK_USERNAME,
            "tiktok_connected": self.orchestrator.tiktok.is_running,
            "voice_provider": Config.TTS_PROVIDER,
            "queue_size": self.orchestrator.queue_mgr.get_queue_size(),
            "active_user": self.orchestrator.queue_mgr.current_reading.username if self.orchestrator.queue_mgr.current_reading else None,
            "local_ip": local_ip,
            "local_mobile_url": f"http://{local_ip}:{Config.SERVER_PORT}/index.html",
            "public_mobile_url": f"{pub_url}/index.html" if pub_url else None
        })

    async def api_set_voice_provider(self, request):
        try:
            data = await request.json()
            provider = data.get("provider", "video_voice").lower()
            Config.TTS_PROVIDER = provider
            if self.orchestrator:
                self.orchestrator.voice.provider = provider
            print(f"[OverlayServer] Ses motoru değiştirildi: {provider.upper()}")
            return web.json_response({"success": True, "provider": provider})
        except Exception as e:
            return web.json_response({"error": str(e)}, status=400)

    async def api_test_comment(self, request):
        if not self.orchestrator:
            return web.json_response({"error": "Orchestrator bağlı değil"}, status=500)
        
        try:
            data = await request.json()
        except Exception:
            data = {}

        username = data.get("username", "test_izleyici")
        question = data.get("question", "Eski sevgilim geri dönecek mi?")

        await self.orchestrator.queue_mgr.add_request(
            username=username,
            question=question,
            tier=TIER_FREE
        )
        return web.json_response({"success": True, "message": f"@{username} normal yorumu kuyruğa eklendi."})

    async def api_test_gift(self, request):
        if not self.orchestrator:
            return web.json_response({"error": "Orchestrator bağlı değil"}, status=500)
        
        try:
            data = await request.json()
        except Exception:
            data = {}

        username = data.get("username", "Canli_Izleyici")
        tier = data.get("tier", TIER_DONAT)
        question = data.get("question", "Aşk ve gelecek durumu")
        coins = int(data.get("coins", 0))

        await self.orchestrator.queue_mgr.add_request(
            username=username,
            question=question,
            tier=tier,
            gift_coins=coins
        )
        return web.json_response({"success": True, "message": f"🎁 @{username} ({tier.upper()}) sıraya eklendi!"})

    async def api_update_tiktok_user(self, request):
        try:
            data = await request.json()
            new_user = data.get("username", "").strip().lstrip("@")
            if new_user:
                Config.TIKTOK_USERNAME = new_user
                # .env dosyasına kalıcı olarak kaydet
                env_file = Path(__file__).resolve().parent / ".env"
                if env_file.exists():
                    try:
                        lines = env_file.read_text(encoding="utf-8").splitlines()
                        new_lines = []
                        found = False
                        for l in lines:
                            if l.startswith("TIKTOK_USERNAME="):
                                new_lines.append(f"TIKTOK_USERNAME={new_user}")
                                found = True
                            else:
                                new_lines.append(l)
                        if not found:
                            new_lines.append(f"TIKTOK_USERNAME={new_user}")
                        env_file.write_text("\n".join(new_lines), encoding="utf-8")
                    except Exception as env_err:
                        print(f"[Server] .env yazma hatası: {env_err}")

                if self.orchestrator:
                    await self.orchestrator.tiktok.stop()
                    self.orchestrator.tiktok.username = new_user
                    asyncio.create_task(self.orchestrator.tiktok.start())
                print(f"[Server] Hedef TikTok hesabı güncellendi: @{new_user}")
                return web.json_response({"success": True, "username": new_user})
        except Exception as e:
            return web.json_response({"error": str(e)}, status=400)
        return web.json_response({"error": "Geçersiz kullanıcı adı"}, status=400)

    async def api_toggle_tiktok(self, request):
        if not self.orchestrator:
            return web.json_response({"error": "Orchestrator hazır değil"}, status=500)
        
        if self.orchestrator.tiktok.is_running:
            await self.orchestrator.tiktok.stop()
            return web.json_response({"running": False, "message": "TikTok dinleme durduruldu."})
        else:
            asyncio.create_task(self.orchestrator.tiktok.start())
            return web.json_response({"running": True, "message": "TikTok dinleme başlatıldı."})

    async def websocket_handler(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        self.websockets.add(ws)

        try:
            async for msg in ws:
                if msg.type == web.WSMsgType.TEXT:
                    try:
                        data = json.loads(msg.data)
                        if data.get("type") == "READING_FINISHED" and self.orchestrator:
                            self.orchestrator.on_reading_finished()
                    except Exception:
                        pass
        finally:
            self.websockets.remove(ws)

        return ws

    async def broadcast(self, event_type: str, data: dict):
        if not self.websockets:
            return
            
        message = json.dumps({"type": event_type, "data": data}, ensure_ascii=False)
        tasks = [ws.send_str(message) for ws in self.websockets if not ws.closed]
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def start(self):
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, Config.SERVER_HOST, Config.SERVER_PORT)
        await site.start()
        print(f"[OverlayServer] Almina Tarot yayını hazır: http://{Config.SERVER_HOST}:{Config.SERVER_PORT}/index.html")

if __name__ == "__main__":
    from run import main
    main()

