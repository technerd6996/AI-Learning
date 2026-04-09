### Main screen Page without Connecting to Groq

import streamlit as st
import os
import chromadb
from groq import Groq
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Page config
st.set_page_config(
    page_title="SRE Assistant",
    page_icon="🔧"
)

st.title("🔧 SRE Knowledge Assistant")
st.caption("Powered by RAG + LangChain + ChromaDB")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask your SRE question..."):
    # Show user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Add to history
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })
    
    # Placeholder response for now
    response = "RAG pipeline will go here..."
    
    with st.chat_message("assistant"):
        st.markdown(response)
    
    st.session_state.messages.append({
        "role": "assistant", 
        "content": response
    })