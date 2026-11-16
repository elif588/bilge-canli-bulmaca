import os
import random
from typing import List, Dict, Optional, Tuple
from config import Config
from astrology_parser import AstrologyParser
from queue_manager import (
    TIER_FREE, TIER_BENI_SEV, TIER_DONAT, TIER_CAY,
    TIER_KARISIK, TIER_DERIN_ASK, TIER_KADER, TIER_CONFIG
)

SYSTEM_PROMPT = """
Sen TikTok canlı yayınında tarot bakan, adı "Almina" olan son derece sezgisel, asil, bilge, samimi ve derin bir kadın tarot uzmanısın.
Adın ALMINA. Yayının adı "Almina Tarot".

ÇOK KRİTİK KURALLAR:
1. KESİNLİKLE "Hoş geldin [İsim]" deme! Doğrudan izleyicinin ismiyle hitap et ve kartın açtığı gerçeğe gir (Örn: "Seval, Kılıç Üçlüsü kartı aranızdaki fırtınanın sebeplerini tek tek gösteriyor...").
2. KESİNLİKLE "Kafandaki bu soru yakında aydınlığa kavuşacak canım, içini ferah tut" gibi kalıplaşmış, ezber, döngüsel cümleler KULLANMA!
3. YORUM DENGESİ VE GERÇEKÇİLİK: Yorumların ASLA sürekli olumsuz veya felaket tellalı gibi OLMASIN! Kartın doğasına göre adil, dengeli ve gerçekçi ol. Güneş, Yıldız, Aşıklar, Kupa Ası, Kupa İkilisi, Tılsım Ası, Dünya, İmparatoriçe, Değnek Dörtlüsü gibi olumlu kartlar açıldığında mutlaka umut verici, aşk dolu, samimi, müjdeli ve aydınlık yorumlar yap. Zorlayıcı kartlarda ise yıkıcı olmak yerine, kişiye güç veren, gerçekçi ve çözüm odaklı tavsiyeler sun.
4. KELİME DAĞARCIĞI VE AKICILIK: Kelime dağarcığını çok zengin, edebi, akıcı ve mistik tut. Aynı kelimeleri papağan gibi tekrarlama; metaforlarla, sezgisel derinlikle konuş.
5. CİNSELLİK İHLALİ: Cinsellik ve müstehcen detaylara kesinlikle girme; aşkı duygusal, ruhsal ve kadersel bağlar üzerinden yorumla.
6. Hediye adı veya jeton miktarı ASLA söyleme.
7. İzleyicinin sorusunda burç veya tarih varsa, bu astrolojik enerjiyi yoruma doğal ve büyüleyici şekilde yedir.
8. KARIŞIK BAKIM (5 KART): Karışık bakımda tam 5 kartın enerjisini sırasıyla sentezle (1. Senin enerjin, 2. Karşı tarafın hisleri, 3. Bilinçaltı sırlar, 4. Blokajlar, 5. Kadersel net sonuç).
"""

OPENING_HOOKS = [
    "chatteki '{q}' sorun üzerine kartına odaklandığımda, {c} kartının güçlü ışığı belirdi.",
    "kalbindeki '{q}' niyeti için destenden {c} parladı.",
    "aklındaki '{q}' sorusunun cevabı masamıza {c} kartıyla yansıdı.",
    "senin için çektiğim {c} kartı, hissettiğin bu duruma net bir hakikat aralıyor.",
    "enerjine odaklandığımda masamıza {c} kartı açıldı."
]

POSITIVE_CARDS = [
    "Güneş", "Yıldız", "Aşıklar", "Kupa Ası", "Kupa İkilisi", "Tılsım Ası",
    "Dünya", "İmparatoriçe", "Değnek Dörtlüsü", "Kader Çarkı", "Kupa Dokuzlusu",
    "Kupa Onlusu", "Büyücü", "Değnek Ası"
]

