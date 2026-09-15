"""
Database Seeder Script for UCP Merchant Catalog
"""

from app.database import SessionLocal, engine, Base
from app.models import ProductModel

def seed_catalog():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Check if already seeded
    if db.query(ProductModel).count() > 0:
        print("Database already contains catalog items.")
        db.close()
        return

    items = [
        {"sku": "SKU-IPH15-256", "title": "Apple iPhone 15 Pro Max (256GB, Natural Titanium)", "brand": "Apple", "category": "smartphones", "price": 159900.0, "rating": 4.9, "stock_qty": 50},
        {"sku": "SKU-IPH15-128", "title": "Apple iPhone 15 (128GB, Blue)", "brand": "Apple", "category": "smartphones", "price": 79900.0, "rating": 4.8, "stock_qty": 40},
        {"sku": "SKU-IPH14-128", "title": "Apple iPhone 14 (128GB, Midnight)", "brand": "Apple", "category": "smartphones", "price": 59900.0, "rating": 4.7, "stock_qty": 35},
        {"sku": "SKU-S24U-512", "title": "Samsung Galaxy S24 Ultra (512GB, Titanium Gray)", "brand": "Samsung", "category": "smartphones", "price": 139999.0, "rating": 4.9, "stock_qty": 25},
        {"sku": "SKU-S24-256", "title": "Samsung Galaxy S24 (256GB, Onyx Black)", "brand": "Samsung", "category": "smartphones", "price": 79999.0, "rating": 4.7, "stock_qty": 30},
        {"sku": "SKU-MBA-M3", "title": "Apple MacBook Air M3 (16GB RAM, 512GB SSD, Midnight)", "brand": "Apple", "category": "laptops", "price": 134900.0, "rating": 4.9, "stock_qty": 20},
        {"sku": "SKU-MBP-M3PRO", "title": "Apple MacBook Pro 16 M3 Pro (36GB RAM, 512GB SSD)", "brand": "Apple", "category": "laptops", "price": 249900.0, "rating": 5.0, "stock_qty": 15},
        {"sku": "SKU-DELL-XPS13", "title": "Dell XPS 13 Intel Core Ultra 7 (16GB, 512GB SSD)", "brand": "Dell", "category": "laptops", "price": 149990.0, "rating": 4.6, "stock_qty": 18},
        {"sku": "SKU-SONY-XM5", "title": "Sony WH-1000XM5 Wireless ANC Headphones", "brand": "Sony", "category": "headphones", "price": 29990.0, "rating": 4.8, "stock_qty": 60},
        {"sku": "SKU-SONY-CH720N", "title": "Sony WH-CH720N Noise Cancelling Headphones", "brand": "Sony", "category": "headphones", "price": 9990.0, "rating": 4.6, "stock_qty": 80},
        {"sku": "SKU-APP-PRO2", "title": "Apple AirPods Pro (2nd Gen, USB-C)", "brand": "Apple", "category": "headphones", "price": 24900.0, "rating": 4.9, "stock_qty": 70},
        {"sku": "SKU-NIKE-PEG40", "title": "Nike Pegasus 40 Running Shoes (Size 9, Black/White)", "brand": "Nike", "category": "shoes", "price": 11895.0, "rating": 4.7, "stock_qty": 45},
        {"sku": "SKU-NIKE-REV7", "title": "Nike Revolution 7 Road Running Shoes (Size 8)", "brand": "Nike", "category": "shoes", "price": 4995.0, "rating": 4.4, "stock_qty": 50},
    ]

    for item in items:
        prod = ProductModel(**item)
        db.add(prod)

    db.commit()
    print(f"Successfully seeded {len(items)} catalog products into SQLite database.")
    db.close()

if __name__ == "__main__":
    seed_catalog()
