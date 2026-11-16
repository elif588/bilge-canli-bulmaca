import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

if ENV_PATH.exists():
    load_dotenv(ENV_PATH)
else:
    load_dotenv(BASE_DIR / ".env.example")

class Config:
    TIKTOK_USERNAME = os.getenv("TIKTOK_USERNAME", "kargamlbb")
    
    # LLM
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini").lower()
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    
    # TTS
    TTS_PROVIDER = os.getenv("TTS_PROVIDER", "edge-tts").lower()
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
    ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")
    EDGE_TTS_VOICE = os.getenv("EDGE_TTS_VOICE", "tr-TR-EmelNeural")
    
    # Queue & Priority
    GIFT_PRIORITY_ENABLED = os.getenv("GIFT_PRIORITY_ENABLED", "true").lower() == "true"
    MIN_GIFT_COINS = int(os.getenv("MIN_GIFT_COINS", "1"))
    FREE_READING_INTERVAL = int(os.getenv("FREE_READING_INTERVAL", "10"))
    USER_COOLDOWN_SECONDS = int(os.getenv("USER_COOLDOWN_SECONDS", "120"))
    
    # Server
    SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
    SERVER_PORT = int(os.getenv("PORT", os.getenv("SERVER_PORT", "8765")))
    
    # Directories
    AUDIO_DIR = BASE_DIR / "web_overlay" / "audio"
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
