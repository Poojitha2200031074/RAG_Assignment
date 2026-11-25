from src.query import retrieve_documents
from src.generation import generate_answer

question = input("Enter your question: ")

# Retrieve relevant PDF chunks
results = retrieve_documents(question, top_k=3)

# Generate an answer using Ollama
answer = generate_answer(question, results)

print("\nANSWER:")
print(answer)