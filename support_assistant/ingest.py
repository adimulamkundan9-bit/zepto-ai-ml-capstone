from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parent
DOCS_DIR = BASE_DIR / "docs"
DB_DIR = BASE_DIR / "chroma_db"

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path=str(DB_DIR))

collection = client.get_or_create_collection(
    name="zepto_policies",
    metadata={"hnsw:space": "cosine"}
)

documents = []
ids = []
metadatas = []

for file_path in sorted(DOCS_DIR.glob("*.txt")):
    text = file_path.read_text(encoding="utf-8").strip()

    documents.append(text)
    ids.append(file_path.stem)
    metadatas.append({"source": file_path.stem})

embeddings = model.encode(documents).tolist()

collection.upsert(
    ids=ids,
    documents=documents,
    embeddings=embeddings,
    metadatas=metadatas
)

print(f"Documents loaded: {len(documents)}")
print(f"ChromaDB collection count: {collection.count()}")

results = collection.query(
    query_embeddings=[model.encode("What is the delivery policy?").tolist()],
    n_results=3
)

print("\nTop 3 results:")
for i, document_id in enumerate(results["ids"][0]):
    print(f"{i + 1}. {document_id}")