import asyncio
import time
from config import Config
from queue_manager import QueueManager
from tarot_deck import TarotDeck
from tarot_ai import TarotAI
from voice_engine import VoiceEngine
from server import OverlayServer

async def run_simulation():
    print("=======================================================")
    print("🧪 TIKTOK LIVE TAROT TEST VE SİMÜLASYON MODU")
    print("Bu mod, canlı yayına gerek kalmadan sistemi bilgisayarınızda")
    print("birebir canlı yayın gibi test etmenizi sağlar.")
    print("=======================================================\n")

    queue_mgr = QueueManager()
    ai = TarotAI()
    voice = VoiceEngine()
    server = OverlayServer()

    # 1. Sunucuyu Başlat
    await server.start()
    print(f"👉 Tarayıcınızda veya OBS'te şu adresi açın: http://{Config.SERVER_HOST}:{Config.SERVER_PORT}/index.html\n")

    # 2. Simülasyon Senaryoları Ekle
    print("📥 Simülasyon istekleri kuyruğa ekleniyor...")
    
    # Normal izleyici yorumu
    await queue_mgr.add_request(
        username="selin_ozdemir",
        question="Eski sevgilim geri dönecek mi, aramız düzelir mi?",
        is_vip=False
    )
    print("   [1] @selin_ozdemir (Normal Yorum: Aşk sorusu) eklendi.")

    # VIP Hediye Gönderen (Hemen sıranın önüne geçecek!)
    await queue_mgr.add_request(
        username="mert_kaya",
        question="İlişki ve Gelecek Açılımı",
        is_vip=True,
        gift_name="Gül",
        gift_coins=1
    )
    print("   [2] 🌹 @mert_kaya (VIP HEDİYE: Gül) eklendi -> Sıranın en önüne geçecek!")

    print("\n⏳ 3 saniye sonra test döngüsü başlıyor...")
    await asyncio.sleep(3)

    # 3. Kuyruktaki istekleri sırayla işlet
    while queue_mgr.get_queue_size() > 0:
        req = await queue_mgr.get_next()
        
        print("\n" + "="*50)
        print(f"🔮 İŞLENİYOR: @{req.username} | VIP: {req.is_vip}")
        if req.gift_name:
            print(f"🎁 Hediye: {req.gift_name}")
        if req.question:
            print(f"❓ Soru: {req.question}")

        # Kart çek
        card_count = 3 if req.is_vip else 1
        cards = TarotDeck.draw(count=card_count)
        print(f"🎴 Çekilen Kartlar: {', '.join([c['name_tr'] + ' (' + c['orientation'] + ')' for c in cards])}")

        # AI Yorum Üret
        print("🧠 AI Yorum üretiyor...")
        reading_text = await ai.generate_reading(
            username=req.username,
            user_question=req.question,
            cards=cards,
            is_vip=req.is_vip,
            gift_name=req.gift_name
        )
        print(f"💬 Metin: {reading_text}")

        # Seslendir
        print("🎙️ Seslendiriliyor...")
        audio_file = await voice.speak(reading_text)
        audio_url = f"/audio/{audio_file}" if audio_file else None

        # Ekrana bas
        payload = {
            "username": req.username,
            "question": req.question,
            "is_vip": req.is_vip,
            "gift_name": req.gift_name,
            "cards": cards,
            "text": reading_text,
            "audio_url": audio_url
        }
        await server.broadcast("NEW_READING", payload)

        duration = max(len(reading_text.split()) * 0.35 + 2.0, 8.0)
        print(f"⏳ Ekranda gösteriliyor ve okunuyor (~{int(duration)} sn)...")
        await asyncio.sleep(duration)
        
        queue_mgr.mark_done()
        await server.broadcast("IDLE", {})
        print(f"✅ @{req.username} açılımı tamamlandı.")
        await asyncio.sleep(2)

    print("\n🎉 Tüm test istekleri başarıyla işlendi!")
    print("Sunucu açık kalmaya devam ediyor. Çıkmak için CTRL+C yapabilirsiniz.")
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    try:
        asyncio.run(run_simulation())
    except KeyboardInterrupt:
        print("\nTest sonlandırıldı.")
