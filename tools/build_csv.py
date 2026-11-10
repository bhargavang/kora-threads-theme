"""
Writes demo-data/products.csv, the Shopify product import for the demo store.

    python3 tools/build_csv.py

Uses the column names from Shopify's current product CSV template.
Images are fetched by Shopify at import time from this repo on GitHub,
so the repo has to be public (it is).

The four metafield columns only import if the metafield definitions
already exist in the store (Settings > Custom data > Products). The README
lists them.
"""

import csv
import random
from pathlib import Path

from catalogue import PRODUCTS, detail_name, image_name, slug

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "demo-data" / "products.csv"
IMAGE_BASE = "https://raw.githubusercontent.com/bhargavang/kora-threads-theme/main/demo-data/images/"

HEADERS = [
    "Title",
    "URL handle",
    "Description",
    "Vendor",
    "Product category",
    "Type",
    "Tags",
    "Published on online store",
    "Status",
    "SKU",
    "Option1 name",
    "Option1 value",
    "Option2 name",
    "Option2 value",
    "Price",
    "Compare-at price",
    "Charge tax",
    "Inventory tracker",
    "Inventory quantity",
    "Continue selling when out of stock",
    "Weight value (grams)",
    "Weight unit for display",
    "Requires shipping",
    "Fulfillment service",
    "Product image URL",
    "Image position",
    "Image alt text",
    "Variant image URL",
    "Gift card",
    "SEO title",
    "SEO description",
    "Fabric (product.metafields.custom.fabric)",
    "Craft (product.metafields.custom.craft)",
    "Care instructions (product.metafields.custom.care)",
    "Size chart (product.metafields.custom.size_chart)",
]

WEIGHTS = {
    "kurta": 280, "kurti": 220, "kurta_set": 520, "coord": 560, "palazzo": 300, "maxi": 450,
    "wrap": 380, "dupatta": 180, "shirt_band": 220, "shirt_classic": 260, "men_kurta": 320, "nehru": 480,
}

# A few sold-out sizes so the variant picker shows real stock states.
SOLD_OUT = {
    ("neel-block-print-kurta", "Madder Red", "XXL"),
    ("kesar-tiered-maxi-dress", "Ivory", "XS"),
    ("ajrakh-print-shirt", "Madder Ajrakh", "S"),
    ("lucknowi-chikankari-kurti", "Powder Pink", "XL"),
}


def sku(product, colour, size):
    code = "".join(w[0] for w in product["handle"].split("-"))[:4].upper()
    col = "".join(w[:3] for w in colour["name"].upper().split())[:6]
    return f"KT-{code}-{col}" + (f"-{size}" if size else "")


def build():
    rnd = random.Random(42)
    rows = []
    for p in PRODUCTS:
        images = [
            (IMAGE_BASE + image_name(p, c), f"{p['title']} in {c['name']}, flat lay illustration")
            for c in p["colours"]
        ] + [(IMAGE_BASE + detail_name(p), f"Close-up of the {p['title']} fabric")]

        variants = []
        for c in p["colours"]:
            for size in p["sizes"] or [None]:
                variants.append((c, size))

        for i, (colour, size) in enumerate(variants):
            first = i == 0
            qty = 0 if (p["handle"], colour["name"], size) in SOLD_OUT else rnd.randint(3, 18)
            row = dict.fromkeys(HEADERS, "")
            row.update({
                "URL handle": p["handle"],
                "SKU": sku(p, colour, size),
                "Option1 value": colour["name"],
                "Option2 value": size or "",
                "Price": f"{p['price']:.2f}",
                "Compare-at price": f"{p['compare_at']:.2f}" if p.get("compare_at") else "",
                "Charge tax": "true",
                "Inventory tracker": "shopify",
                "Inventory quantity": qty,
                "Continue selling when out of stock": "deny",
                "Weight value (grams)": WEIGHTS[p["garment"]],
                "Weight unit for display": "g",
                "Requires shipping": "true",
                "Fulfillment service": "manual",
                "Variant image URL": IMAGE_BASE + image_name(p, colour),
            })
            if first:
                row.update({
                    "Title": p["title"],
                    "Description": p["body"],
                    "Vendor": "Kora Threads",
                    "Type": p["type"],
                    "Tags": ", ".join(p["tags"]),
                    "Published on online store": "true",
                    "Status": "active",
                    "Option1 name": "Colour",
                    "Option2 name": "Size" if p["sizes"] else "",
                    "Gift card": "false",
                    "SEO title": f"{p['title']} | Kora Threads",
                    "SEO description": p["seo_description"],
                    "Fabric (product.metafields.custom.fabric)": p["fabric"],
                    "Craft (product.metafields.custom.craft)": p["craft"],
                    "Care instructions (product.metafields.custom.care)": p["care"],
                    "Size chart (product.metafields.custom.size_chart)": p["size_chart"],
                })
            if i < len(images):
                row["Product image URL"], row["Image alt text"] = images[i]
                row["Image position"] = i + 1
            rows.append(row)

        # Products with fewer variants than images get image-only rows.
        for j in range(len(variants), len(images)):
            row = dict.fromkeys(HEADERS, "")
            row["URL handle"] = p["handle"]
            row["Product image URL"], row["Image alt text"] = images[j]
            row["Image position"] = j + 1
            rows.append(row)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=HEADERS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows for {len(PRODUCTS)} products to {OUT}")


if __name__ == "__main__":
    build()
