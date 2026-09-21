import sqlite3

DB_FILE = "books.db"
SQL_FILE = "queries.sql"
OUTPUT_FILE = "sql_results.txt"

connection = sqlite3.connect(DB_FILE)
cursor = connection.cursor()

with open(SQL_FILE, "r", encoding="utf-8") as file:
    sql_script = file.read()

lines = []

for line in sql_script.splitlines():
    if not line.strip().startswith("--"):
        lines.append(line)

sql_script = "\n".join(lines)

queries = [
    query.strip()
    for query in sql_script.split(";")
    if query.strip()
]

with open(OUTPUT_FILE, "w", encoding="utf-8") as output:

    for number, query in enumerate(queries, start=1):

        cursor.execute(query)

        columns = [description[0] for description in cursor.description]
        rows = cursor.fetchall()

        print(f"\nQuery {number}")
        print("-" * 50)
        print(columns)

        for row in rows:
            print(row)

        output.write(f"\nQuery {number}\n")
        output.write("-" * 50 + "\n")
        output.write(query + "\n\n")
        output.write("Columns: " + str(columns) + "\n")

        for row in rows:
            output.write(str(row) + "\n")

connection.close()

print("\nAll SQL queries executed successfully.")
print(f"Results saved to {OUTPUT_FILE}")