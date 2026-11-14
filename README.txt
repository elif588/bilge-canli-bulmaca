BİLGE CANLI BULMACA - RENDER SUNUCU DOSYALARI

Bu ZIP'in içindekiler:
- server.py        : FastAPI + TikTok LIVE olaylarını WebSocket'e aktaran sunucu
- requirements.txt: Gerekli Python paketleri

ÖNEMLİ
- Bu dosyalar GitHub deposunun kök dizinine, index.html ile aynı seviyeye yüklenmelidir.
- ZIP dosyasının kendisini Render'a kaynak olarak vermeyin. ZIP'i iPhone Dosyalar uygulamasında açıp içindeki iki dosyayı GitHub'a yükleyin.
- TikTokLive, TikTok'un resmî API'si değildir; üçüncü taraf bir kütüphanedir. TikTok tarafındaki değişiklikler bağlantıyı etkileyebilir.
- Render ücretsiz Web Service 15 dakika gelen trafik olmazsa uykuya geçebilir ve yeniden başlarken gecikme yaşanabilir. Kesintisiz yayın garantisi değildir.

RENDER AYARLARI
Language: Python 3
Branch: main
Root Directory: boş
Build Command: pip install -r requirements.txt
Start Command: uvicorn server:app --host 0.0.0.0 --port $PORT
Compute: Free (ücretli plan seçmeyin)

DEPLOY SONRASI
Sunucu adresiniz https://SERVIS-ADINIZ.onrender.com biçiminde olur.
Sağlık kontrolü: https://SERVIS-ADINIZ.onrender.com/health
WebSocket adresi: wss://SERVIS-ADINIZ.onrender.com/ws
Bu WebSocket adresini oyunun içindeki "Bağlantı sunucusu WebSocket adresi" alanına girin.

TÜRKÇE SES VE OTOMATİK OYUN
- Bilge, Microsoft'un tr-TR-EmelNeural Türkçe kadın sinir ağı sesini kullanır.
- Ses internet üzerinden üretilir; API anahtarı gerekmez.
- TikTok kullanıcı adı ve anons metni Microsoft'un çevrimiçi ses hizmetine gönderilerek ses oluşturulur.
- Sunucu veya internet erişimi yoksa robotik tarayıcı sesine dönmez; hata etkinlik akışında görünür.
- Sayfa açılınca varsayılan TikTok hesabına bağlanmayı dener; bağlantı koparsa otomatik yeniden bağlanır.
- Gelen her yorum akışta gösterilir; doğru cevapla eşleşen veya cevabı içeren yorum otomatik puanlanır.
- Bu doğal konuşmaya yakın yapay zekâ sesidir, gerçek insan kaydı değildir.