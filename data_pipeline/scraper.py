
import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

BASE_URL = "https://books.toscrape.com/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

books = []

response = requests.get(BASE_URL, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

category_links = soup.select(".side_categories ul li ul li a")
selected_categories = category_links[:5]

for category_link in selected_categories:
    category_name = category_link.get_text(strip=True)
    category_url = urljoin(BASE_URL, category_link["href"])

    page_url = category_url
    category_books = 0

    while page_url and category_books < 20:
        response = requests.get(page_url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        book_items = soup.select("article.product_pod")

        for book in book_items:
            if category_books >= 20:
                break

            title = book.h3.a["title"]

            price_text = book.select_one(".price_color").get_text(strip=True)
            price_gbp = float(price_text.replace("Â£","").replace("£", ""))

            rating_text = book.select_one(".star-rating")["class"]
            rating_map = {
                "One": 1,
                "Two": 2,
                "Three": 3,
                "Four": 4,
                "Five": 5
            }
            rating = rating_map[rating_text[1]]

            stock_text = book.select_one(".availability").get_text(" ", strip=True)
            in_stock = "In stock" in stock_text

            book_url = urljoin(
                page_url,
                book.h3.a["href"]
            )

            books.append({
                "title": title,
                "category": category_name,
                "price_gbp": price_gbp,
                "rating": rating,
                "in_stock": in_stock,
                "url": book_url
            })

            category_books += 1

        next_button = soup.select_one("li.next a")

        if next_button:
            page_url = urljoin(page_url, next_button["href"])
        else:
            page_url = None

print(f"Total books scraped: {len(books)}")

with open("books_raw.csv", "w", newline="", encoding="utf-8") as file:
    fieldnames = [
        "title",
        "category",
        "price_gbp",
        "rating",
        "in_stock",
        "url"
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(books)

print("Data saved to books_raw.csv")