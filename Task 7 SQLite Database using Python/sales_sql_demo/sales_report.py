import os
from sqlalchemy import create_engine, text
import matplotlib.pyplot as plt

# Use SQLite by default. Switch to my DB by setting DB_URL.
DB_URL = os.getenv("DB_URL", "sqlite:///sales.db")

engine = create_engine(DB_URL, future=True)

def seed_if_needed():
    # Only seed if using the default local SQLite file and it doesn't exist yet.
    is_sqlite_file = DB_URL.startswith("sqlite:///") and DB_URL.endswith("sales.db")
    db_file = "sales.db"
    if is_sqlite_file and not os.path.exists(db_file):
        with engine.begin() as conn:
            conn.execute(text("""
                CREATE TABLE sales (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_date TEXT,
                    product TEXT,
                    quantity INTEGER,
                    unit_price REAL,
                    discount REAL
                );
            """))
            conn.execute(text("""
                INSERT INTO sales (order_date, product, quantity, unit_price, discount) VALUES
                ('2025-07-01','Apple Watch',3,299.99,2.50),
                ('2025-07-01','AirPods',5,149.00,1.75),
                ('2025-07-02','iPhone Case',10,19.99,2.25),
                ('2025-07-03','MacBook Pro',1,1999.00,0.50),
                ('2025-07-03','iPad',2,499.00,0.00),
                ('2025-07-04','AirPods',2,149.00,1.25),
                ('2025-07-05','Apple Watch',1,299.99,3.50),
                ('2025-07-05','iPhone Case',4,19.99,2.75);
            """))

def main():
    seed_if_needed()

    # Total Quantity and Total Revenue
    sql = text("""
        SELECT
            COALESCE(SUM(quantity), 0) AS Total_Quantity,
            COALESCE(SUM(quantity * unit_price), 0) AS Total_Revenue,
            COALESCE(SUM((quantity * unit_price) * (1 - discount / 100.0)), 0) AS Discounted_Revenue
        FROM sales;
    """)

    with engine.connect() as conn:
        row = conn.execute(sql).mappings().one()

    Total_Quantity = int(row["Total_Quantity"] or 0)
    Total_Revenue = float(row["Total_Revenue"] or 0.0)
    Discounted_Revenue = float(row["Discounted_Revenue"] or 0.0)

    # Print results
    print("Sales Report Summary")
    print(f"Total Quantity sold: {Total_Quantity}")
    print(f"Total Revenue: {Total_Revenue:,.2f}")
    print(f"Discounted Revenue: {Discounted_Revenue:,.2f}")

    # Simple bar chart with two bars
    labels = ["Total Quantity", "Total Revenue", "Discounted Revenue"]
    values = [Total_Quantity, Total_Revenue, Discounted_Revenue]

    fig, ax = plt.subplots()
    ax.bar(labels, values)
    ax.set_title("Sales summary")
    ax.set_ylabel("Value")
    # annotate values above bars
    for i, v in enumerate(values):
        label = f"{v:,.2f}" if i in (1, 2) else f"{int(v)}"
        ax.text(i, v, label, ha="center", va="bottom")
    fig.tight_layout()
    # Save chart as PNG before showing
    fig.savefig("sales_sql_demo/sales_summary.png")

    # Show chart window
    plt.show()

if __name__ == "__main__":
    main()