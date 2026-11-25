
import requests

# Ollama model name
MODEL_NAME = "llama3.2:1b"

# Ollama API URL
OLLAMA_URL = "http://localhost:11434/api/generate"


def generate_answer(question, retrieved_chunks):

    # Check whether any PDF content was retrieved
    if not retrieved_chunks:
        return "I could not find this information in the provided documents."

    # Prepare context from retrieved PDF chunks
    context = ""

    for chunk in retrieved_chunks:
        context += f"""
Source: {chunk['source']}
Page: {chunk['page']}

Content:
{chunk['text']}

-------------------------
"""

    # Create a prompt for the LLM
    prompt = f"""
You are a helpful PDF question-answering assistant.

Your task is to answer the user's question using ONLY the
information provided in the document context below.

Follow these instructions carefully:

1. Read all the provided context carefully.
2. Identify information that directly answers the question.
3. Give a clear and simple answer.
4. Do not say information is missing if the context contains the answer.
5. Do not use your own outside knowledge.
6. If the answer is genuinely not available in the context,
   say exactly:
   "I could not find this information in the provided documents."
7. Mention the source filename and page number used for the answer.

DOCUMENT CONTEXT:
{context}

USER QUESTION:
{question}

ANSWER:
"""

    try:
        # Send the prompt to the local Ollama model
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1
                }
            },
            timeout=180
        )

        # Check for API errors
        response.raise_for_status()

        # Extract the generated answer
        result = response.json()

        answer = result.get("response", "").strip()

        if not answer:
            return "The model did not generate an answer. Please try again."

        return answer

    except requests.exceptions.ConnectionError:
        return (
            "Could not connect to Ollama. "
            "Please make sure Ollama is running."
        )

    except requests.exceptions.Timeout:
        return "Ollama took too long to respond. Please try again."

    except requests.exceptions.RequestException as error:
        return f"Error communicating with Ollama: {error}"


if __name__ == "__main__":
    print("Generation module is ready.")
