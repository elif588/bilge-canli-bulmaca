import asyncio
import signal
import sys
import json
from config import Config
from tarot_deck import TarotDeck
from tarot_ai import TarotAI
from voice_engine import VoiceEngine
from queue_manager import QueueManager, TIER_CONFIG, TIER_FREE, is_sexual_or_inappropriate
from server import OverlayServer, get_local_ip
from tiktok_listener import TikTokListener

class AlminaTarotOrchestrator:
    def __init__(self):
        self.queue_mgr = QueueManager()
        self.ai = TarotAI()
        self.voice = VoiceEngine()
        self.server = OverlayServer(orchestrator=self)
        self.tiktok = TikTokListener(Config.TIKTOK_USERNAME, self.queue_mgr)
        self.is_running = True
        self.reading_finished_event = asyncio.Event()
        self.ngrok_process = None
        self.public_url = None

    def on_reading_finished(self):
        """Web ekranından ses bittiğinde anlık tetiklenir."""
        self.reading_finished_event.set()

    async def start_tunnel(self):
        """Mobil cihazlardan (Safari & Chrome) tam ekran PWA indirilebilmesi için tüneli başlatır."""
        try:
            import subprocess
            import urllib.request
            self.ngrok_process = subprocess.Popen(
                ["ngrok", "http", str(Config.SERVER_PORT), "--log=stdout"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            for _ in range(8):
                await asyncio.sleep(0.5)
                try:
                    with urllib.request.urlopen("http://127.0.0.1:4040/api/tunnels", timeout=1) as resp:
                        data = json.loads(resp.read().decode())
                        tunnels = data.get("tunnels", [])
                        if tunnels:
                            self.public_url = tunnels[0].get("public_url")
                            break
                except Exception:
                    pass
        except Exception as e:
            print(f"[Tunnel] Otomatik tünel başlatılamadı (isteğe bağlı): {e}")

    async def worker_loop(self):
        print("[Almina Tarot] Canlı bakım döngüsü hazır.")
        
        while self.is_running:
            try:
                req = await self.queue_mgr.get_next()
                
                # Cinsellikle alakalı soru ise yanıt vermeden es geç, doğrudan sıradaki yoruma geç
                if is_sexual_or_inappropriate(req.question):
                    print(f"⚠️ [Cinsellik/Uygunsuz Soru Es Geçildi]: @{req.username} -> '{req.question}'")
                    self.queue_mgr.mark_done()
                    continue

                tier_info = TIER_CONFIG.get(req.tier, TIER_CONFIG[TIER_FREE])
                
                print(f"\n=======================================================")
                print(f"✨ [AÇILIM BAŞLADI] @{req.username} | {tier_info['title']}")
                print(f"❓ İzleyicinin Chatteki Sorusu: '{req.question}'")

                # Eğer hediye atan izleyici henüz soru yazmadıysa (veya sadece hediye attım dediyse)
                if req.question == "SORU_BEKLENIYOR" or not req.question:
                    prompt_speech = f"{req.username}, güzel enerjin için teşekkürler canım. Kartlarını açmadan önce niyetini ve sorunu chatten bekliyorum, lütfen hemen yaz."
                    print(f"⏳ @{req.username} henüz soru yazmadı, sorusu chatten bekleniyor...")
                    
                    audio_prompt, prompt_dur = await self.voice.speak(prompt_speech)
                    wait_payload = {
                        "username": req.username,
                        "question": "✦ Niyetini ve aklındaki soruyu chat'e yaz, bekleniyor... ✦",
                        "tier": req.tier,
                        "badge": tier_info["badge"],
                        "zodiac_badge": "❓ Soru Bekleniyor",
                        "text": prompt_speech,
                        "audio_url": f"/audio/{audio_prompt}" if audio_prompt else None
                    }
                    await self.server.broadcast("WAIT_FOR_QUESTION", wait_payload)
                    
                    user_q = await self.tiktok.wait_for_user_question(req.username, timeout=12.0)
                    if user_q and not is_sexual_or_inappropriate(user_q):
                        req.question = user_q
                        print(f"🎯 @{req.username} sorusunu chatten yazdı: '{req.question}'")
                    else:
                        req.question = "Kalbindeki Niyet ve Yakın Gelecek"
                        print(f"ℹ️ Süre doldu, genel aşk ve kader niyetine bakılıyor.")

                # 1. Kademeye Uygun Sayıda Kart Çek
                card_count = tier_info["card_count"]
                cards = TarotDeck.draw(count=card_count, allow_reversed=False)
                
                card_names = ", ".join([f"{c['name_tr']}" for c in cards])
                print(f"🎴 Masaya Açılan Kartlar ({card_count} Kart): {card_names}")

                # 2. Almina'nın Sezgisel Yorumunu Üret (Soru & Burç & Tarih Odaklı)
                print("🧠 Almina soruya ve enerjilere özel yorumluyor...")
                reading_text, astro = await self.ai.generate_reading(
                    username=req.username,
                    user_question=req.question,
                    cards=cards,
                    tier=req.tier
                )
                if astro.get("badge_pill"):
                    print(f"✨ [Astroloji/Tarih Rozeti]: {astro['badge_pill']}")
                print(f"💬 Metin: {reading_text}")

                # 3. İnsan Sesi Üret
                print("🎙️ Seslendiriliyor...")
                audio_file, exact_duration = await self.voice.speak(reading_text)
                audio_url = f"/audio/{audio_file}" if audio_file else None

                # 4. OBS Ekranına Fırlat
                payload = {
                    "username": req.username,
                    "question": req.question,
                    "tier": req.tier,
                    "badge": tier_info["badge"],
                    "zodiac_badge": astro.get("badge_pill"),
                    "cards": cards,
                    "text": reading_text,
                    "audio_url": audio_url
                }
                self.reading_finished_event.clear()
                await self.server.broadcast("NEW_READING", payload)

                # 5. Sesin bitişini bekle (Web ekranından anlık sinyal VEYA maksimum süre)
                max_wait = exact_duration + 2.0
                print(f"⏳ Yayında seslendiriliyor ({exact_duration:.1f} sn)...")
                try:
                    await asyncio.wait_for(self.reading_finished_event.wait(), timeout=max_wait)
                    print(f"✅ Seslendirme web tarafında bitti.")
                except asyncio.TimeoutError:
                    print(f"ℹ️ Ses süresi tamamlandı.")

                # 6. Snappy Geçiş: Yalnızca 0.5 saniyelik doğal nefes alma beklemesi
                self.queue_mgr.mark_done()
                await self.server.broadcast("IDLE", {})
                await asyncio.sleep(0.5)

            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"[Orchestrator] Hata: {e}")
                await asyncio.sleep(1)

    async def start(self):
        await self.start_tunnel()
        local_ip = get_local_ip()

        print("=======================================================")
        print("🔮 ALMİNA TAROT - CANLI YAYIN SİSTEMİ")
        print(f"🎯 Hedef TikTok Hesabı: @{Config.TIKTOK_USERNAME}")
        print(f"🎙️ Ses Motoru: {Config.TTS_PROVIDER.upper()}")
        print(f"🧠 Zeka Modeli: {Config.LLM_PROVIDER.upper()}")
        print(f"🖥️ Bilgisayar Ekranı: http://127.0.0.1:{Config.SERVER_PORT}/index.html")
        print(f"🎛️ Yönetim Paneli: http://127.0.0.1:{Config.SERVER_PORT}/panel.html")
        print(f"📱 Telefon/Tablet (Aynı Wi-Fi): http://{local_ip}:{Config.SERVER_PORT}/index.html")
        if self.public_url:
            print(f"🌐 Telefon/Tablet (İnternet PWA Linki): {self.public_url}/index.html")
        print("=======================================================\n")

        await self.server.start()
        worker_task = asyncio.create_task(self.worker_loop())
        tiktok_task = asyncio.create_task(self.tiktok.start())

        try:
            await asyncio.gather(worker_task, tiktok_task)
        except asyncio.CancelledError:
            pass
        finally:
            await self.shutdown()

    async def shutdown(self):
        print("\n[Almina Tarot] Sistem kapatılıyor...")
        self.is_running = False
        if self.ngrok_process:
            try:
                self.ngrok_process.terminate()
            except Exception:
                pass
        await self.tiktok.stop()

def main():
    orchestrator = AlminaTarotOrchestrator()
    try:
        asyncio.run(orchestrator.start())
    except KeyboardInterrupt:
        print("\nKullanıcı tarafından durduruldu.")

if __name__ == "__main__":
    main()
