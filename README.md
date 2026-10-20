# Kiosk Manager

A command-line inventory and sales management system for a small Nairobi kiosk, written in Python. It began as a single-file capstone project and was rebuilt using classes, services, and a proper package structure.

## Features

- **Inventory management**: view stock, restock existing products, add new ones
- **Selling**: stock is checked before every sale, so the kiosk can never oversell
- **Customers**: every sale is tied to a customer, with running total spend tracked per person
- **Employees**: every sale records who served the customer, with a top-employee line in the report
- **Sales report**: itemised sales, total revenue, unique products sold, best-selling product
- **Search**: case-insensitive, partial-match product search
- **Persistence**: inventory is saved between runs, sales history is appended, and customer/employee totals are rebuilt on startup
- **Remembered setup**: kiosk name and owner are asked once, then loaded automatically
- **Low-stock alerts**: products running low are written to `restock_alerts.txt` on exit
- **Input validation**: bad input (letters, empty values, out-of-range choices) never crashes the program

## Project structure

```
kiosk_manager_v/
├── main.py                 # menu loop and program flow
├── models/
│   ├── product.py          # Product: owns its own stock logic
│   ├── customer.py         # Customer: tracks total spent
│   ├── employee.py         # Employee: tracks sales handled
│   └── sale.py             # Sale: one transaction (product, customer, employee)
├── services/
│   ├── inventory.py        # Inventory: manages the collection of products
│   └── sales.py            # SalesService: sales log, customers, employees, reports
└── utils/
    └── validation.py       # reusable input-cleaning and validation helpers
```

**Design idea:** `models/` holds single objects that know only about themselves. `services/` coordinates collections of those objects and holds the business logic. `main.py` ties it together and runs the menu.

## How to run

Requires Python 3. No external libraries are needed.

```
python main.py
```

Always run `main.py` from the project root. The other files are imported by it and are not meant to be run directly.

On first run the kiosk starts with a small default inventory. Data files are created automatically when you exit with option 6:

| File | Purpose |
|------|---------|
| `inventory.txt` | current stock, overwritten on each exit |
| `sales_history.txt` | every sale ever made, appended on each exit |
| `restock_alerts.txt` | products that are low on stock |
| `kiosk.txt` | kiosk name and owner, asked once on first run and remembered after that |

## Skills demonstrated

Classes and objects, encapsulation, composition, single responsibility, packages and imports, dictionaries, lists, tuples, sets, string handling, file reading and writing, input validation, and debugging.

## Author

Your Name Here
