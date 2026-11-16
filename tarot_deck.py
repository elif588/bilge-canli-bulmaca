# ==============================================================================
# ALMİNA TAROT - 78 KARTLIK EKSİKSİZ RIDER-WAITE DESTESİ VE GERÇEK ANLAMLARI
# ==============================================================================
import random
from typing import Dict, List, Optional

# 22 BÜYÜK ARKANA (MAJOR ARCANA)
MAJOR_ARCANA = [
    {
        "id": "m00", "name_tr": "Joker (Deli)", "name_en": "The Fool", "image": "cards/00_Fool.jpg",
        "keywords": ["Sıfırdan Başlangıç", "Cesaret", "Plansız Adım", "Özgürlük"],
        "love": "Aklındaki kişi seninle ilgili ani ve hesapsız bir adım atmak üzere. Kafasındaki tüm kaygıları bir kenara bırakıp sürpriz bir mesaj atabilir.",
        "truth": "Numaranı silmemiş, aksine aranızdaki durumu akışa bırakmış. Bir sabah aniden iletişime geçebilir.",
        "career": "Kariyerinde risk almaktan korkma, karşına çıkacak yeni bir teklif sana bambaşka kapılar açacak.",
        "advice": "Geçmişin yüklerini sırtından indir, yeni bir sayfa açmak için mükemmel bir zamandasın."
    },
    {
        "id": "m01", "name_tr": "Büyücü", "name_en": "The Magician", "image": "cards/01_Magician.jpg",
        "keywords": ["Manifest", "İletişim Ustalığı", "Eylem Gücü", "İkna"],
        "love": "İletişim kapısı ardına kadar açık! Aklındaki kişi kelimelerini özenle seçerek seninle irtibata geçecek.",
        "truth": "Kesinlikle silmemiş. Hatta numaran elinin altında ve seninle nasıl tekrar konuşacağının provasını yapıyor.",
        "career": "Yeteneğin ve zekanla öne çıkacaksın. İstediğin bir iş ya da terfiyi rahatlıkla bağlayabilirsin.",
        "advice": "İpleri başkasına bırakma, niyetini netleştir ve ilk adımı atmaktan çekinme."
    },
    {
        "id": "m02", "name_tr": "Azize", "name_en": "The High Priestess", "image": "cards/02_High_Priestess.jpg",
        "keywords": ["Gizli Sırlar", "Derin Sezgi", "Sessizlik", "Gizli Bağ"],
        "love": "Aklındaki kişi şu an sessizlik zırhına bürünmüş. Sana karşı derin hisleri var ama bunu gururundan gizliyor.",
        "truth": "Numaran duruyor ama seni gizli bir hesaptan ya da ortak tanıdıklardan gizlice takip ediyor.",
        "career": "İş ortamında henüz bilmediğin bazı arka plan konuşmaları var. Karar vermeden önce gözlem yap.",
        "advice": "Mantığınla değil iç sesinle hareket et, hissettiğin her şey gerçeğin ta kendisi."
    },
    {
        "id": "m03", "name_tr": "İmparatoriçe", "name_en": "The Empress", "image": "cards/03_Empress.jpg",
        "keywords": ["Bereket", "Büyük Cazibe", "Aşkın Yeşermesi", "Evlilik Potansiyeli"],
        "love": "Sen onun gözünde son derece çekici, değerli ve yeri doldurulamaz bir kadınsın. Bu bağ evliliğe ve resmiyete çok açık.",
        "truth": "Numaranı asla silmemiş. Seni kaybetmekten içten içe korkuyor ve sana duyduğu hayranlık çok yüksek.",
        "career": "Maddi ve manevi olarak bolluk dönemine giriyorsun. Emek verdiğin bir işin paraya dönüştüğünü göreceksin.",
        "advice": "Kendi değerinin farkına var, sen parladıkça o da sana doğru çekilecek."
    },
    {
        "id": "m04", "name_tr": "İmparator", "name_en": "The Emperor", "image": "cards/04_Emperor.jpg",
        "keywords": ["Otorite", "Gurur", "Sağlam Duruş", "Liderlik"],
        "love": "Karşında inatçı ve geri adım atmakta zorlanan gururlu bir eril enerji var. Seni seviyor ama ilk adımı senden bekliyor.",
        "truth": "Numaranı silmedi. Ancak kendi prensiplerinden taviz vermemek için inadını sürdürüyor.",
        "career": "İşinde patronluk, liderlik veya sağlam bir söz hakkı elde edeceksin. Saygınlığın artıyor.",
        "advice": "Onun inadına inatla karşılık verme, sınırlarını koruyarak dik bir duruş sergile."
    },
    {
        "id": "m05", "name_tr": "Aziz", "name_en": "The Hierophant", "image": "cards/05_Hierophant.jpg",
        "keywords": ["Ciddiyet", "Gelenek", "Evlilik Kararı", "Sadakat"],
        "love": "Bu ilişki sıradan bir flört değil, ciddiye giden ve ailelerin onaylayacağı sağlam bir sürece evriliyor.",
        "truth": "Numaran kayıtlı ve sana karşı sorumluluk hissediyor. Gelip geçici bir heves olarak görmüyor.",
        "career": "Kurumsal bir yükseliş, resmi bir sözleşme veya eğitim/sınav başarısı kapıda.",
        "advice": "Günübirlik oyunlardan uzak dur, dürüst ve ahlaki değerlere bağlı kalmak sana kazandıracak."
    },
    {
        "id": "m06", "name_tr": "Aşıklar", "name_en": "The Lovers", "image": "cards/06_Lovers.jpg",
        "keywords": ["Ruh İkizi", "Büyük Tutku", "Kadersel Tercih", "Karşılıklı Aşk"],
        "love": "İki kalbin birbirine görünmez bağlarla bağlı olduğu gerçek bir ruh bağı var. Aranızdaki çekimi ne mesafe ne de tartışmalar bitirebilir.",
        "truth": "Numaran kesinlikle silinmedi. Aklında sürekli sen varsın ve senin lehine bir karar aşamasında.",
        "career": "Çok önemli iki seçenek arasında kalabilirsin, kalbinin heyecan duyduğu seçeneğe yönel.",
        "advice": "Kafandaki şüpheleri bırak, aranızdaki çekim gerçek ve karşılıklı."
    },
    {
        "id": "m07", "name_tr": "Savaş Arabası", "name_en": "The Chariot", "image": "cards/07_Chariot.jpg",
        "keywords": ["Hızlı İlerleme", "Geliş", "Engelleri Aşma", "Zafer"],
        "love": "Aklındaki kişi mesafeleri veya engelleri aşarak hızla sana doğru bir hamle yapacak. Ani bir ziyaret veya kararlı bir adım var.",
        "truth": "Numaran duruyor ve çok yakında sessizliğini bozup hızla iletişime geçecek.",
        "career": "Hedefine odaklan, rakiplerini geride bırakıp zafer kazanacağın bir dönemdesin.",
        "advice": "Duygularınla mantığını aynı hedefe yönelt, kontrolü elden bırakma."
    },
    {
        "id": "m08", "name_tr": "Güç", "name_en": "Strength", "image": "cards/08_Strength.jpg",
        "keywords": ["Sabırla Kazanma", "Tutkuyu Ehlileştirme", "Şefkat", "Cesaret"],
        "love": "Karşındaki kişinin içindeki egoyu ve öfkeyi sadece senin şefkatin eritebilir. Aranızdaki tutku son derece güçlü.",
        "truth": "Numaranı silmedi. Ancak kendini tutmaya çalışıyor ama bunu uzun süre başaramayacak.",
        "career": "Zor bir kriz veya yönetici baskısı seni yıldırsa da sabrınla bu sınavdan galip çıkacaksın.",
        "advice": "Öfkeyle değil zarafetle yaklaş, gücün yumuşaklığında saklı."
    },
    {
        "id": "m09", "name_tr": "Ermiş", "name_en": "The Hermit", "image": "cards/09_Hermit.jpg",
        "keywords": ["Kendi Kabuğuna Çekilme", "Aydınlanma", "İçsel Hesaplaşma", "Mesafe"],
        "love": "Aklındaki kişi şu an kendi dünyasına çekilmiş, hayatını ve yaptığı hataları sorguluyor. Uzak durması sevgisizlikten değil içsel yorgunluğundan.",
        "truth": "Numaran duruyor. Ancak şu an kimseyle konuşmak istemediği bir inziva döneminde.",
        "career": "Tek başına çalışıp derinleşeceğin bir proje ya da araştırma sana büyük başarı getirecek.",
        "advice": "Ona nefes alacak alan tanı, kendi fenerini yaktığında sana doğru yürümeyi öğrenecek."
    },
    {
        "id": "m10", "name_tr": "Kader Çarkı", "name_en": "Wheel of Fortune", "image": "cards/10_Wheel_of_Fortune.jpg",
        "keywords": ["Kadersel Dönüşüm", "Beklenmedik Şans", "Döngünün Sonu", "İlahi Zamanlama"],
        "love": "İlişkinizde çark tamamen tersine dönüyor! Üzülen taraftın ama şimdi onun sana muhtaç olduğu, pişmanlıkla kapını çalacağı yeni bir döngü başlıyor.",
        "truth": "Numaranı silmiş olsa bile kadersel bir tesadüf veya denk gelişle tekrar karşına çıkacak.",
        "career": "Maddi anlamda talih kuşu konuyor, şans oyunları veya beklenmedik bir para akışı var.",
        "advice": "Değişime direnme, hayat seni hak ettiğin yüksek noktaya taşımak için dönüyor."
    },
    {
        "id": "m11", "name_tr": "Adalet", "name_en": "Justice", "image": "cards/11_Justice.jpg",
        "keywords": ["İlahi Hak Ediş", "Gerçeğin Ortaya Çıkışı", "Denge", "Yüzleşme"],
        "love": "Sana haksızlık yaptıysa veya aldattıysa ilahi adalet terazisi kuruldu. Yaşattığını yaşamadan bu döngüden çıkamaz.",
        "truth": "Gerçekler çok yakında gün yüzüne çıkacak. Kim haklı kim haksız netleşiyor.",
        "career": "Mahkeme, resmi evrak, sözleşme veya hak ettiğin tazminat/zam senin lehine sonuçlanacak.",
        "advice": "Haklılığından şüphe etme, ilahi sistem senin hakkını kuruşu kuruşuna teslim edecek."
    },
    {
        "id": "m12", "name_tr": "Asılan Adam", "name_en": "The Hanged Man", "image": "cards/12_Hanged_Man.jpg",
        "keywords": ["Askıda Kalma", "Farklı Açıdan Bakma", "Fedakarlık", "Bekleyiş"],
        "love": "Şu an her şey havada ve belirsiz. Karşı taraf ne ileri gidiyor ne de tamamen kopuyor; bir bekleme ve kilitlenme enerjisi hakim.",
        "truth": "Numaranı silmedi ama eylemsiz kalmayı tercih ediyor. Durumu anlamlandırmaya çalışıyor.",
        "career": "İşinde beklediğin haber biraz gecikebilir. Bu zamanı kendini geliştirmek için kullan.",
        "advice": "Zorla oldurmaya çalışma, akışa teslim ol; bekleme süreci senin lehine işliyor."
    },
    {
        "id": "m13", "name_tr": "Ölüm", "name_en": "Death", "image": "cards/13_Death.jpg",
        "keywords": ["Büyük Dönüşüm", "Eskiye Veda", "Küllerinden Doğuş", "Kaçınılmaz Son"],
        "love": "Eski ilişki kalıpları tamamen bitti. Yeniden bir araya gelseniz bile eski halinizle değil, bambaşka olgunlukla devam edebilirsiniz.",
        "truth": "Eski iletişimi tamamen kesmiş, numaranı rehberden kaldırmış olabilir. Ancak bu son, yeni bir başlangıcın habercisi.",
        "career": "Mevcut işinden ayrılma veya radikal bir sektör değişikliği seni çok daha güçlü kılacak.",
        "advice": "Biten bir şeye tutunma; gidenin gitmesine izin ver ki yeni gelen hayatını güzelleştirsin."
    },
    {
        "id": "m14", "name_tr": "Denge", "name_en": "Temperance", "image": "cards/14_Temperance.jpg",
        "keywords": ["Şifalanma", "Uyum", "Orta Yol", "Huzurlu Barışma"],
        "love": "Fırtına dindi, sular duruluyor. Kırılan kalplerin onarıldığı, karşılıklı anlayışla gelen yumuşak bir barışma enerjisi var.",
        "truth": "Numaranı silmemiş. Sana karşı olan hisleri sakinleşmiş ve yapıcı bir konuşma arıyor.",
        "career": "Gelir ve giderlerin dengeleneceği, iş yerindeki huzurun yerine geleceği ferah bir dönem.",
        "advice": "Aşırılıklardan kaçın; ne çok mesafeli ol ne de çok üzerine düş, denge sana kazandıracak."
    },
    {
        "id": "m15", "name_tr": "Şeytan", "name_en": "The Devil", "image": "cards/15_Devil.jpg",
        "keywords": ["Kör Kütük Bağımlılık", "Toksik Tutku", "Manipülasyon", "Kopamama"],
        "love": "Birbirinize karşı hem öfkelisiniz hem de teniniz birbirinden kopamıyor. Toksik ama aşırı tutkulu bir çekim var; seni aklından çıkaramıyor.",
        "truth": "Numaranı asla silemez. Seni takıntı haline getirmiş durumda, sürekli kontrol ediyor.",
        "career": "Seni sömüren bir iş ortamına ya da manipülatif bir iş arkadaşına karşı dikkatli ol.",
        "advice": "Bu bağın seni besliyor mu yoksa tüketiyor mu olduğunu dürüstçe gör; ipleri onun eline verme."
    },
    {
        "id": "m16", "name_tr": "Yıkılan Kule", "name_en": "The Tower", "image": "cards/16_Tower.jpg",
        "keywords": ["Ani Sarsıntı", "Yalanların Çöküşü", "Şok Gelişme", "Arınma"],
        "love": "Beklenmedik ani bir patlama ya da gizlenen büyük bir gerçeğin ortaya çıkışı! Sahte temeller üzerine kurulu her şey sarsılıyor.",
        "truth": "Ani bir öfkeyle numaranı silmiş veya engellemiş olabilir. Ancak bu şok dalgası geçtikten sonra gerçekle yüzleşecek.",
        "career": "İş yerinde ani bir anlaşmazlık veya kriz çıkabilir. Yıkılan şey seni daha sağlam bir yere taşıyacak.",
        "advice": "Korkan yanına değil gerçeğe sarıl, çürük olan yıkılmalıdır ki sağlam olan inşa edilsin."
    },
    {
        "id": "m17", "name_tr": "Yıldız", "name_en": "The Star", "image": "cards/17_Star.jpg",
        "keywords": ["Umutların Gerçekleşmesi", "Şifa", "İlahi Koruma", "Müjdeli Haber"],
        "love": "Karanlık gecenin ardından parlayan en parlak müjde! Aklındaki kişiyle aranızdaki soğukluk bitiyor, dileğin kabul oluyor.",
        "truth": "Numaran duruyor. Sana dair hayalleri taptaze, çok yakında sıcak bir adımla sana dönecek.",
        "career": "Kariyerinde yıldızının parlayacağı, takdir toplayacağın ve kazancının katlanacağı bir evre.",
        "advice": "Umutsuzluğa kapılma, ilahi ışık senin yolunu aydınlatıyor."
    },
    {
        "id": "m18", "name_tr": "Ay", "name_en": "The Moon", "image": "cards/18_Moon.jpg",
        "keywords": ["Bilinmeyenler", "Gizli Gerçekler", "Korkular", "Sezgisel Rüyalar"],
        "love": "Şu an her şey sis perdesi arkasında. Senden sakladığı bir durum veya kafasındaki büyük korkular aranıza mesafe koymuş.",
        "truth": "Numaran kayıtlı ama kafası aşırı karışık. Seni stalklıyor ve rüyalarında görüyor.",
        "career": "Göründüğü gibi olmayan sözleşmelere ve samimiyetsiz iş arkadaşlarına karşı uyanık ol.",
        "advice": "Gözünle gördüğüne değil iç sesine güven, yakında sis tamamen dağılacak."
    },
    {
        "id": "m19", "name_tr": "Güneş", "name_en": "The Sun", "image": "cards/19_Sun.jpg",
        "keywords": ["Büyük Zafer", "Kavuşma", "Aydınlık", "Sonsuz Neşe"],
        "love": "Destenin en mutlu kartı! Aşkta barışma, kavuşma, net bir itiraf ve yüzünü güldürecek büyük bir mutluluk çok yakın.",
        "truth": "Numaranı asla silmemiş. Seni hayatının ışığı olarak görüyor, tüm buzlar eriyecek.",
        "career": "Maddi başarı, sınav kazanma, işe kabul edilme ve hayatının en parlak dönemi başlıyor.",
        "advice": "Gülümse ve anı yaşa, hak ettiğin güneş sonunda senin için doğdu."
    },
    {
        "id": "m20", "name_tr": "Mahkeme", "name_en": "Judgement", "image": "cards/20_Judgement.jpg",
        "keywords": ["Büyük Uyanış", "İkinci Şans", "Hesaplaşma", "Geri Dönüş"],
        "love": "Geçmişten gelen büyük bir uyanış ve ikinci şans! Pişmanlıkla kapına gelen, af dileyen bir geri dönüş var.",
        "truth": "Numaran duruyor. Vicdan azabı çekiyor ve seninle açıkça konuşup yeni bir şans istemek için hazırlanıyor.",
        "career": "Geçmişte yaptığın bir başvurudan veya ertelenen bir projeden çok olumlu bir dönüş alacaksın.",
        "advice": "Eski hataları tekrarlamadan olgunlukla karar ver; bu ikinci şans dönüm noktan olacak."
    },
    {
        "id": "m21", "name_tr": "Dünya", "name_en": "The World", "image": "cards/21_World.jpg",
        "keywords": ["Tamamlanma", "Büyük Zafer", "Mutlu Son", "Kavuşma"],
        "love": "Eksik parçan tamamlanıyor. Ayrılık bitti, kadersel birleşme taçlandı. Evlilik veya uzun süreli bağ kapıda.",
        "truth": "Numaranı silmedi. Sen onun için tüm dünyasın ve bu hikaye yarım kalmayacak.",
        "career": "Büyük bir kariyer sıçraması, terfi ve finansal özgürlük seni bekliyor.",
        "advice": "Kutla, zorlu sınavlar bitti, artık ödülünü alma zamanı."
    }
]

