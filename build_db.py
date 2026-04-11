import chromadb
import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

PROCESSED_FILES = "processed_files.txt"

files = ["sre_notes.txt", "SRE_Google.txt", "SRE_Google_10.txt", 
         "SRE_Google_20.txt", "SRE_Google_30.txt", 
         "SRE_Intro.txt", "SRE_DevOps.txt"]

# Step 1 — Read already processed files
if os.path.exists(PROCESSED_FILES):
    with open(PROCESSED_FILES, "r") as f:
        processed = f.read().splitlines()
else:
    processed = []

# Step 2 — Filter only new files
new_files = []
for file in files:
    if file not in processed:
        new_files.append(file)

if not new_files:
    print("✅ No new files to process.")
    exit()

print(f"📂 Processing {len(new_files)} new files: {new_files}")

# Step 3 — Chunk new files
all_chunks = []
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=150
)

for file in new_files:
    loader = TextLoader(file, encoding="utf-8")
    documents = loader.load()
    chunks = splitter.split_documents(documents)
    all_chunks.extend(chunks)
    print(f"  ✅ Loaded {len(chunks)} chunks from {file}")

# Step 4 — Add to existing ChromaDB
chroma_client = chromadb.PersistentClient(path="./DB")
collection = chroma_client.get_or_create_collection(name="SRE_Knowledge_Base")

for i, chunk in enumerate(all_chunks):
    chunk_id = f"{chunk.metadata['source'].replace('.txt', '')}_chunk_{i}"
    collection.add(
        documents=[chunk.page_content],
        ids=[chunk_id]
    )

# Step 5 — Update processed files list
with open(PROCESSED_FILES, "a") as f:
    for file in new_files:
        f.write(file + "\n")

print(f"✅ Done! {collection.count()} total chunks in DB")