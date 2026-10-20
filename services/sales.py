import os
from models.sale import Sale
from models.customer import Customer
from models.employee import Employee

class SalesService:
    def __init__(self):
        self.sales_log = []
        self.customers = {}
        self.unique_products = set()
        self.employees = {}

    def get_or_create_customer(self, name):
        
        if name in self.customers:
            return self.customers[name]

        else:
            new_customer = Customer(name)
            self.customers[name] = new_customer
            return new_customer

        
    def get_or_create_employee(self, name):
        if name in self.employees:
            return self.employees[name]
        else:
            new_employee = Employee(name)
            self.employees[name] = new_employee
            return new_employee

    def make_sale(self, inventory, product_name, quantity, customer_name, employee_name):
        if not inventory.has_sufficient_stock(product_name, quantity):
            print(f"Not enough stock for {product_name}.")
            return None

        product = inventory.get_product(product_name)
        customer = self.get_or_create_customer(customer_name)
        employee = self.get_or_create_employee(employee_name)
        sale = Sale(product, quantity, customer, employee)

        product.reduce_stock(quantity)
        customer.record_purchase(sale.total_price)
        employee.record_sale(sale.total_price)
        self.sales_log.append(sale)
        self.unique_products.add(product.name)

        return sale


    def total_revenue(self):
        total = 0
        for sale in self.sales_log:
            total += sale.total_price
        return total

    def best_seller(self):
        totals_by_product = {}
        for sale in self.sales_log:
            name = sale.product.name
            if name in totals_by_product:
                totals_by_product[name] += sale.quantity_sold
            else:
                totals_by_product[name] = sale.quantity_sold

        best_product = None
        best_qty = 0
        for name, qty in totals_by_product.items():
            if qty > best_qty:
                best_qty = qty
                best_product = name

        return best_product, best_qty  

    def top_employee(self):
        best = None
        for employee in self.employees.values():
            if best is None or employee.total_sales > best.total_sales:
                best = employee
        return best

    def print_report(self):
        print("\n========== SALES REPORT ==========")
        for sale in self.sales_log:
            print(sale)

        print(f"\nTotal Revenue: KES {self.total_revenue()}")
        print(f"Unique Products Sold: {len(self.unique_products)}")

        if self.sales_log:
            top = self.top_employee()
            print(f"Top Employee: {top}")
            product, qty = self.best_seller()
            print(f"Best-selling Product: {product} ({qty} units)")
        else:
            print("No sales yet.")

    def load_history(self, filename="sales_history.txt"):
        if not os.path.exists(filename):
            return

        file = open(filename, "r")
        for line in file:
            line = line.strip()
            if line:
                parts = line.split(",")
                if len(parts) == 5:
                    customer_name, employee_name, product_name, qty, total = parts
                    customer = self.get_or_create_customer(customer_name)
                    employee = self.get_or_create_employee(employee_name)
                    customer.record_purchase(int(total))
                    employee.record_sale(int(total))
        file.close()
        


    def save_history(self, filename="sales_history.txt"):
        file = open(filename, "a")
        for sale in self.sales_log:
            file.write(f"{sale.customer.name},{sale.employee.name},{sale.product.name},{sale.quantity_sold},{sale.total_price}\n")
        file.close()