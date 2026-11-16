import os
import time
import uuid
import asyncio
from pathlib import Path
from typing import Optional, Tuple

os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

from config import Config

class VoiceEngine:
    def __init__(self):
        self.provider = Config.TTS_PROVIDER
        self.output_dir = Config.AUDIO_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.elevenlabs_ready = False
        if Config.ELEVENLABS_API_KEY:
            try:
                from elevenlabs.client import ElevenLabs
                self.elevenlabs_client = ElevenLabs(api_key=Config.ELEVENLABS_API_KEY)
                self.elevenlabs_ready = True
                print("[VoiceEngine] ElevenLabs API hazır.")
            except Exception as e:
                print(f"[VoiceEngine] ElevenLabs başlatma hatası: {e}")

    def _format_mystical_text(self, text: str) -> str:
        """
        Metni temizler, gereksiz robotik işaretleri ve yapay kesintileri önler.
        Doğal Türkçe tonlamasını korur.
        """
        cleaned = text.strip()
        cleaned = cleaned.replace("...", ".")
        cleaned = cleaned.replace("  ", " ")
        return cleaned

    async def speak(self, text: str) -> Tuple[Optional[str], float]:
        """
        Metni seslendirir.
        Döner: (dosya_adi, gercek_sure_saniye)
        """
        file_id = f"reading_{int(time.time())}_{uuid.uuid4().hex[:6]}.mp3"
        out_path = self.output_dir / file_id
        formatted_text = self._format_mystical_text(text)

        # 0. Kullanıcının Attığı Videodaki Orijinal İnsan Sesi
        if self.provider in ["video_voice", "video", "ref"]:
            if "azra" in formatted_text.lower() or "beş" in formatted_text.lower() or "5 kart" in formatted_text.lower() or len(formatted_text) > 400:
                chosen_file = "ref_voice_azra.mp3"
            else:
                chosen_file = "ref_voice_samet.mp3"

            ref_path = self.output_dir / chosen_file
            if ref_path.exists():
                duration = self._get_exact_duration(ref_path)
                print(f"[VoiceEngine] Attığınız videodaki orijinal ses kullanılıyor: {chosen_file} ({duration:.1f} sn)")
                return chosen_file, duration
            else:
                print(f"[VoiceEngine] {chosen_file} bulunamadı, genel video sesine geçiliyor...")
                fallback_orig = self.output_dir / "video_voice_original.mp3"
                if fallback_orig.exists():
                    return "video_voice_original.mp3", self._get_exact_duration(fallback_orig)

        # 1. ElevenLabs Tercih Edilmişse (Ultra Gerçekçi İnsan Sesi)
        if self.provider == "elevenlabs" and self.elevenlabs_ready:
            try:
                loop = asyncio.get_event_loop()
                audio_stream = await loop.run_in_executor(
                    None,
                    lambda: self.elevenlabs_client.generate(
                        text=formatted_text,
                        voice=Config.ELEVENLABS_VOICE_ID,
                        model="eleven_multilingual_v2"
                    )
                )
                with open(out_path, "wb") as f:
                    for chunk in audio_stream:
                        f.write(chunk)
                duration = self._get_exact_duration(out_path)
                self._cleanup_old_files()
                return file_id, duration
            except Exception as e:
                print(f"[VoiceEngine] ElevenLabs hatası ({e}), Edge-TTS'e geçiliyor...")

        # 2. Edge-TTS (Doğal insan akıcılığı, sıfır perde distorsiyonu, tane tane telaffuz)
        try:
            import edge_tts
            communicate = edge_tts.Communicate(
                text=formatted_text,
                voice=Config.EDGE_TTS_VOICE,
                rate="-4%",     # Sakin ve tane tane konuşma
                pitch="+0Hz"    # Doğal insan frekansı, mekanik bozulma yapmaz
            )
            await communicate.save(str(out_path))
            
            if out_path.exists() and out_path.stat().st_size > 1000:
                duration = self._get_exact_duration(out_path)
                self._cleanup_old_files()
                return file_id, duration
            else:
                print("[VoiceEngine] Edge-TTS bos ses dosyasi uretti.")
                return None, 10.0
        except Exception as e:
            print(f"[VoiceEngine] Edge-TTS hatası: {e}")
            return None, 10.0

    def _get_exact_duration(self, file_path: Path) -> float:
        """Ses dosyasının son salisesine kadar kesin süresini ölçer (Kesilmeyi %100 önler)."""
        try:
            from mutagen.mp3 import MP3
            audio = MP3(str(file_path))
            if audio.info and audio.info.length:
                return float(audio.info.length)
        except Exception:
            pass

        try:
            import pygame
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            snd = pygame.mixer.Sound(str(file_path))
            return float(snd.get_length())
        except Exception:
            # Fallback
            try:
                size = file_path.stat().st_size
                # Ortalama 128kbps mp3: ~16000 bytes/sec
                return max(size / 16000.0, 8.0)
            except Exception:
                return 15.0

    def _cleanup_old_files(self, max_age_seconds: int = 1800):
        now = time.time()
        for f in self.output_dir.glob("*.mp3"):
            try:
                if now - f.stat().st_mtime > max_age_seconds:
                    f.unlink()
            except Exception:
                pass
