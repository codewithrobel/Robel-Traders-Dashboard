import sqlite3
import pandas as pd

DB_NAME = "robel.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        ProductCode TEXT PRIMARY KEY,
        ProductName TEXT,
        Price REAL,
        Rating REAL,
        Reviews INTEGER,
        Score REAL,
        Source TEXT,
        LastUpdated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

def save_products(df):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute(
            """
            INSERT OR REPLACE INTO products
            (ProductCode, ProductName, Price, Rating, Reviews, Score, Source)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                row.get("ProductCode", ""),
                row.get("ProductName", ""),
                row.get("Price", 0),
                row.get("Rating", 0),
                row.get("Reviews", 0),
                row.get("Score", 0),
                row.get("Source", "")
            )
        )

    conn.commit()
    conn.close()

def load_products():
    conn = sqlite3.connect(DB_NAME)

    df = pd.read_sql(
        "SELECT * FROM products",
        conn
    )

    conn.close()

    if "ProductCode" in df.columns:
        df["ProductCode"] = df["ProductCode"].astype(str).str.strip()

    if "Reviews" in df.columns:
        df["Reviews"] = pd.to_numeric(df["Reviews"], errors="coerce").fillna(0)

    if "Rating" in df.columns:
        df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce").fillna(0)

    if "Price" in df.columns:
        df["Price"] = pd.to_numeric(df["Price"], errors="coerce").fillna(0)

    return df