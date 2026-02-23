import streamlit as st
import requests
import base64
import json
import os

API_URL = "http://localhost:8000/api/v1/chat"
RESUME_PATH = "data/Hargurjeet_Lead_GenAI_Specialist.pdf"

st.set_page_config(
    page_title="Hargurjeet · AI Assistant",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CUSTOM CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background-color: #0f0f0f;
    color: #e8e8e8;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: #141414;
    border-right: 1px solid #222;
}

[data-testid="stSidebar"] * {
    color: #e8e8e8 !important;
}

/* ── Hide default header ── */
#MainMenu, header, footer { visibility: hidden; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background-color: #1a1a1a;
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
    border: 1px solid #2a2a2a;
}

.stTabs [data-baseweb="tab"] {
    background-color: transparent;
    color: #888 !important;
    border-radius: 8px;
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    font-size: 14px;
    padding: 8px 20px;
    transition: all 0.2s ease;
}

.stTabs [aria-selected="true"] {
    background-color: #ff5733 !important;
    color: #fff !important;
}

/* ── Chat container ── */
[data-testid="stVerticalBlock"] > div:has(.stContainer) > div {
    border-radius: 16px;
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background-color: #1a1a1a !important;
    border: 1px solid #252525;
    border-radius: 14px !important;
    padding: 14px 18px !important;
    margin-bottom: 8px;
}

[data-testid="stChatMessage"] p {
    font-size: 15px;
    line-height: 1.7;
    color: #e0e0e0;
}

/* ── Chat input ── */
[data-testid="stChatInput"] {
    background-color: #1a1a1a !important;
    border: 1px solid #333 !important;
    border-radius: 14px !important;
    color: #e8e8e8 !important;
}

[data-testid="stChatInput"]:focus-within {
    border-color: #ff5733 !important;
    box-shadow: 0 0 0 2px rgba(255, 87, 51, 0.15) !important;
}

/* ── Expander (Sources) ── */
[data-testid="stExpander"] {
    background-color: #161616 !important;
    border: 1px solid #252525 !important;
    border-radius: 10px !important;
}

