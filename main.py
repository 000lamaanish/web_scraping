
import csv

import requests
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/"

response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")


books =soup.find_all("article", class_="product_pod")
print(len(books))

books = soup.find_all("article", class_="product_pod")

print(len(books))

# lets scrap the price of the same book
first_book=books[0]
print(first_book)
title_element=first_book.find('h3')
title=title_element.find("a").get_text(strip=True)
print(title)

price=first_book.find('p', class_="price_color").get_text(strip=True)
print(price)
scrapped_books=[]
for book in books:
    title = book.find("h3").find("a").get_text(strip=True)

    price = book.find(
        "p", class_="price_color"
    ).get_text(strip=True)

    book_data={
        'title':title,
        'price':price
    }
    scrapped_books.append(book_data)

print(scrapped_books)


with open("books.csv", "w", newline="", encoding="utf-8") as file:
    fieldnames = ["title", "price"]

    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(scrapped_books)

print("Data successfully saved to books.csv")

