# main.py
import os
import pandas as pd
from scraper import scrape_all_books

DATA_DIR = "data"
OUT_FILE = os.path.join(DATA_DIR, "books.csv")

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def main():
    ensure_data_dir()
    print("Starting scraper...")
    books = scrape_all_books()
    if not books:
        print("No books scraped. Exiting.")
        return

    df = pd.DataFrame(books)
    df.to_csv(OUT_FILE, index=False, encoding="utf-8")
    print(f"Saved raw scraped data to: {OUT_FILE}")
    print(df.head(5).to_string(index=False))

if __name__ == "__main__":
    main()
