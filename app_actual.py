### Main screen Page after Connecting to Groq

import streamlit as st
import os
import chromadb
from groq import Groq
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Page config
st.set_page_config(page_title="SRE Assistant", page_icon="🔧")
st.title("🔧 SRE Knowledge Assistant")
st.caption("Powered by RAG + LangChain + ChromaDB and Fueled by Laziness of an Engineer 😴")

# Initialize RAG pipeline once
if "collection" not in st.session_state:
    with st.spinner("⚙️ Loading SRE Knowledge Base... (this may take 10-15 mins on cold start)"):
        
        chroma_client = chromadb.PersistentClient(path="./DB")
        collection = chroma_client.get_or_create_collection(name="SRE_Knowledge_Base")
        
              
        st.session_state.collection = collection
        st.session_state.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "system",
        "content": "You are SRE Expert Engineer and i have given to the data from you need to answer the question. If you don't find anything respond with my knowledge is limited. Be ethical and professional while answering the question. While giving the answer be technically deep and not generic"
    }]

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