# KUPA SERİSİ (CUPS - 14 KART)
CUPS = [
    {"id": "c01", "name_tr": "Kupa Ası", "name_en": "Ace of Cups", "image": "cards/Cups01.jpg", "keywords": ["Saf Sevgi", "Aşk İtirafı", "Duygusal Başlangıç"], "love": "Kalbi sana karşı sevgiyle dolup taşıyor, çok yakında net bir aşk teklifi veya duygusal itiraf kapında.", "truth": "Numaranı silmedi, aksine telefonuna bakıp sana yazma cesareti topluyor.", "advice": "Kalbinin kapılarını aç, samimi duygu akışına izin ver."},
    {"id": "c02", "name_tr": "Kupa İkilisi", "name_en": "Two of Cups", "image": "cards/Cups02.jpg", "keywords": ["Ruh Eşi Bağı", "Karşılıklı Aşk", "Barışma"], "love": "İki kalbin aynı ritimde atması! Aşkta barışma, karşılıklı özlem ve sarılma enerjisi hakim.", "truth": "Kesinlikle silmedi. Seni düşünüyor ve seninle tekrar aynı frekansta buluşmak istiyor.", "advice": "Gururu kenara bırak, aranızdaki bağ iki taraf için de kutsal."},
    {"id": "c03", "name_tr": "Kupa Üçlüsü", "name_en": "Three of Cups", "image": "cards/Cups03.jpg", "keywords": ["Kutlama", "Sevinçli Haber", "Buluşma"], "love": "Arkadaş ortamında karşılaşma ya da sevinçli bir buluşma var. Kalbini ferahlatan bir haber alacaksın.", "truth": "Numaran duruyor, seninle ilgili ortak çevrelerden haber almaya çalışıyor.", "advice": "Sosyal ol, enerjini yüksek tut; neşeli gelişmeler kapıda."},
    {"id": "c04", "name_tr": "Kupa Dörtlüsü", "name_en": "Four of Cups", "image": "cards/Cups04.jpg", "keywords": ["Gönülsüzlük", "Fırsatı Görmeme", "Kapris"], "love": "Şu an sana karşı bir kırgınlık ve kapris yapıyor. Önündeki sevgiyi görmezden gelerek içine kapanmış.", "truth": "Numaranı silmedi ama inatla mesaj atmayarak seni meraklandırmaya çalışıyor.", "advice": "Üstüne düşme, aramadığında kendi kendine eksikliğini hissedecek."},
    {"id": "c05", "name_tr": "Kupa Beşlisi", "name_en": "Five of Cups", "image": "cards/Cups05.jpg", "keywords": ["Derin Pişmanlık", "Kayıp Duygusu", "Gözyaşı"], "love": "Yaptığı hatanın farkına varmış, arkasını dönüp döktüğü süte ağlıyor. Seni kaybettiği için yoğun pişmanlık duyuyor.", "truth": "Numaranı silmiş olsa bile vicdan azabından kıvranıyor ve geri dönmek istiyor.", "advice": "Dökülen süte ağlama, arkanda hala ayakta duran iki kadehin var."},
    {"id": "c06", "name_tr": "Kupa Altılısı", "name_en": "Six of Cups", "image": "cards/Cups06.jpg", "keywords": ["Geçmişten Gelen Aşk", "Masum Anılar", "Geri Dönüş"], "love": "Geçmişteki o saf, temiz aşk günleri canlanıyor. Aklındaki eski sevgili pişmanlıkla geri dönecek.", "truth": "Numaran kayıtlı ve eski fotoğraflarınıza bakıp nostalji yapıyor.", "advice": "Geçmişin güzel hatıralarını hatırla ama yeni geleceği inşa etmeyi unutma."},
    {"id": "c07", "name_tr": "Kupa Yedilisi", "name_en": "Seven of Cups", "image": "cards/Cups07.jpg", "keywords": ["Kafa Karışıklığı", "İllüzyon", "Çok Seçenek"], "love": "Kafası çok karışık, ne istediğini kendisi de bilmiyor. Hayaller ve gerçekler arasında bocalıyor.", "truth": "Numaranı silmedi ama kafasını toparlamadan atacağı adımlar havada kalabilir.", "advice": "Somut adımlara bak, laflara ve kuru vaatlere kanma."},
    {"id": "c08", "name_tr": "Kupa Sekizlisi", "name_en": "Eight of Cups", "image": "cards/Cups08.jpg", "keywords": ["Arkasını Dönüp Gitme", "Arayış", "Duygusal Mola"], "love": "Kendini yetersiz hissettiği için bir süreliğine arkasını dönüp gitmiş. Ancak bu gidiş bir arayış, sonsuz bir veda değil.", "truth": "Numaran kayıtlı ama şu an kendi içsel boşluğunu doldurmaya çalışıyor.", "advice": "Gitmesine izin ver; kendi değerini anladığında arkasına bakarak geri gelecek."},
    {"id": "c09", "name_tr": "Kupa Dokuzlusu", "name_en": "Nine of Cups", "image": "cards/Cups09.jpg", "keywords": ["Dilek Kartı", "Manevi Doyum", "Muradına Erme"], "love": "Tarotun dilek kartı! Kalbinden dilediğin o kişiyle ilgili muradın hasıl oluyor; sevginin karşılığını fazlasıyla alacaksın.", "truth": "Numaranı silmedi, seni el üstünde tutacağı bir barışma hazırlığında.", "advice": "Dileğin kabul oldu, şükürde kal ve mutluluğu kabul et."},
    {"id": "c10", "name_tr": "Kupa Onlusu", "name_en": "Ten of Cups", "image": "cards/Cups10.jpg", "keywords": ["Mutlu Yuva", "Aile Saadeti", "Evlilik"], "love": "Gözyaşlarının bittiği, el ele tutuşup huzurlu bir yuva kuracağınız nihai mutluluk tablosu.", "truth": "Numaran duruyor, seninle ciddi bir gelecek ve evlilik hayal ediyor.", "advice": "Korkularını bırak, sevgi seni kucaklamaya geliyor."},
    {"id": "c11", "name_tr": "Kupa Prensi", "name_en": "Page of Cups", "image": "cards/Cups11.jpg", "keywords": ["Tatlı Bir Mesaj", "Flörtöz Adım", "Duygu Kırıntısı"], "love": "Çok yakında sana tatlı, masum ve şirin bir mesaj atacak. 'Nasılsın?' diye başlayan bir konuşma kapıda.", "truth": "Numaranı kesinlikle silmemiş, ilk fırsatta minik bir bahaneyle yazacak.", "advice": "Çocuksu heveslerine anlayışla yaklaş, mesaj geldiğinde hemen tersleme."},
    {"id": "c12", "name_tr": "Kupa Şövalyesi", "name_en": "Knight of Cups", "image": "cards/Cups12.jpg", "keywords": ["Romantik Aşık", "Teklif", "Duygusal Geliş"], "love": "Elinde sevgi kadehiyle sana doğru koşan bir aşık! Romantik bir buluşma ve aşk teklifi var.", "truth": "Numaran duruyor, seni büyülemek için güzel bir plan yapıyor.", "advice": "Romantizmin tadını çıkar, gelen sevgiyi kabul et."},
    {"id": "c13", "name_tr": "Kupa Kraliçesi", "name_en": "Queen of Cups", "image": "cards/Cups13.jpg", "keywords": ["Derin Şefkat", "Sezgisel Kadın", "Aşk"], "love": "Sen onun hayatındaki en merhametli ve sezgisel kadınsın. Kalbindeki sevgiyi hiçbir şey silemez.", "truth": "Numaranı silmedi, senin şefkatine ve enerjine aşırı derecede muhtaç.", "advice": "Kendi duygusal sınırlarını çiz ama kalbini taşa çevirme."},
    {"id": "c14", "name_tr": "Kupa Kralı", "name_en": "King of Cups", "image": "cards/Cups14.jpg", "keywords": ["Duygusal Olgunluk", "Sadakat", "Huzur Veren Erkek"], "love": "Duygularını içinde yaşayan ama sana derinden bağlı olan olgun bir eril enerji seni sahiplenecek.", "truth": "Numaran kayıtlı, sana karşı hissettiği güven ve sevgi sağlam.", "advice": "Sabırlı ol, sevgisini sözlerle değil davranışlarıyla gösterecek."}
]

# KILIÇ SERİSİ (SWORDS - 14 KART)
SWORDS = [
    {"id": "s01", "name_tr": "Kılıç Ası", "name_en": "Ace of Swords", "image": "cards/Swords01.jpg", "keywords": ["Büyük Gerçek", "Keskin Karar", "Netlik"], "love": "Aranızdaki tüm belirsizlikler tek bir net konuşmayla bıçak gibi kesilip aydınlanacak.", "truth": "Eğer numaranı sildiyse bile gururundan sildi; ama gerçeklerle yüzleşmekten kaçamaz, çok net bir hesaplaşma var.", "advice": "Duygularına değil gerçeklere odaklan, netlik sana özgürlük getirecek."},
    {"id": "s02", "name_tr": "Kılıç İkilisi", "name_en": "Two of Swords", "image": "cards/Swords02.jpg", "keywords": ["Arada Kalma", "Gözleri Kapatma", "Sessizlik"], "love": "İki durum arasında sıkışıp kalmış, ne sana gelebiliyor ne de senden vazgeçebiliyor.", "truth": "Numaranı silmedi ama sana yazmamak için adeta gözlerini ve kulağını dünyaya kapattı.", "advice": "Karar vermesi için onu zorlama, kendi iç çatışmasını çözmesini bekle."},
    {"id": "s03", "name_tr": "Kılıç Üçlüsü", "name_en": "Three of Swords", "image": "cards/Swords03.jpg", "keywords": ["Kalp Kırıklığı", "Üçüncü Kişi", "Ayrılık Acısı"], "love": "Kalbe saplanan üç kılıç! Arada üçüncü bir kişinin lafı, ihanet ya da çok ağır sözler var.", "truth": "Evet, öfkeyle numaranı silmiş ya da engellemiş olabilir. İki tarafın da kalbi kanıyor.", "advice": "Kırılan kalbini iyileştirmeye odaklan, bu acı seni olgunlaştıracak."},
    {"id": "s04", "name_tr": "Kılıç Dörtlüsü", "name_en": "Four of Swords", "image": "cards/Swords04.jpg", "keywords": ["Dinlenme Molası", "Geri Çekilme", "Sessizlik"], "love": "Şu an ilişki yoğun bakımda. Kavga etmek yerine iki tarafın da kafasını dinlemesi gerekiyor.", "truth": "Numaran duruyor ama telefonu eline alıp yazacak enerjisi yok, zihnen çok yorgun.", "advice": "Hiçbir şey yapma ve geri çekil, dinlenmek en iyi ilaçtır."},
    {"id": "s05", "name_tr": "Kılıç Beşlisi", "name_en": "Five of Swords", "image": "cards/Swords05.jpg", "keywords": ["Ego Savaşı", "Laf Sokma", "Haksız Zafer"], "love": "Aranızda anlamsız bir ego ve güç savaşı var. Haklı çıkmak uğruna kalpler kırılmış.", "truth": "Gururundan numaranı silmiş gibi yapabilir ama bu sadece sana acı çektirme taktiği.", "advice": "Ego savaşından çekil, kazananı olmayan bir savaşı sürdürme."},
    {"id": "s06", "name_tr": "Kılıç Altılısı", "name_en": "Six of Swords", "image": "cards/Swords06.jpg", "keywords": ["Fırtınadan Kaçış", "Sakin Sular", "Mesafe"], "love": "Kavgalı ve fırtınalı ortamdan uzaklaşıp daha huzurlu, sakin bir döneme doğru yol alıyorsunuz.", "truth": "Numaran kayıtlı. Olaylar soğuduktan sonra daha mantıklı bir dille seninle konuşacak.", "advice": "Geçmişin yüklerini eski kıyıda bırak, önüne bak."},
    {"id": "s07", "name_tr": "Kılıç Yedilisi", "name_en": "Seven of Swords", "image": "cards/Swords07.jpg", "keywords": ["Gizli İşler", "Stalk", "Arka Planda Kaçış"], "love": "Senden gizlediği bazı şeyler olabilir. Açıkça yazmıyor ama sahte hesaplardan seni izliyor.", "truth": "Numaranı silmemiş ama sinsi ve stratejik davranıyor. Dürüstlüğünü test etmelisin.", "advice": "Gözünü dört aç, arkandan çevrilen işlere karşı uyanık ol."},
    {"id": "s08", "name_tr": "Kılıç Sekizlisi", "name_en": "Eight of Swords", "image": "cards/Swords08.jpg", "keywords": ["Kendi Tuzağına Düşme", "Çaresizlik", "Engeller"], "love": "Etrafını kılıçlarla çevrilmiş hissediyor; elini kolunu bağlayan engeller veya aile baskısı olabilir.", "truth": "Numaran duruyor ama cesaretsizliğinden dolayı adım atamayacak kadar kilitlenmiş.", "advice": "Gözündeki bağı çöz, seni hapseden tek şey kendi korkuların."},
    {"id": "s09", "name_tr": "Kılıç Dokuzlusu", "name_en": "Nine of Swords", "image": "cards/Swords09.jpg", "keywords": ["Uykusuz Geceler", "Yoğun Pişmanlık", "Kabuslar"], "love": "Geceleri uyuyamıyor, yatakta bir sağa bir sola dönüyor! Sana yaşattıklarının vicdan azabı boğazına dizilmiş.", "truth": "Numaranı asla silemez. Gece yarısı pişmanlıkla gelen bir mesaj görebilirsin.", "advice": "Kendi kendini tüketme, kurduğun senaryoların çoğu gerçek değil."},
    {"id": "s10", "name_tr": "Kılıç Onlusu", "name_en": "Ten of Swords", "image": "cards/Swords10.jpg", "keywords": ["Dibe Vuruş", "Acının Sonu", "Yeni Gün Doğuşu"], "love": "Darbe üstüne darbe aldın ama artık dibe vurdun. Buradan sonra gideceğin tek yön yukarıdır.", "truth": "Evet, numaranı silmiş veya aradaki bağı koparmış olabilir. Ancak bu acı bitti, yeni bir gün doğuyor.", "advice": "Artık sırtındaki kılıçları çıkar, karanlık bitti şafak söküyor."},
    {"id": "s11", "name_tr": "Kılıç Prensi", "name_en": "Page of Swords", "image": "cards/Swords11.jpg", "keywords": ["Stalk Ustası", "Meraklı Gözler", "Tetikte Olma"], "love": "Seni 7/24 takip ediyor! Kimin fotoğrafını beğendin, kimi takip ettin hepsini tek tek inceliyor.", "truth": "Numaranı kesinlikle silmedi. Seni radarında tutuyor ve her hareketini kolluyor.", "advice": "Sosyal medyada açık verme, onun seni merak etmesine izin ver."},
    {"id": "s12", "name_tr": "Kılıç Şövalyesi", "name_en": "Knight of Swords", "image": "cards/Swords12.jpg", "keywords": ["Fevri Çıkış", "Öfkeli Mesaj", "Hızlı Yüzleşme"], "love": "Aniden öfkeyle parlayıp fevri bir mesaj atabilir veya tartışmayla çıkıp gelebilir.", "truth": "Numaran kayıtlı. Sinirle sildiğini söylese bile hemen geri yükleyecek kadar fevri.", "advice": "Onun öfkesine aynı sertlikle karşılık verme, sakin kalırsan kontrol sende olur."},
    {"id": "s13", "name_tr": "Kılıç Kraliçesi", "name_en": "Queen of Swords", "image": "cards/Swords13.jpg", "keywords": ["Soğuk ve Mesafeli", "Sınırlarını Çizen", "Zeki Kadın"], "love": "Artık taviz vermeyen, sınırlarını net çizen ve yalanlara tahammülü olmayan güçlü bir kadınsın.", "truth": "O senin bu dik ve mesafeli duruşundan çekindiği için adım atamıyor.", "advice": "Duyguların aklının önüne geçmesin, sınırlarını koru."},
    {"id": "s14", "name_tr": "Kılıç Kralı", "name_en": "King of Swords", "image": "cards/Swords14.jpg", "keywords": ["Mantık İnsanı", "Ketum", "Duygusunu Gizleyen"], "love": "Duygularını asla belli etmeyen, mantığıyla hareket eden sert mizaçlı bir eril enerji var.", "truth": "Numaran kayıtlı ama zayıf görünmemek için gururundan asla taviz vermiyor.", "advice": "Duygusal ajitasyon yapma, onunla mantık ve olgunluk çerçevesinde konuş."}
]

