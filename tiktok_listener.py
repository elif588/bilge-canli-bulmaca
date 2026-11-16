import time
import asyncio
from typing import Optional, Dict
from TikTokLive import TikTokLiveClient
from TikTokLive.events import CommentEvent, GiftEvent, ConnectEvent, DisconnectEvent
from queue_manager import (
    QueueManager, TIER_FREE, TIER_BENI_SEV, TIER_DONAT, TIER_CAY,
    TIER_KARISIK, TIER_DERIN_ASK, TIER_KADER, is_sexual_or_inappropriate
)
from config import Config

META_PHRASES = [
    "bakmadı", "bakmadın", "baksana", "bana da bak", "bana nezaman", "ne zaman bakacaksın",
    "sıra", "sıradayım", "hediye attım", "beni sev attım", "gül attım", "çay attım",
    "donat attım", "gönderdim", "gönderdim baksana", "neden bakmıyorsun", "görmüyorsun",
    "cevap ver", "bekliyorum", "selam", "merhaba", "hoşgeldin", "takip ettim", "beğendim",
    "la baksana", "bana bak", "benimki ne zaman", "neredesin", "ses yok", "açılmadı", "atıyorum"
]

def is_valid_tarot_question(text: str) -> bool:
    """Yorumun gerçek bir niyet veya tarot sorusu olup olmadığını denetler (Sitemleri ve cinselliği eler)."""
    if not text or len(text.strip()) < 4:
        return False

    # 1. Cinsellik içeren sorular kesinlikle elenir ve yanıtlanmaz!
    if is_sexual_or_inappropriate(text):
        return False

    lower = text.lower().strip()
    
    # 2. Sadece sitem, sabırsızlık veya hediye bildirimi ise GERÇEK SORU DEĞİLDİR
    for phrase in META_PHRASES:
        if phrase in lower and not any(w in lower for w in [
            "dön", "sev", "ara", "yaz", "evli", "barış", "aldat", "akrep", "terazi", "koç",
            "boğa", "ikizler", "yengeç", "aslan", "başak", "yay", "oğlak", "kova", "balık", "199", "200"
        ]):
            return False
            
    tarot_triggers = [
        "mi", "mı", "mu", "mü", "?", "niyet", "niyetim", "niyetlendim", "dönecek", "döner",
        "seviyor", "sever", "barış", "barışma", "evlilik", "aldat", "aldatma",
        "aklındaki", "aklımda", "kalbinde", "arayacak", "arar", "yazacak", "yazar",
        "mesaj", "adım", "özlüyor", "özler", "pişman", "hissediyor", "düşünüyor",
        "neler", "ne olacak", "ne zaman", "nasıl", "ilişki", "durumumuz",
        "kariyer", "para", "iş", "sınav", "kavga", "ayrılık", "hakkında", "hakkımda",
        "engel", "kader", "kısmet", "şans", "enerji", "fal", "tarot",
        "akrep", "terazi", "koç", "boğa", "ikizler", "yengeç", "aslan", "başak", "yay", "oğlak", "kova", "balık"
    ]
    return any(trig in lower for trig in tarot_triggers)

