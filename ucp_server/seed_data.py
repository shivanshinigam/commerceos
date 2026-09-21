"""
Database Seeder Script for UCP Merchant Catalog
Seeds products from catalog.json (derived from Dataset/CSV/Product_data.csv)
"""

import os
import json
from app.database import SessionLocal, engine, Base
from app.models import ProductModel

def seed_catalog():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Clear existing and seed from catalog.json
    db.query(ProductModel).delete()

    catalog_path = os.path.join(os.path.dirname(__file__), '..', 'catalog.json')
    if not os.path.exists(catalog_path):
        print(f"Catalog file {catalog_path} not found.")
        db.close()
        return

    with open(catalog_path, 'r', encoding='utf-8') as f:
        catalog_items = json.load(f)

    items_to_add = []
    for item in catalog_items:
        prod = ProductModel(
            sku=item.get('id', f"SKU-{item.get('product_id', 0)}"),
            title=item.get('title', ''),
            brand=item.get('brand', ''),
            category=item.get('category', 'apparel'),
            price=float(item.get('best_price', 999.0)),
            rating=float(item.get('rating', 4.5)),
            stock_qty=int(item.get('inventory', {}).get('nova', 10))
        )
        items_to_add.append(prod)

    db.bulk_save_objects(items_to_add)
    db.commit()
    print(f"Successfully seeded {len(items_to_add)} products from catalog.json into UCP SQLite database.")
    db.close()

if __name__ == "__main__":
    seed_catalog()
