#!/usr/bin/env python3
"""Download product images from Pexels and create ProductImages entries.

Usage:
  python scripts/fetch_pexels_images.py --api-key YOUR_KEY [--limit N] [--per-product M]

The script will process up to `--limit` products (default 50) and download up to
`--per-product` images per product (default 3). Images are saved under
`MEDIA_ROOT/product-images/<product.pid>/` and a `ProductImages` instance is
created for each saved file.
"""
import os
import sys
import argparse
import json
from pathlib import Path
import requests


def setup_django():
    repo_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(repo_root))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecomprj.settings")
    import django

    django.setup()


def download_file(url, dest_path):
    resp = requests.get(url, stream=True, timeout=30)
    resp.raise_for_status()
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    with open(dest_path, "wb") as f:
        for chunk in resp.iter_content(1024 * 8):
            if chunk:
                f.write(chunk)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--api-key", required=True)
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--per-product", type=int, default=3)
    args = parser.parse_args()

    setup_django()

    from goods.models import Product, ProductImages
    from django.conf import settings

    headers = {"Authorization": args.api_key}
    session = requests.Session()
    session.headers.update(headers)

    products = Product.objects.all()[: args.limit]
    results = {}

    for product in products:
        query = product.title
        print(f"Searching Pexels for: {query}")
        try:
            r = session.get(
                "https://api.pexels.com/v1/search",
                params={"query": query, "per_page": 15, "page": 1},
                timeout=30,
            )
            r.raise_for_status()
            data = r.json()
        except Exception as e:
            print(f"Failed search for {query}: {e}")
            continue

        photos = data.get("photos", [])
        saved = []
        count = 0
        for photo in photos:
            if count >= args.per_product:
                break
            src = photo.get("src", {})
            # Prefer 'large' then 'medium' then 'original'
            url = src.get("large") or src.get("medium") or src.get("original")
            if not url:
                continue

            # Build filename and path
            ext = os.path.splitext(url.split("?")[0])[1] or ".jpg"
            filename = f"{product.pid}_{photo.get('id')}{ext}"
            rel_folder = Path("product-images") / product.pid
            media_root = Path(settings.MEDIA_ROOT)
            dest = media_root / rel_folder / filename
            try:
                download_file(url, dest)
            except Exception as e:
                print(f"Failed download {url}: {e}")
                continue

            # Create ProductImages record with relative path
            rel_path = str(rel_folder / filename).replace("\\", "/")
            pi = ProductImages(product=product)
            # set the file path to the ImageField
            pi.images.name = rel_path
            pi.save()
            # If product has default image, update main image to the first downloaded
            try:
                if not product.image or product.image.name in (None, "", "product.jpg"):
                    product.image.name = rel_path
                    product.save()
            except Exception:
                # ignore if product.image not writable for some reason
                pass
            saved.append(rel_path)
            count += 1

        results[str(product.pid)] = saved

    out = Path("product_images_fixture.json")
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2))
    print(f"Done, wrote {out} with {len(results)} products")


if __name__ == "__main__":
    main()