[data-testid="stExpander"] summary {
    font-size: 13px !important;
    color: #888 !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* ── Suggestion buttons ── */
div[data-testid="stHorizontalBlock"] .stButton > button {
    background-color: #1a1a1a !important;
    color: #888 !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 20px !important;
    font-size: 13px !important;
    padding: 8px 16px !important;
    font-weight: 400 !important;
    transition: all 0.2s ease;
}

div[data-testid="stHorizontalBlock"] .stButton > button:hover {
    background-color: #222 !important;
    color: #ff5733 !important;
    border-color: #ff5733 !important;
}

/* ── Buttons ── */
.stButton > button {
    background-color: transparent;
    color: #ff5733 !important;
    border: 1px solid #ff5733 !important;
    border-radius: 10px;
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    font-size: 13px;
    padding: 6px 16px;
    transition: all 0.2s ease;
    width: 100%;
}

.stButton > button:hover {
    background-color: #ff5733 !important;
    color: #fff !important;
}

.stDownloadButton > button {
    background-color: #ff5733 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px;
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    width: 100%;
    padding: 10px;
}

/* ── Divider ── */
hr {
    border-color: #222 !important;
    margin: 16px 0;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0f0f0f; }
::-webkit-scrollbar-thumb { background: #333; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #ff5733; }

/* ── Spinner ── */
[data-testid="stSpinner"] { color: #ff5733 !important; }

/* ── Caption / small text ── */
.stCaption, [data-testid="stCaptionContainer"] {
    color: #555 !important;
    font-size: 13px !important;
}
</style>
""", unsafe_allow_html=True)


# ── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    # Profile header
    st.markdown("""
    <div style="text-align: center; padding: 24px 0 16px 0;">
        <div style="
            width: 72px; height: 72px;
            background: linear-gradient(135deg, #ff5733, #ff8c42);
            border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            font-size: 28px;
            margin: 0 auto 14px auto;
            box-shadow: 0 4px 20px rgba(255,87,51,0.3);
        ">H</div>
        <div style="font-family: 'DM Serif Display', serif; font-size: 20px; color: #f0f0f0; margin-bottom: 4px;">
            Hargurjeet Singh
        </div>
        <div style="font-size: 12px; color: #ff5733; font-weight: 500; letter-spacing: 1.5px; text-transform: uppercase;">
            Lead GenAI Specialist
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Quick links
    st.markdown("""
    <div style="padding: 0 4px;">
        <div style="font-size: 11px; color: #555; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 12px; font-weight: 600;">Connect</div>
        <a href="https://www.linkedin.com/in/hargurjeet/" target="_blank" style="
            display: flex; align-items: center; gap: 10px;
            color: #aaa; text-decoration: none; font-size: 14px;
            padding: 8px 10px; border-radius: 8px;
            transition: background 0.2s;
            margin-bottom: 4px;
        " onmouseover="this.style.background='#222'" onmouseout="this.style.background='transparent'">
            🔗 &nbsp;LinkedIn
        </a>
        <a href="https://github.com/hargurjeet" target="_blank" style="
            display: flex; align-items: center; gap: 10px;
            color: #aaa; text-decoration: none; font-size: 14px;
            padding: 8px 10px; border-radius: 8px;
            margin-bottom: 4px;
        " onmouseover="this.style.background='#222'" onmouseout="this.style.background='transparent'">
            🐙 &nbsp;GitHub
        </a>
        <a href="mailto:gurjeet333@gmail.com" style="
            display: flex; align-items: center; gap: 10px;
            color: #aaa; text-decoration: none; font-size: 14px;
            padding: 8px 10px; border-radius: 8px;
        " onmouseover="this.style.background='#222'" onmouseout="this.style.background='transparent'">
            ✉️ &nbsp;Email
        </a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Stats
    st.markdown("""
    <div style="padding: 0 4px;">
        <div style="font-size: 11px; color: #555; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 12px; font-weight: 600;">Quick Facts</div>
        <div style="display: flex; flex-direction: column; gap: 10px;">
            <div style="display: flex; justify-content: space-between; font-size: 13px;">
                <span style="color: #777;">Experience</span>
                <span style="color: #ff5733; font-weight: 600;">15+ years</span>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 13px;">
                <span style="color: #777;">Speciality</span>
                <span style="color: #ff5733; font-weight: 600;">GenAI / ML</span>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 13px;">
                <span style="color: #777;">Cloud</span>
                <span style="color: #ff5733; font-weight: 600;">AWS · GCP</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Clear chat button
    if st.button("🗑️  Clear Conversation"):
        st.session_state.messages = []
        st.session_state.sources = {}
        st.rerun()

    st.markdown("""
    <div style="text-align: center; margin-top: 16px; font-size: 11px; color: #333;">
        Powered by GPT-4o-mini · LangChain · FAISS
    </div>
    """, unsafe_allow_html=True)


# ── PAGE HEADER ────────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding: 32px 0 20px 0;">
    <div style="font-family: 'DM Serif Display', serif; font-size: 36px; color: #f0f0f0; line-height: 1.1;">
        Ask me anything
    </div>
    <div style="font-size: 15px; color: #555; margin-top: 6px;">
        about Hargurjeet's experience, skills, and background
    </div>
</div>
""", unsafe_allow_html=True)

# ── TABS ───────────────────────────────────────────────────────────────────────
chat_tab, resume_tab = st.tabs(["💬  Chat", "📄  Resume"])


# ── TAB 1: CHAT ────────────────────────────────────────────────────────────────
with chat_tab:

    # Initialise session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "sources" not in st.session_state:
        st.session_state.sources = {}
    if "preset_question" not in st.session_state:
        st.session_state.preset_question = None

    def build_chat_history():
        history = []
        msgs = st.session_state.messages
        for i in range(0, len(msgs) - 1, 2):
            if msgs[i]["role"] == "user" and msgs[i + 1]["role"] == "assistant":
                history.append([msgs[i]["content"], msgs[i + 1]["content"]])
        return history

    # Scrollable chat container
    chat_container = st.container(height=520)
    with chat_container:
        if not st.session_state.messages:
            st.markdown("""
            <div style="
                display: flex; flex-direction: column;
                align-items: center; justify-content: center;
                height: 280px; gap: 12px;
            ">
                <div style="font-size: 40px;">⚡</div>
                <div style="font-family: 'DM Serif Display', serif; font-size: 22px; color: #444;">
                    Start a conversation
                </div>
                <div style="font-size: 13px; color: #333; text-align: center; max-width: 320px; line-height: 1.6;">
                    Click a suggestion below or type your own question
                </div>
            </div>
            """, unsafe_allow_html=True)

        for i, msg in enumerate(st.session_state.messages):
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                if msg["role"] == "assistant" and i in st.session_state.sources:
                    with st.expander("📎 Sources"):
                        for j, src in enumerate(st.session_state.sources[i]):
                            st.markdown(f"`[{j+1}]` {src['source']} — page {src['page']}")

    # ── Suggestion buttons (only shown when no messages yet) ──
    if not st.session_state.messages:
        suggestions = [
            "What's his GenAI experience?",
            "What cloud platforms has he used?",
            "What's his most recent role?",
        ]
        cols = st.columns(len(suggestions))
        for col, suggestion in zip(cols, suggestions):
            with col:
                if st.button(suggestion, use_container_width=True):
                    st.session_state.preset_question = suggestion
                    st.rerun()

    # ── Chat input — also handles preset questions from suggestion buttons ──
    user_input = st.chat_input("Ask anything about Hargurjeet...")

    # Pick up either typed input or button-triggered preset
    question = user_input or st.session_state.pop("preset_question", None)

    if question:

        chat_history = build_chat_history()
        st.session_state.messages.append({"role": "user", "content": question})

        try:
            with requests.post(
                API_URL,
                json={"question": question, "chat_history": chat_history},
                stream=True
            ) as response:
                response.raise_for_status()

                full_answer = ""
                sources = []

                with chat_container:
                    with st.chat_message("assistant"):
                        token_placeholder = st.empty()

                        for line in response.iter_lines():
                            if not line:
                                continue
                            line = line.decode("utf-8")
                            if not line.startswith("data: "):
                                continue
                            payload = line[len("data: "):]
                            if payload == "[DONE]":
                                break

                            data = json.loads(payload)

                            if "token" in data:
                                full_answer += data["token"]
                                token_placeholder.markdown(full_answer + "▌")

                            if "sources" in data:
                                sources = data["sources"]

                        token_placeholder.markdown(full_answer)

                        if sources:
                            with st.expander("📎 Sources"):
                                for j, src in enumerate(sources):
                                    st.markdown(f"`[{j+1}]` {src['source']} — page {src['page']}")

                assistant_idx = len(st.session_state.messages)
                st.session_state.messages.append({"role": "assistant", "content": full_answer})
                st.session_state.sources[assistant_idx] = sources

        except requests.exceptions.ConnectionError:
            st.session_state.messages.append({
                "role": "assistant",
                "content": "⚠️ Could not connect to the API. Make sure FastAPI is running on port 8000."
            })
        except Exception as e:
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"⚠️ Something went wrong: {str(e)}"
            })

        st.rerun()


# ── TAB 2: RESUME ──────────────────────────────────────────────────────────────
with resume_tab:
    if os.path.exists(RESUME_PATH):
        with open(RESUME_PATH, "rb") as f:
            pdf_bytes = f.read()

        base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
        st.markdown(f"""
            <iframe
                src="data:application/pdf;base64,{base64_pdf}"
                width="100%"
                height="900px"
                style="border: none; border-radius: 12px; margin-top: 12px;">
            </iframe>
        """, unsafe_allow_html=True)

        st.download_button(
            label="⬇️  Download Resume",
            data=pdf_bytes,
            file_name="Hargurjeet_Lead_GenAI_Specialist.pdf",
            mime="application/pdf"
        )
    else:
        st.error(f"⚠️ Resume not found at `{RESUME_PATH}`.")