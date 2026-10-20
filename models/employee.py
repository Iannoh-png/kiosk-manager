class Employee:
    def __init__(self, name):
        self.name = name
        self.total_sales = 0
        self.sales_count = 0

    def record_sale(self, amount):
        self.total_sales += amount
        self.sales_count += 1

    def __str__(self):
        return f"{self.name} - {self.sales_count} sales, KES {self.total_sales}"
    