#!/usr/bin/env python
"""
Generate comprehensive fixture with 100 products across 15 categories and 10 vendors
"""
import json
from datetime import datetime, timedelta

# Product data templates for each category
PRODUCTS_DATA = {
    1: {  # Electronics
        "category": 1,
        "vendor": 1,
        "products": [
            (
                "Smartphone X Pro",
                "Latest flagship smartphone with advanced camera",
                899.99,
                1299.99,
            ),
            (
                "Wireless Headphones",
                "Premium noise-cancelling wireless headphones",
                199.99,
                399.99,
            ),
            (
                "Smart Watch Ultra",
                "Advanced fitness tracking smartwatch",
                299.99,
                499.99,
            ),
            ("Tablet 12 inch", "Large screen tablet for entertainment", 449.99, 799.99),
            (
                "Laptop Pro 15",
                "High-performance laptop for professionals",
                1299.99,
                1999.99,
            ),
            ("USB-C Hub", "All-in-one USB connectivity hub", 49.99, 79.99),
            ("Portable Charger", "20000mAh fast charging power bank", 34.99, 59.99),
            ("Screen Protector", "Tempered glass screen protector set", 9.99, 19.99),
            ("Phone Case Premium", "Durable protective phone case", 19.99, 39.99),
            (
                "Bluetooth Speaker",
                "Waterproof portable Bluetooth speaker",
                79.99,
                149.99,
            ),
        ],
    },
    2: {  # Men's Fashion
        "category": 2,
        "vendor": 2,
        "products": [
            ("Classic T-Shirt", "Cotton blend comfortable t-shirt", 19.99, 39.99),
            ("Jeans Premium", "Premium denim jeans for men", 59.99, 99.99),
            ("Casual Shirt", "Oxford cotton casual shirt", 39.99, 79.99),
            ("Sports Hoodie", "Lightweight athletic hoodie", 49.99, 89.99),
            ("Dress Pants", "Formal wool blend dress pants", 79.99, 129.99),
            ("Leather Jacket", "Genuine leather jacket for men", 199.99, 399.99),
            ("Polo Shirt", "Classic polo shirt in various colors", 29.99, 59.99),
            ("Swim Shorts", "Quick-dry swim shorts", 24.99, 49.99),
            ("Windbreaker", "Water-resistant windbreaker jacket", 59.99, 99.99),
            ("Cargo Pants", "Multi-pocket cargo pants", 44.99, 79.99),
        ],
    },
    3: {  # Women's Fashion
        "category": 3,
        "vendor": 2,
        "products": [
            ("Summer Dress", "Light and breezy summer dress", 34.99, 69.99),
            ("Yoga Pants", "Comfortable stretchy yoga pants", 44.99, 84.99),
            ("Blouse Elegant", "Elegant silk blend blouse", 49.99, 99.99),
            ("Jean Shorts", "Trendy denim shorts", 29.99, 59.99),
            ("Cardigan Sweater", "Cozy cardigan sweater for all seasons", 39.99, 79.99),
            ("Maxi Skirt", "Long flowing maxi skirt", 39.99, 74.99),
            ("Sports Bra", "High-support sports bra", 34.99, 64.99),
            ("Leggings", "Premium quality leggings", 34.99, 59.99),
            ("Crop Top", "Stylish crop top for casual wear", 24.99, 49.99),
            ("Trench Coat", "Classic trench coat for women", 129.99, 249.99),
        ],
    },
    4: {  # Furniture
        "category": 4,
        "vendor": 3,
        "products": [
            ("Sofa 3-Seater", "Comfortable 3-seater sofa", 599.99, 999.99),
            ("Dining Table", "Solid wood dining table", 399.99, 699.99),
            ("Office Chair", "Ergonomic office chair", 199.99, 399.99),
            ("Bed Frame Queen", "Premium queen size bed frame", 349.99, 699.99),
            ("Bookshelf", "Wall-mounted wooden bookshelf", 149.99, 299.99),
            ("Coffee Table", "Modern minimalist coffee table", 99.99, 199.99),
            ("Bar Stool", "Adjustable height bar stools set", 129.99, 249.99),
            ("Nightstand", "Wooden nightstand with drawer", 89.99, 179.99),
            ("Desk Workspace", "Large wooden work desk", 249.99, 449.99),
            ("Sectional Couch", "L-shaped sectional couch", 799.99, 1299.99),
        ],
    },
    5: {  # Home Decor
        "category": 5,
        "vendor": 3,
        "products": [
            ("Wall Clock", "Modern wall clock with LED", 29.99, 59.99),
            ("Picture Frames", "Set of 5 wooden picture frames", 34.99, 69.99),
            ("Throw Pillow", "Decorative throw pillow set", 24.99, 49.99),
            ("Area Rug", "Large area rug for living room", 149.99, 299.99),
            ("Wall Mirror", "Large decorative wall mirror", 79.99, 159.99),
            ("Curtains", "Blackout curtains for bedroom", 59.99, 119.99),
            (
                "Table Lamp",
                "Modern table lamp with adjustable brightness",
                39.99,
                79.99,
            ),
            ("Vase Set", "Decorative ceramic vase set", 34.99, 69.99),
            ("Wall Art", "Canvas wall art set of 3", 49.99, 99.99),
            ("Candles", "Scented candles gift set", 24.99, 49.99),
        ],
    },
    6: {  # Fruits & Vegetables
        "category": 6,
        "vendor": 4,
        "products": [
            ("Fresh Apples", "Crisp and juicy red apples", 4.99, 8.99),
            ("Bananas Bunch", "Golden ripe bananas", 2.99, 5.99),
            ("Carrots Bundle", "Sweet orange carrots", 3.99, 7.99),
            ("Tomatoes Fresh", "Ripe red tomatoes", 4.99, 9.99),
            ("Broccoli", "Fresh green broccoli crowns", 3.99, 7.99),
            ("Lettuce", "Crisp head lettuce", 2.99, 5.99),
            ("Strawberries", "Fresh red strawberries", 5.99, 11.99),
            ("Onions Bag", "Yellow onions bulk bag", 3.99, 7.99),
            ("Bell Peppers", "Assorted color bell peppers", 4.99, 9.99),
            ("Potatoes Sack", "Large russet potatoes", 4.99, 8.99),
        ],
    },
    7: {  # Organic Foods
        "category": 7,
        "vendor": 4,
        "products": [
            ("Organic Rice", "100% organic brown rice", 12.99, 19.99),
            ("Organic Honey", "Pure raw organic honey", 14.99, 24.99),
            ("Organic Almonds", "Raw organic almond nuts", 16.99, 29.99),
            ("Organic Tea", "Premium organic green tea", 9.99, 19.99),
            ("Organic Milk", "Fresh organic milk carton", 5.99, 9.99),
            ("Organic Yogurt", "Plain organic yogurt", 4.99, 8.99),
            ("Organic Olive Oil", "Extra virgin organic olive oil", 19.99, 39.99),
            ("Organic Coffee", "Premium organic coffee beans", 14.99, 24.99),
            ("Organic Cheese", "Artisan organic cheese block", 11.99, 21.99),
            ("Organic Eggs", "Free-range organic eggs dozen", 6.99, 12.99),
        ],
    },
    8: {  # Beauty & Makeup
        "category": 8,
        "vendor": 5,
        "products": [
            ("Lipstick Set", "Matte lipstick collection 12 colors", 24.99, 49.99),
            ("Foundation Cream", "Full coverage liquid foundation", 19.99, 39.99),
            ("Eye Shadow Palette", "32 color eye shadow palette", 16.99, 34.99),
            ("Mascara Volumizing", "Waterproof volumizing mascara", 14.99, 29.99),
            ("Eyeliner Pen", "Precision eyeliner pen set", 9.99, 19.99),
            ("Blush Powder", "Rosy cheek blush powder", 11.99, 23.99),
            ("Highlighter", "Glow highlighter stick", 12.99, 24.99),
            ("Concealer", "Full coverage liquid concealer", 13.99, 27.99),
            ("Makeup Brush Set", "Professional makeup brush set 20pc", 16.99, 34.99),
            ("Makeup Primer", "Pore-minimizing makeup primer", 15.99, 31.99),
        ],
    },
    9: {  # Skincare
        "category": 9,
        "vendor": 5,
        "products": [
            ("Face Cleanser", "Gentle facial cleanser gel", 12.99, 24.99),
            ("Moisturizer Cream", "Hydrating facial moisturizer", 16.99, 34.99),
            ("Serum Essence", "Vitamin C brightening serum", 18.99, 37.99),
            ("Night Cream", "Rich night repair cream", 19.99, 39.99),
            ("Face Mask Sheet", "Korean sheet face mask pack", 9.99, 19.99),
            ("Sunscreen SPF50", "UV protection sunscreen", 14.99, 29.99),
            ("Toner Lotion", "Balancing facial toner", 11.99, 23.99),
            ("Eye Cream", "Anti-aging eye cream", 17.99, 35.99),
            ("Exfoliating Scrub", "Gentle exfoliating face scrub", 12.99, 25.99),
            ("Lip Balm", "Nourishing lip balm stick", 5.99, 11.99),
        ],
    },
    10: {  # Sports & Fitness
        "category": 10,
        "vendor": 6,
        "products": [
            ("Running Shoes", "Professional running shoes", 89.99, 149.99),
            ("Yoga Mat", "Non-slip yoga mat with carrying strap", 24.99, 49.99),
            ("Dumbbells Set", "Adjustable dumbbell set", 149.99, 299.99),
            ("Resistance Bands", "Elastic resistance band set", 16.99, 34.99),
            ("Fitness Tracker", "Advanced fitness tracking bracelet", 79.99, 159.99),
            ("Sports Bottle", "Insulated water bottle 1 liter", 24.99, 49.99),
            ("Gym Bag", "Large capacity sports gym bag", 39.99, 79.99),
            ("Weight Scale", "Digital body weight scale", 34.99, 69.99),
            ("Jump Rope", "Speed jump rope for training", 14.99, 29.99),
            ("Exercise Ball", "Stability exercise ball 65cm", 19.99, 39.99),
        ],
    },
    11: {  # Books & Media
        "category": 11,
        "vendor": 7,
        "products": [
            (
                "Python Programming",
                "Learn Python programming complete guide",
                34.99,
                59.99,
            ),
            ("Fiction Novel", "Best-selling fiction novel", 14.99, 24.99),
            ("Self-Help Book", "Personal development guide book", 16.99, 29.99),
            ("Cooking Guide", "Professional cooking techniques book", 24.99, 44.99),
            ("Business Strategy", "Business management strategy book", 19.99, 39.99),
            ("Art History", "Comprehensive art history book", 29.99, 54.99),
            ("Science Magazine", "Monthly science magazine subscription", 7.99, 14.99),
            ("Comics Series", "Popular comics graphic novel set", 14.99, 29.99),
            ("Children's Book", "Illustrated children's story book", 9.99, 19.99),
            ("Poetry Collection", "Modern poetry collection anthology", 12.99, 24.99),
        ],
    },
    12: {  # Jewelry
        "category": 12,
        "vendor": 8,
        "products": [
            ("Gold Necklace", "18K gold plated necklace", 79.99, 159.99),
            ("Diamond Ring", "Cubic zirconia diamond ring", 99.99, 199.99),
            ("Silver Bracelet", "Sterling silver bracelet", 59.99, 119.99),
            ("Earrings Studs", "Pearl stud earrings set", 39.99, 79.99),
            ("Watch Elegant", "Stainless steel elegant watch", 129.99, 249.99),
            ("Anklet", "Fashion gold-tone ankle bracelet", 24.99, 49.99),
            ("Pendant", "Gemstone pendant necklace", 49.99, 99.99),
            ("Brooch", "Vintage-style brooch pin", 29.99, 59.99),
            ("Locket", "Heart-shaped locket necklace", 34.99, 69.99),
            ("Choker Necklace", "Trendy choker necklace", 19.99, 39.99),
        ],
    },
    13: {  # Auto Parts
        "category": 13,
        "vendor": 9,
        "products": [
            ("Car Air Filter", "Universal car air filter replacement", 14.99, 29.99),
            ("Oil Filter", "Premium car oil filter", 12.99, 24.99),
            ("Brake Pads", "High-quality brake pad set", 44.99, 89.99),
            ("Car Wax", "Professional car wax polish", 19.99, 39.99),
            (
                "Windshield Wipers",
                "Universal windshield wiper blades pair",
                24.99,
                49.99,
            ),
            ("Car Mats", "All-weather car floor mats set", 34.99, 69.99),
            ("Battery", "12V car battery", 99.99, 199.99),
            ("Spark Plugs", "Spark plug set 8 pieces", 29.99, 59.99),
            ("Car Light Bulbs", "LED car light bulb kit", 19.99, 39.99),
            ("Tire Gauge", "Digital tire pressure gauge", 14.99, 29.99),
        ],
    },
    14: {  # Toys & Games
        "category": 14,
        "vendor": 10,
        "products": [
            ("Building Blocks", "1000 piece building block set", 34.99, 69.99),
            ("Board Game", "Family board game set", 24.99, 49.99),
            ("Action Figure", "Collectible action figure", 14.99, 29.99),
            ("Puzzle 1000", "1000 piece jigsaw puzzle", 12.99, 24.99),
            ("Remote Car", "Remote control racing car", 29.99, 59.99),
            ("Drone Toy", "Mini drone with camera", 79.99, 159.99),
            ("LEGO Set", "LEGO building set 500 pieces", 44.99, 89.99),
            ("Card Game", "Trading card game starter set", 19.99, 39.99),
            ("Doll House", "Miniature dollhouse set", 39.99, 79.99),
            ("Toy Robot", "Interactive toy robot", 49.99, 99.99),
        ],
    },
    15: {  # Pet Supplies
        "category": 15,
        "vendor": 1,
        "products": [
            ("Dog Food", "Premium dog food 20kg bag", 34.99, 69.99),
            ("Cat Litter", "Clumping cat litter 10kg", 14.99, 29.99),
            ("Pet Toy Ball", "Interactive pet toy ball set", 12.99, 24.99),
            ("Dog Leash", "Retractable dog leash 5m", 16.99, 34.99),
            ("Pet Bed", "Comfortable pet bed cushion", 44.99, 89.99),
            ("Cat Scratching Post", "Tall cat scratching post tower", 39.99, 79.99),
            ("Pet Collar", "Adjustable pet collar set", 11.99, 23.99),
            ("Food Bowl", "Stainless steel pet food bowl", 9.99, 19.99),
            ("Pet Shampoo", "Gentle pet shampoo bottle", 12.99, 25.99),
            ("Bird Cage", "Large bird cage with stand", 79.99, 159.99),
        ],
    },
}


