
from sentence_transformers import SentenceTransformer
from chunking import load_documents, create_chunks


# Load the embedding model
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def generate_embeddings(chunks):

    # Extract text from all chunks
    texts = [chunk["text"] for chunk in chunks]

    # Generate embeddings in batches
    embeddings = model.encode(
        texts,
        batch_size=16,
        show_progress_bar=True,
        normalize_embeddings=True
    )

    return embeddings


if __name__ == "__main__":

    # Load PDF documents
    documents = load_documents()

    # Divide documents into chunks
    chunks = create_chunks(documents)

    # Generate embeddings
    embeddings = generate_embeddings(chunks)

    print("\nEMBEDDING GENERATION COMPLETED")

    print("Total chunks:", len(chunks))
    print("Total embeddings:", len(embeddings))
    print("Vector dimensions:", embeddings.shape[1])

    print("\nFirst embedding:")
    print(embeddings[0])
