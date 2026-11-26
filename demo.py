import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("scraper.log"),
        logging.StreamHandler()
    ]
)


import csv
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

def fetch_page(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.content

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
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

    return books



def transform_book(book):
    title = book["title"].strip()
    price = book["price"].replace("£", "").strip()

    if not title:
        return None

    try:
        numeric_price = float(price)

    except ValueError:
        return None

    if numeric_price <= 0:
        return None

    cleaned_book = {
        "title": title,
        "price": numeric_price
    }

    return cleaned_book


def scrape_all_pages():
    all_books = []
    page = 1

    while True:
        url = f"https://books.toscrape.com/catalogue/page-{page}.html"

        print(f"Scraping page {page}...")

        html = fetch_page(url)

        if html is None:
            break

        extracted_books = extract_books(html)

        if not extracted_books:
            break

        for book in extracted_books:
            cleaned_book = transform_book(book)

            if cleaned_book is not None:
                all_books.append(cleaned_book)

        page += 1

    return all_books

def save_to_csv(books):
    if not books:
        print("No books available to save.")
        return

    with open("books.csv", "w", newline="", encoding="utf-8") as file:
        fieldnames = ["title", "price"]

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(books)

    print(f"Successfully saved {len(books)} books to books.csv")


# url = "https://books.toscrape.com/"
# html=fetch_page(url)  
# if html:
#     print("successful")  

# extracted_books=extract_books(html)  
# print(extracted_books[0])

# cleaned_books=[]
# for book in extracted_books:
#     cleaned_book=transform_book(book)
#     if cleaned_book is not None:
#         cleaned_books.append(cleaned_book)
    
# print(cleaned_books[0])

# print(f"\nTotal books scraped: {len(books)}")
# print(books[:5])


def main():
    books = scrape_all_pages()
    save_to_csv(books)

    print(f"Total books processed: {len(books)}")

if __name__ == "__main__":
    main()








def save_to_csv(books):
    pass


def main():
    pass


# if __name__ == "__main__":
#     main()



# if __name__ == "__main__":
#     url = "https://books.toscrape.com/"
#     html = fetch_page(url)

#     if html:
#         print("Page fetched successfully!")
#         print(type(html))
#         print(len(html))