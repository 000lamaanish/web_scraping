
import csv
import logging
import requests
from bs4 import BeautifulSoup

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("scraper.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)


def fetch_page(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        logging.info("Successfully fetched: %s", url)
        return response.content

    except requests.exceptions.RequestException as e:
        logging.error("Request failed for %s: %s", url, e)
        return None


def extract_books(html):
    soup = BeautifulSoup(html, "html.parser")
    book_containers = soup.find_all("article", class_="product_pod")

    books = []

    for book in book_containers:
        title = book.find("h3").find("a").get_text(strip=True)
        price = book.find("p", class_="price_color").get_text(strip=True)

        book_data = {
            "title": title,
            "price": price
        }

        books.append(book_data)

    logging.info("Extracted %d books", len(books))
    return books


def transform_book(book):
    title = book["title"].strip()
    price = book["price"].replace("£", "").strip()

    if not title:
        logging.warning("Skipping book with empty title")
        return None

    try:
        numeric_price = float(price)

    except ValueError:
        logging.warning("Invalid price for book: %s", title)
        return None

    if numeric_price <= 0:
        logging.warning("Non-positive price for book: %s", title)
        return None

    return {
        "title": title,
        "price": numeric_price
    }


def scrape_all_pages():
    all_books = []
    page = 1

    while True:
        url = f"https://books.toscrape.com/catalogue/page-{page}.html"

        logging.info("Starting page %d", page)

        html = fetch_page(url)

        if html is None:
            logging.info("Stopping pagination at page %d", page)
            break

        extracted_books = extract_books(html)

        if not extracted_books:
            logging.info("No books found on page %d", page)
            break

        for book in extracted_books:
            cleaned_book = transform_book(book)

            if cleaned_book is not None:
                all_books.append(cleaned_book)

        logging.info(
            "Completed page %d. Total collected: %d",
            page,
            len(all_books)
        )

        page += 1

    return all_books


def save_to_csv(books):
    if not books:
        logging.warning("No books available to save")
        return

    with open("books.csv", "w", newline="", encoding="utf-8") as file:
        fieldnames = ["title", "price"]

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(books)

    logging.info("Successfully saved %d books to books.csv", len(books))


def main():
    logging.info("Scraper pipeline started")

    books = scrape_all_pages()
    save_to_csv(books)

    logging.info("Scraper pipeline finished. Total books: %d", len(books))


if __name__ == "__main__":
    main()
