
# 📚 RAG-Based PDF Question Answering Chatbot

## 1. Project Overview

This project is a Retrieval-Augmented Generation (RAG) based PDF Question Answering Chatbot developed using Python.

It allows users to upload or provide PDF documents and ask questions about their content. The chatbot retrieves relevant information from the documents and generates answers using a locally running Large Language Model (LLM).

The application uses Streamlit for the user interface, ChromaDB for vector storage, Sentence Transformers for embeddings, and Ollama for local LLM-based answer generation.

## 2. Technologies and Libraries Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| PyMuPDF | Extracts text from PDF documents |
| Sentence Transformers | Generates text embeddings |
| all-MiniLM-L6-v2 | Embedding model |
| ChromaDB | Persistent vector database |
| Ollama | Runs the LLM locally |
| Llama 3.2 1B | Generates answers |
| Requests | Communicates with Ollama API |
| Streamlit | Creates the chatbot interface |

## 3. Project Architecture

The project follows a Retrieval-Augmented Generation workflow.

### Document Indexing Process

1. PDF documents are placed inside the `data/documents/` folder.
2. PyMuPDF extracts text from each PDF page.
3. Extracted text is divided into smaller chunks with overlap.
4. Sentence Transformers converts chunks into numerical embeddings.
5. ChromaDB stores the embeddings, text, and document metadata.

### Question Answering Process

1. The user enters a question through the Streamlit interface.
2. The question is converted into an embedding.
3. ChromaDB retrieves the most relevant document chunks.
4. The retrieved content is passed to the Ollama LLM.
5. The LLM generates an answer using the retrieved context.
6. The answer and source information are displayed in the chatbot.

## 4. Architecture and Design Decisions

### 4.1 Chunking Strategy

- Chunk size: 800 characters
- Chunk overlap: 150 characters

**Reason for selection:**

Documents are divided into smaller chunks to make information retrieval more effective.

An overlap of 150 characters helps preserve context between consecutive chunks and reduces the chance of losing information at chunk boundaries.

The chunk size can be adjusted based on document content and retrieval performance.

### 4.2 Embedding Model

**Selected model:** sentence-transformers/all-MiniLM-L6-v2

**Reason for selection:**

- Lightweight and suitable for CPU-based execution.
- Generates 384-dimensional embeddings.
- Supports semantic similarity search.
- Suitable for small document collections and resource-constrained systems.

The same embedding model is used for both document chunks and user questions to ensure consistent vector representations.

### 4.3 Vector Database

**Selected database:** ChromaDB

**Reason for selection:**

- Easy to integrate with Python.
- Supports vector similarity search.
- Provides persistent local storage.
- Stores document metadata along with embeddings.
- Suitable for a local document question-answering application.

ChromaDB is used to retrieve relevant document chunks based on the user's question.

### 4.4 LLM Selection

**Selected model:** Llama 3.2 1B through Ollama.

**Reason for selection:**

- Runs locally without requiring an external LLM API.
- Suitable for experimenting with local RAG applications.
- Avoids sending document content to an external LLM service.
- Uses fewer resources than larger language models, although response speed depends on available hardware.

### 4.5 Prompt Design

The prompt instructs the LLM to:

- Answer using the retrieved document context.
- Avoid adding unsupported information.
- Return a predefined response when the answer is unavailable.
- Mention source filenames and page numbers.

## 5. Project Folder Structure

```text
RAG_Q&A_BOT/
│
├── data/
│   └── documents/
│       ├── 01_Introduction_to_Artificial_Intelligence.pdf
│       ├── 02_Machine_Learning_Fundamentals.pdf
│       ├── 03_Generative_AI_Overview.pdf
│       ├── 04_Natural_Language_Processing.pdf
│       └── 05_Large_Language_Models.pdf
│
├── src/
│   ├── ingest.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── query.py
│   └── generation.py
│
├── vectorstore/
├── app.py
├── test_generation.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 6. Installation and Setup Instructions

### Prerequisites

Install the following before running the project:

- Python 3.11
- Visual Studio Code
- Git
- Ollama

### Step 1: Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd RAG-PDF-Chatbot
```

### Step 2: Create a Virtual Environment

```bash
python -m venv .venv
```

### Step 3: Activate the Virtual Environment

For Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 4: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Install and Configure Ollama

Download Ollama from:

https://ollama.com/download

Pull the required language model:

```bash
ollama pull llama3.2:1b
```

Verify the installed model:

```bash
ollama list
```

Make sure the model name matches the configuration in `src/generation.py`.

### Step 6: Add PDF Documents

Place the PDF documents inside:

```text
data/documents/
```

### Step 7: Build the Vector Database

Run the indexing script:

```bash
python src/vector_store.py
```

This process extracts document content, creates chunks, generates embeddings, and stores them in ChromaDB.

Run this step again when adding new PDFs or changing the chunking or embedding configuration.

### Step 8: Start the Chatbot

Run the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your web browser.

## 7. Example Questions

Users can ask questions such as:

- What is Artificial Intelligence?
- What is Machine Learning?
- Explain Generative AI.
- What is Natural Language Processing?
- What are Large Language Models?

The chatbot retrieves relevant content from the PDF documents and generates answers with source information.

## 8. Key Features

- PDF text extraction.
- Text chunking with overlap.
- Batch embedding generation.
- Persistent vector storage.
- Semantic document retrieval.
- Local LLM-based answer generation.
- Source filename and page metadata.
- Interactive Streamlit chatbot.
- Chat history during the current session.
- Responses grounded in retrieved document context.

## 9. Limitations

- Answer quality depends on the retrieved document content.
- Response speed depends on the computer's hardware and the selected LLM.
- Scanned PDFs may require OCR before text extraction.
- The chatbot currently works with the documents placed in the configured folder.
- Chat history is maintained during the current application session.

## 10. Future Improvements

- Support additional document formats.
- Improve retrieval accuracy using reranking.
- Add OCR support for scanned PDFs.
- Add persistent chat history.
- Improve response speed through streaming.
- Support multiple language models.

## 11. Author

**Avvaru Poojitha**

GitHub: YOUR_GITHUB_PROFILE_URL
