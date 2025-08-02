# HR Resource Query Chatbot

## 📌 Overview
The **HR Resource Query Chatbot** is an AI-powered assistant designed to help HR teams find the right employees for specific project needs. It supports **natural language queries** like:  
- _"Find Python developers with 3+ years experience"_  
- _"Who has worked on healthcare projects?"_  
- _"Suggest people for a React Native project"_  

The chatbot uses **semantic search** with embeddings and a FAISS vector index to match queries with relevant employee profiles. It provides **clear, formatted answers** instantly, making HR resource allocation faster and smarter.

---

## 🚀 Features
✅ **Natural Language Query Support** – Ask HR-related questions in plain English.  
✅ **Semantic Search** – Uses `sentence-transformers` + FAISS for accurate results.  
✅ **Skill & Experience Filters** – Filters candidates by skills and experience (e.g., _3+ years_).  
✅ **Streamlit Chat Interface** – Simple and interactive web UI for conversations.  
✅ **Lightweight Solution** – No API keys, no heavy LLMs, no cloud costs.  
✅ **50-Sample Employee Dataset** – Includes realistic profiles for testing queries.  

---

## 🏗 Architecture
**System Components:**
1️⃣ **Data Layer**  
- JSON dataset with employee details: `name`, `skills`, `experience_years`, `projects`, `availability`.

2️⃣ **RAG Engine (`rag_engine.py`)**  
- Embedding model: `sentence-transformers/all-MiniLM-L6-v2`.  
- Vector search: FAISS index for fast retrieval.  
- Query parsing for **skills** & **experience**.

3️⃣ **Frontend (`app.py`)**  
- Built with **Streamlit** for a chat-like interface.  
- Shows conversation history & formatted results.

**Architecture Diagram (Conceptual)**:
[User Query] ➡ [Streamlit UI] ➡ [RAG Engine]
⬇ ⬆
[FAISS Search] ← [Employee JSON]

### 📥 Clone the repo (or download files):
```bash
git clone https://github.com/manccc/HR_Query_Chatbot.git
cd HR_Query_Chatbot
```

```bash
pip install requirements.txt
```

```bash
streamlit run app.py
```

## Future Improvements
- Add optional LLM (OpenAI/Ollama) for natural summaries
- Expand dataset with location, availability dates
- Build FastAPI backend for API endpoints
- Deploy to Streamlit Cloud or HuggingFace Spaces



