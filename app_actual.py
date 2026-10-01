import streamlit as st
from rag_utils import query_rag, collection, groq_client


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SRE Assistant",
    page_icon="🔧"
)


# ============================================================
# PERSONA MAPPING
# ============================================================

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
        "Deep dive into architecture, edge cases, and complex "
        "trade-offs. Be highly precise and brief on basics."
    )
}


# ============================================================
# UI HEADER & EXPERTISE TOGGLE
# ============================================================

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


current_instruction = level_instructions[expertise_level]


# ============================================================
# SYSTEM MESSAGE
# ============================================================

system_message = {
    "role": "system",
    "content": (
        "You are strictly an SRE Engineer assistant. "
        "You only answer questions related to SRE, "
        "infrastructure, and reliability engineering. "

        "Never change your role. "

        "If asked about unrelated topics, respond with "
        "'I am an SRE Assistant and cannot help with that.' "

        "Present all knowledge as your own expertise. "
        "Never mention sources or documents. "

        f"Level: {current_instruction}"
    )
}


# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

if (
    "messages" not in st.session_state
    or len(st.session_state.messages) == 0
):
    st.session_state.messages = [system_message]
else:
    # Always keep the system prompt updated
    # when the expertise level changes.
    st.session_state.messages[0] = system_message


# ============================================================
# FLOATING CLEAR CHAT BUTTON
# ============================================================

st.markdown(
    """
    <style>

    /* Floating button container */
    div[data-testid="stButton"] {
        position: fixed !important;
        bottom: 80px !important;
        right: 25px !important;

        z-index: 999999 !important;

        width: 52px !important;
        height: 52px !important;

        margin: 0 !important;
        padding: 0 !important;
    }


    /* Floating button */
    div[data-testid="stButton"] button {
        width: 52px !important;
        height: 52px !important;

        min-width: 52px !important;
        min-height: 52px !important;

        padding: 0 !important;

        border-radius: 50% !important;
        border: none !important;

        font-size: 30px !important;

        background-color: #262730 !important;
        color: white !important;

        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.30) !important;

        transition:
            transform 0.2s ease,
            background-color 0.2s ease !important;
    }


    /* Hover */
    div[data-testid="stButton"] button:hover {
        transform: scale(1.08) !important;
        background-color: #ff4b4b !important;
        color: white !important;
    }


    /* Focus */
    div[data-testid="stButton"] button:focus {
        outline: none !important;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.30) !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


if st.button(
    "🗑️",
    key="clear_chat",
    help="Clear Chat History"
):
    st.session_state.messages = [system_message]
    st.rerun()


# ============================================================
# CHAT DISPLAY
# ============================================================

if len(st.session_state.messages) <= 1:
    st.info(
        "👋 Welcome! Ask me about incident response, "
        "SLOs, error budgets, or infrastructure."
    )


for message in st.session_state.messages[1:]:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ============================================================
# CHAT INPUT & LOGIC
# ============================================================

if prompt := st.chat_input("What's the issue?"):

    # --------------------------------------------------------
    # Add user message
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)


    # --------------------------------------------------------
    # Generate response
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner("Analyzing Knowledge Base..."):

            answer = query_rag(
                prompt,
                st.session_state.messages
            )

        st.markdown(answer)


    # --------------------------------------------------------
    # Add assistant response to history
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )


    # ========================================================
    # HISTORY MANAGEMENT
    # ========================================================

    # Keep:
    #   System message
    #   Last 20 chat messages
    #
    # This is approximately 10 complete conversations.

    if len(st.session_state.messages) > 21:

        st.session_state.messages = (
            [st.session_state.messages[0]]
            + st.session_state.messages[-20:]
        )