# ==============================================================================
# ALMİNA TAROT - ASTROLOJİ VE NUMEROLOJİ ANALİZ MOTORU
# Canlı chatteki burç ve doğum tarihlerini ayrıştırır, sembolleri ve yorumları üretir.
# ==============================================================================

import re
from typing import Dict, Optional, Tuple

ZODIAC_INFO = {
    "koç": {
        "name": "Koç", "symbol": "♈", "element": "Ateş", "quality": "Öncü",
        "nature": "dürtüsel cesareti ve sabırsız tutkusu",
        "keywords": ["koc", "koç", "koçum", "kocum", "koçla", "kocla", "koçuz", "kocuz"]
    },
    "boğa": {
        "name": "Boğa", "symbol": "♉", "element": "Toprak", "quality": "Sabit",
        "nature": "güven, sadakat ve sağlamlık arayışı",
        "keywords": ["boga", "boğa", "boğayım", "bogayim", "boğayla", "bogayla", "boğayız", "bogayiz"]
    },
    "ikizler": {
        "name": "İkizler", "symbol": "♊", "element": "Hava", "quality": "Değişken",
        "nature": "hareketli zihni ve meraklı kalbi",
        "keywords": ["ikizler", "ikizlerim", "ikizlerle", "ikizleriz"]
    },
    "yengeç": {
        "name": "Yengeç", "symbol": "♋", "element": "Su", "quality": "Öncü",
        "nature": "hassas kalbi, korumacı sevgisi ve geçmişe bağlılığı",
        "keywords": ["yengec", "yengeç", "yengecim", "yengecle", "yengeçle", "yengeciz", "yengeçiz"]
    },
    "aslan": {
        "name": "Aslan", "symbol": "♌", "element": "Ateş", "quality": "Sabit",
        "nature": "gururu, asil duruşu ve ilgi görme arzusu",
        "keywords": ["aslan", "aslanım", "aslanla", "aslanız", "aslaniz"]
    },
    "başak": {
        "name": "Başak", "symbol": "♍", "element": "Toprak", "quality": "Değişken",
        "nature": "her detayı tartan analitik zihni ve titizliği",
        "keywords": ["basak", "başak", "başağım", "basagim", "başakla", "basakla", "başağız", "basagiz", "başaklar"]
    },
    "terazi": {
        "name": "Terazi", "symbol": "♎", "element": "Hava", "quality": "Öncü",
        "nature": "kararsızlığı, denge arayışı ve zarafeti",
        "keywords": ["terazi", "teraziyim", "teraziyle", "teraziyiz"]
    },
    "akrep": {
        "name": "Akrep", "symbol": "♏", "element": "Su", "quality": "Sabit",
        "nature": "derin tutkuları, sarsılmaz sezgisi ve gizemli bağı",
        "keywords": ["akrep", "akrebim", "akreple", "akrebiz", "akrepler"]
    },
    "yay": {
        "name": "Yay", "symbol": "♐", "element": "Ateş", "quality": "Değişken",
        "nature": "özgür ruhu, dobra tavırları ve sınır tanımazlığı",
        "keywords": ["yay", "yayım", "yayla", "yayız", "yayiz"]
    },
    "oğlak": {
        "name": "Oğlak", "symbol": "♑", "element": "Toprak", "quality": "Öncü",
        "nature": "mesafeli kabuğu, sorumluluk bilinci ve ciddiyeti",
        "keywords": ["oglak", "oğlak", "oğlağım", "oglagim", "oğlakla", "oglakla", "oğlağız", "oglagiz"]
    },
    "kova": {
        "name": "Kova", "symbol": "♒", "element": "Hava", "quality": "Sabit",
        "nature": "kural tanımaz özgürlüğü ve zihinsel inatlaşması",
        "keywords": ["kova", "kovayım", "kovayla", "kovayız", "kovayiz", "kovalar"]
    },
    "balık": {
        "name": "Balık", "symbol": "♓", "element": "Su", "quality": "Değişken",
        "nature": "sonsuz fedakarlığı, yüksek hissiyatı ve rüyaları",
        "keywords": ["balik", "balık", "balığım", "baligim", "balıkla", "balikla", "balığız", "baligiz", "balıklar"]
    }
}

NUMEROLOGY_CYCLES = {
    1: "yeni bir kader döngüsünün başladığını, kendi ayakları üzerinde durup bağımsızlaşma vaktini",
    2: "kalp dengesini, ruhsal eşleşmeyi ve karşılıklı sabrın sınandığı kadersel bir kavşağı",
    3: "bastırılan hislerin kelimelere dökülüşünü, iletişim kıvılcımını ve kendini ifade vaktini",
    4: "sağlam temeller atmayı, kalıcı adımları ve kararlılıkla beklenen sonucu alma sürecini",
    5: "büyük kadersel virajı, beklenmeyen ani değişimleri ve sınırları aşma evresini",
    6: "kalıcı sevgiyi, sadakati ve bağlardaki pürüzlerin arınarak dinginliğe kavuşmasını",
    7: "içsel uyanışı, maskelerin düşüşünü ve ardında yatan hakikatin idrakini",
    8: "ilahi adaleti, karmik hak edişi ve ektiğini biçme zamanını",
    9: "eski bir sancılı dönemin nihai kapanışını ve yeni bir temiz sayfanın açılışını",
    11: "yüksek psişik sezgiyi, telepatik bağı ve iki ruh arasındaki görünmez çekimi",
    22: "büyük kadersel birleşmeyi ve hayat değiştiren mukadderat ortaklığını"
}

