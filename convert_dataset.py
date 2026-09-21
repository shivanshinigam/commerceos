#!/usr/bin/env python3
import csv
import json
import os
import re

def get_emoji(product_type):
    p = str(product_type).lower()
    if 'sweatshirt' in p:
        return '🧥'
    elif 't-shirt' in p:
        return '👕'
    elif 'shirt' in p:
        return '👔'
    return '👗'

def get_base_price(product_type, brand, prod_id):
    p = str(product_type).lower()
    seed = (int(prod_id) * 37 + len(brand) * 13) % 50
    if 'sweatshirt' in p:
        price = 1499 + seed * 40
    elif 't-shirt' in p:
        price = 599 + seed * 20
    elif 'shirt' in p:
        price = 999 + seed * 30
    else:
        price = 899 + seed * 25
    return price

def convert():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, 'Dataset', 'CSV', 'Product_data.csv')
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found")
        return

    catalog = []
    apparel_items_js = []

    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pid = row.get('ProductID', '').strip()
            product = row.get('Product', '').strip()
            brand = row.get('BrandName', '').strip()
            category = row.get('Category', '').strip() # Men / Women / Kids
            color = row.get('Color', '').strip()
            style = row.get('Style', '').strip()
            size = row.get('Size', '').strip()
            desc = row.get('Product Description', '').strip()

            base_price = get_base_price(product, brand, pid)
            nova_price = base_price
            velomart_price = int(base_price * 0.95)
            urbancart_price = int(base_price * 0.98)

            pid_num = int(pid)
            rating = round(4.0 + (pid_num % 10) * 0.09, 1)
            if rating > 4.9:
                rating = 4.9
            reviews = 50 + (pid_num * 17) % 2000
            emoji = get_emoji(product)

            # Standardized category slug
            if 'sweatshirt' in product.lower():
                cat_slug = 'sweatshirt'
            elif 't-shirt' in product.lower():
                cat_slug = 't_shirt'
            elif 'shirt' in product.lower():
                cat_slug = 'shirt'
            else:
                cat_slug = 'apparel'

            title = f"{brand} {color} {style} {product} ({category}'s, Size {size})"

            item = {
                "id": f"APP-{pid_num:04d}",
                "product_id": pid_num,
                "title": title,
                "brand": brand,
                "product_type": product,
                "category": cat_slug,
                "gender": category,
                "color": color,
                "style": style,
                "size": size,
                "emoji": emoji,
                "best_price": velomart_price,
                "price": {
                    "nova": nova_price,
                    "velomart": velomart_price,
                    "urbancart": urbancart_price
                },
                "rating": rating,
                "reviews": reviews,
                "inventory": {
                    "nova": (pid_num * 3 + 5) % 25 + 2,
                    "velomart": (pid_num * 5 + 7) % 20 + 1,
                    "urbancart": (pid_num * 2 + 3) % 30 + 3
                },
                "in_stock": True,
                "sizes": [size],
                "attrs": {
                    "color": color,
                    "style": style,
                    "size": size,
                    "gender": category,
                    "brand": brand
                },
                "tags": [product.lower(), brand.lower(), category.lower(), color.lower(), style.lower(), size.lower()],
                "delivery": {
                    "nova": "2 days",
                    "velomart": "3 days",
                    "urbancart": "2 days"
                },
                "search_text": f"{brand} {color} {style} {product} {category} size {size} {desc}".lower(),
                "description": desc,
                "image": f"https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png"
            }
            catalog.append(item)

            # JS item representation for build_part2.py
            js_item = {
                "id": item["id"],
                "title": item["title"],
                "brand": item["brand"],
                "category": item["category"],
                "best_price": item["best_price"],
                "rating": item["rating"],
                "emoji": item["emoji"],
                "image": item["image"],
                "search_text": item["search_text"],
                "sizes": item["sizes"],
                "in_stock": True
            }
            apparel_items_js.append(js_item)

    print(f"Converted {len(catalog)} products from Product_data.csv")

    # Save to catalog.json
    out_json = os.path.join(base_dir, 'catalog.json')
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, indent=2)
    print(f"Saved {out_json}")

    # Inject dataset JS catalog into build_part2.py
    build_part2_path = os.path.join(base_dir, 'build_part2.py')
    with open(build_part2_path, 'r', encoding='utf-8') as f:
        part2_code = f.read()

    # Convert first 150 items for super-fast inline browser loading, plus full dataset in raw catalog
    apparel_json_str = json.dumps(apparel_items_js, indent=2)

    # Insert into CURATED_CATALOG inside build_part2.py
    marker = "const CURATED_CATALOG = ["
    if marker in part2_code:
        idx = part2_code.find(marker) + len(marker)
        formatted_apparel = json.dumps(apparel_items_js[:100], indent=4)[1:-1] # first 100 inline
        new_part2_code = part2_code[:idx] + "\n  // --- DATASET FROM GenAI-Product-Recommender (Product_data.csv) ---" + formatted_apparel + ",\n" + part2_code[idx:]
        with open(build_part2_path, 'w', encoding='utf-8') as f:
            f.write(new_part2_code)
        print("Updated build_part2.py with dataset items!")

    # Update build_part3.py INTENT_PARSER & SEARCH_ENGINE
    build_part3_path = os.path.join(base_dir, 'build_part3.py')
    with open(build_part3_path, 'r', encoding='utf-8') as f:
        part3_code = f.read()

    # Add apparel categories & brands to INTENT_PARSER if not present
    if "'sweatshirt'" not in part3_code:
        part3_code = part3_code.replace(
            "'running_shoes':",
            "'sweatshirt': ['sweatshirt','sweatshirts','hoodie','pullover'],\n    't_shirt': ['t-shirt','tshirt','tee','t-shirts'],\n    'shirt': ['shirt','shirts','button shirt'],\n    'running_shoes':"
        )
        part3_code = part3_code.replace(
            "BRANDS: [",
            "BRANDS: ['lee','myntra','flying machine','wrangler','scullers','benetton','highlander','puma',"
        )
        with open(build_part3_path, 'w', encoding='utf-8') as f:
            f.write(part3_code)
        print("Updated build_part3.py with apparel keywords!")

if __name__ == '__main__':
    convert()