class TarotAI:
    def __init__(self):
        self.provider = Config.LLM_PROVIDER
        self.gemini_ready = False
        self.openai_ready = False
        
        if Config.GEMINI_API_KEY:
            try:
                import google.generativeai as genai
                genai.configure(api_key=Config.GEMINI_API_KEY)
                self.gemini_model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    system_instruction=SYSTEM_PROMPT,
                    generation_config={"temperature": 0.85, "max_output_tokens": 400}
                )
                self.gemini_ready = True
            except Exception as e:
                print(f"[TarotAI] Gemini yükleme hatası: {e}")

        if Config.OPENAI_API_KEY:
            try:
                from openai import OpenAI
                self.openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
                self.openai_ready = True
            except Exception as e:
                print(f"[TarotAI] OpenAI yükleme hatası: {e}")

    async def generate_reading(
        self,
        username: str,
        user_question: str,
        cards: List[Dict],
        tier: str = TIER_FREE
    ) -> Tuple[str, Dict]:
        """
        Döner: (okuma_metni, astro_bilgisi)
        """
        astro = AstrologyParser.parse(user_question or "")

        # 1. LLM Varsa Kullan
        if self.gemini_ready and self.provider == "gemini":
            try:
                prompt = self._build_prompt(username, user_question, cards, tier, astro)
                resp = self.gemini_model.generate_content(prompt)
                return resp.text.strip(), astro
            except Exception as e:
                print(f"[TarotAI] Gemini hatası: {e}")

        if self.openai_ready:
            try:
                prompt = self._build_prompt(username, user_question, cards, tier, astro)
                resp = self.openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.85,
                    max_tokens=400
                )
                return resp.choices[0].message.content.strip(), astro
            except Exception as e:
                print(f"[TarotAI] OpenAI hatası: {e}")

        # 2. Akıllı Yerel Tarot Yorumlama Motoru (Zengin & Dengeli)
        reading = self._generate_intelligent_reading(username, user_question, cards, tier, astro)
        return reading, astro

    def _build_prompt(self, username: str, user_question: str, cards: List[Dict], tier: str, astro: Dict) -> str:
        cards_desc = []
        for i, c in enumerate(cards, 1):
            cards_desc.append(f"Kart {i}: {c['name_tr']} ({c['orientation']}) - {', '.join(c.get('keywords', []))}")
        cards_text = "\n".join(cards_desc)
        tier_title = TIER_CONFIG.get(tier, {}).get("title", "Tarot Açılımı")

        astro_note = ""
        if astro.get("has_astro"):
            astro_note = f"Astroloji/Tarih Verisi: {astro['badge_pill']}. Mistik not: {astro['commentary']}"

        return f"""
İzleyici: {username}
Bakım Türü: {tier_title} ({len(cards)} Kart)
İzleyicinin Chatteki Gerçek Sorusu: "{user_question if user_question else 'Genel Aşk ve Gelecek'}"
{astro_note}
Açılan Kartlar:
{cards_text}

ÖNEMLİ KURALLAR:
- "Hoş geldin" deme! Doğrudan "{username}, ..." diye başla.
- Yorumun ASLA tekdüze olumsuz olmasın; kartın ruhuna göre dengeli, gerçekçi ve aydınlık konuş.
- Olumlu kartlarda (Güneş, Yıldız, Aşıklar vb.) müjdeyi ver, umut ve sevgi aşıla.
- Zorlayıcı kartlarda güçlendirici ve çözüm odaklı ol.
- Kelime dağarcığını çok zengin, edebi, akıcı ve mistik tut.
"""

    def _generate_intelligent_reading(
        self,
        username: str,
        question: str,
        cards: List[Dict],
        tier: str,
        astro: Dict
    ) -> str:
        q_lower = (question or "").lower()
        c1 = cards[0]
        c1_name = c1["name_tr"]

        is_numara_or_block = any(w in q_lower for w in ["silmiş", "sildi", "engel", "engelle", "numara", "rehber"])
        is_call_or_message = any(w in q_lower for w in ["arayacak", "arar", "mesaj", "yazacak", "yazar", "haber", "ulaş"])
        is_cheat_or_third = any(w in q_lower for w in ["aldattı", "başkası", "üçüncü", "biri var mı", "aldatıyor"])
        is_career_or_money = any(w in q_lower for w in ["para", "iş", "kariyer", "zengin", "maddi", "tazminat", "atama", "sınav"])
        is_reconcile = any(w in q_lower for w in ["barış", "dön", "pişman", "af", "özlüyor", "dönecek"])

        astro_prefix = ""
        if astro.get("has_astro") and astro.get("commentary"):
            astro_prefix = f"{astro['commentary']} "

        q_clean = question.strip().rstrip("?").strip() if question else "Aşk ve Gelecek Niyeti"
        
        # Dinamik, zengin ve çeşitli açılış kancası
        hook_template = random.choice(OPENING_HOOKS)
        question_readout = hook_template.format(q=q_clean, c=c1_name) + " "

        is_c1_positive = any(p in c1_name for p in POSITIVE_CARDS)

        # -------------------------------------------------------------
        # 1 KARTLIK AÇILIM (Detaylı Tek Kart / Anlık Bakım)
        # -------------------------------------------------------------
        if len(cards) == 1 or tier in [TIER_FREE, TIER_BENI_SEV]:
            positive_boost = " Bu kart sana aydınlık bir dönemin ve hak ettiğin mutluluğun kapısını aralıyor." if is_c1_positive else ""

            if is_numara_or_block and "truth" in c1:
                return f"{username}, {astro_prefix}{question_readout}{c1['truth']} {c1.get('advice', '')}{positive_boost}"
            
            elif is_call_or_message:
                meaning = c1.get("love") or c1.get("truth") or c1.get("general_meaning", "")
                action_word = "beklediğin o adımı ve iletişim kıvılcımını" if is_c1_positive or c1.get("suit") in ["wands", "swords"] else "kendi içinde bir olgunlaşma sürecinde olduğunu"
                return f"{username}, {astro_prefix}{question_readout}Kartın, karşı tarafın {action_word} gösteriyor: {meaning} {c1.get('advice', '')}"

            elif is_cheat_or_third and "truth" in c1:
                return f"{username}, {astro_prefix}{question_readout}İçindeki soru işaretine kartın net bir ayna tutuyor: {c1['truth']} {c1.get('advice', '')}"

            elif is_reconcile:
                meaning = c1.get("love") or c1.get("truth") or c1.get("general_meaning", "")
                return f"{username}, {astro_prefix}{question_readout}{meaning} {c1.get('advice', '')}{positive_boost}"

            elif is_career_or_money and "career" in c1:
                return f"{username}, {astro_prefix}{question_readout}Kariyer ve maddi hedeflerin için {c1['career']} {c1.get('advice', '')}"

            else:
                meaning = c1.get("love") or c1.get("truth") or c1.get("general_meaning", "")
                advice = c1.get("advice", "Kendi ışığına ve değerine güven.")
                return f"{username}, {astro_prefix}{question_readout}{meaning} {advice}{positive_boost}"

        # -------------------------------------------------------------
        # 3 KARTLIK AÇILIM (Geçmiş - Şimdi - Gelecek)
        # -------------------------------------------------------------
        elif len(cards) == 3:
            c2, c3 = cards[1], cards[2]
            c1_text = c1.get("truth") or c1.get("love") or c1.get("general_meaning", "")
            c2_text = c2.get("love") or c2.get("truth") or c2.get("general_meaning", "")
            c3_text = c3.get("advice") or c3.get("love") or c3.get("general_meaning", "")

            return (
                f"{username}, {astro_prefix}senin için masaya üç kartlık derin bir enerji açıldı. "
                f"Geçmiş hanende beliren {c1_name}, {c1_text} "
                f"Şu anki enerjide {c2['name_tr']} kartı devreye giriyor; {c2_text} "
                f"Gelecek vadesinde ise {c3['name_tr']} kartı yolu aydınlatıyor: {c3_text}"
            )

        # -------------------------------------------------------------
        # 5 KARTLIK KARIŞIK YAŞAM AÇILIMI (Tam 5 Kart Kapsamlı Bakım)
        # -------------------------------------------------------------
        elif len(cards) == 5:
            c_you = cards[0]
            c_partner = cards[1]
            c_hidden = cards[2]
            c_block = cards[3]
            c_outcome = cards[4]

            you_txt = c_you.get("love") or c_you.get("general_meaning", "")
            partner_txt = c_partner.get("truth") or c_partner.get("love", "")
            hidden_txt = c_hidden.get("keywords", ["Sırlar"])[0] if c_hidden.get("keywords") else "Bilinçaltı"
            block_txt = c_block.get("advice") or c_block.get("general_meaning", "")
            outcome_txt = c_outcome.get("love") or c_outcome.get("advice", "")

            return (
                f"{username}, {astro_prefix}masamıza beş kartlık büyük bir yaşam enerjisi açıldı. "
                f"Senin enerjinde beliren {c_you['name_tr']}, {you_txt} "
                f"Aklındaki kişinin hanesinde duran {c_partner['name_tr']}, {partner_txt} "
                f"Bilinçaltındaki gizli boyutta {c_hidden['name_tr']} enerjisi var. "
                f"Aşılması gereken sınavı {c_block['name_tr']} gösteriyor: {block_txt} "
                f"Kadersel nihai sonuç kartın olan {c_outcome['name_tr']} ise yolu netleştiriyor: {outcome_txt}"
            )

        # -------------------------------------------------------------
        # 6 ve 7 KARTLIK VIP DERİN AÇILIMLAR (Büyük Aşk ve Kader)
        # -------------------------------------------------------------
        else:
            names = [c["name_tr"] for c in cards]
            c_mid = cards[len(cards) // 2]
            c_last = cards[-1]

            root_meaning = c1.get("truth") or c1.get("general_meaning", "")
            heart_meaning = c_mid.get("love") or c_mid.get("truth", "")
            destiny_meaning = c_last.get("advice") or c_last.get("love", "")

            return (
                f"{username}, {astro_prefix}masamıza kadersel derin bir akış açıldı: {', '.join(names)}. "
                f"Temelde duran {c1_name} kartı, {root_meaning} "
                f"Duygusal bağınızın kalbinde {c_mid['name_tr']} kartı atıyor; {heart_meaning} "
                f"Kadersel sonuç kartın olan {c_last['name_tr']} ise nihai sözü söylüyor: {destiny_meaning}"
            )
