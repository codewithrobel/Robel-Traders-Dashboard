import pandas as pd
from database import load_products as db_load_products
from database import save_products as db_save_products


def load_products():
    try:
        return db_load_products()
    except Exception:
        return pd.DataFrame(
            columns=[
                "ProductCode",
                "Price",
                "Reviews",
                "Rating",
                "Score",
                "Rank",
            ]
        )



def save_products(df):
    db_save_products(df)