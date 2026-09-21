import sqlite3
import csv

# Name of the cleaned CSV file
CSV_FILE = "books_clean.csv"

# Name of the SQLite database
DB_FILE = "books.db"

# Connect to the SQLite database
# If books.db does not exist, SQLite will create it
connection = sqlite3.connect(DB_FILE)

# Create a cursor to execute SQL commands
cursor = connection.cursor()

# Create the categories table
# category_id is the Primary Key
# category_name stores each category only once
cursor.execute("""
CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT NOT NULL UNIQUE
)
""")

# Create the books table
# book_id is the Primary Key
# category_id is the Foreign Key connected to categories
cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    price_gbp REAL NOT NULL,
    price_inr REAL NOT NULL,
    rating INTEGER NOT NULL,
    in_stock BOOLEAN NOT NULL,
    url TEXT,
    FOREIGN KEY (category_id)
        REFERENCES categories(category_id)
)
""")

# Open the cleaned CSV file
with open(CSV_FILE, "r", encoding="utf-8") as file:

    # Read the CSV as dictionaries
    reader = csv.DictReader(file)

    # Process each book
    for row in reader:

        # Insert the category into the categories table
        # INSERT OR IGNORE prevents duplicate categories
        cursor.execute(
            """
            INSERT OR IGNORE INTO categories (category_name)
            VALUES (?)
            """,
            (row["category"],)
        )

        # Find the ID of the category
        cursor.execute(
            """
            SELECT category_id
            FROM categories
            WHERE category_name = ?
            """,
            (row["category"],)
        )

        # Get the category ID from the query result
        category_id = cursor.fetchone()[0]

        # Insert the book into the books table
        cursor.execute(
            """
            INSERT INTO books (
                title,
                category_id,
                price_gbp,
                price_inr,
                rating,
                in_stock,
                url
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                row["title"],
                category_id,
                float(row["price_gbp"]),
                float(row["price_inr"]),
                int(row["rating"]),
                row["in_stock"].lower() == "true",
                row["url"]
            )
        )

# Save all changes permanently
connection.commit()

# Close the database connection
connection.close()

# Display success messages
print("Database created successfully.")
print("Data loaded into SQLite.")