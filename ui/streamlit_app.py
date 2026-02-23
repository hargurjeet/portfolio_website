import streamlit as st
import requests
import base64
import os

API_URL = "http://localhost:8000/api/v1/chat"
RESUME_PATH = "data/Hargurjeet_Lead_GenAI_Specialist.pdf"

st.set_page_config(page_title="RAG Chatbot", page_icon="🤖", layout="wide")
st.title("🤖 Hargurjeet's AI Assistant")

# ── TABS ───────────────────────────────────────────────────────────────────────
chat_tab, resume_tab = st.tabs(["💬 Chat", "📄 Resume"])


# ── TAB 1: CHAT ────────────────────────────────────────────────────────────────
with chat_tab:
    st.caption("Ask anything about Hargurjeet's experience and background")

    # Initialise session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "sources" not in st.session_state:
        st.session_state.sources = {}

    # ── Build (human, ai) tuple history to send to the API ──
    def build_chat_history():
        history = []
        msgs = st.session_state.messages
        for i in range(0, len(msgs) - 1, 2):
            if msgs[i]["role"] == "user" and msgs[i + 1]["role"] == "assistant":
                history.append([msgs[i]["content"], msgs[i + 1]["content"]])
        return history

    # ── Scrollable chat history container (fixed height, always visible) ──
    chat_container = st.container(height=550)
    with chat_container:
        if not st.session_state.messages:
            st.markdown(
                "<div style='text-align:center; color:gray; margin-top: 200px;'>"
                "👋 Ask me anything about Hargurjeet's experience!"
                "</div>",
                unsafe_allow_html=True
            )
        for i, msg in enumerate(st.session_state.messages):
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                if msg["role"] == "assistant" and i in st.session_state.sources:
                    with st.expander("📄 Sources"):
                        for j, src in enumerate(st.session_state.sources[i]):
                            st.write(f"**[{j+1}]** {src['source']} — page {src['page']}")

    # ── Chat input always anchored below the container ──
    if question := st.chat_input("Ask a question..."):

        # Build history BEFORE appending the new question so pairing stays correct
        chat_history = build_chat_history()

        st.session_state.messages.append({"role": "user", "content": question})

        with st.spinner("Thinking..."):
            try:
                response = requests.post(API_URL, json={
                    "question": question,
                    "chat_history": chat_history
                })
                response.raise_for_status()
                data = response.json()

                answer = data["answer"]
                sources = data["sources"]

                assistant_idx = len(st.session_state.messages)
                st.session_state.messages.append({"role": "assistant", "content": answer})
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
    st.caption("View Hargurjeet's resume")

    if os.path.exists(RESUME_PATH):
        with open(RESUME_PATH, "rb") as f:
            pdf_bytes = f.read()

        base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
        pdf_display = f"""
            <iframe
                src="data:application/pdf;base64,{base64_pdf}"
                width="100%"
                height="900px"
                style="border: none; border-radius: 8px;">
            </iframe>
        """
        st.markdown(pdf_display, unsafe_allow_html=True)

        st.download_button(
            label="⬇️ Download Resume",
            data=pdf_bytes,
            file_name="Hargurjeet_Lead_GenAI_Specialist.pdf",
            mime="application/pdf"
        )
    else:
        st.error(f"⚠️ Resume not found at `{RESUME_PATH}`. Make sure the file exists in the `data/` folder.")