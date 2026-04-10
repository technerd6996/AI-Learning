### Main screen Page after Connecting to Groq

import streamlit as st
import os
import chromadb
from groq import Groq
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Page config


# --- UI Layout: Top Header ---

# Create two columns. The ratio [3, 1] keeps the selector small on the right.

col1, col2 = st.columns([3, 1])

with col1:
    st.title("🔧 SRE Assistant")
    st.caption("RAG-powered Knowledge Base")

with col2:
    # This acts as your "Top Right" toggle

    expertise_level = st.selectbox(
        "Level of Expertise",
        options=["Level 1: Beginner", "Level 2: Intermediate", "Level 3: Advanced", "Level 4: Expert"],
        index=1,
        help="Adjusts the technical depth of the response."
    )

# --- Logic: Map Level to Persona (Same as before) ---

level_instructions = {
    "Level 1: Beginner": "Explain in layman's terms with analogies. No jargon.",
    "Level 2: Intermediate": "Use standard IT terms. Clear and instructional.",
    "Level 3: Advanced": "Technical depth for engineers. Focus on SRE metrics and tools.",
    "Level 4: Expert": "Deep dive into architecture, edge cases, and complex trade-offs."
}
current_persona_instruction = level_instructions[expertise_level]

st.divider() # Optional: Adds a clean line between the header and the chat


# Initialize RAG pipeline once

if "collection" not in st.session_state:
    with st.spinner("⚙️ Loading SRE Knowledge Base... (this may take 10-15 mins on cold start)"):

        # Load documents

        files = ["sre_notes.txt", "SRE_Google.txt", "SRE_Google_10.txt", "SRE_Google_20.txt", "SRE_Google_30.txt"]
        all_chunks = []
        
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=4500,
            chunk_overlap=50
        )
        
        for file in files:
            loader = TextLoader(file)
            documents = loader.load()
            chunks = splitter.split_documents(documents)
            all_chunks.extend(chunks)
        
        # Store in ChromaDB

        chroma_client = chromadb.Client()
        collection = chroma_client.get_or_create_collection(name="sre_knowledge")
        
        for i, chunk in enumerate(all_chunks):
            collection.add(
                documents=[chunk.page_content],
                ids=[f"chunk_{i}"]
            )
        
        st.session_state.collection = collection
        st.session_state.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# Always update system message when expertise changes

system_message = {
    "role": "system",
    "content": f"You are SRE Expert Engineer and I have given you data to answer questions. If you don't find anything respond with 'my knowledge is limited'. Be ethical and professional. {current_persona_instruction}"
}

if "messages" not in st.session_state:
    st.session_state.messages = [system_message]
else:
    # Update system message if expertise level changed

    st.session_state.messages[0] = system_message

# Display chat history - skip system message

for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input

if prompt := st.chat_input("Ask your SRE question..."):
    # Show user message

    with st.chat_message("user"):
        st.markdown(prompt)

    # Retrieve from ChromaDB

    results = st.session_state.collection.query(
        query_texts=[prompt],
        n_results=2
    )
    context = "\n".join(results["documents"][0])

    # Augment prompt

    augmented_prompt = f"""
Use this context to answer the question:

Context:
{context}

Question: {prompt}
"""

    # Add to history

    st.session_state.messages.append({
        "role": "user",
        "content": augmented_prompt
    })

    # Generate response

    with st.spinner("Thinking..."):
        response = st.session_state.groq_client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=st.session_state.messages
        )
        answer = response.choices[0].message.content

    # Display and save response

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })