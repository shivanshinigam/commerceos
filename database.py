import json
import os

class Database:
    def __init__(self):
        self.catalog = []
        self.merchants = {}
        self.load_data()

    def load_data(self):
        base_dir = os.path.dirname(__file__)
        
        try:
            with open(os.path.join(base_dir, 'catalog.json'), 'r') as f:
                self.catalog = json.load(f)
        except FileNotFoundError:
            print("Warning: catalog.json not found")
            self.catalog = []
            
        try:
            with open(os.path.join(base_dir, 'merchants.json'), 'r') as f:
                self.merchants = json.load(f)
        except FileNotFoundError:
            print("Warning: merchants.json not found")
            self.merchants = {}

    def search_catalog(self, query: str = None, category: str = None, max_price: float = None) -> list:
        # Simple simulated search filter
        results = self.catalog
        
        if category:
            results = [p for p in results if p.get('category') == category]
            
        if max_price is not None:
            filtered = []
            for p in results:
                # Get the minimum price among merchants for this product
                prices = [v for k, v in p.get('price', {}).items() if v > 0]
                if prices and min(prices) <= max_price:
                    filtered.append(p)
            results = filtered
            
        return results

# Singleton instance
db = Database()
