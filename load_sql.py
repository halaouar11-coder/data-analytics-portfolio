
import sqlite3
from pathlib import Path

import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"
POWERBI_DIR = PROJECT_DIR / "powerbi"

csv_file = POWERBI_DIR / "sales_analyzed.csv"
database_file = DATA_DIR / "sales.db"

# Load the analyzed CSV
df = pd.read_csv(csv_file)

# Create the SQLite database and import the data
with sqlite3.connect(database_file) as connection:
    df.to_sql(
        "sales_analyzed",
        connection,
        if_exists="replace",
        index=False,
    )

    # Run a sample SQL query
    query = """
    SELECT
        Product,
        ROUND(SUM(Revenue), 2) AS Revenue,
        ROUND(SUM(Profit), 2) AS Profit
    FROM sales_analyzed
    GROUP BY Product
    ORDER BY Revenue DESC;
    """

    result = pd.read_sql_query(query, connection)

print("===== PRODUCT PERFORMANCE (SQL) =====")
print(result.to_string(index=False))
print(f"\nDatabase created at: {database_file}")
