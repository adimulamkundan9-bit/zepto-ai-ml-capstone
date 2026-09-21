import sqlite3

DB_FILE = "books.db"

connection = sqlite3.connect(DB_FILE)
cursor = connection.cursor()

cursor.execute("SELECT COUNT(*) FROM books")
book_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM categories")
category_count = cursor.fetchone()[0]

cursor.execute("""
SELECT category_id, category_name
FROM categories
ORDER BY category_name
""")

categories = cursor.fetchall()

cursor.execute("""
SELECT
    books.book_id,
    books.title,
    categories.category_name,
    books.price_gbp,
    books.price_inr,
    books.rating,
    books.in_stock
FROM books
JOIN categories
    ON books.category_id = categories.category_id
ORDER BY books.book_id
LIMIT 5
""")

books = cursor.fetchall()

print("Total books:", book_count)
print("Total categories:", category_count)

print("\nCategories:")
for category in categories:
    print(category)

print("\nFirst 5 books:")
for book in books:
    print(book)

connection.close()