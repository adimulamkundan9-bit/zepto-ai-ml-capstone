# Zepto Support Assistant

## Overview

The Zepto Support Assistant is a Retrieval-Augmented Generation (RAG) based support system that answers questions related to Zepto policies.

The system retrieves relevant information from Zepto policy documents and generates a structured response containing the answer, retrieved sources, and confidence.

Questions outside the Zepto policy domain are restricted by the system.

## Features

- Policy document ingestion
- Text embeddings using Sentence Transformers
- Vector storage and retrieval using ChromaDB
- Top-3 relevant document retrieval
- Policy-focused question answering
- Question routing
- Structured responses using Pydantic
- FastAPI REST API
- Swagger API documentation
- Docker support

## Project Structure

support_assistant/
├── docs/
│   ├── doc_01.txt
│   ├── doc_02.txt
│   ├── doc_03.txt
│   ├── doc_04.txt
│   ├── doc_05.txt
│   ├── doc_06.txt
│   ├── doc_07.txt
│   └── doc_08.txt
├── chroma_db/
├── ingest.py
├── main.py
├── requirements.txt
├── Dockerfile
├── .gitignore
└── README.md

## How It Works

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
Structured Response
↓
FastAPI /ask

For non-policy questions, the system returns a restricted response instead of generating an answer.

## Document Ingestion

The policy documents are stored in the docs directory.

Run:

```bash
python ingest.py
```

The ingestion process reads the policy documents, generates embeddings using Sentence Transformers, and stores the vectors in ChromaDB.

## Installation

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Running the Application

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The API will be available at:

http://127.0.0.1:8000

Swagger documentation:

http://127.0.0.1:8000/docs

## API Endpoint

### POST /ask

The `/ask` endpoint accepts a user query.

Example request:

```json
{
  "query": "What is the delivery time?"
}
```

Example policy response:

```json
{
  "answer": "Based on the retrieved context: Zepto delivers grocery and household essentials to serviceable pin codes within the stated delivery time.",
  "sources": [
    "doc_01",
    "doc_05",
    "doc_03"
  ],
  "confidence": 1.0
}
```

## General Question Handling

The assistant only answers questions related to Zepto policies.

Example:

```text
What is the capital of India?
```

Response:

```json
{
  "answer": "I can only answer questions about Zepto policies right now.",
  "sources": [],
  "confidence": 1.0
}
```

## Technology Stack

- Python
- FastAPI
- Uvicorn
- Pydantic
- ChromaDB
- Sentence Transformers
- BeautifulSoup
- Requests
- Docker

## API Testing

The FastAPI Swagger interface was used to test the application.

The following were successfully tested:

- GET /docs
- GET /openapi.json
- POST /ask

The `/ask` endpoint returned HTTP 200 responses for the tested requests.

## Docker

Build the Docker image:

```bash
docker build -t zepto-support-assistant .
```

Run the container:

```bash
docker run -p 8000:8000 zepto-support-assistant
```

Swagger documentation will then be available at:

http://localhost:8000/docs

## Module 3 Output

The completed Support Assistant provides:

- Retrieval of relevant Zepto policy information
- Top-3 source retrieval
- Source identification
- Structured answers
- Confidence values
- Policy-only question handling
- FastAPI REST API
- Swagger API documentation
- Docker support
