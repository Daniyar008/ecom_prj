import os
import json
import requests
from urllib.parse import urlencode

THIS = os.path.abspath(os.path.dirname(__file__))
# try a few likely base paths to find the fixture
possible_bases = [
    os.path.join(THIS, ".."),
    os.path.join(THIS, "..", ".."),
    os.path.join(THIS, "..", "..", ".."),
]
BASE = None
for p in possible_bases:
    candidate = os.path.abspath(p)
    if os.path.exists(os.path.join(candidate, "comprehensive_fixture.json")):
        BASE = candidate
        break
if BASE is None:
    # fallback to current working directory
    BASE = os.getcwd()

FIXTURE_PATH = os.path.join(BASE, "comprehensive_fixture.json")
MEDIA_DIR = os.path.join(BASE, "media", "product_images")
OUT_FIXTURE = os.path.join(BASE, "product_images_fixture.json")

os.makedirs(MEDIA_DIR, exist_ok=True)

with open(FIXTURE_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

# collect products
products = []
for item in data:
    if item.get("model") == "goods.product":
        pk = item.get("pk")
        fields = item.get("fields", {})
        pid = fields.get("pid")
        title = fields.get("title")
        products.append({"pk": pk, "pid": pid, "title": title})

print(f"Found {len(products)} products in fixture")

session = requests.Session()
session.headers.update(
    {"User-Agent": "ecomprj-image-fetcher/1.0 (contact: admin@local)"}
)

new_entries = []
next_pk = 100000

# limit to first N products to avoid long runs; change as needed
LIMIT = 50
for idx, p in enumerate(products[:LIMIT]):
    pid = p["pid"] or f"p{p['pk']}"
    title = p["title"]
    print(f"[{idx+1}/{min(LIMIT,len(products))}] Searching images for: {title}")
    # search commons
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": title,
        "srnamespace": 6,  # file namespace
        "srlimit": 15,
    }
    try:
        r = session.get(
            "https://commons.wikimedia.org/w/api.php", params=params, timeout=30
        )
        r.raise_for_status()
        results = r.json().get("query", {}).get("search", [])
    except Exception as e:
        print(" search failed:", e)
        results = []
    count = 0
    pid_dir = os.path.join(MEDIA_DIR, pid)
    os.makedirs(pid_dir, exist_ok=True)
    for res in results:
        if count >= 3:
            break
        title_file = res.get("title")  # like 'File:Some_image.jpg'
        if not title_file or not title_file.lower().startswith("file:"):
            continue
        # get imageinfo
        params2 = {
            "action": "query",
            "format": "json",
            "prop": "imageinfo",
            "titles": title_file,
            "iiprop": "url",
        }
        try:
            r2 = session.get(
                "https://commons.wikimedia.org/w/api.php", params=params2, timeout=30
            )
            r2.raise_for_status()
            pages = r2.json().get("query", {}).get("pages", {})
        except Exception as e:
            print(" imageinfo failed:", e)
            pages = {}
        for page in pages.values():
            iinfo = page.get("imageinfo")
            if not iinfo:
                continue
            url = iinfo[0].get("url")
            if not url:
                continue
            # skip svg
            if url.lower().endswith(".svg"):
                continue
            try:
                ext = os.path.splitext(url)[1]
                fname = f"{pid}_{count+1}{ext}"
                outpath = os.path.join(pid_dir, fname)
                if os.path.exists(outpath):
                    print("exists", outpath)
                    count += 1
                    continue
                print(" downloading", url)
                dl = session.get(url, timeout=60)
                dl.raise_for_status()
                with open(outpath, "wb") as fh:
                    fh.write(dl.content)
                # make fixture entry
                new_entries.append(
                    {
                        "model": "goods.productimages",
                        "pk": next_pk,
                        "fields": {
                            "images": f"product_images/{pid}/{fname}",
                            "product": p["pk"],
                            "date": None,
                        },
                    }
                )
                next_pk += 1
                count += 1
            except Exception as e:
                print(" download failed", e)

print(f"Downloaded {len(new_entries)} images for {min(LIMIT,len(products))} products")

with open(OUT_FIXTURE, "w", encoding="utf-8") as of:
    json.dump(new_entries, of, ensure_ascii=False, indent=2)

print("Wrote fixture", OUT_FIXTURE)
print("Done")
