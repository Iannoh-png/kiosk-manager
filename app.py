import streamlit as st
import pandas as pd
from services.inventory import Inventory
from services.sales import SalesService
from utils.validation import clean_text
from utils.kiosk_settings import load_kiosk_details, save_kiosk_details
st.set_page_config(page_title="Kiosk Manager", page_icon = "🛒", layout="wide")


def setup():
    inventory = Inventory()
    loaded = inventory.load_from_file()
    if not loaded:
        inventory.add_product("Bread", 65, 20)
        inventory.add_product("Milk", 70, 15)
        inventory.add_product("Sugar", 150, 10)

    sales = SalesService()
    sales.load_history()
    return inventory, sales

def product_rows(products, threshold =5):
    rows = []
    for product in products:
        status = "Low" if product.quantity <= threshold else "OK"
        rows.append({
            "Product": product.name,
            "Price (KES)": product.price,
            "Quantity": product.quantity,
            "Status": status
        })
    return rows

def highlight_low(row):
    if row.get("Status") == "Low":
        return ["background-color: #ffe0b2; color: #5d3a00"] * len(row)
    return [""] * len(row)


def show_table(rows):
    if not rows:
        st.info("No products to show.")
        return
    df = pd.DataFrame(rows)
    st.dataframe(df.style.apply(highlight_low, axis=1), hide_index=True)

def show_stock(inventory):
    st.header("Current Stock")

    low = inventory.low_stock_items()
    if low:
        names=[f"{p.name} ({p.quantity})" for p in low]
        st.warning("Low stock: "+",".join(names))

    show_table(product_rows(inventory.get_all_products()))

def show_restock(inventory):
    st.header("Add or Restock Product")

    with st.form("add_restock_form", clear_on_submit=True):
        name = st.text_input("Product name")
        price = st.number_input("Price in KES (only needed for a new product)", min_value=0, step=1)
        qty = st.number_input("Quantity", min_value=1, step=1)
        submitted = st.form_submit_button("Save product")

    if submitted:
        name = clean_text(name)
        if name == "":
            st.error("Please enter a product name.")
        elif name in inventory.products:
            inventory.restock_product(name, int(qty))
            inventory.save_to_file()
            st.success(f"{name} restocked. New quantity: {inventory.products[name].quantity}")
        elif price <= 0:
            st.error("A new product needs a price above 0.")
        else:
            inventory.add_product(name, int(price), int(qty))
            inventory.save_to_file()
            st.success(f"{name} added to inventory.")


def show_people(sales):
    st.header("Customers and Employees")

    customers = sales.customer_leaderboard()
    employees = sales.employee_leaderboard()

    if not customers and not employees:
        st.info("No sales yet.")
        return

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top customers")
        customer_rows = []
        for c in customers:
            customer_rows.append({"Customer": c.name, "Total spent (KES)": c.total_spent})
        st.dataframe(customer_rows, hide_index=True)

    with col2:
        st.subheader("Employees")
        employee_rows = []
        for e in employees:
            employee_rows.append({
                "Employee": e.name,
                "Sales": e.sales_count,
                "Total (KES)": e.total_sales,
            })
        st.dataframe(employee_rows, hide_index=True)

def show_sell(inventory, sales):
    st.header("Sell Product")

    product_names = [p.name for p in inventory.get_all_products()]
    if not product_names:
        st.info("No products in stock yet. Add one on the Restock page.")
        return

    with st.form("sell_form", clear_on_submit=True):
        sell_product = st.selectbox("Product", product_names)
        sell_qty = st.number_input("Units to sell", min_value=1, step=1)
        customer_name = st.text_input("Customer name")
        employee_name = st.text_input("Employee serving")
        sell_submitted = st.form_submit_button("Complete sale")

    if sell_submitted:
        customer_name = clean_text(customer_name)
        employee_name = clean_text(employee_name)

        if customer_name == "" or employee_name == "":
            st.error("Please enter both the customer and employee name")
        else:
            sale, error = sales.make_sale(
                inventory, sell_product, int(sell_qty), customer_name, employee_name
            )
            if error:
                st.error(error)
            else:
                inventory.save_to_file()
                sales.save_sale(sale)
                st.success(f"Sold! {sale}")


def show_report(sales):
    st.header("Sales Report")

    report = sales.get_history_report()

    if not report["rows"]:
        st.info("No sales yet.")
        return

    col1, col2, col3 = st.columns(3)
    col1.metric("Total revenue", f"KES{report['total_revenue']}")
    col2.metric("Products sold", report["unique_count"])
    col3.metric("Best seller", f"{report['best_product']} ({report['best_qty']} units)")

    top = report["top_employee"]
    if top:
        st.write(f"Top employee: {top}")
        chart_rows = []
        for product, qty in report ["qty_by_product"].items():
            chart_rows.append({"Product": product, "Units sold": qty})

        st.subheader("Units sold per product")
        st.bar_chart(chart_rows, x= "Product", y="Units sold")



        st.subheader("All sales")
        st.dataframe(list(reversed(report["rows"])), hide_index=True)


def show_search(inventory):
    st.header("Search Products")
    term = st.text_input("Search by product name", key="search_term")

    if term.strip() == "":
        st.caption("Type part of a product name, for example 'bre' for Bread.")
        return

    matches = inventory.search(term)
    if matches:
        show_table(product_rows(matches))
    else:
        st.warning(f"No products match '{term}'.")
if "inventory" not in st.session_state:
            inventory, sales = setup()
            st.session_state.inventory = inventory
            st.session_state.sales = sales

inventory = st.session_state.inventory
sales = st.session_state.sales

kiosk_name, owner_name = load_kiosk_details()

if kiosk_name is None:
    st.title("Welcome to Kiosk Manager")
    st.write("First-time setup")

    with st.form("setup_form"):
        name_input = st.text_input("Kiosk name")
        owner_input = st.text_input("Owner's name")
        done = st.form_submit_button("Save and continue")
    if done:
        name_input = clean_text(name_input)
        owner_input = clean_text(owner_input)
        if name_input == "" or owner_input == "":
            st.error("Please enter both names.")
        else:
            save_kiosk_details(name_input, owner_input)
            st.rerun()

    st.stop()
st.title(kiosk_name)
st.caption(f"Owner: {owner_name}")

st.sidebar.title("Menu")
page = st.sidebar.radio("Go to", ["Stock", "Sell", "Restock", "Report", "Search"])

if page == "Stock":
    show_stock(inventory)
elif page == "Sell":
    show_sell(inventory, sales)
elif page == "Restock":
    show_restock(inventory)
elif page == "Report":
    show_report(sales)
elif page == "Search":
    show_search(inventory)




                    
                    
                    
            