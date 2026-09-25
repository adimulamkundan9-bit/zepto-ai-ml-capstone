# Zepto AI/ML Capstone Project

## Project Overview

This project is an end-to-end AI/ML capstone project demonstrating data
collection, data cleaning, database creation, SQL analysis, and
preparation of data for further analytics and machine learning tasks.

## Module 1: Data Pipeline

Module 1 focuses on building a complete data pipeline using book data
collected from Books to Scrape.

The pipeline collects book information, cleans and transforms the data,
stores it in a normalized SQLite database, and performs SQL-based
analysis.

## Technologies Used

-   Python
-   Requests
-   BeautifulSoup
-   CSV
-   SQLite
-   SQL

## Data Pipeline

The pipeline consists of the following stages:

1.  Web Scraping
2.  Data Cleaning and Transformation
3.  SQLite Database Creation
4.  Database Verification
5.  SQL Analysis

## 1. Web Scraping

The `scraper.py` script collects book information from Books to Scrape
using Requests and BeautifulSoup.

The scraper collects:

-   Book title
-   Category
-   Price in GBP
-   Rating
-   Stock status
-   Book URL

A total of 90 books were scraped across 5 categories.

The raw data is saved in:

``` text
books_raw.csv
```

## 2. Data Cleaning and Transformation

The `cleaner.py` script cleans and transforms the scraped data.

The following transformations are performed:

-   `price_gbp` is converted to a numeric value
-   `rating` is converted to an integer
-   `in_stock` is converted to a Boolean value
-   `price_inr` is calculated using a fixed conversion rate of ₹105.50
    per GBP
-   Text fields are cleaned

The cleaned data is saved in:

``` text
books_clean.csv
```

The cleaned dataset contains:

-   `title`
-   `category`
-   `price_gbp`
-   `price_inr`
-   `rating`
-   `in_stock`
-   `url`

## 3. SQLite Database Creation

The `database.py` script creates and populates the SQLite database.

Database:

``` text
books.db
```

The database contains two normalized tables:

### categories

Stores unique book categories.

-   `category_id` --- Primary Key
-   `category_name`

### books

Stores book information.

-   `book_id` --- Primary Key
-   `title`
-   `category_id` --- Foreign Key
-   `price_gbp`
-   `price_inr`
-   `rating`
-   `in_stock`
-   `url`

The `books.category_id` foreign key references `categories.category_id`.

The database contains:

-   90 books
-   5 categories

## 4. Database Verification

The `verify_db.py` script verifies the contents and relationships of the
SQLite database.

It verifies:

-   Total number of books
-   Total number of categories
-   Category records
-   Book records
-   Book-category relationship using a SQL JOIN

## 5. SQL Analysis

The `queries.sql` file contains the SQL queries used for database
analysis.

The queries demonstrate:

-   `SELECT`
-   `WHERE`
-   `ORDER BY`
-   `LIMIT`
-   `DISTINCT`
-   `BETWEEN`
-   `IN`
-   `JOIN`

The `run_queries.py` script executes the SQL queries against the SQLite
database.

The query results are saved in:

``` text
sql_results.txt
```

## Project Structure

``` text
zepto-ai-ml-capstone/
│
├── README.md
├── requirements.txt
│
├── analytics/
│
├── data_pipeline/
│   ├── scraper.py
│   ├── cleaner.py
│   ├── database.py
│   ├── verify_db.py
│   ├── run_queries.py
│   ├── queries.sql
│   ├── books_raw.csv
│   ├── books_clean.csv
│   ├── books.db
│   └── sql_results.txt
│
└── support_assistant/
```

## Installation

### 1. Clone the Repository

``` bash
git clone https://github.com/adimulamkundan9-bit/zepto-ai-ml-capstone.git
cd zepto-ai-ml-capstone
```

### 2. Create a Virtual Environment

``` bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

For Windows PowerShell:

``` powershell
.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

``` bash
pip install -r requirements.txt
```

## Module 1 Execution

Navigate to the data pipeline directory:

``` bash
cd data_pipeline
```

### Run the Web Scraper

``` bash
python scraper.py
```

This generates:

``` text
books_raw.csv
```

### Run the Data Cleaner

``` bash
python cleaner.py
```

This generates:

``` text
books_clean.csv
```

### Create the SQLite Database

``` bash
python database.py
```

This generates:

``` text
books.db
```

### Verify the Database

``` bash
python verify_db.py
```

### Run the SQL Queries

``` bash
python run_queries.py
```

This generates:

``` text
sql_results.txt
```

## Module 1 Status

-   Web scraping completed
-   90 books collected
-   5 categories collected
-   Data cleaning completed                                                         
-   GBP to INR conversion completed
-   SQLite database created
-   Normalized database structure implemented
-   Primary key and foreign key relationship implemented
-   Database verification completed
-   SQL queries executed successfully
-   SQL query results saved
-   Requirements file created
                                                                                                                                                                                                                                                                                                                           
## Final Submission Notes
This repository contains the complete three-module Zepto AI/ML capstone project.
