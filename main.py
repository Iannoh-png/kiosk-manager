import os
from services.inventory import Inventory
from services.sales import SalesService
from utils.validation import clean_text, get_valid_number, get_menu_choice


def load_kiosk_details(filename="kiosk.txt"):
    if not os.path.exists(filename):
        return None, None

    file = open(filename, "r")
    lines = file.read().splitlines()
    file.close()

    if len (lines) >= 2:
        return lines[0], lines[1]
    return None, None

def save_kiosk_details(kiosk_name, owner_name, filename="kiosk.txt"):
    file = open(filename, "w")
    file.write(f"{kiosk_name}\n{owner_name}\n")
    file.close()

def get_kiosk_details():
    kiosk_name, owner_name = load_kiosk_details()

    if kiosk_name is None:
        kiosk_name = clean_text(input("What's your kiosk name? "))
        owner_name = clean_text(input("Owners name? "))
        save_kiosk_details(kiosk_name, owner_name)
    
    return kiosk_name, owner_name

def display_menu():
    print("""
    =====MAIN MENU =====
    1. View Stock
    2. Add/Restock Product
    3. Sell Product
    4. View Sales Report
    5. Search Products
    6. Exit
    """)

def main():
    inventory = Inventory()
    loaded = inventory.load_from_file()
    if not loaded:
        inventory.add_product("Bread", 65, 20)
        inventory.add_product("Milk", 70, 15)
        inventory.add_product("Sugar", 150, 10)

    sales = SalesService()
    sales.load_history()

    kiosk_name, owner_name = get_kiosk_details()
    print(f"Welcome to {kiosk_name}'s Kiosk Manager, run by {owner_name}")

    while True:
        display_menu()
        choice = get_menu_choice("Enter choice: ", 1, 6)

        if choice == 1:
            inventory.view_stock()
        elif choice == 2:
            name = clean_text(input("Product name? "))
            if name in inventory.products:
                amount = get_valid_number("Quantity to add ")
                inventory.restock_product(name, amount)
            else:
                price = get_valid_number("Price? ")
                qty = get_valid_number("Quantity? ")
                inventory.add_product(name, price, qty)

        elif choice == 3:
            name = clean_text(input("Which product? "))
            qty = get_valid_number("How many units? ")
            customer_name = clean_text(input("Customer name? "))
            employee_name = clean_text(input("Which employee is serving "))
            sale, error = sales.make_sale(inventory, name, qty, customer_name, employee_name)
            if error:
                print(error)
            else:print(f"Sold! {sale}")

        elif choice == 4:
            sales.print_report()

        elif choice == 5:
            term = input("Search for product: ").strip().lower()
            if term == "":
                print("Please enter a search term. ")

            else:
                found = False
                for product in inventory.products.values():
                    if term in product.name.lower():
                        print(product)
                        found = True
                if not found:
                        print("No matches found.")
        elif choice == 6:
            inventory.save_to_file()
            sales.save_history()
            low = inventory.save_low_stock_alerts()
            if low:
                print("\nLow stock - saved to restock_alarts.txt:")
                for product in low:
                    print(f" {product.name}: {product.quantity} left")
            print("Goodbye !")
            break
    

main()  
                
