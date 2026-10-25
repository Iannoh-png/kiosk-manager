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
        
        product = inventory.get_product(product_name)

        if product is None:
            return None, f"{product_name} not found in inventory. "

        if not product.has_sufficient_stock(quantity):
            return None, f"Not enough stock. Only {product.quantity} {product_name} left."

        
        customer = self.get_or_create_customer(customer_name)
        employee = self.get_or_create_employee(employee_name)
        sale = Sale(product, quantity, customer, employee)

        product.reduce_stock(quantity)
        customer.record_purchase(sale.total_price)
        employee.record_sale(sale.total_price)
        self.sales_log.append(sale)
        self.unique_products.add(product.name)

        return sale, None

    def get_report(self):
        best_product, best_qty = self.best_seller()
        return {
            "sales": self.sales_log,
            "total_revenue": self.total_revenue(),
            "unique_count": len(self.unique_products),
            "best_product": best_product,
            "best_qty": best_qty,
            "top_employee": self.top_employee(),
        }


    def total_revenue(self):
        total = 0
        for sale in self.sales_log:
            total += sale.total_price
        return total
    def customer_leaderboard(self):
        return sorted(self.customers.values(), key=lambda c: c.total_spent, reverse=True)

    def employee_leaderboard(self):
        return sorted(self.employees.values(), key=lambda e: e.total_sales, reverse=True)
    

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
    
    def save_sale(self, sale, filename="sales_history.txt"):
            file = open(filename, "a")
            file.write(f"{sale.customer.name},{sale.employee.name},{sale.product.name},{sale.quantity_sold},{sale.total_price}\n")
            file.close()

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

    def read_history(self, filename="sales_history.txt"):
        rows = []
        if not os.path.exists(filename):
            return rows
        file = open(filename, "r")
        for line in file:
            parts = line.strip().split(",")
            if len(parts) == 5:
                customer, employee, product, qty, total = parts
                rows.append({
                    "Customer": customer,
                    "Employee": employee,
                    "Product": product,
                    "Quantity": int(qty),
                    "Total (KES)": int(total),
                })
        file.close()
        return rows

    def get_history_report(self, filename="sales_history.txt"):
        rows = self.read_history(filename)

        total_revenue = 0
        qty_by_product = {}
        for row in rows:
            total_revenue +=  row["Total (KES)"]
            product = row["Product"]
            qty_by_product[product] = qty_by_product.get(product, 0) + row["Quantity"]

        best_product = None
        best_qty = 0
        for product, qty in qty_by_product.items():
            if qty > best_qty:
                best_qty = qty
                best_product = product

        return {
            "rows": rows,
            "total_revenue": total_revenue,
            "unique_count": len(qty_by_product),
            "best_product": best_product,
            "best_qty": best_qty,
            "qty_by_product": qty_by_product,
            "top_employee": self.top_employee(),
        }
        


    def save_history(self, filename="sales_history.txt"):
        file = open(filename, "a")
        for sale in self.sales_log:
            file.write(f"{sale.customer.name},{sale.employee.name},{sale.product.name},{sale.quantity_sold},{sale.total_price}\n")
        file.close()

    