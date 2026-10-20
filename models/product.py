class Product:
    def __init__(self, name, price, quantity):
         self.name = name
         self.price = price
         self.quantity = quantity
    def restock(self, amount):
         self.quantity += amount

    def has_sufficient_stock(self, amount):
         return self.quantity >= amount

    def reduce_stock(self, amount):
         self.quantity -= amount

    def __str__(self):
         return f"{self.name} - KES {self.price} - {self.quantity} units"

if __name__ == "__main__":
    bread = Product("Bread", 65, 20)
    print(bread)
    bread.restock(10)
    print(bread)
    print(bread.has_sufficient_stock(5))
    bread.reduce_stock(5)
    print(bread)    

    
      

   