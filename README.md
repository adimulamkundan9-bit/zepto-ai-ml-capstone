# Zepto AI/ML Capstone Project

## Project Overview

This project is an end-to-end AI/ML capstone organized into three modules:

1. Data Pipeline
2. Analytics and Modeling
3. Support Assistant

The project demonstrates data collection, data cleaning, database creation, SQL analysis, exploratory data analysis, machine learning, and a retrieval-augmented support assistant.

## Repository Structure

```text
zepto-ai-ml-capstone/
│
├── data_pipeline/
├── analytics/
├── support_assistant/
│   ├── docs/
│   ├── chroma_db/
│   ├── ingest.py
│   ├── main.py
│   ├── Dockerfile
│   └── README.md
│
├── README.md
├── requirements.txt
└── .gitignore
```

## Setup

This project uses one consolidated root `requirements.txt` for the dependencies required across the project.

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Module 1 – Data Pipeline

### Purpose

Module 1 collects book data from Books to Scrape, cleans the collected data, stores it in a normalized SQLite database, and performs SQL and pandas analysis.

### Data Collection

The scraper uses Requests and BeautifulSoup to collect book information from multiple categories.

The collected fields include:

- Book title
- Category
- Price in GBP
- Rating
- Stock availability

The project collects at least 60 books across at least 3 categories.

### Data Cleaning

The raw data is cleaned before database insertion.

The cleaning process includes:

- Converting ratings to integers
- Converting stock availability to boolean values
- Converting GBP prices to INR
- Using the fixed conversion rate of 1 GBP = 105.50 INR

### Database

A normalized SQLite database is used to store the cleaned data.

The database design uses related tables with primary keys and foreign keys to reduce duplication and maintain relationships between entities.

### SQL Analysis

The module includes SQL queries covering:

- SELECT and WHERE
- ORDER BY
- LIMIT
- DISTINCT
- IN or BETWEEN
- JOIN

At least two SQL query results are also read into pandas DataFrames, and the JOIN operation is reproduced using `pandas.merge()`.

### How to Run

From the project root:

```bash
cd data_pipeline
python scraper.py
python cleaner.py
```

The generated raw and cleaned data and SQLite database are used for the remaining analysis steps included in the module.

### Design Decisions

Requests and BeautifulSoup were selected for straightforward HTML scraping. The data is cleaned before database insertion so that the database contains consistent values. SQLite was selected because the project requires a lightweight relational database without an external database server.

---

## Module 2 – Analytics and Modeling

### Purpose

Module 2 performs exploratory data analysis and machine learning using the prepared project data.

The module covers data exploration, preprocessing, model training, evaluation, model comparison, and prediction.

### Data Analysis

The analytics workflow includes:

- Understanding the dataset
- Checking data types and missing values
- Examining numerical and categorical features
- Exploring distributions and relationships
- Identifying patterns relevant to the prediction task

### Data Preprocessing

The preprocessing workflow handles numerical and categorical variables separately.

Numerical features are scaled where required, while categorical features are encoded before being passed to machine learning models.

The preprocessing steps are integrated with the machine learning workflow to avoid inconsistent transformations between training and prediction.

### Machine Learning Models

The module evaluates multiple classification models, including:

- Logistic Regression
- Decision Tree
- Random Forest

Class imbalance is handled using balanced class weights where appropriate.

Model performance is evaluated using classification metrics and compared to understand the behavior of the different approaches.

### Model Selection and Evaluation

The workflow also includes model tuning and evaluation techniques such as cross-validation and parameter search where applicable.

The trained model artifacts are saved so that they can be reused without retraining the models every time the application is executed.

### How to Run

From the project root:

```bash
cd analytics
```

Run the notebooks or Python scripts provided in the `analytics` directory according to their execution order.

For notebook-based analysis, open the required `.ipynb` file in Jupyter Notebook or VS Code and run the cells from top to bottom.

### Design Decisions

Multiple models are used instead of relying on a single algorithm so their performance can be compared. Preprocessing is kept inside the machine learning workflow to maintain consistency. Class balancing is used because the target classes are not evenly distributed. Saved model artifacts make later prediction and application use more efficient.

---

## Module 3 – Support Assistant

### Purpose

Module 3 implements a retrieval-augmented support assistant that answers user questions using a collection of support and policy documents.

The system combines document ingestion, embeddings, vector search, question routing, and an API interface.

### Documents

The support assistant uses a collection of text documents stored inside:

```text
support_assistant/docs/
```

These documents provide the knowledge base used for retrieval.

### Document Ingestion

The ingestion process:

1. Reads the support documents.
2. Processes the document text.
3. Creates embeddings using a sentence-transformer model.
4. Stores the embeddings in ChromaDB.

The vector database allows relevant documents to be retrieved for a user question.

### Question Routing

The assistant first routes the incoming user question.

For policy-related questions, the system retrieves the top 3 relevant documents from the vector database before generating the response.

The overall flow is:

```text
User Question
      ↓
Question Routing
      ↓
Policy Question?
      ↓
Retrieve Top-3 Relevant Documents
      ↓
Generate Answer
      ↓
Return Response
```

### API

The support assistant provides an API through FastAPI.

The main application is located in:

```text
support_assistant/main.py
```

The document ingestion process is located in:

```text
support_assistant/ingest.py
```

### How to Run

From the project root:

```bash
cd support_assistant
```

Install the project requirements if they have not already been installed:

```bash
pip install -r ../requirements.txt
```

Run the ingestion process:

```bash
python ingest.py
```

Start the FastAPI application:

```bash
uvicorn main:app --reload
```

The API can then be tested through the FastAPI documentation interface.

### Docker

The module also contains a `Dockerfile` for containerized execution.

Build the image:

```bash
docker build -t support-assistant .
```

Run the container:

```bash
docker run -p 8000:8000 support-assistant
```

### Design Decisions

A vector database is used because semantic similarity is more suitable than simple keyword matching for retrieving relevant support information. Sentence-transformer embeddings are used to represent document meaning. ChromaDB provides lightweight local vector storage. FastAPI provides a simple API interface, while Docker provides a reproducible way to run the support assistant.

---

## Technologies Used

- Python
- Requests
- BeautifulSoup
- pandas
- SQLite
- SQL
- NumPy
- scikit-learn
- Jupyter Notebook
- Sentence Transformers
- ChromaDB
- FastAPI
- Uvicorn
- Docker
- Git and GitHub

## Git Workflow

The repository uses Git for version control.

The project history includes a feature branch with multiple commits followed by a merge back into the `main` branch, demonstrating the required feature-branch workflow.

## Conclusion

This capstone combines data engineering, analytics, machine learning, and an AI-powered support assistant in a single repository. Each module is independently organized while sharing the same project-level setup and documentation.
