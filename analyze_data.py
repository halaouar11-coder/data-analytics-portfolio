
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Locate the project folders
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"
REPORTS_DIR = PROJECT_DIR / "reports"
POWERBI_DIR = PROJECT_DIR / "powerbi"

REPORTS_DIR.mkdir(parents=True, exist_ok=True)
POWERBI_DIR.mkdir(parents=True, exist_ok=True)

# Load the sales dataset
input_file = DATA_DIR / "sales.csv"
df = pd.read_csv(input_file, parse_dates=["OrderDate"])

# Calculate business metrics
df["Revenue"] = df["Quantity"] * df["UnitPrice"]
df["TotalCost"] = df["Quantity"] * df["UnitCost"]
df["Profit"] = df["Revenue"] - df["TotalCost"]
df["Month"] = df["OrderDate"].dt.to_period("M").astype(str)

# Basic KPIs
total_revenue = df["Revenue"].sum()
total_cost = df["TotalCost"].sum()
total_profit = df["Profit"].sum()
total_orders = df["OrderID"].nunique()
total_units = df["Quantity"].sum()
profit_margin = total_profit / total_revenue if total_revenue else 0

print("\n===== SALES ANALYSIS =====")
print(f"Total Revenue: {total_revenue:,.2f} MAD")
print(f"Total Cost: {total_cost:,.2f} MAD")
print(f"Total Profit: {total_profit:,.2f} MAD")
print(f"Total Orders: {total_orders}")
print(f"Units Sold: {total_units}")
print(f"Profit Margin: {profit_margin:.2%}")

# Performance by product
product_summary = (
    df.groupby("Product", as_index=False)
    .agg(
        Revenue=("Revenue", "sum"),
        TotalCost=("TotalCost", "sum"),
        Profit=("Profit", "sum"),
        UnitsSold=("Quantity", "sum"),
        Orders=("OrderID", "nunique"),
    )
    .sort_values("Revenue", ascending=False)
)

print("\n===== PERFORMANCE BY PRODUCT =====")
print(product_summary.to_string(index=False))

# Performance by region
region_summary = (
    df.groupby("Region", as_index=False)
    .agg(
        Revenue=("Revenue", "sum"),
        Profit=("Profit", "sum"),
        Orders=("OrderID", "nunique"),
    )
    .sort_values("Revenue", ascending=False)
)

# Performance by month
monthly_summary = (
    df.groupby("Month", as_index=False)
    .agg(
        Revenue=("Revenue", "sum"),
        Profit=("Profit", "sum"),
        Orders=("OrderID", "nunique"),
    )
    .sort_values("Month")
)

# Export analysis files for Power BI
df.to_csv(POWERBI_DIR / "sales_analyzed.csv", index=False)
product_summary.to_csv(POWERBI_DIR / "product_summary.csv", index=False)
region_summary.to_csv(POWERBI_DIR / "region_summary.csv", index=False)
monthly_summary.to_csv(POWERBI_DIR / "monthly_summary.csv", index=False)

# Create a revenue-by-product chart
plt.figure(figsize=(9, 5))
plt.bar(product_summary["Product"], product_summary["Revenue"])
plt.title("Revenue by Product")
plt.xlabel("Product")
plt.ylabel("Revenue (MAD)")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig(REPORTS_DIR / "revenue_by_product.png", dpi=150)
plt.close()

print("\nAnalysis completed successfully!")
print("Power BI files saved in the powerbi folder.")
print("Chart saved in the reports folder.")
