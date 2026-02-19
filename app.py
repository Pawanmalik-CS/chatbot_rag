import streamlit as st
import time
import requests

# ─── Page Config ───────────────────────────────────────────────
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# ─── Custom CSS (Dark Theme) ────────────────────────────────────
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }

    section[data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }

    .stChatInput input {
        background-color: #161b22 !important;
        color: #ffffff !important;
        border: 1px solid #30363d !important;
        border-radius: 12px !important;
    }

    .user-bubble {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white;
        padding: 12px 18px;
        border-radius: 18px 18px 4px 18px;
        margin: 6px 0;
        max-width: 75%;
        float: right;
        clear: both;
        font-size: 15px;
        box-shadow: 0 4px 12px rgba(99,102,241,0.3);
    }

    .bot-bubble {
        background: linear-gradient(135deg, #1f2937, #374151);
        color: #e5e7eb;
        padding: 12px 18px;
        border-radius: 18px 18px 18px 4px;
        margin: 6px 0;
        max-width: 75%;
        float: left;
        clear: both;
        font-size: 15px;
        border: 1px solid #30363d;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }

    .avatar {
        font-size: 24px;
        margin: 4px;
    }

    .message-row-user {
        display: flex;
        justify-content: flex-end;
        align-items: flex-end;
        gap: 8px;
        margin: 8px 0;
        clear: both;
    }

    .message-row-bot {
        display: flex;
        justify-content: flex-start;
        align-items: flex-end;
        gap: 8px;
        margin: 8px 0;
        clear: both;
    }

    .history-item {
        background-color: #21262d;
        border-radius: 8px;
        padding: 8px 12px;
        margin: 4px 0;
        font-size: 13px;
        color: #8b949e;
        border-left: 3px solid #6366f1;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    .stButton > button {
        background: linear-gradient(135deg, #ef4444, #dc2626);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 8px 20px;
        font-weight: bold;
        width: 100%;
        transition: 0.3s;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #dc2626, #b91c1c);
        transform: scale(1.02);
    }

    h1 {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2rem !important;
    }

    hr {
        border-color: #30363d;
    }

    .stChatMessage {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }

    @keyframes bounce {
        from { transform: translateY(0px); opacity: 0.4; }
        to { transform: translateY(-8px); opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

# ─── Initialize Session State ───────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ─── Sidebar ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🤖 AI Chatbot")
    st.markdown("---")

    st.markdown("### 💬 Chat History")
    if st.session_state.messages:
        user_messages = [m for m in st.session_state.messages if m["role"] == "user"]
        if user_messages:
            for msg in user_messages[-10:]:
                st.markdown(f'<div class="history-item">💬 {msg["content"][:40]}...</div>', unsafe_allow_html=True)
        else:
            st.markdown("*No messages yet*")
    else:
        st.markdown("*No messages yet*")

    st.markdown("---")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("**Status:** 🟢 Online")

# ─── Main Chat Area ─────────────────────────────────────────────
st.markdown("# 🤖 AI Assistant")
st.markdown("*Your intelligent daily life companion*")
st.markdown("---")

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"""
        <div class="message-row-user">
            <div class="user-bubble">{message["content"]}</div>
            <div class="avatar">👤</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="message-row-bot">
            <div class="avatar">🤖</div>
            <div class="bot-bubble">{message["content"]}</div>
        </div>
        """, unsafe_allow_html=True)

# ─── Typing Animation ───────────────────────────────────────────
def typing_effect(response_text):
    placeholder = st.empty()
    displayed = ""
    for char in response_text:
        displayed += char
        placeholder.markdown(f"""
        <div class="message-row-bot">
            <div class="avatar">🤖</div>
            <div class="bot-bubble">{displayed}▌</div>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.02)
    placeholder.markdown(f"""
    <div class="message-row-bot">
        <div class="avatar">🤖</div>
        <div class="bot-bubble">{displayed}</div>
    </div>
    """, unsafe_allow_html=True)

# ─── Chat Input ─────────────────────────────────────────────────
if prompt := st.chat_input("Ask me anything..."):

    # Show user message
    st.markdown(f"""
    <div class="message-row-user">
        <div class="user-bubble">{prompt}</div>
        <div class="avatar">👤</div>
    </div>
    """, unsafe_allow_html=True)

    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    # ─── Thinking Animation ─────────────────────────────────────
    thinking_placeholder = st.empty()
    thinking_placeholder.markdown("""
    <div class="message-row-bot">
        <div class="avatar">🤖</div>
        <div class="bot-bubble">
            <span style="display:flex; align-items:center; gap:8px;">
                <span style="width:10px; height:10px; background:#6366f1;
                    border-radius:50%; display:inline-block;
                    animation: bounce 0.8s infinite alternate;"></span>
                <span style="width:10px; height:10px; background:#8b5cf6;
                    border-radius:50%; display:inline-block;
                    animation: bounce 0.8s 0.2s infinite alternate;"></span>
                <span style="width:10px; height:10px; background:#a78bfa;
                    border-radius:50%; display:inline-block;
                    animation: bounce 0.8s 0.4s infinite alternate;"></span>
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Call backend
    try:
        response = requests.post(
            "http://127.0.0.1:8000/chat",
            json={"message": prompt, "history": st.session_state.messages},timeout=30
        )
        bot_reply = response.json()["reply"]
    except:
        bot_reply = "⚠️ Could not connect to backend. Make sure FastAPI is running!"

    # Clear thinking animation
    thinking_placeholder.empty()

    # Show reply with typing effect
    typing_effect(bot_reply)

    # Save bot message
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})