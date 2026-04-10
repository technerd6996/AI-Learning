import chromadb
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

files = ["sre_notes.txt", "SRE_Google.txt", "SRE_Google_10.txt", "SRE_Google_20.txt", "SRE_Google_30.txt"]
all_chunks = []

splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500,
            chunk_overlap=150
        )

for file in files:
    loader = TextLoader(file)
    documents = loader.load()
    chunks = splitter.split_documents(documents)
    all_chunks.extend(chunks)
    
# Store in ChromaDB
chroma_client = chromadb.PersistentClient(path="./DB")
collection = chroma_client.get_or_create_collection(name="SRE_Knowledge_Base")

for i, chunk in enumerate(all_chunks):
    collection.add(
    documents=[chunk.page_content],
    ids=[f"chunk_{i}"]
            )
    
print(f"✅ Done! {collection.count()} chunks stored in ./DB")