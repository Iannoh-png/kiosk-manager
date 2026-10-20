from models.product import Product

class Sale:
    def __init__(self, product, quantity_sold, customer, employee):
        self.product = product
        self.quantity_sold = quantity_sold
        self.customer = customer
        self.employee = employee
        self.unit_price = product.price # Captures price at the time of sale
        self.total_price = self.calculate_total()
        

    def calculate_total(self):
        return self.unit_price * self.quantity_sold

    def __str__(self):
        return f"{self.customer.name} bought {self.quantity_sold} {self.product.name} - Total: KES {self.total_price} (served by {self.employee.name})"
    

