import urllib.request
import json
import shutil
from pathlib import Path

# 1. Background image copy
bg_src = Path(r"C:\Users\CAN\.gemini\antigravity\brain\f1c5fec0-6289-423b-bceb-24769eb7d8fe\mystic_tarot_reader_table_1794782711560.jpg")
images_dir = Path("web_overlay/images")
images_dir.mkdir(parents=True, exist_ok=True)
if bg_src.exists():
    shutil.copy(bg_src, images_dir / "almina_bg.jpg")
    print("Almina background copied successfully!")

# 2. Download all 78 Rider-Waite 720px cards from GitHub
cards_dir = Path("web_overlay/cards")
cards_dir.mkdir(parents=True, exist_ok=True)

url = "https://api.github.com/repos/mixvlad/TarotCards/contents/tarot/rider-waite/720px"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        print(f"Downloading {len(data)} cards...")
        
        index = {}
        for item in data:
            name = item["name"]
            dl_url = item["download_url"]
            out_file = cards_dir / name
            
            if not out_file.exists():
                r = urllib.request.Request(dl_url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(r) as dl_resp, open(out_file, "wb") as f:
                    f.write(dl_resp.read())
            
            # Map clean key
            clean_key = name.lower().replace(".jpg", "").replace(".png", "")
            index[clean_key] = f"cards/{name}"
            
        with open("web_overlay/cards/index.json", "w", encoding="utf-8") as f:
            json.dump(index, f, indent=2)
        print("All cards downloaded and indexed!")
        
except Exception as e:
    print("Download cards error:", e)
