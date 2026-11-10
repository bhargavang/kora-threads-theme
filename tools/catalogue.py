"""
Demo catalogue for the fictional Kora Threads store.

Single source of truth for both the product illustrations
(build_images.py) and the Shopify import file (build_csv.py), so the
colours in the pictures always match the colour options in the CSV.

Prices are in INR. Nothing here is a real product.
"""

WOMEN_SIZES = ["XS", "S", "M", "L", "XL", "XXL"]
WOMEN_SIZES_SHORT = ["XS", "S", "M", "L", "XL"]
MEN_SIZES = ["S", "M", "L", "XL", "XXL"]

CARE_COTTON = "Hand wash or gentle machine wash in cold water\nWash dark colours separately for the first few washes\nDry inside out, in shade\nWarm iron on the reverse"
CARE_DELICATE = "Hand wash in cold water with a mild detergent\nDon't wring or tumble dry\nDry flat, in shade\nIron on the reverse, avoiding the embroidery"

PRODUCTS = [
    {
        "handle": "neel-block-print-kurta",
        "title": "Neel Block-Print Kurta",
        "type": "Kurta",
        "garment": "kurta",
        "tags": ["women", "kurtas", "new-arrivals", "block-print"],
        "price": 1490,
        "compare_at": 1790,
        "sizes": WOMEN_SIZES,
        "colours": [
            {"name": "Indigo", "hex": "#26385F", "motif": "#EFE6D3", "accent": "#B9502F"},
            {"name": "Madder Red", "hex": "#9C3A25", "motif": "#F1E3CC", "accent": "#2B3558"},
        ],
        "print": "booti",
        "size_chart": "women-tops",
        "fabric": "100% cotton cambric",
        "craft": "Hand block-printed in Sanganer, Rajasthan",
        "care": CARE_COTTON,
        "body": "<p>A straight, calf-length kurta covered in a small five-petal booti, stamped by hand one block at a time. It has a round neck with a short button placket, three-quarter sleeves and side slits so it moves easily.</p><p>Wear it with our handloom palazzos for work, or with jeans on the weekend.</p><ul><li>Straight fit, about 44 inches long</li><li>Side slits from the knee</li><li>Contrast print border at the hem and cuffs</li></ul>",
        "seo_description": "Calf-length cotton kurta with a hand block-printed booti motif. Straight fit, round neck, three-quarter sleeves. In indigo and madder red.",
    },
    {
        "handle": "haldi-kurta-and-pant-set",
        "title": "Haldi Kurta and Pant Set",
        "type": "Kurta set",
        "garment": "kurta_set",
        "tags": ["women", "sets", "new-arrivals"],
        "price": 2290,
        "sizes": WOMEN_SIZES_SHORT,
        "colours": [
            {"name": "Turmeric", "hex": "#D69A2D", "motif": "#FBF2DD", "accent": "#7A4B12"},
            {"name": "Sage", "hex": "#8D9C7E", "motif": "#F2F0E4", "accent": "#4A5440"},
        ],
        "print": "dabu",
        "size_chart": "women-tops",
        "fabric": "100% cotton mulmul, lined at the yoke",
        "craft": "Dabu mud-resist print from Akola, Rajasthan",
        "care": CARE_COTTON,
        "body": "<p>A two-piece set in soft mulmul: a knee-length kurta with a scattered dabu dot print and matching straight pants with an elasticated waist and drawstring.</p><p>The colour is bright without being loud. It works for a day at the office and for a family lunch after.</p><ul><li>Kurta is about 40 inches long</li><li>Pants have two side pockets</li><li>Sold as a set</li></ul>",
        "seo_description": "Two-piece cotton mulmul kurta and pant set with a hand dabu dot print. Elasticated drawstring pants with pockets. In turmeric and sage.",
    },
    {
        "handle": "kesar-tiered-maxi-dress",
        "title": "Kesar Tiered Maxi Dress",
        "type": "Dress",
        "garment": "maxi",
        "tags": ["women", "dresses", "new-arrivals"],
        "price": 2490,
        "sizes": WOMEN_SIZES_SHORT,
        "colours": [
            {"name": "Saffron", "hex": "#DD7F35", "motif": "#FBE9D2", "accent": "#8A3A16"},
            {"name": "Ivory", "hex": "#EEE5D1", "motif": "#B5552C", "accent": "#7C8B6A"},
        ],
        "print": "buta",
        "size_chart": "women-tops",
        "fabric": "100% cotton voile",
        "craft": "Hand block-printed in Bagru, Rajasthan",
        "care": CARE_COTTON,
        "body": "<p>A floor-length dress with three gathered tiers, flutter sleeves and a V neck. The small buta print is light enough for summer and the tiers keep the volume where you want it.</p><ul><li>Relaxed fit through the waist</li><li>Fully lined bodice</li><li>Side seam pockets</li></ul>",
        "seo_description": "Floor-length tiered maxi dress in cotton voile with a hand block-printed buta motif. Flutter sleeves, V neck, pockets. In saffron and ivory.",
    },
    {
        "handle": "kora-cotton-co-ord-set",
        "title": "Kora Cotton Co-ord Set",
        "type": "Co-ord set",
        "garment": "coord",
        "tags": ["women", "sets"],
        "price": 2690,
        "sizes": WOMEN_SIZES_SHORT,
        "colours": [
            {"name": "Natural", "hex": "#E2D4B9", "motif": "#B8A684", "accent": "#8C7A58"},
            {"name": "Charcoal", "hex": "#3E3C3A", "motif": "#5B5856", "accent": "#C9BFAE"},
        ],
        "print": "slub",
        "size_chart": "women-tops",
        "fabric": "100% handloom kora cotton",
        "craft": "Handwoven in Andhra Pradesh, left undyed in Natural",
        "care": CARE_COTTON,
        "body": "<p>Our namesake set: a boxy short-sleeve top and wide pants in handwoven kora cotton, the unbleached cloth the brand is named after. You can see and feel the slubs in the weave.</p><p>Wear the pieces together or split them up.</p><ul><li>Boxy, cropped top</li><li>Wide pants with elasticated back waist</li><li>Natural is undyed, so each batch varies slightly</li></ul>",
        "seo_description": "Two-piece co-ord set in handwoven, unbleached kora cotton. Boxy short-sleeve top and wide pants. In natural and charcoal.",
    },
    {
        "handle": "lucknowi-chikankari-kurti",
        "title": "Lucknowi Chikankari Kurti",
        "type": "Kurti",
        "garment": "kurti",
        "tags": ["women", "kurtas", "new-arrivals"],
        "price": 1890,
        "sizes": WOMEN_SIZES,
        "colours": [
            {"name": "White", "hex": "#F4F0E8", "motif": "#D9D1C2", "accent": "#C9BFAE"},
            {"name": "Powder Pink", "hex": "#E8C3BB", "motif": "#FAF1EC", "accent": "#C99B90"},
        ],
        "print": "chikan",
        "size_chart": "women-tops",
        "fabric": "100% cotton mulmul",
        "craft": "Hand-embroidered chikankari from Lucknow",
        "care": CARE_DELICATE,
        "body": "<p>A hip-length kurti with chikankari vines worked by hand in matching thread, so the embroidery shows up as texture rather than colour. Light enough to layer, and it goes with everything in your wardrobe.</p><ul><li>Regular fit, about 32 inches long</li><li>Embroidered yoke and sleeves</li><li>Slightly sheer: wear a camisole with White</li></ul>",
        "seo_description": "Hip-length cotton mulmul kurti with hand chikankari embroidery from Lucknow. Tone-on-tone vines. In white and powder pink.",
    },
    {
        "handle": "handloom-cotton-palazzo",
        "title": "Handloom Cotton Palazzo",
        "type": "Palazzo",
        "garment": "palazzo",
        "tags": ["women", "bottoms"],
        "price": 990,
        "sizes": WOMEN_SIZES,
        "colours": [
            {"name": "Off-white", "hex": "#EEE6D8", "motif": "#D4C8B2", "accent": "#B9502F"},
            {"name": "Black", "hex": "#22211F", "motif": "#3A3835", "accent": "#C9A24A"},
        ],
        "print": "slub",
        "size_chart": "women-bottoms",
        "fabric": "100% handloom cotton",
        "craft": "Handwoven in West Bengal",
        "care": CARE_COTTON,
        "body": "<p>Wide-leg palazzos in a soft handloom cotton, with a full elastic waist and a drawstring with tassels. They pair with every kurta in the store.</p><ul><li>Ankle length, about 39 inches</li><li>Two side pockets</li><li>Elastic waist with drawstring</li></ul>",
        "seo_description": "Wide-leg handloom cotton palazzo pants with elastic drawstring waist and pockets. In off-white and black.",
    },
    {
        "handle": "bagru-print-wrap-dress",
        "title": "Bagru Print Wrap Dress",
        "type": "Dress",
        "garment": "wrap",
        "tags": ["women", "dresses", "block-print"],
        "price": 2190,
        "compare_at": 2490,
        "sizes": WOMEN_SIZES_SHORT,
        "colours": [
            {"name": "Indigo", "hex": "#2A3B62", "motif": "#EEE3CF", "accent": "#C9A24A"},
            {"name": "Mustard", "hex": "#C8962C", "motif": "#4A2E17", "accent": "#F4E9D2"},
        ],
        "print": "floral",
        "size_chart": "women-tops",
        "fabric": "100% cotton cambric",
        "craft": "Hand block-printed in Bagru, Rajasthan",
        "care": CARE_COTTON,
        "body": "<p>A true wrap dress with a deep V, elbow sleeves and a long tie at the waist. The bold Bagru floral is printed with natural-dye blocks, so the colour softens nicely with each wash.</p><ul><li>Adjustable wrap fit</li><li>Midi length, about 46 inches</li><li>Inside tie for a secure wrap</li></ul>",
        "seo_description": "Cotton wrap dress with a hand block-printed Bagru floral. Midi length, elbow sleeves, waist tie. In indigo and mustard.",
    },
    {
        "handle": "kalamkari-cotton-dupatta",
        "title": "Kalamkari Cotton Dupatta",
        "type": "Dupatta",
        "garment": "dupatta",
        "tags": ["women", "accessories", "new-arrivals"],
        "price": 890,
        "sizes": None,
        "colours": [
            {"name": "Rust", "hex": "#A9532F", "motif": "#F2E2C6", "accent": "#26385F"},
            {"name": "Indigo", "hex": "#26385F", "motif": "#EDE1C8", "accent": "#B9502F"},
        ],
        "print": "kalamkari",
        "size_chart": "",
        "fabric": "100% cotton, 2.25 m x 1 m",
        "craft": "Kalamkari block print from Pedana, Andhra Pradesh",
        "care": CARE_COTTON,
        "body": "<p>A full-length cotton dupatta with an all-over kalamkari floral, a wide printed border at both ends and little tassels to finish. Throw it over a plain kurta and the outfit is done.</p><ul><li>2.25 metres long, 1 metre wide</li><li>Tassels at both ends</li><li>One size</li></ul>",
        "seo_description": "Full-length cotton dupatta with a kalamkari floral block print, printed border and tassels. 2.25 m. In rust and indigo.",
    },
    {
        "handle": "mulmul-band-collar-shirt",
        "title": "Mulmul Band-Collar Shirt",
        "type": "Shirt",
        "garment": "shirt_band",
        "tags": ["men", "shirts", "new-arrivals"],
        "price": 1290,
        "sizes": MEN_SIZES,
        "colours": [
            {"name": "White", "hex": "#F3EFE7", "motif": "#DDD5C6", "accent": "#C9BFAE"},
            {"name": "Sky Blue", "hex": "#A8C2D8", "motif": "#C3D5E4", "accent": "#7F9BB3"},
        ],
        "print": "slub",
        "size_chart": "men-tops",
        "fabric": "100% cotton mulmul",
        "craft": "Woven and stitched in Tiruppur, Tamil Nadu",
        "care": CARE_COTTON,
        "body": "<p>A featherlight full-sleeve shirt with a band collar and a curved hem, cut from double-washed mulmul so it's soft from the first wear. Good for hot days and long journeys.</p><ul><li>Regular fit</li><li>Wooden buttons</li><li>One chest pocket</li></ul>",
        "seo_description": "Lightweight men's cotton mulmul shirt with band collar, curved hem and wooden buttons. In white and sky blue.",
    },
    {
        "handle": "ajrakh-print-shirt",
        "title": "Ajrakh Print Shirt",
        "type": "Shirt",
        "garment": "shirt_classic",
        "tags": ["men", "shirts", "new-arrivals", "block-print"],
        "price": 1790,
        "sizes": MEN_SIZES,
        "colours": [
            {"name": "Indigo Ajrakh", "hex": "#22335A", "motif": "#B5452B", "accent": "#EFE4CE"},
            {"name": "Madder Ajrakh", "hex": "#8E3322", "motif": "#22335A", "accent": "#EFE4CE"},
        ],
        "print": "ajrakh",
        "size_chart": "men-tops",
        "fabric": "100% cotton poplin",
        "craft": "Ajrakh resist print from Ajrakhpur, Kutch",
        "care": CARE_COTTON,
        "body": "<p>A classic-collar full-sleeve shirt in ajrakh, the geometric resist print from Kutch that goes through more than a dozen rounds of printing and washing. Each shirt has small variations from the hand process.</p><ul><li>Regular fit</li><li>Classic collar, one chest pocket</li><li>Natural dyes: wash separately the first few times</li></ul>",
        "seo_description": "Men's full-sleeve cotton shirt in hand-printed ajrakh from Kutch. Classic collar, regular fit. In indigo and madder.",
    },
    {
        "handle": "khadi-short-kurta",
        "title": "Khadi Short Kurta",
        "type": "Kurta",
        "garment": "men_kurta",
        "tags": ["men", "kurtas", "new-arrivals"],
        "price": 1590,
        "sizes": MEN_SIZES,
        "colours": [
            {"name": "Ecru", "hex": "#E5DAC3", "motif": "#C9BB9F", "accent": "#8C7A58"},
            {"name": "Olive", "hex": "#6B6E45", "motif": "#80835A", "accent": "#D8CDAE"},
        ],
        "print": "slub",
        "size_chart": "men-tops",
        "fabric": "100% hand-spun khadi cotton",
        "craft": "Hand-spun and handwoven khadi from Gujarat",
        "care": CARE_COTTON,
        "body": "<p>A hip-length men's kurta in hand-spun khadi with a mandarin collar, half placket and side slits. Khadi gets softer every time it's washed.</p><ul><li>Regular fit, about 32 inches long</li><li>Coconut-shell buttons</li><li>Side pockets</li></ul>",
        "seo_description": "Men's hip-length short kurta in hand-spun khadi cotton. Mandarin collar, side slits, pockets. In ecru and olive.",
    },
    {
        "handle": "linen-cotton-nehru-jacket",
        "title": "Linen-Cotton Nehru Jacket",
        "type": "Jacket",
        "garment": "nehru",
        "tags": ["men", "jackets"],
        "price": 2490,
        "compare_at": 2990,
        "sizes": MEN_SIZES,
        "colours": [
            {"name": "Charcoal", "hex": "#3B3D40", "motif": "#4C4E52", "accent": "#C9A24A"},
            {"name": "Beige", "hex": "#D6C4A2", "motif": "#C4B08B", "accent": "#5B4A30"},
        ],
        "print": "herringbone",
        "size_chart": "men-tops",
        "fabric": "55% linen, 45% cotton herringbone, fully lined",
        "craft": "Tailored in Jaipur",
        "care": "Dry clean recommended\nOr hand wash cold and dry flat in shade\nSteam or iron on the reverse",
        "body": "<p>A sleeveless Nehru jacket in a linen-cotton herringbone, with a mandarin collar, a chest welt pocket and two hip pockets. Layer it over a kurta for a wedding or over a shirt for the office.</p><ul><li>Tailored fit, fully lined</li><li>Brass-tone buttons</li><li>Three pockets</li></ul>",
        "seo_description": "Men's sleeveless Nehru jacket in linen-cotton herringbone. Mandarin collar, fully lined, three pockets. In charcoal and beige.",
    },
]


def slug(text):
    return "".join(c if c.isalnum() else "-" for c in text.lower()).strip("-").replace("--", "-")


def image_name(product, colour):
    return f"{product['handle']}-{slug(colour['name'])}.jpg"


def detail_name(product):
    return f"{product['handle']}-detail.jpg"
