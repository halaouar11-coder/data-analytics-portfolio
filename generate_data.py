
import csv
import random
from datetime import date, timedelta
from pathlib import Path

# Make the results reproducible
random.seed(42)

# Project folders
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = DATA_DIR / "sales.csv"

# Sample business data
products = {
    "Laptop": 7500,
    "Monitor": 1800,
    "Keyboard": 250,
    "Mouse": 120,
    "Headphones": 400,
}

regions = ["Casablanca", "Rabat", "Kenitra", "Marrakech", "Tangier"]
payment_methods = ["Cash", "Card", "Bank Transfer"]

start_date = date(2025, 1, 1)

with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=[
            "OrderID",
            "OrderDate",
            "Product",
            "Region",
            "Quantity",
            "UnitPrice",
            "UnitCost",
            "PaymentMethod",
        ],
    )
    writer.writeheader()

    for order_id in range(1, 501):
        product = random.choice(list(products.keys()))
        unit_price = products[product]
        unit_cost = round(unit_price * random.uniform(0.55, 0.80), 2)
        quantity = random.randint(1, 5)
        order_date = start_date + timedelta(days=random.randint(0, 364))

        writer.writerow({
            "OrderID": order_id,
            "OrderDate": order_date.isoformat(),
            "Product": product,
            "Region": random.choice(regions),
            "Quantity": quantity,
            "UnitPrice": unit_price,
            "UnitCost": unit_cost,
            "PaymentMethod": random.choice(payment_methods),
        })

print(f"Success! Dataset created at: {OUTPUT_FILE}")
print("Number of orders: 500")
