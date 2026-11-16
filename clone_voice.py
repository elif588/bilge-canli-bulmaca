# ==============================================================================
# ALMİNA TAROT - ELEVENLABS SES KLONLAMA YARDIMCISI
# Attığınız videodaki orijinal sesi ElevenLabs hesabınıza 1 tıkla klonlar.
# ==============================================================================

import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"
load_dotenv(ENV_FILE)

API_KEY = os.getenv("ELEVENLABS_API_KEY", "").strip()
REF_AUDIO = BASE_DIR / "web_overlay" / "audio" / "reference_voice.wav"

def main():
    print("=======================================================")
    print("🎙️ ALMİNA TAROT - VİDEODAKİ SESİ KLONLAMA ARACI")
    print("=======================================================\n")

    if not API_KEY:
        print("❌ ELEVENLABS_API_KEY bulunamadı!")
        print("Lütfen .env dosyasına ElevenLabs API anahtarınızı girin.")
        print("Ücretsiz API anahtarı almak için: https://elevenlabs.io")
        return

    if not REF_AUDIO.exists():
        print(f"❌ Referans ses dosyası bulunamadı: {REF_AUDIO}")
        return

    print(f"📁 Referans Ses: {REF_AUDIO.name} ({REF_AUDIO.stat().st_size / 1024:.1f} KB)")
    print("🚀 ElevenLabs'e ses klonlama isteği gönderiliyor...")

    try:
        from elevenlabs.client import ElevenLabs
        client = ElevenLabs(api_key=API_KEY)

        # Sesi klonla
        with open(REF_AUDIO, "rb") as f:
            voice = client.clone(
                name="Almina_Tarot_Serra_Clone",
                description="Kullanıcının gönderdiği videodan klonlanan orijinal kadın tarot sesi",
                files=[f]
            )

        print(f"\n🎉 SES BAŞARIYLA KLONLANDI!")
        print(f"👉 Yeni Voice ID: {voice.voice_id}")

        # .env dosyasını güncelle
        lines = []
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("ELEVENLABS_VOICE_ID="):
                    lines.append(f"ELEVENLABS_VOICE_ID={voice.voice_id}\n")
                elif line.startswith("TTS_PROVIDER="):
                    lines.append("TTS_PROVIDER=elevenlabs\n")
                else:
                    lines.append(line)

        with open(ENV_FILE, "w", encoding="utf-8") as f:
            f.writelines(lines)

        print("✅ .env dosyası yeni ses ile güncellendi ve TTS_PROVIDER=elevenlabs yapıldı.")
        print("Artık Almina chatteki tüm yeni soruları videodaki kadının sesiyle okuyacak!\n")

    except Exception as e:
        print(f"❌ Klonlama sırasında hata: {e}")

if __name__ == "__main__":
    main()
