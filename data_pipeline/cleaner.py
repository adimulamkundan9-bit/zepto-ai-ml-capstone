import csv

INPUT_FILE = "books_raw.csv"
OUTPUT_FILE = "books_clean.csv"

GBP_TO_INR = 105.50

cleaned_books = []

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        price_gbp = float(row["price_gbp"])
        rating = int(row["rating"])
        in_stock = row["in_stock"].strip().lower() == "true"
        price_inr = round(price_gbp * GBP_TO_INR, 2)

        cleaned_books.append({
            "title": row["title"].strip(),
            "category": row["category"].strip(),
            "price_gbp": price_gbp,
            "price_inr": price_inr,
            "rating": rating,
            "in_stock": in_stock,
            "url": row["url"].strip()
        })

with open(
    OUTPUT_FILE,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    fieldnames = [
        "title",
        "category",
        "price_gbp",
        "price_inr",
        "rating",
        "in_stock",
        "url"
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(cleaned_books)

print(f"Cleaned books: {len(cleaned_books)}")
print(f"Data saved to {OUTPUT_FILE}")