# DEĞNEK SERİSİ (WANDS - 14 KART)
WANDS = [
    {"id": "w01", "name_tr": "Değnek Ası", "name_en": "Ace of Wands", "image": "cards/Wands01.jpg", "keywords": ["Yeni Tutku", "Ateşli Kıvılcım", "Aksiyon"], "love": "İçinde alev alev yanan yeni bir tutku ve arzu var. Ani bir cinsel veya romantik çekimle sana gelecek.", "truth": "Numaranı silmedi, aksine sana karşı içinde büyük bir kıvılcım yanıyor.", "advice": "Bu tutkulu enerjiyi doğru yönet, ateşin seni yakmasına izin verme."},
    {"id": "w02", "name_tr": "Değnek İkilisi", "name_en": "Two of Wands", "image": "cards/Wands02.jpg", "keywords": ["Gelecek Planı", "İki Yol", "Uzaklara Bakış"], "love": "Dünyayı avucunun içine almış, seninle olan geleceğini ve bundan sonra ne yapacağını planlıyor.", "truth": "Numaran duruyor, adım atmak için doğru zamanı ve stratejiyi kolluyor.", "advice": "Kendi geleceğinin efendisi ol, onun kararına bağımlı kalma."},
    {"id": "w03", "name_tr": "Değnek Üçlüsü", "name_en": "Three of Wands", "image": "cards/Wands03.jpg", "keywords": ["Ufuk Açılması", "Yolculuk", "Beklenen Gemi"], "love": "Gözü yollarda! Mesafeler olsa bile sana doğru yola çıkacak gemileri hazırlıyor.", "truth": "Numaran kayıtlı, aranızdaki mesafeleri aşmak için bir planı var.", "advice": "Ufkunu geniş tut, beklediğin güzel gelişmeler yakında kıyıya yanaşacak."},
    {"id": "w04", "name_tr": "Değnek Dörtlüsü", "name_en": "Four of Wands", "image": "cards/Wands04.jpg", "keywords": ["Kutlama", "Nişan/Evlilik", "Sağlam Yuva"], "love": "Tebrikler! İlişkinin resmiyete döküldüğü, söz, nişan veya birlikte yaşam kararının alındığı sağlam bir evre.", "truth": "Numaran duruyor ve seninle bir yuva kurma niyetinde.", "advice": "Huzurunu kutla, sağlam temeller üzerine kurulmuş bir bağdasın."},
    {"id": "w05", "name_tr": "Değnek Beşlisi", "name_en": "Five of Wands", "image": "cards/Wands05.jpg", "keywords": ["Çatışma", "Rakipler", "Anlaşmazlık"], "love": "Aranızda sürekli didişme ve çekişme var. Çevredeki rakipler veya arkadaş baskısı işleri karıştırıyor.", "truth": "Numaranı silmedi ama çevresindeki insanların lafıyla kafası karışmış durumda.", "advice": "Gereksiz münakaşalardan uzak dur, enerjini boşa tüketme."},
    {"id": "w06", "name_tr": "Değnek Altılısı", "name_en": "Six of Wands", "image": "cards/Wands06.jpg", "keywords": ["Zafer", "Haklı Çıkma", "Gurur"], "love": "Haklılığın kanıtlanıyor! O sana boyun eğerek ve değerini anlayarak gelecek, zafer senin.", "truth": "Numaran duruyor ve sana karşı duyduğu saygı katlanarak arttı.", "advice": "Başarını gururlanmadan zarafetle kutla."},
    {"id": "w07", "name_tr": "Değnek Yedilisi", "name_en": "Seven of Wands", "image": "cards/Wands07.jpg", "keywords": ["Sınırlarını Savunma", "Meydan Okuma", "Direniş"], "love": "Bu ilişki için dış etkenlere karşı direniyorsun. Kimsenin aranıza girmesine izin vermemelisin.", "truth": "Numaran duruyor, sana ulaşmak için kendi engelleriyle mücadele ediyor.", "advice": "Mevzini koru, inandığın sevginin arkasında dik dur."},
    {"id": "w08", "name_tr": "Değnek Sekizlisi", "name_en": "Eight of Wands", "image": "cards/Wands08.jpg", "keywords": ["Işık Hızında Mesaj", "Ani Arama", "Hızlı Gelişme"], "love": "Telefonun her an çalabilir! Havada uçuşan değnekler ani bir mesajı, aramayı ve hızlı gelişmeleri müjdeliyor.", "truth": "Kesinlikle silmedi, eli telefonda ve çok hızlı bir bildirim alacaksın.", "advice": "Hazırlıklı ol, olaylar tahmin ettiğinden çok daha hızlı gelişecek."},
    {"id": "w09", "name_tr": "Değnek Dokuzlusu", "name_en": "Nine of Wands", "image": "cards/Wands09.jpg", "keywords": ["Gardını İndirmeme", "Yaralı Savaşçı", "Güvensizlik"], "love": "Geçmişte çok yara almış, bu yüzden sana karşı gardını almış ve tedirgin bekliyor.", "truth": "Numaran duruyor ama korkusundan dolayı temkinli ve mesafeli duruyor.", "advice": "Yaralarını kaşıma, güvenini kazanacak adımlar at."},
    {"id": "w10", "name_tr": "Değnek Onlusu", "name_en": "Ten of Wands", "image": "cards/Wands10.jpg", "keywords": ["Ağır Yük Taşıma", "Tükenmişlik", "Sorumluluk"], "love": "İlişkinin tüm yükünü sen sırtlamışsın ve artık taşımakta zorlanıyorsun. Biraz yükü bırakma vakti.", "truth": "Numaran duruyor ama hayatındaki diğer sorumluluklar onu boğmuş durumda.", "advice": "Sana ait olmayan yükleri yere bırak, kendini tüketme."},
    {"id": "w11", "name_tr": "Değnek Prensi", "name_en": "Page of Wands", "image": "cards/Wands11.jpg", "keywords": ["Hevesli Mesaj", "Merak", "Flört"], "love": "İçinde kıpır kıpır bir merak var. Bir bahane bulup sana yazacak hevesli bir adım kapıda.", "truth": "Numaran duruyor ve sana yazmak için can atıyor.", "advice": "Hevesini kırma, flörtöz enerjisine karşılık ver."},
    {"id": "w12", "name_tr": "Değnek Şövalyesi", "name_en": "Knight of Wands", "image": "cards/Wands12.jpg", "keywords": ["Ateşli Geliş", "Sabırsız Aşık", "Maceracı"], "love": "Dolu dizgin sana doğru koşan ateşli bir aşık! Çok sabırsız ve aniden kapına gelebilir.", "truth": "Numaranı silmedi, aklı fikri seninle buluşmakta.", "advice": "Hızına kapıl ama kalıcılığını sorgulamayı da unutma."},
    {"id": "w13", "name_tr": "Değnek Kraliçesi", "name_en": "Queen of Wands", "image": "cards/Wands13.jpg", "keywords": ["Çekici Kadın", "Özgüven", "Büyüleyici Cazibe"], "love": "Sen ortamın en çekici, en parlayan kadınısın. Onun aklını başından alıyorsun.", "truth": "Numaran duruyor, sana karşı yoğun bir arzu ve hayranlık besliyor.", "advice": "Işığını saklama, özgüvenin senin en büyük silahın."},
    {"id": "w14", "name_tr": "Değnek Kralı", "name_en": "King of Wands", "image": "cards/Wands14.jpg", "keywords": ["Baskın Karakter", "Tutkulu Lider", "Girişimci"], "love": "Ne istediğini çok iyi bilen, tutkulu ve lider ruhlu bir erkek senin için harekete geçecek.", "truth": "Numaranı silmedi, kendi şartlarıyla sana gelmeye hazırlanıyor.", "advice": "Onunla güç yarışına girme, vizyonuna saygı duy."}
]

