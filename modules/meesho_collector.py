

import pandas as pd
from datetime import datetime
from utils.data_manager import save_products
import os
import json
import requests
import google.generativeai as genai


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
        try:
            response = requests.get(
                product_url,
                timeout=20,
                headers={"User-Agent": "Mozilla/5.0"}
            )

            html = response.text[:30000]

            api_key = os.getenv("GEMINI_API_KEY")

            if not api_key:
                return pd.DataFrame([
                    {
                        "ProductCode": "URL-NO-KEY",
                        "ProductName": "Gemini API Key Missing",
                        "Price": 0,
                        "Reviews": 0,
                        "Rating": 0,
                        "Score": 0,
                        "Source": "URL"
                    }
                ])

            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-2.5-flash")

            prompt = (
                "Analyze this Meesho product page HTML and return ONLY valid JSON with keys: "
                "product_name, price, rating, reviews. Use null if unavailable."
            )

            result = model.generate_content([prompt, html])

            text = result.text.strip()
            text = text.replace("```json", "").replace("```", "")

            data = json.loads(text)

            price = float(data.get("price") or 0)
            rating = float(data.get("rating") or 0)
            reviews = int(float(data.get("reviews") or 0))

            score = (reviews * 0.4) + (rating * 1000 * 0.6)

            return pd.DataFrame([
                {
                    "ProductCode": f"URL-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "ProductName": str(data.get("product_name") or "Unknown Product"),
                    "Price": price,
                    "Reviews": reviews,
                    "Rating": rating,
                    "Score": score,
                    "Source": "Gemini URL"
                }
            ])

        except Exception as e:
            return pd.DataFrame([
                {
                    "ProductCode": "URL-ERROR",
                    "ProductName": str(e),
                    "Price": 0,
                    "Reviews": 0,
                    "Rating": 0,
                    "Score": 0,
                    "Source": "URL"
                }
            ])


collector = MeeshoCollector()