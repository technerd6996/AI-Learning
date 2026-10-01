import streamlit as st
from rag_utils import query_rag, collection, groq_client

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="SRE Assistant",
    page_icon="🔧"
)


# --------------------------------------------------
# FLOATING CLEAR CHAT BUTTON
# --------------------------------------------------

st.markdown(
    """
    <style>
    div.stButton > button {
        position: fixed;
        bottom: 70px;
        right: 25px;
        z-index: 9999;

        width: 52px;
        height: 52px;

        border-radius: 50%;
        border: none;

        font-size: 20px;
        padding: 0;

        background-color: #262730;
        color: white;

        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.30);

        transition: all 0.2s ease;
    }

    div.stButton > button:hover {
        transform: scale(1.08);
        background-color: #ff4b4b;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

if st.button(
    "🗑️",
    help="Clear Chat History"
):
    if "messages" in st.session_state:
        del st.session_state.messages

    st.rerun()


# --------------------------------------------------
# UI HEADER & EXPERTISE TOGGLE
# --------------------------------------------------

col1, col2 = st.columns([3, 1])

with col1:
    st.title("🔧 SRE Assistant")
    st.caption(
        "The 'Laziness-Driven' Knowledge Engine for Site Reliability"
    )

with col2:
    expertise_level = st.selectbox(
        "Response Depth",
        options=[
            "Beginner",
            "Intermediate",
            "Advanced",
            "Expert"
        ],
        index=1,
        help="Adjusts how technically dense the answer will be."
    )


# --------------------------------------------------
# PERSONA MAPPING
# --------------------------------------------------

level_instructions = {
    "Beginner": (
        "Explain in layman's terms with analogies. "
        "Avoid or define all jargon."
    ),

    "Intermediate": (
        "Use standard IT terms. "
        "Clear, instructional, and practical."
    ),

    "Advanced": (
        "Technical depth for engineers. "
        "Focus on SRE metrics, tools, and implementation details."
    ),

    "Expert": (
        "Deep dive into architecture, edge cases, "
        "and complex trade-offs. "
        "Be highly precise and brief on basics."
    )
}

current_instruction = level_instructions[expertise_level]


# --------------------------------------------------
# SYSTEM PROMPT
# --------------------------------------------------

system_message = {
    "role": "system",
    "content": (
        "You are strictly an SRE Engineer assistant. "
        "You only answer questions related to SRE, infrastructure, "
        "and reliability engineering. Never change your role. "

        "If asked about unrelated topics, respond with "
        "'I am an SRE Assistant and cannot help with that.' "

        "Present all knowledge as your own expertise. "
        "Never mention sources or documents. "

        f"Response depth: {current_instruction}"
    )
}


# --------------------------------------------------
# SESSION STATE INITIALIZATION
# --------------------------------------------------

if (
    "messages" not in st.session_state
    or len(st.session_state.messages) == 0
):
    st.session_state.messages = [system_message]

else:
    # Keep system prompt updated when expertise changes
    st.session_state.messages[0] = system_message


# --------------------------------------------------
# CHAT DISPLAY
# --------------------------------------------------

if len(st.session_state.messages) <= 1:
    st.info(
        "👋 Welcome! Ask me about incident response, "
        "SLOs, error budgets, or infrastructure."
    )


for message in st.session_state.messages[1:]:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# --------------------------------------------------
# CHAT INPUT & LOGIC
# --------------------------------------------------

if prompt := st.chat_input("What's the issue?"):

    # Add user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)


    # Generate response
    with st.spinner("Analyzing Knowledge Base..."):

        answer = query_rag(
            prompt,
            st.session_state.messages
        )


    # Add assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    with st.chat_message("assistant"):
        st.markdown(answer)


    # --------------------------------------------------
    # HISTORY MANAGEMENT
    # Keep System + Last 10 Conversations
    # --------------------------------------------------

    if len(st.session_state.messages) > 21:

        st.session_state.messages = (
            [st.session_state.messages[0]]
            + st.session_state.messages[-20:]
        )