def generate_fixture():
    fixture = []
    product_pk = 1

    # Add existing fixture data first (users, vendors, categories)
    with open("comprehensive_fixture.json", "r") as f:
        fixture = json.load(f)

    # Generate products
    for category_id, category_data in PRODUCTS_DATA.items():
        category = category_data["category"]
        vendor = category_data["vendor"]

        for title, description, price, old_price in category_data["products"]:
            product = {
                "model": "goods.product",
                "pk": product_pk,
                "fields": {
                    "pid": f"pid{product_pk:05d}abc",
                    "user": 1,
                    "category": category,
                    "vendor": vendor,
                    "title": title,
                    "image": "product.jpg",
                    "description": f"<p>{description}</p>",
                    "price": price,
                    "old_price": old_price,
                    "specifications": "<p>High quality product with best materials</p>",
                    "type": "Premium",
                    "stock_count": str(__import__("random").randint(5, 100)),
                    "life": "12 months",
                    "mfd": "2024-01-01T00:00:00Z",
                    "product_status": "published",
                    "status": True,
                    "in_stock": True,
                    "featured": __import__("random").choice([True, False]),
                    "digital": False,
                    "sku": f"sku{product_pk:04d}",
                    "date": (
                        datetime.now()
                        - timedelta(days=__import__("random").randint(1, 300))
                    ).isoformat()
                    + "Z",
                    "updated": None,
                },
            }
            fixture.append(product)
            product_pk += 1

    return fixture


if __name__ == "__main__":
    fixture = generate_fixture()

    with open("comprehensive_fixture.json", "w") as f:
        json.dump(fixture, f, indent=2)

    print(f"Generated fixture with {len(fixture)} items")
    print(
        f"Total products: {sum(1 for item in fixture if item['model'] == 'goods.product')}"
    )
