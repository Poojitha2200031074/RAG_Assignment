
import chromadb
from pathlib import Path

from ingest import load_documents
from chunking import create_chunks
from embeddings import generate_embeddings


# Project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Persistent database location
DB_PATH = BASE_DIR / "vectorstore"


# Initialize ChromaDB
client = chromadb.PersistentClient(
    path=str(DB_PATH)
)

COLLECTION_NAME = "document_collection"


def store_embeddings(chunks, embeddings):

    # Rebuild collection when indexing again
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )

    # Prepare data
    ids = [f"chunk_{i}" for i in range(len(chunks))]

    texts = [chunk["text"] for chunk in chunks]

    metadatas = [
        {
            "source": chunk["source"],
            "page": chunk["page"]
        }
        for chunk in chunks
    ]

    # Store in batches
    batch_size = 100

    for start in range(0, len(chunks), batch_size):

        end = start + batch_size

        collection.add(
            ids=ids[start:end],
            documents=texts[start:end],
            metadatas=metadatas[start:end],
            embeddings=embeddings[start:end].tolist()
        )

    print("\nEmbeddings stored successfully!")
    print("Total records:", collection.count())


if __name__ == "__main__":

    # Step 1: Load PDF documents
    documents = load_documents()

    # Step 2: Create chunks
    chunks = create_chunks(documents)

    # Step 3: Generate embeddings
    embeddings = generate_embeddings(chunks)

    # Step 4: Store embeddings
    store_embeddings(chunks, embeddings)
