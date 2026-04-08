import os
import chromadb
from groq import Groq
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Setup
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("Error: GROQ_API_KEY not found.")
    exit()

client = Groq(api_key=api_key)

# Step 1 — Load and chunk documents
loader = TextLoader("sre_notes.txt")
documents = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=50
)
chunks = splitter.split_documents(documents)

# Step 2 — Store in ChromaDB
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="sre_knowledge")

for i, chunk in enumerate(chunks):
    collection.add(
        documents=[chunk.page_content],
        ids=[f"chunk_{i}"]
    )

print(f"✅ Loaded {len(chunks)} chunks into ChromaDB")

# Step 3 — RAG function
def ask_sre_assistant(question, history):
    # Retrieve relevant chunks
    results = collection.query(
        query_texts=[question],
        n_results=2
    )
    
    retrieved_chunks = results["documents"][0]
    context = "\n".join(retrieved_chunks)
    
    # Augment — add context to prompt
    augmented_question = f"""
Use this context to answer the question:

Context:
{context}

Question: {question}
"""
    
    # Add to history
    history.append({"role": "user", "content": augmented_question})
    
    # Generate
    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=history
    )
    
    answer = response.choices[0].message.content
    history.append({"role": "assistant", "content": answer})
    return answer

# Step 4 — Conversation loop
history = [{
    "role": "system",
    "content": "You are an expert SRE Engineer. Answer questions using the provided context. Be technical and concise."
}]

print("SRE Assistant ready. Type 'exit' to quit.\n")

while True:
    question = input("You: ")
    if question.lower() == "exit":
        break
    
    answer = ask_sre_assistant(question, history)
    print(f"\nAssistant: {answer}\n")