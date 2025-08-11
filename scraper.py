# scraper.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

BASE = "http://books.toscrape.com/"

session = requests.Session()
session.headers.update({"User-Agent": "books-scraper-bot/1.0 (+https://example.com)"})


def parse_book_detail(book_url):
    """Given an absolute URL to a book detail page, return dict of extra fields."""
    try:
        r = session.get(book_url, timeout=10)
        r.raise_for_status()
    except Exception as e:
        print(f"  ! Failed to fetch detail {book_url}: {e}")
        return {}

    s = BeautifulSoup(r.text, "html.parser")

    # Description
    desc_tag = s.select_one("#product_description ~ p")
    description = desc_tag.text.strip() if desc_tag else ""

    # Product info table (UPC, product type, price ex/tax etc.)
    product_info = {}
    for row in s.select("table.table.table-striped tr"):
        th = row.select_one("th").text.strip()
        td = row.select_one("td").text.strip()
        product_info[th] = td

    # Category: breadcrumb, second last <a>
    category = ""
    breadcrumb = s.select("ul.breadcrumb li a")
    if len(breadcrumb) >= 3:
        category = breadcrumb[-1].text.strip()

    return {
        "Description": description,
        "UPC": product_info.get("UPC", ""),
        "Product Type": product_info.get("Product Type", ""),
        "Category": category,
    }


def parse_listing_page(page_url):
    """Parse one listing page and return list of book dicts (basic fields + detail fields)."""
    try:
        r = session.get(page_url, timeout=10)
        r.raise_for_status()
    except Exception as e:
        print(f"! Failed to fetch page {page_url}: {e}")
        return []

    soup = BeautifulSoup(r.text, "html.parser")
    books = []

    for article in soup.select("article.product_pod"):
        # Title
        a = article.select_one("h3 a")
        title = a["title"].strip()

        # Relative link to detail
        rel_link = a["href"]
        # Build absolute URL carefully
        detail_url = urljoin(page_url, rel_link)

        # Price
        price = article.select_one("p.price_color").text.strip()

        # Availability text
        availability = article.select_one("p.instock.availability").text.strip()

        # Rating is stored as class e.g., <p class="star-rating Three">
        rating_tag = article.select_one("p.star-rating")
        rating = ""
        if rating_tag:
            classes = rating_tag.get("class", [])
            # classes contains ['star-rating', 'Three']
            for c in classes:
                if c != "star-rating":
                    rating = c

        # Now fetch detail page for category, description, UPC
        detail = parse_book_detail(detail_url)
        time.sleep(0.2)  # polite pause

        book = {
            "Title": title,
            "Price": price,
            "Availability": availability,
            "Rating": rating,
            "DetailURL": detail_url,
            "Category": detail.get("Category", ""),
            "UPC": detail.get("UPC", ""),
            "Description": detail.get("Description", ""),
            "Product Type": detail.get("Product Type", ""),
        }
        books.append(book)

    return books


def scrape_all_books():
    """Scrape all pages (handles index and catalogue pagination). Returns list of dicts."""
    all_books = []

    # Page 1 (index)
    print("Scraping page 1 (index)...")
    all_books.extend(parse_listing_page(urljoin(BASE, "index.html")))
    time.sleep(0.2)

    # Pages 2..50 (catalogue)
    for i in range(2, 51):
        page_url = urljoin(BASE, f"catalogue/page-{i}.html")
        print(f"Scraping page {i} ...")
        books = parse_listing_page(page_url)
        if not books:
            print(f"  -> no books found on page {i}, stopping early.")
            break
        all_books.extend(books)
        time.sleep(0.2)

    return all_books


if __name__ == "__main__":
    # quick test run
    books = scrape_all_books()
    print(f"Scraped {len(books)} books")
