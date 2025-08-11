# clean_data.py
import pandas as pd
import os
import re

IN_FILE = os.path.join("data", "books.csv")
OUT_FILE = os.path.join("data", "books_cleaned.csv")

def clean_price(s):
    if pd.isna(s):
        return None
    # remove non-digit except dot
    cleaned = re.sub(r"[^0-9.]+", "", str(s))
    try:
        return float(cleaned) if cleaned else None
    except:
        return None

def extract_stock(s):
    if pd.isna(s):
        return 0
    m = re.search(r"(\d+)", str(s))
    return int(m.group(1)) if m else 0

def normalize_columns(df):
    # Normalize column names to consistent ones used below (keep original case too)
    # If scraped columns differ, try common fallbacks
    cols = {c.lower(): c for c in df.columns}
    mapping = {}
    if "title" in cols:
        mapping[cols["title"]] = "Title"
    if "price" in cols:
        mapping[cols["price"]] = "Price"
    if "availability" in cols:
        mapping[cols["availability"]] = "Availability"
    if "rating" in cols:
        mapping[cols["rating"]] = "Rating"
    if "category" in cols:
        mapping[cols["category"]] = "Category"
    if "upc" in cols:
        mapping[cols["upc"]] = "UPC"
    if "description" in cols:
        mapping[cols["description"]] = "Description"
    if "detailurl" in cols:
        mapping[cols["detailurl"]] = "DetailURL"
    if mapping:
        df = df.rename(columns=mapping)
    return df

def main():
    if not os.path.exists(IN_FILE):
        raise FileNotFoundError(f"{IN_FILE} not found. Run main.py to scrape first.")

    df = pd.read_csv(IN_FILE, encoding="utf-8", on_bad_lines="skip")
    df = normalize_columns(df)

    # Clean Price -> numeric float
    if "Price" in df.columns:
        df["Price_clean"] = df["Price"].apply(clean_price)
    else:
        df["Price_clean"] = None

    # Availability -> stock count numeric
    if "Availability" in df.columns:
        df["Stock"] = df["Availability"].apply(extract_stock)
    else:
        df["Stock"] = 0

    # Ensure Rating is present
    if "Rating" in df.columns:
        df["Rating_clean"] = df["Rating"].astype(str)
    else:
        df["Rating_clean"] = ""

    # Fill missing Category with Unknown
    if "Category" not in df.columns:
        df["Category"] = ""

    # Keep a clean, consistent set of columns
    cleaned = df[["Title", "Price", "Price_clean", "Stock", "Rating", "Rating_clean", "Category", "UPC", "Description", "DetailURL"]].copy()

    # Rename to friendly column names
    cleaned = cleaned.rename(columns={
        "Price_clean": "PriceNum",
        "Rating_clean": "RatingText"
    })

    # Fill NaNs
    cleaned["PriceNum"] = cleaned["PriceNum"].fillna(0.0)
    cleaned["Stock"] = cleaned["Stock"].fillna(0).astype(int)
    cleaned["Category"] = cleaned["Category"].fillna("Unknown")
    cleaned["Title"] = cleaned["Title"].fillna("Unknown Title")

    cleaned.to_csv(OUT_FILE, index=False, encoding="utf-8")
    print(f"✅ Cleaned data saved to {OUT_FILE}")
    print(cleaned.head(6).to_string(index=False))

if __name__ == "__main__":
    main()
