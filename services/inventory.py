import os
from models.product import Product

class Inventory:
    def __init__(self):
        self.products = {}

    def add_product(self, name, price, quantity):
        self.products[name] = Product(name, price, quantity)

    def restock_product(self, name, amount):
        if name in self.products:
            self.products[name].restock(amount)
            return True
        return False

       

    def get_product(self, name):
        return self.products.get(name)

    def has_sufficient_stock(self, name, quantity):
        product = self.get_product(name)
        if product is None:
            return False
        return product.has_sufficient_stock(quantity)

    def view_stock(self):
        print("\n========== STOCK ==========")
        print(f"{'Product': <15}{'Price':<10}{'Quantity':<10}")
        for product in self.products.values():
            print(f"{product.name:<15}{product.price:<10}{product.quantity:<10}")

    def get_all_products(self):
        return list(self.products.values())

    def search(self, term):
        term = term.strip().lower()
        if term == "":
            return[]
        results = []
        for product in self.products.values():
            if term in product.name.lower():
                results.append(product)
        return results

    def low_stock_items(self, threshold=5):
        low = []
        for product in self.products.values():
            if product.quantity <= threshold:
                low.append(product)
        return low

    def save_low_stock_alerts(self, threshold=5, filename="restock_alerts.txt"):
        low = self.low_stock_items(threshold)
        file = open(filename, "w")
        for product in low:
            file.write(f"{product.name} - only{product.quantity} left\n")
        file.close()
        return low



    


    def save_to_file(self, filename="inventory.txt"):
        file = open(filename, "w")
        for product in self.products.values():
            file.write(f"{product.name},{product.price},{product.quantity}\n")
        file.close()

    def load_from_file(self, filename="inventory.txt"):
        if not os.path.exists(filename):
            return False

        file = open(filename, "r")
        for line in file:
            line = line.strip()
            if line:
                name, price, qty = line.split(",")
                self.add_product(name, int(price), int(qty))

        file.close()
        return True