class AstrologyParser:
    @staticmethod
    def parse(text: str) -> Dict:
        if not text:
            return {
                "has_astro": False, "user_sign": None, "partner_sign": None,
                "badge_pill": None, "birth_date": None, "life_path": None, "commentary": ""
            }

        cleaned = text.lower()
        
        # 1. Doğum Tarihi Tespiti (DD.MM.YYYY veya YYYY)
        birth_date = None
        life_path = None
        date_match = re.search(r'\b(\d{1,2})[.\/-](\d{1,2})[.\/-](\d{4})\b', text)
        if date_match:
            d, m, y = date_match.groups()
            birth_date = f"{int(d):02d}.{int(m):02d}.{y}"
            digits_sum = sum(int(c) for c in f"{d}{m}{y}")
            while digits_sum > 9 and digits_sum not in [11, 22]:
                digits_sum = sum(int(c) for c in str(digits_sum))
            life_path = digits_sum
        else:
            year_match = re.search(r'\b(19\d{2}|20\d{2})\b', text)
            if year_match and any(w in cleaned for w in ["doğum", "doğumluyum", "luyum", "liyim"]):
                birth_date = year_match.group(1)

        # 2. Burç Tespiti
        tokens = re.findall(r'\b[a-zçğıöşü]+\b', cleaned)
        detected_signs = []
        for token in tokens:
            for sign_key, info in ZODIAC_INFO.items():
                if token in info["keywords"]:
                    if sign_key not in [s[0] for s in detected_signs]:
                        detected_signs.append((sign_key, info))
                    break

        user_sign = None
        partner_sign = None

        if len(detected_signs) >= 2:
            user_sign = detected_signs[0][1]
            partner_sign = detected_signs[1][1]
        elif len(detected_signs) == 1:
            if any(w in cleaned for w in ["ikimiz", "ikimizde", "ikisi", "çift"]):
                user_sign = detected_signs[0][1]
                partner_sign = detected_signs[0][1]
            else:
                user_sign = detected_signs[0][1]

        # 3. Rozet Metni (Badge Pill)
        badge_parts = []
        if user_sign and partner_sign:
            if user_sign["name"] == partner_sign["name"]:
                badge_parts.append(f"{user_sign['symbol']} Çift {user_sign['name']}")
            else:
                badge_parts.append(f"{user_sign['symbol']} {user_sign['name']} · {partner_sign['symbol']} {partner_sign['name']}")
        elif user_sign:
            badge_parts.append(f"{user_sign['symbol']} {user_sign['name']} Burcu")

        if birth_date:
            badge_parts.append(f"📅 {birth_date}")

        badge_pill = " · ".join(badge_parts) if badge_parts else None

        # 4. Mistik Astroloji & Numeroloji Yorumu
        commentary = AstrologyParser._build_astro_commentary(user_sign, partner_sign, birth_date, life_path)

        return {
            "has_astro": bool(user_sign or birth_date),
            "user_sign": user_sign["name"] if user_sign else None,
            "partner_sign": partner_sign["name"] if partner_sign else None,
            "badge_pill": badge_pill,
            "birth_date": birth_date,
            "life_path": life_path,
            "commentary": commentary
        }

    @staticmethod
    def _build_astro_commentary(u_sign, p_sign, date_str, life_path) -> str:
        pieces = []

        if u_sign and p_sign:
            u_name = u_sign["name"]
            p_name = p_sign["name"]
            u_nat = u_sign["nature"]
            p_nat = p_sign["nature"]

            if u_name == p_name:
                pieces.append(f"İkinizin de {u_name} burcunda buluşması, aranızdaki aynalama etkisini çok yükseltiyor. İki tarafın da {u_nat} zaman zaman inatlaşmaya dönse de aranızdaki manyetik bağ çok kuvvetli.")
            else:
                el_u = u_sign["element"]
                el_p = p_sign["element"]
                
                if {el_u, el_p} == {"Su", "Hava"}:
                    pieces.append(f"Senin {u_name} olarak hissettiğin {u_nat} ile onun {p_name} aklındaki {p_nat} bir noktada derin bir çekim yaratıyor. Kalp ile zihnin uzlaşma arayışı masaya yansıyor.")
                elif {el_u, el_p} == {"Ateş", "Su"}:
                    pieces.append(f"Senin {u_name} tarafındaki {u_nat} ile onun {p_name} enerjisi su ve ateşin karşılaşması gibi; yoğun bir tutku barındırıyor ancak ani fevriliklere dikkat etmelisin.")
                elif {el_u, el_p} == {"Toprak", "Su"}:
                    pieces.append(f"{u_name} ve {p_name} uyumu toprağın suyu sarması gibi; aranızdaki bağ karşılıklı şefkat ve kalıcı güven temeli üzerine oturuyor.")
                elif {el_u, el_p} == {"Ateş", "Hava"}:
                    pieces.append(f"{u_name} ile {p_name} enerjisi havanın ateşi harlaması gibi; aranızda sönmeyen bir merak ve heyecan kıvılcımı dolaşıyor.")
                else:
                    pieces.append(f"Senin {u_name} olarak taşıdığın {u_nat} ile onun {p_name} yapısındaki {p_nat} aranızda çözülmesi gereken kadersel bir sınavı işaret ediyor.")

        elif u_sign:
            u_name = u_sign["name"]
            u_nat = u_sign["nature"]
            pieces.append(f"Bir {u_name} olarak hissettiğin o {u_nat} masadaki kartların enerjisinde hemen kendini hissettiriyor.")

        if date_str and life_path:
            cycle_desc = NUMEROLOGY_CYCLES.get(life_path, "kadersel bir tamamlanma ve muradına erme evresini")
            pieces.append(f"Verdiğin {date_str} tarihi numerolojide {life_path} hayat yolu sayısını veriyor; bu da sana {cycle_desc} fısıldıyor.")

        return " ".join(pieces)
