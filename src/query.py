
import chromadb
from pathlib import Path

from sentence_transformers import SentenceTransformer


# Project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Database location
DB_PATH = BASE_DIR / "vectorstore"

# Embedding model
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


# Connect to ChromaDB
client = chromadb.PersistentClient(
    path=str(DB_PATH)
)

collection = client.get_collection(
    name="document_collection"
)


def retrieve_documents(question, top_k=3):

    # Convert question into embedding
    question_embedding = model.encode(
        [question],
        normalize_embeddings=True
    )

    # Search relevant chunks
    results = collection.query(
        query_embeddings=question_embedding.tolist(),
        n_results=min(top_k, collection.count())
    )

    retrieved_chunks = []

    for i in range(len(results["documents"][0])):

        retrieved_chunks.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "page": results["metadatas"][0][i]["page"]
        })

    return retrieved_chunks


if __name__ == "__main__":

    question = input("\nEnter your question: ")

    results = retrieve_documents(question)

    print("\nRETRIEVED DOCUMENTS")

    for i, result in enumerate(results):

        print(f"\nResult {i + 1}")

        print("Source:", result["source"])
        print("Page:", result["page"])

        print("Content:")
        print(result["text"])
