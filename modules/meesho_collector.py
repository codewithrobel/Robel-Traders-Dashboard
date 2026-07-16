

import pandas as pd
from datetime import datetime
from utils.data_manager import save_products


class MeeshoCollector:
    def __init__(self):
        self.last_run = None

    def collect_sample_data(self, keyword="demo"):
        data = [
            {
                "ProductCode": f"{keyword.upper()}-001",
                "ProductName": f"{keyword} Product 1",
                "Price": 499,
                "Reviews": 1200,
                "Rating": 4.3,
                "Score": 0,
            },
            {
                "ProductCode": f"{keyword.upper()}-002",
                "ProductName": f"{keyword} Product 2",
                "Price": 699,
                "Reviews": 800,
                "Rating": 4.5,
                "Score": 0,
            },
        ]

        df = pd.DataFrame(data)
        df["Score"] = (df["Reviews"] * 0.4) + (df["Rating"] * 1000 * 0.6)

        save_products(df)

        self.last_run = datetime.now()
        return df

    def collect_from_url(self, product_url):
        """
        Placeholder for user-supplied product URL analysis.
        This method intentionally does not perform automated login or scraping.
        """
        return pd.DataFrame([
            {
                "ProductCode": "URL-001",
                "ProductName": "Pending URL Analysis",
                "Price": 0,
                "Reviews": 0,
                "Rating": 0.0,
                "Score": 0,
                "Source": product_url,
            }
        ])


collector = MeeshoCollector()