class TikTokListener:
    def __init__(self, username: str, queue_manager: QueueManager):
        self.username = username.lstrip("@")
        self.queue_manager = queue_manager
        self.client: Optional[TikTokLiveClient] = None
        self.is_running = False
        self.user_recent_questions: Dict[str, Dict] = {}
        self.pending_question_waiters: Dict[str, asyncio.Future] = {}

    def _save_user_question(self, user, text: str):
        if not user or not text or not is_valid_tarot_question(text):
            return
        now = time.time()
        keys = []
        if getattr(user, "unique_id", None):
            keys.append(user.unique_id.lower().strip())
        if getattr(user, "nick_name", None):
            keys.append(user.nick_name.lower().strip())
        for k in keys:
            if k:
                self.user_recent_questions[k] = {
                    "question": text,
                    "time": now
                }
        expired = [u for u, d in self.user_recent_questions.items() if now - d["time"] > 1800]
        for u in expired:
            del self.user_recent_questions[u]

    def _get_user_question(self, user) -> Optional[str]:
        if not user:
            return None
        now = time.time()
        keys = []
        if getattr(user, "unique_id", None):
            keys.append(user.unique_id.lower().strip())
        if getattr(user, "nick_name", None):
            keys.append(user.nick_name.lower().strip())
        for k in keys:
            if k:
                data = self.user_recent_questions.get(k)
                if data and now - data["time"] < 1800:
                    return data["question"]
        return None

    async def wait_for_user_question(self, username: str, timeout: float = 12.0) -> Optional[str]:
        """Soru sormamış hediye atan kullanıcının sorusunu canlı yayında belirli bir süre bekler."""
        clean_user = username.lower().strip().lstrip("@")
        loop = asyncio.get_event_loop()
        future = loop.create_future()
        self.pending_question_waiters[clean_user] = future
        try:
            return await asyncio.wait_for(future, timeout=timeout)
        except asyncio.TimeoutError:
            return None
        finally:
            self.pending_question_waiters.pop(clean_user, None)

    def setup_client(self):
        self.client = TikTokLiveClient(unique_id=f"@{self.username}")

        @self.client.on(ConnectEvent)
        async def on_connect(event: ConnectEvent):
            print(f"[TikTokLive] Almina Tarot canlı yayına bağlandı: @{self.username}")

        @self.client.on(DisconnectEvent)
        async def on_disconnect(event: DisconnectEvent):
            print(f"[TikTokLive] Yayından kopuldu: @{self.username}")

        @self.client.on(CommentEvent)
        async def on_comment(event: CommentEvent):
            try:
                user_name = event.user.nick_name if (event.user and event.user.nick_name) else (getattr(event.user, "unique_id", "Misafir") if event.user else "Misafir")
                user_id = (event.user.unique_id if event.user else "").lower().strip()
                comment = event.comment.strip()
                
                if len(comment) < 2:
                    return

                # Cinsellik içeren yorumları anında eler, hiçbir işleme almaz!
                if is_sexual_or_inappropriate(comment):
                    print(f"[Chat Filtresi] ⛔ Cinsel/Uygunsuz soru atlandı: @{user_name}")
                    return

                # Bekleyen bir hediye sorusu varsa eşleştir
                for waiter_key, fut in list(self.pending_question_waiters.items()):
                    if waiter_key in [user_name.lower().strip(), user_id]:
                        if is_valid_tarot_question(comment):
                            if not fut.done():
                                fut.set_result(comment)
                                print(f"[TikTokLive] Beklenen soru chatten geldi: @{user_name} -> '{comment}'")
                                return

                # Gerçek niyet sorusu değilse (sitem, baksana vb.) hafızaya ve sıraya ALMA!
                if not is_valid_tarot_question(comment):
                    return

                # Kullanıcının geçerli sorusunu hafızaya al
                self._save_user_question(event.user, comment)

                # Normal izleyici yorumu: Sorusu doğrultusunda tek kart açılacak
                added = await self.queue_manager.add_request(
                    username=user_name,
                    question=comment,
                    tier=TIER_FREE
                )
                if added:
                    print(f"[Chat] @{user_name} -> '{comment[:35]}...'")
            except Exception as e:
                print(f"[TikTokLive] Yorum hatası: {e}")

        @self.client.on(GiftEvent)
        async def on_gift(event: GiftEvent):
            try:
                if event.streaking:
                    return

                user_name = event.user.nick_name if (event.user and event.user.nick_name) else (getattr(event.user, "unique_id", "Misafir") if event.user else "Değerli İzleyici")
                raw_gift_name = event.gift.gift_name if event.gift else ""
                gift_name_lower = raw_gift_name.lower().strip()
                coins = getattr(event, "value", 0) or 0
                
                # 1. Kural: Gül hediyesi tamamen pasif (ihlal almamak için)
                if "gül" in gift_name_lower or "rose" in gift_name_lower:
                    return

                tier = None
                
                # KURAL: YALNIZCA BELİRTİLEN HEDİYELER VE JETON TUTARLARI GEÇERLİDİR!
                # 1 jetonluk "Beni Sev"
                if ("beni sev" in gift_name_lower or "love me" in gift_name_lower) or coins == 1:
                    tier = TIER_BENI_SEV
                
                # 30 jetonluk "Donat"
                elif ("donat" in gift_name_lower or "donut" in gift_name_lower or "doughnut" in gift_name_lower) or coins == 30:
                    tier = TIER_DONAT
                
                # 50 jetonluk "Çay"
                elif ("çay" in gift_name_lower or "tea" in gift_name_lower) or coins == 50:
                    tier = TIER_CAY
                
                # 100 jeton (Karışık Bakım - 5 Kart)
                elif coins == 100:
                    tier = TIER_KARISIK
                
                # 199 jeton (Büyük Derin Aşk Açılımı - 6 Kart)
                elif coins == 199:
                    tier = TIER_DERIN_ASK
                
                # 699 jeton (Kadersel Dönüm Noktası - 7 Kart)
                elif coins == 699:
                    tier = TIER_KADER
                
                # Belirtilenler dışındaki tüm hediyeler GEÇERSİZ SAYILIR
                else:
                    print(f"[Hediye] ⚠️ Belirtilen tutarlar dışındaki hediye geçersiz sayıldı: @{user_name} ({raw_gift_name} / {coins} Jeton)")
                    return

                if tier:
                    # KULLANICININ CHATTE SORDUĞU ASIL SORUYU HAFIZADAN ÇEK
                    saved_question = self._get_user_question(event.user)
                    final_question = saved_question if saved_question else "SORU_BEKLENIYOR"
                    
                    print(f"[VIP HEDİYE] 🎁 @{user_name} ({coins} Jeton) -> Soru: '{final_question}' | Kademe: {tier.upper()}")
                    
                    await self.queue_manager.add_request(
                        username=user_name,
                        question=final_question,
                        tier=tier,
                        gift_coins=coins
                    )
            except Exception as e:
                print(f"[TikTokLive] Hediye işleme hatası: {e}")

    async def start(self):
        self.is_running = True
        while self.is_running:
            self.setup_client()
            try:
                print(f"[TikTokLive] @{self.username} canlı yayını dinleniyor...")
                await self.client.start()
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"[TikTokLive] @{self.username} yayın durumu: {e}")
                print(f"[TikTokLive] 6 saniye sonra otomatik tekrar bağlanılacak...")
                try:
                    await asyncio.sleep(6)
                except asyncio.CancelledError:
                    break

    async def stop(self):
        if self.client and self.is_running:
            await self.client.disconnect()
            self.is_running = False
