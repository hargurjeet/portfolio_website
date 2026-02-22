import streamlit as st
import requests

API_URL = "http://localhost:8000/api/v1/chat"

st.set_page_config(page_title="RAG Chatbot", page_icon="🤖")
st.title("🤖 RAG Chatbot")
st.caption("Ask anything about your documents")

# Initialise chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render existing chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if question := st.chat_input("Ask a question..."):

    # Show user message
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    # Call FastAPI
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(API_URL, json={"question": question})
                response.raise_for_status()
                data = response.json()

                answer = data["answer"]
                sources = data["sources"]

                st.markdown(answer)

                # Show sources in an expander
                if sources:
                    with st.expander("📄 Sources"):
                        for i, src in enumerate(sources):
                            st.write(f"**[{i+1}]** {src['source']} — page {src['page']}")

                # Save full answer to history
                st.session_state.messages.append({"role": "assistant", "content": answer})

            except requests.exceptions.ConnectionError:
                err = "⚠️ Could not connect to the API. Make sure FastAPI is running on port 8000."
                st.error(err)
            except Exception as e:
                err = f"⚠️ Something went wrong: {str(e)}"
                st.error(err)