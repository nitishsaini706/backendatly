import json
from models import Product  # Assuming Product is a Pydantic model

class Database:
    def __init__(self):
        self.db_file = 'products.json'
        self.load_db()

    def load_db(self):
        try:
            with open(self.db_file, 'r') as file:
                self.products = json.load(file)
        except FileNotFoundError:
            self.products = []

    def save_products(self, products):
        print("here insva")
        products_data = [product.dict() for product in products]
        with open(self.db_file, 'w') as file:
            json.dump(products_data, file, indent=4)  # Pretty print with indentation
        return len(products)

    def get_product(self, product_id):
        for product in self.products:
            if product.get('product_id') == product_id:
                return product
        return None
