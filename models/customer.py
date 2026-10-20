class Customer:
    def __init__(self, name):
        self.name = name
        self.total_spent = 0

    def record_purchase(self, amount):
        self.total_spent += amount

    def __str__(self):
        return f"{self.name} - Total spent: KES {self.total_spent}"
    
    

