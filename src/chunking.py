
from ingest import load_documents


# Chunking configuration
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150


def create_chunks(documents):

    chunks = []

    for document in documents:

        text = document["text"]

        start = 0

        while start < len(text):

            end = start + CHUNK_SIZE

            chunk_text = text[start:end]

            if chunk_text.strip():

                chunks.append({
                    "text": chunk_text,
                    "source": document["source"],
                    "page": document["page"]
                })

            if end >= len(text):
                break

            start = end - CHUNK_OVERLAP

    return chunks


if __name__ == "__main__":

    # Load extracted PDF content
    documents = load_documents()

    # Create smaller text chunks
    chunks = create_chunks(documents)

    print("\nCHUNKING COMPLETED")
    print("Total pages:", len(documents))
    print("Total chunks:", len(chunks))

    # Display first three chunks
    for i, chunk in enumerate(chunks[:3]):

        print(f"\nChunk {i + 1}")
        print("Source:", chunk["source"])
        print("Page:", chunk["page"])
        print("Content:", chunk["text"][:150])
