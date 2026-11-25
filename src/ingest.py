
import fitz
from pathlib import Path

# Get the project folder
BASE_DIR = Path(__file__).resolve().parent.parent

# PDF documents folder
DOCUMENTS_DIR = BASE_DIR / "data" / "documents"


def load_documents():

    documents = []

    # Read all PDF files
    pdf_files = list(DOCUMENTS_DIR.glob("*.pdf"))

    if not pdf_files:
        print("No PDF documents found!")
        return documents

    for pdf_file in pdf_files:

        print(f"\nReading: {pdf_file.name}")

        pdf = fitz.open(pdf_file)

        for page_number, page in enumerate(pdf):

            text = page.get_text("text").strip()

            if text:
                documents.append({
                    "text": text,
                    "source": pdf_file.name,
                    "page": page_number + 1
                })

        pdf.close()

    return documents


if __name__ == "__main__":

    documents = load_documents()

    print("\nPDF EXTRACTION COMPLETED")
    print("Total pages extracted:", len(documents))

    for document in documents[:2]:
        print("\nSource:", document["source"])
        print("Page:", document["page"])
        print("Text preview:", document["text"][:300])
