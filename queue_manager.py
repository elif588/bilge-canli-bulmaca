import time
import asyncio
import re
from typing import Optional, Dict, List, Any, Set
from dataclasses import dataclass, field

# Bakım ve Açılım Kademeleri (TikTok İhlal Önleme: Hediye ismi ve jeton miktarı ASLA içermez)
TIER_FREE = "free"                 # Ücretsiz chat yorumu
TIER_BENI_SEV = "beni_sev"         # 1 jeton dengi
TIER_DONAT = "donat"               # 30 jeton dengi
TIER_CAY = "cay"                   # 50 jeton dengi
TIER_KARISIK = "karisik"           # 100 jeton dengi (5 Kart)
TIER_DERIN_ASK = "derin_ask"       # 199 jeton dengi (6 Kart)
TIER_KADER = "kader"               # 699 jeton dengi (7 Kart)

TIER_CONFIG = {
    TIER_FREE: {
        "priority": 6,
        "title": "Detaylı Tek Kart",
        "card_count": 1,
        "badge": "Detaylı Tek Kart",
        "target_duration": 14
    },
    TIER_BENI_SEV: {
        "priority": 5,
        "title": "Detaylı Tek Kart",
        "card_count": 1,
        "badge": "Detaylı Tek Kart",
        "target_duration": 18
    },
    TIER_DONAT: {
        "priority": 4,
        "title": "3 Kart Açılım",
        "card_count": 3,
        "badge": "3 Kart Açılım",
        "target_duration": 38
    },
    TIER_CAY: {
        "priority": 3,
        "title": "Aşk Bakım ve Tavsiye",
        "card_count": 3,
        "badge": "Aşk Bakım ve Tavsiye",
        "target_duration": 48
    },
    TIER_KARISIK: {
        "priority": 2,
        "title": "Karışık Bakım",
        "card_count": 5,  # Karışık bakımda 5 kart
        "badge": "Karışık Bakım",
        "target_duration": 65
    },
    TIER_DERIN_ASK: {
        "priority": 1,
        "title": "Derin Aşk Açılımı",
        "card_count": 6,
        "badge": "Derin Aşk Açılımı",
        "target_duration": 78
    },
    TIER_KADER: {
        "priority": 0,
        "title": "Kader Açılımı",
        "card_count": 7,
        "badge": "Kader Açılımı",
        "target_duration": 95
    }
}

SEXUAL_PATTERNS = [
    r"\bcinsel\b", r"\bcinsellik\b", r"\bseks\b", r"\bsex\b",
    r"\byattı\b", r"\byattık\b", r"\byatağa\b", r"\byatakta\b",
    r"\bseviştik\b", r"\bsevişecek\b", r"\bsevişme\b",
    r"\bbirlikte olduk\b", r"\bilişkiye girdik\b", r"\bilişkiye girecek\b",
    r"\böpüştük\b", r"\bten uyumu\b", r"\bmastürbasyon\b", r"\bporno\b",
    r"\bboşalma\b", r"\bazgın\b", r"\bçıplak\b", r"\bpenis\b", r"\bvajina\b"
]

def is_sexual_or_inappropriate(text: str) -> bool:
    """Cinsellik veya müstehcen içerik içeren soruları kelime sınırıyla tespit eder ve eler."""
    if not text:
        return False
    lower = text.lower().strip()
    return any(re.search(pattern, lower) for pattern in SEXUAL_PATTERNS)

@dataclass(order=True)
class ReadingRequest:
    priority: int
    timestamp: float
    username: str = field(compare=False)
    question: str = field(compare=False)
    tier: str = field(compare=False, default=TIER_FREE)
    gift_coins: int = field(compare=False, default=0)

