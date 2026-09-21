SELECT title, rating
FROM books
WHERE rating = 5;

SELECT title, price_inr
FROM books
ORDER BY price_inr DESC;

SELECT title, price_inr
FROM books
LIMIT 10;

SELECT DISTINCT category_name
FROM categories
ORDER BY category_name;

SELECT title, price_inr
FROM books
WHERE price_inr BETWEEN 2000 AND 4000;

SELECT title, category_id
FROM books
WHERE category_id IN (1, 12, 32);

SELECT
    books.title,
    categories.category_name,
    books.price_gbp,
    books.price_inr,
    books.rating
FROM books
JOIN categories
    ON books.category_id = categories.category_id;

SELECT
    books.title,
    categories.category_name,
    books.rating
FROM books
JOIN categories
    ON books.category_id = categories.category_id
WHERE books.rating >= 4
ORDER BY books.rating DESC;