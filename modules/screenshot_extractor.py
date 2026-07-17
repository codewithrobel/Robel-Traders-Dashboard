import re
import pandas as pd
from datetime import datetime
import os
import json

try:
    from PIL import Image, ImageEnhance, ImageFilter
except ImportError:
    Image = None

try:
    import google.generativeai as genai
except ImportError:
    genai = None

try:
    import pytesseract
except ImportError:
    pytesseract = None


class ScreenshotExtractor:
    def extract_data(self, image_path):
        if Image is None:
            raise ImportError("Required image libraries are not installed")

        api_key = os.getenv("GEMINI_API_KEY")

        if api_key and genai is not None:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-2.5-flash")

                image = Image.open(image_path)

                prompt = '''
Analyze this Meesho product screenshot.
Return ONLY valid JSON.

Rules:
- Extract the exact product title.
- Extract price as a number only.
- Extract rating as a number only.
- Extract reviews as a number only.
- Extract product_id only if it is clearly visible in the screenshot.
- If product_id is not visible, return null for product_id.
- Extract the selling price from the product card.
- Never invent a product_id.
- Never return random strings such as ao6lz6.
- Never return 0 for price unless the screenshot clearly shows 0.
- If a value is missing, return null.

{
  "product_name":"",
  "price":null,
  "rating":null,
  "reviews":null,
  "product_id":""
}
'''

                response = model.generate_content([prompt, image])
                text_response = response.text.strip()
                text_response = text_response.replace("```json", "").replace("```", "")

                data = json.loads(text_response)

                price = str(data.get("price", "")).replace("₹", "").replace(",", "").strip()
                reviews = str(data.get("reviews", "")).replace("Reviews", "").replace("reviews", "").replace(",", "").strip()
                rating = str(data.get("rating", "")).strip()

                try:
                    price = float(price) if price else 0
                except:
                    price = 0

                try:
                    reviews = int(float(reviews)) if reviews else 0
                except:
                    reviews = 0

                try:
                    rating = float(rating) if rating else 0
                except:
                    rating = 0

                product_id = str(data.get("product_id", "")).strip()

                if product_id and product_id.lower() != "null":
                    product_code = f"RT-{product_id}"
                else:
                    product_code = f"RT-{datetime.now().strftime('%Y%m%d%H%M%S')}"

                return pd.DataFrame([
                    {
                        "ProductCode": product_code,
                        "ProductName": str(data.get("product_name", "")).strip(),
                        "Price": price,
                        "Reviews": reviews,
                        "Rating": rating,
                        "Score": 0,
                        "Source": "Gemini"
                    }
                ])
            except Exception as e:
                print(f"Gemini extraction error: {e}")

        if pytesseract is None:
            return pd.DataFrame([
                {
                    "ProductCode": f"RT-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "ProductName": "Image Processed",
                    "Price": 0,
                    "Reviews": 0,
                    "Rating": 0,
                    "Score": 0,
                    "Source": "Screenshot"
                }
            ])
        image = Image.open(image_path)
        image = image.convert('L')
        image = ImageEnhance.Contrast(image).enhance(2.0)
        image = image.filter(ImageFilter.SHARPEN)
        text = pytesseract.image_to_string(image)

        rating_match = re.search(r"(\d\.\d)", text)
        reviews_match = re.search(r"(\d+[\,\d]*)\s*Reviews", text, re.IGNORECASE)

        return pd.DataFrame([
            {
                "ProductCode": f"RT-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "ProductName": "Extracted From Screenshot",
                "Price": 0,
                "Reviews": int(reviews_match.group(1).replace(',', '')) if reviews_match else 0,
                "Rating": float(rating_match.group(1)) if rating_match else 0,
                "Score": 0,
                "Source": "Screenshot"
            }
        ])


extractor = ScreenshotExtractor()