class QueueManager:
    def __init__(self):
        # 1. Hediye atanlar için öncelikli kuyruk (VIP 0-5 öncelik)
        self.gift_queue: asyncio.PriorityQueue[ReadingRequest] = asyncio.PriorityQueue()
        # 2. Chatten yazan ücretsiz izleyiciler için kuyruk (FIFO)
        self.chat_queue: asyncio.Queue[ReadingRequest] = asyncio.Queue()
        self.last_free_reading_time: float = 0.0          # Son ücretsiz chat bakımının bittiği an
        self.FREE_COOLDOWN_SECONDS: float = 60.0          # Hediye yokken 60 saniyede bir chat yorumu bakılır
        
        self.active_users: Set[str] = set()               # Kuyrukta veya şu an masada olan kullanıcılar
        self.user_last_reading: Dict[str, float] = {}     # Kullanıcının son bakım zamanı
        self.recent_questions: List[str] = []            # Son okunan/kuyruğa alınan sorular (spam engelleme)
        self.current_reading: Optional[ReadingRequest] = None
        self.recent_history: List[Dict[str, Any]] = []

    def _normalize_user(self, username: str) -> str:
        if not username:
            return ""
        return username.lower().strip().lstrip("@")

    def _normalize_question(self, text: str) -> str:
        if not text:
            return ""
        clean = re.sub(r'[^\w\s]', '', text.lower()).strip()
        clean = re.sub(r'\s+', ' ', clean)
        return clean

    async def add_request(
        self,
        username: str,
        question: str = "",
        tier: str = TIER_FREE,
        gift_coins: int = 0
    ) -> bool:
        if not username:
            return False

        # Cinsellikle alakalı soru sorulursa kesinlikle ES GEÇ, yanıtlama!
        if is_sexual_or_inappropriate(question):
            print(f"[Filtre] ⛔ Cinsellik/Müstehcen soru elendi: @{username} -> '{question}'")
            return False

        u_key = self._normalize_user(username)
        if not u_key:
            return False

        now = time.time()

        # 1. KULLANICI ŞU AN KUYRUKTA VEYA MASADA İSE ASLA TEKRAR EKLEME!
        if u_key in self.active_users:
            if tier == TIER_FREE:
                return False

        # 2. Ücretsiz izleyici spam koruması (Aynı kullanıcı 90 saniye içinde tekrar ücretsiz eklenemez)
        if tier == TIER_FREE:
            last = self.user_last_reading.get(u_key, 0)
            if now - last < 90:
                return False

            # 3. Aynı sorunun ardı ardına tekrar eklenmesini önle
            q_norm = self._normalize_question(question)
            if q_norm and q_norm in self.recent_questions:
                return False

        tier_info = TIER_CONFIG.get(tier, TIER_CONFIG[TIER_FREE])
        priority = tier_info["priority"]

        item = ReadingRequest(
            priority=priority,
            timestamp=now,
            username=username,
            question=question,
            tier=tier,
            gift_coins=gift_coins
        )

        self.active_users.add(u_key)
        self.user_last_reading[u_key] = now

        q_norm = self._normalize_question(question)
        if q_norm:
            self.recent_questions.append(q_norm)
            if len(self.recent_questions) > 40:
                self.recent_questions.pop(0)

        # Hediyeler doğrudan VIP öncelik kuyruğuna, ücretsiz yorumlar chat kuyruğuna aktarılır
        if tier != TIER_FREE:
            await self.gift_queue.put(item)
            print(f"[Kuyruk] 🎁 VIP HEDİYE ÖNCELİKLE EKLENDİ: @{username} ({tier.upper()})")
        else:
            await self.chat_queue.put(item)
            print(f"[Kuyruk] 💬 Chat yorumu kuyruğa alındı: @{username} -> '{question[:30]}'")
            
        return True

    async def get_next(self) -> ReadingRequest:
        while True:
            # 1. Hediye atan var mı? Varsa ANINDA çek ve masaya al (Hiç beklemez!)
            if not self.gift_queue.empty():
                item = await self.gift_queue.get()
                self.current_reading = item
                u_key = self._normalize_user(item.username)
                self.user_last_reading[u_key] = time.time()
                return item

            # 2. Hediye yoksa, chat kuyruğunu kontrol et
            if not self.chat_queue.empty():
                now = time.time()
                elapsed = now - self.last_free_reading_time
                
                # 60 saniyelik bekleme kuralı:
                if elapsed < self.FREE_COOLDOWN_SECONDS:
                    wait_time = self.FREE_COOLDOWN_SECONDS - elapsed
                    # Bu 60 saniye dolana kadar hediye gelmesini bekle!
                    try:
                        item = await asyncio.wait_for(self.gift_queue.get(), timeout=wait_time)
                        # Hediye geldi! 60s bekleme hemen kesilir ve hediye açılır:
                        self.current_reading = item
                        u_key = self._normalize_user(item.username)
                        self.user_last_reading[u_key] = time.time()
                        return item
                    except asyncio.TimeoutError:
                        # 60 saniye doldu ve hiç hediye gelmedi, sıradaki chat yorumuna geç!
                        pass

                # 60 saniye tamamlandı: Chat kuyruğundaki ilk yorumu çek
                # (Eğer tam bu anda hediye geldiyse yine hediyeyi al)
                if not self.gift_queue.empty():
                    item = await self.gift_queue.get()
                else:
                    item = await self.chat_queue.get()
                    self.last_free_reading_time = time.time()

                self.current_reading = item
                u_key = self._normalize_user(item.username)
                self.user_last_reading[u_key] = time.time()
                return item

            # 3. İki kuyruk da tamamen boşsa: Hediye VEYA chat yorumu gelene kadar bekle
            get_gift_task = asyncio.create_task(self.gift_queue.get())
            get_chat_task = asyncio.create_task(self.chat_queue.get())

            done, pending = await asyncio.wait(
                [get_gift_task, get_chat_task],
                return_when=asyncio.FIRST_COMPLETED
            )

            for t in pending:
                t.cancel()

            for t in done:
                item = t.result()
                if item.tier != TIER_FREE:
                    # Gelen hediye! Anında masaya al
                    self.current_reading = item
                    u_key = self._normalize_user(item.username)
                    self.user_last_reading[u_key] = time.time()
                    return item
                else:
                    # Gelen ücretsiz chat yorumu: Chat kuyruğuna koyup 60 saniye döngüsüne sok
                    await self.chat_queue.put(item)
                    break

    def mark_done(self):
        if self.current_reading:
            u_key = self._normalize_user(self.current_reading.username)
            self.active_users.discard(u_key)
            self.user_last_reading[u_key] = time.time()
            # Ücretsiz chat bakımı bittiğinde 60 saniyelik dinlenme süresi başlar
            if self.current_reading.tier == TIER_FREE:
                self.last_free_reading_time = time.time()
                
            self.recent_history.append({
                "username": self.current_reading.username,
                "tier": self.current_reading.tier,
                "question": self.current_reading.question,
                "time": time.time()
            })
            if len(self.recent_history) > 30:
                self.recent_history.pop(0)
        self.current_reading = None

    def get_queue_size(self) -> int:
        return self.gift_queue.qsize() + self.chat_queue.qsize()
