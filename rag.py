from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb

# Step 1 — Load the document

loader = TextLoader("sre_notes.txt")
documents = loader.load()  

#Step 2 - Split the document

splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=50
)

chunks = splitter.split_documents(documents)

#print(f"Total chunks: {len(chunks)}")
#print(f"\nSecond chunk:\n{chunks[1].page_content}")
#print(f"Loaded {len(documents)} document")
#print(f"Total characters: {len(documents[0].page_content)}")


# Step 3 — Store chunks in ChromaDB
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="sre_knowledge")

# Add chunks to the collection
for i, chunk in enumerate(chunks):
    collection.add(
        documents=[chunk.page_content],
        ids=[f"chunk_{i}"]
    )

# print(f"\nStored {collection.count()} chunks in ChromaDB")

# Step 4 - Search ChromaDB

query = "how do I fix high CPU on Linux Server?"

results = collection.query(
    query_texts=[query],
    n_results=2
)

print(f"\nQuery: {query}")
print(f"\nTop Results:")
for doc in results["documents"][0]:
    print(f"\n---\n{doc}")