import streamlit as st
from rag_engine import RAGEngine
rag = RAGEngine(data_path="employees.json")

st.set_page_config(page_title="HR Resource Chatbot", page_icon="🤖")

st.title("🤖 HR Resource Query Chatbot")
st.markdown("Ask me about employees! I can help you find the right person based on skills, experience, and projects.")

if "messages" not in st.session_state:
    st.session_state["messages"] = []
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])
query = st.chat_input("Type your HR query here...")

if query:
    st.session_state["messages"].append({"role": "user", "content": query})
    st.chat_message("user").write(query)
    results = rag.search(query)
    answer = rag.format_response(query, results)
    st.session_state["messages"].append({"role": "assistant", "content": answer})
    st.chat_message("assistant").write(answer)
