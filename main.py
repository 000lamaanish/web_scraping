
import csv
import requests
from bs4 import BeautifulSoup

base_url = "https://books.toscrape.com/catalogue/page-{}.html"

scrapped_books = []
page = 1

while True:
    url = base_url.format(page)

    # response = requests.get(url)

    # if response.status_code != 200:
    #     break
    try:
       response = requests.get(url, timeout=10)
       response.raise_for_status()

    except requests.exceptions.RequestException as e:
       print(f"Failed to scrape page {page}: {e}")
       break

    soup = BeautifulSoup(response.content, "html.parser")

    books = soup.find_all("article", class_="product_pod")

    if not books:
        break

    for book in books:
        title = book.find("h3").find("a").get_text(strip=True)
        price = book.find("p", class_="price_color").get_text(strip=True)

        if not title:
            continue

        try:
            cleaned_price = price.replace("£", "").strip()
            numeric_price = float(cleaned_price)
        except ValueError:
            continue


        if numeric_price <= 0:
            continue

        book_data = {
            "title": title,
            "price": numeric_price
        }

        scrapped_books.append(book_data)

    print(f"Page {page} scraped successfully.")

    page += 1

with open("books.csv", "w", newline="", encoding="utf-8") as file:
    fieldnames = ["title", "price"]

    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(scrapped_books)

print(f"\nTotal books scraped: {len(scrapped_books)}")
print("Data saved successfully!")
