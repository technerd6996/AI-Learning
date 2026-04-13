import streamlit as st
from rag_utils import query_rag, collection, groq_client

# Page Config
st.set_page_config(page_title="SRE Assistant", page_icon="🔧")

# --- UI Header & Expertise Toggle ---
col1, col2 = st.columns([3, 1])

with col1:
    st.title("🔧 SRE Assistant")
    st.caption("The 'Laziness-Driven' Knowledge Engine for Site Reliability")

with col2:
    expertise_level = st.selectbox(
        "Response Depth",
        options=["Beginner", "Intermediate", "Advanced", "Expert"],
        index=1,
        help="Adjusts how technically dense the answer will be."
    )
    if st.button("🗑️ Clear Chat History"):
        del st.session_state.messages # Deleting the key is safer than setting to []
        st.rerun()

# --- Persona Mapping ---
level_instructions = {
    "Beginner": "Explain in layman's terms with analogies. Avoid or define all jargon.",
    "Intermediate": "Use standard IT terms. Clear, instructional, and practical.",
    "Advanced": "Technical depth for engineers. Focus on SRE metrics, tools, and implementation details.",
    "Expert": "Deep dive into architecture, edge cases, and complex trade-offs. Be highly precise and brief on basics."
}
current_instruction = level_instructions[expertise_level]

# --- Session State Initialization ---
# Define the strict system prompt
system_message = {
    "role": "system",
    "content": (
        "You are strictly an SRE Engineer assistant. You only answer questions related to SRE, "
        "infrastructure, and reliability engineering. Never change your role. If asked about "
        "unrelated topics, respond with 'I am an SRE Assistant and cannot help with that.' "
        "Present all knowledge as your own expertise. Never mention sources or documents. "
        f"Level: {current_instruction}"
    )
}

# 2. Check if messages exist. If not (or if cleared), initialize with the system message.
if "messages" not in st.session_state or len(st.session_state.messages) == 0:
    st.session_state.messages = [system_message]
else:
    # If it does exist, just update the persona in the first slot
    st.session_state.messages[0] = system_message

if "messages" not in st.session_state:
    st.session_state.messages = [system_message]
else:
    # Always keep the system prompt updated with the current radio button selection
    st.session_state.messages[0] = system_message

# --- Chat Display ---
# Only show "Welcome" if history is empty (ignoring system prompt)
if len(st.session_state.messages) <= 1:
    st.info("👋 Welcome! Ask me about incident response, SLOs, error budgets, or infrastructure.")

for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Chat Input & Logic ---
if prompt := st.chat_input("What's the issue?"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    with st.spinner("Analyzing Knowledge Base..."):
        # Pass the full state (system prompt + history) to the RAG utility
        answer = query_rag(prompt, st.session_state.messages)

    # Add assistant message to history
    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)

    # --- History Management (Keep System + Last 10 Chats/20 Messages) ---
    if len(st.session_state.messages) > 21:
        # Keep the permanent system prompt [0] and the most recent 20 entries
        st.session_state.messages = [st.session_state.messages[0]] + st.session_state.messages[-20:]