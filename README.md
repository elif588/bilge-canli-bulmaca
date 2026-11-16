# 🔮 Profesyonel TikTok Canlı Yayın AI Tarot Sistemi

Bu proje, TikTok'ta popüler olan (`@tarotserra` benzeri) interaktif yapay zeka tarot yayınlarının tüm altyapısını sunar.

Canlı yayındaki izleyicilerin yorumlarını ve hediyelerini anlık olarak dinler, kuyruğa alır, 78 kartlık tarot destesinden kart çeker, GPT-4o / Gemini ile kişiye özel mistik bir yorum üretir ve gerçek insan sesiyle seslendirerek OBS ekranına 3D kart animasyonlarıyla yansıtır.

---

## 🚀 Öne Çıkan Özellikler

1. **İki Kademeli Öncelik Kuyruğu (Priority Queue):**
   * **Ücretsiz İzleyiciler:** Canlı sohbete soru veya niyet yazanlara tek kartlık rehberlik.
   * **VIP Hediye Gönderenler (Gül vb.):** Sıranın **EN ÖNÜNE** geçer, ekranda altın renkli VIP rozeti parlar ve 3 kartlık (Geçmiş - Şimdi - Gelecek / Derin Aşk) özel açılım yapılır.
2. **Tekrara Düşmeyen Profesyonel Yorumcu Dili:**
   * Gemini 1.5 Flash veya GPT-4o ile izleyicinin ismine ve sorusuna özel, samimi, akıcı ve mistik yorumlar üretilir. Asla robotik cümleler kurmaz.
3. **Gerçek İnsan Sesi (TTS):**
   * **ElevenLabs:** İnsan nefes sesleri ve tonlamalarına sahip ultra-gerçekçi kadın sesi.
   * **Edge-TTS (Ücretsiz):** Microsoft'un `tr-TR-EmelNeural` sakin mistik kadın sesiyle sıfır maliyetle çalışır.
4. **OBS Canlı Yayın Arayüzü (9:16 Dikey Format):**
   * 1080x1920 dikey çözünürlük için tasarlanmış, altın ve mor mistik temalı Web Overlay.
   * 3D Kart çevirme (Flip) animasyonu.
   * Gerçek zamanlı daktilo altyazı efekti ve ses dalgası visualizer.
   * Sıradaki izleyicileri gösteren alt bilgi bandı.

---

## 📁 Proje Dosya Yapısı

* [config.py](file:///c:/Users/CAN/Desktop/tarot/config.py) : Sistem ayarları ve API anahtarları.
* [tarot_deck.py](file:///c:/Users/CAN/Desktop/tarot/tarot_deck.py) : 78 adet Büyük ve Küçük Arkana kartları, sembolleri ve düz/ters anlamları.
* [tarot_ai.py](file:///c:/Users/CAN/Desktop/tarot/tarot_ai.py) : Gemini ve OpenAI destekli profesyonel tarot yorum motoru.
* [voice_engine.py](file:///c:/Users/CAN/Desktop/tarot/voice_engine.py) : ElevenLabs ve Edge-TTS ses sentezleyici.
* [queue_manager.py](file:///c:/Users/CAN/Desktop/tarot/queue_manager.py) : Hediye ve chat öncelik kuyruğu + spam önleyici.
* [tiktok_listener.py](file:///c:/Users/CAN/Desktop/tarot/tiktok_listener.py) : TikTokLive canlı yayın dinleyici (yorumlar & hediyeler).
* [server.py](file:///c:/Users/CAN/Desktop/tarot/server.py) : OBS için WebSocket ve yerel web sunucusu.
* [web_overlay/](file:///c:/Users/CAN/Desktop/tarot/web_overlay/) : OBS Tarayıcı Kaynağı (HTML5/CSS3/JS).
* [test_simulation.py](file:///c:/Users/CAN/Desktop/tarot/test_simulation.py) : Canlı yayına çıkmadan sistemi bilgisayarınızda test eden simülatör.
* [run.py](file:///c:/Users/CAN/Desktop/tarot/run.py) : Canlı yayını başlatan ana orkestratör.

---

## 🛠️ Kurulum ve Ayarlar

### 1. Ayar Dosyasını Düzenleyin (`.env`)
Klasördeki `.env.example` dosyasını kopyalayıp `.env` adıyla kaydedin:
```bash
cp .env.example .env
```
İçerisindeki ayarları isteğinize göre güncelleyin:
* `TIKTOK_USERNAME`: Kendi TikTok kullanıcı adınız (örn: `benim_hesabim`)
* `GEMINI_API_KEY`: [Google AI Studio](https://aistudio.google.com/)'dan ücretsiz alabileceğiniz API anahtarı (Varsayılan olarak aktiftir).
* `TTS_PROVIDER`: `edge-tts` (Tamamen ücretsiz) veya `elevenlabs` (Maksimum doğallık).

---

## 🧪 Canlı Yayına Çıkmadan Önce Test Edin (Simülasyon Modu)

Sistemi denemek için canlı yayına gerek yoktur:
1. Terminalde şu komutu çalıştırın:
   ```bash
   python test_simulation.py
   ```
2. Tarayıcınızda veya OBS'te şu adresi açın:
   ```
   http://127.0.0.1:8765/index.html
   ```
3. Ekranda simülasyon olarak bir normal izleyicinin tek kartlık açılımı, ardından bir hediye gönderenin 3 kartlık VIP açılımı sesli ve animasyonlu olarak oynatılacaktır!

---

## 🎥 OBS Studio ve TikTok Live Studio Ayarları

1. **OBS Studio'yu Açın.**
2. **Kaynaklar (Sources)** kısmından **+ (Ekle)** -> **Tarayıcı (Browser)** seçin.
3. Ayarları şu şekilde yapın:
   * **URL:** `http://127.0.0.1:8765/index.html`
   * **Genişlik (Width):** `1080` (veya test için `576`)
   * **Yükseklik (Height):** `1920` (veya test için `1024`)
   * **"Sesi OBS ile kontrol et" (Control audio via OBS):** İŞARETLEYİN (Böylece ses yayına direkt gider).
4. Terminalde canlı modu başlatın:
   ```bash
   python run.py
   ```
5. TikTok'ta canlı yayını başlattığınız anda sistem chatteki yorumları okumaya, hediyeleri sıraya almaya ve otomatik olarak sesli açılımları yapmaya başlayacaktır!
