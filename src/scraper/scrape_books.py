import requests
import pandas as pd

from bs4 import BeautifulSoup
from datetime import datetime, timezone
from pathlib import Path


BASE_URL = "https://books.toscrape.com/"
OUTPUT_FILE = Path("data/raw/books.csv")
MAX_BOOKS = 20


def get_soup(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def scrape_detail(product_url):
    soup = get_soup(product_url)

    availability = soup.select_one(".availability").get_text(
        " ", strip=True
    )

    stock_quantity = (
        availability
        .replace("In stock (", "")
        .replace(" available)", "")
    )

    return {
        "stock_quantity": int(stock_quantity),
    }


def scrape_page(url):
    soup = get_soup(url)
    books = []

    for book in soup.select("article.product_pod"):
        if len(books) >= MAX_BOOKS:
            break

        title = book.h3.a["title"]
        price = book.select_one(".price_color").text.strip()

        rating_element = book.select_one("p.star-rating")
        rating = rating_element.get("class")[1]

        relative_url = book.h3.a["href"]
        product_url = requests.compat.urljoin(
            url,
            relative_url
        )

        print(f"Scraping detail: {product_url}")

        detail = scrape_detail(product_url)

        books.append(
            {
                "product_name": title,
                "price": price,
                "rating": rating,
                "stock_quantity": detail["stock_quantity"],
                "product_url": product_url,
                "scraped_at": datetime.now(timezone.utc),
            }
        )

    next_button = soup.select_one("li.next a")

    if next_button:
        next_url = requests.compat.urljoin(
            url,
            next_button["href"]
        )
    else:
        next_url = None

    return books, next_url


def main():
    all_books = []
    current_url = BASE_URL

    while current_url and len(all_books) < MAX_BOOKS:
        print(f"\nScraping page: {current_url}")

        books, next_url = scrape_page(current_url)

        all_books.extend(books)

        # Pastikan tidak menyimpan lebih dari MAX_BOOKS
        if len(all_books) >= MAX_BOOKS:
            all_books = all_books[:MAX_BOOKS]
            break

        current_url = next_url

    df = pd.DataFrame(all_books)

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\n=== RESULT ===")
    print(f"Total books: {len(df)}")
    print(f"Columns: {df.columns.tolist()}")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

