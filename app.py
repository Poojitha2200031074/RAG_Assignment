
import streamlit as st
import sys
from pathlib import Path

# Add src folder to Python path
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from query import retrieve_documents
from generation import generate_answer

# Page configuration
st.set_page_config(
    page_title="RAG PDF Chatbot",
    page_icon="📚"
)

st.title("📚 RAG PDF Chatbot")
st.write("Ask questions based on your PDF documents.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display all previous questions and answers
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])

        # Display sources for previous assistant answers
        if message["role"] == "assistant" and "sources" in message:
            with st.expander("View Sources"):
                for source in message["sources"]:
                    st.write(
                        f"📄 {source['source']} | Page {source['page']}"
                    )

# Get a new question
question = st.chat_input("Ask something about your PDFs...")

if question:

    # Display and save user question
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.write(question)

    # Generate assistant response
    with st.chat_message("assistant"):

        with st.spinner("Searching documents and generating answer..."):

            try:
                results = retrieve_documents(question, top_k=5)

                if not results:
                    answer = "I could not find this information in the provided documents."
                else:
                    answer = generate_answer(question, results)

                st.write(answer)

                # Save answer and sources
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": results
                })

                with st.expander("View Sources"):
                    for source in results:
                        st.write(
                            f"📄 {source['source']} | Page {source['page']}"
                        )

            except Exception as e:
                error_message = f"Something went wrong: {e}"
                st.error(error_message)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_message
                })
