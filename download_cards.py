import urllib.request
import json
import time
from pathlib import Path

out_dir = Path("web_overlay/cards")
out_dir.mkdir(parents=True, exist_ok=True)

# Wikimedia commons query for Rider-Waite cards
url = "https://commons.wikimedia.org/w/api.php?action=query&format=json&generator=categorymembers&gcmtitle=Category:Rider-Waite_tarot_deck&gcmtype=file&gcmlimit=80&prop=imageinfo&iiprop=url"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

card_map = {}

try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        pages = data.get("query", {}).get("pages", {})
        print(f"Found {len(pages)} files on Commons.")
        
        for k, v in pages.items():
            title = v.get("title", "")
            img_info = v.get("imageinfo", [{}])[0]
            img_url = img_info.get("url")
            
            if not img_url:
                continue
                
            clean_name = title.replace("File:", "").replace(".png", "").replace(".jpg", "").strip()
            # Clean filename
            safe_filename = clean_name.replace(" ", "_") + ".png"
            file_path = out_dir / safe_filename
            
            if not file_path.exists():
                try:
                    r = urllib.request.Request(img_url, headers={"User-Agent": "Mozilla/5.0"})
                    with urllib.request.urlopen(r) as img_resp, open(file_path, "wb") as f:
                        f.write(img_resp.read())
                    print(f"Downloaded: {safe_filename}")
                except Exception as dl_err:
                    print(f"Error downloading {safe_filename}: {dl_err}")
            
            card_map[clean_name.lower()] = f"cards/{safe_filename}"

    with open("web_overlay/cards/card_index.json", "w", encoding="utf-8") as f:
        json.dump(card_map, f, ensure_ascii=False, indent=2)
    print(f"Done. Saved index of {len(card_map)} cards.")

except Exception as e:
    print("Fetch error:", e)