# TILSIM SERİSİ (PENTACLES - 14 KART)
PENTACLES = [
    {"id": "p01", "name_tr": "Tılsım Ası", "name_en": "Ace of Pentacles", "image": "cards/Pents01.jpg", "keywords": ["Somut Fırsat", "Maddi Şans", "Sağlam Temel"], "love": "Aşkta elle tutulur, somut ve sağlam bir başlangıç. Boş laflar bitti, gerçek adımlar geliyor.", "truth": "Numaran kayıtlı ve seninle sağlam bir temel kurmak istiyor.", "advice": "Önüne uzatılan bu somut fırsatı değerlendir."},
    {"id": "p02", "name_tr": "Tılsım İkilisi", "name_en": "Two of Pentacles", "image": "cards/Pents02.jpg", "keywords": ["Denge Kurma", "İki Durumu İdare Etme", "Bocalama"], "love": "Hayatındaki iş, para veya iki kişi arasında denge kurmaya çalışıyor; kafası biraz meşgul.", "truth": "Numaran duruyor ama şu an hayatının diğer kaoslarıyla boğuşuyor.", "advice": "Dengeyi kaybetme, önceliklerini net belirle."},
    {"id": "p03", "name_tr": "Tılsım Üçlüsü", "name_en": "Three of Pentacles", "image": "cards/Pents03.jpg", "keywords": ["Emek Verme", "İş Birliği", "Ustalık"], "love": "İlişki için karşılıklı emek verilmesi gereken bir süreç. Konuşarak ortak bir paydada buluşabilirsiniz.", "truth": "Numaran kayıtlı, aradaki sorunları çözmek için çaba göstermeye hazır.", "advice": "Birlikte inşa edin, emek olmadan aşk büyümez."},
    {"id": "p04", "name_tr": "Tılsım Dörtlüsü", "name_en": "Four of Pentacles", "image": "cards/Pents04.jpg", "keywords": ["İnatla Tutma", "Kaybetme Korkusu", "Cimrilik"], "love": "Seni kimseyle paylaşmak istemiyor ama adım atmaya da korkuyor. İçten içe sana kilitlenmiş.", "truth": "Numaranı asla silmez! Seni kaybetme korkusu çok yüksek ama inat yapıyor.", "advice": "Sıkı sıkıya tutunmayı bırak, biraz rahat olursan akış düzelecek."},
    {"id": "p05", "name_tr": "Tılsım Beşlisi", "name_en": "Five of Pentacles", "image": "cards/Pents05.jpg", "keywords": ["Yoksunluk", "Dışarıda Kalma", "Maddi/Manevi Soğukluk"], "love": "Kendini terkedilmiş ve sevgisiz hissediyor. Gururundan dolayı soğukta kalmayı göze almış.", "truth": "Numaranı silmiş gibi görünse de içinde büyük bir mahrumiyet ve yalnızlık çekiyor.", "advice": "Kafanı kaldır, sığınabileceğin sıcak bir kapı her zaman var."},
    {"id": "p06", "name_tr": "Tılsım Altılısı", "name_en": "Six of Pentacles", "image": "cards/Pents06.jpg", "keywords": ["Alma-Verme Dengesi", "Cömertlik", "Hak Ediş"], "love": "Sen hep verdin ama karşılığını alamadın. Şimdi o sana borcunu ödemek ve sevgisini sunmak zorunda.", "truth": "Numaran duruyor, sana karşı bir borçluluk ve mahcubiyet hissediyor.", "advice": "Karşılıksız fedakarlık yapma, ne kadar alıyorsan o kadar ver."},
    {"id": "p07", "name_tr": "Tılsım Yedilisi", "name_en": "Seven of Pentacles", "image": "cards/Pents07.jpg", "keywords": ["Hasat Bekleyişi", "Sabır Sınavı", "Emek"], "love": "Ektiğin tohumların yeşermesini bekliyorsun. Sabrının sonu selamet olacak, acele etme.", "truth": "Numaran kayıtlı, durumun olgunlaşmasını bekliyor.", "advice": "Ağacı sarsma, meyve olgunlaşınca kendiliğinden kucağına düşecek."},
    {"id": "p08", "name_tr": "Tılsım Sekizlisi", "name_en": "Eight of Pentacles", "image": "cards/Pents08.jpg", "keywords": ["Özenle Çalışma", "Kariyer Odaklılık", "Kendini Geliştirme"], "love": "Şu an kafasını tamamen işine, parasına ve geleceğine takmış durumda. Seni ihmal etmesi sevgisizlikten değil.", "truth": "Numaran duruyor, maddi durumunu düzeltip karşına daha güçlü çıkmak istiyor.", "advice": "Sen de kendi işine ve yeteneklerine odaklan, başarından etkilenecek."},
    {"id": "p09", "name_tr": "Tılsım Dokuzlusu", "name_en": "Nine of Pentacles", "image": "cards/Pents09.jpg", "keywords": ["Bağımsız Kadın", "Lüks ve Konfor", "Kendi Kendine Yetme"], "love": "Sen kimseye muhtaç olmayan, kendi parasını kazanan ve asil duruşuyla büyüleyen bir kadınsın. O sana layık olmaya çalışıyor.", "truth": "Numaranı silmedi, senin bu güçlü bağımsız duruşun onu hem büyülüyor hem ürkütüyor.", "advice": "Kendi konfor alanını ve asaletini koru, taviz verme."},
    {"id": "p10", "name_tr": "Tılsım Onlusu", "name_en": "Ten of Pentacles", "image": "cards/Pents10.jpg", "keywords": ["Kalıcı Zenginlik", "Aile Mirası", "Büyük Güvence"], "love": "Nesiller boyu sürecek kalıcı bir bağ, evlilik ve aile huzuru. Maddi ve manevi tam bir doyum.", "truth": "Numaran duruyor, seninle ciddi ve uzun vadeli bir gelecek düşünüyor.", "advice": "Sağlam kökler sal, geleceğin güvence altında."},
    {"id": "p11", "name_tr": "Tılsım Prensi", "name_en": "Page of Pentacles", "image": "cards/Pents11.jpg", "keywords": ["Küçük Somut Adım", "Öğrenme", "Fırsat"], "love": "Sana küçük ama çok sağlam bir adımla gelecek. Bir hediye, bir kahve daveti veya somut bir teklif var.", "truth": "Numaran duruyor, sana karşı ciddi ve gerçekçi adımlar atacak.", "advice": "Küçük başlangıçları küçümseme, büyük çınarlar küçük tohumlardan büyür."},
    {"id": "p12", "name_tr": "Tılsım Şövalyesi", "name_en": "Knight of Pentacles", "image": "cards/Pents12.jpg", "keywords": ["Yavaş Ama Emin", "Sadakat", "Güvenilirlik"], "love": "Çok yavaş hareket ediyor ama adımı kalıcı ve sarsılmaz. Bir kez gelirse bir daha asla gitmez.", "truth": "Numaranı asla silmez, son derece sadık ve güvenilir bir bağ var.", "advice": "Sabret, yavaş giden atın yolu menzile varır."},
    {"id": "p13", "name_tr": "Tılsım Kraliçesi", "name_en": "Queen of Pentacles", "image": "cards/Pents13.jpg", "keywords": ["Anaç Kadın", "Bolluk", "Huzur Veren Yuva"], "love": "Sen hem evine hem kalbine bereket getiren kadınsın. Onun sığınabileceği en güvenli limansın.", "truth": "Numaranı silmedi, senin huzuruna ve varlığına derin bir saygısı var.", "advice": "Doğallığını ve cömertliğini koru, bereket seninle."},
    {"id": "p14", "name_tr": "Tılsım Kralı", "name_en": "King of Pentacles", "image": "cards/Pents14.jpg", "keywords": ["Maddi Güç", "Sağlam Karakter", "Zenginlik"], "love": "Maddi olarak güçlü, sözünün eri ve arkanda dağ gibi duracak sağlam bir eril enerji.", "truth": "Numaran duruyor, sana maddi ve manevi olarak sahip çıkma arzusunda.", "advice": "Güvenilir adımlarla ilerle, sağlam temeller kazandırır."}
]

ALL_CARDS = MAJOR_ARCANA + CUPS + SWORDS + WANDS + PENTACLES

class TarotDeck:
    @staticmethod
    def draw(count: int = 1, allow_reversed: bool = False) -> List[Dict]:
        selected = random.sample(ALL_CARDS, count)
        result = []
        for card in selected:
            is_reversed = allow_reversed and (random.random() < 0.15)
            c = card.copy()
            c["is_reversed"] = is_reversed
            c["orientation"] = "Ters" if is_reversed else "Düz"
            result.append(c)
        return result
