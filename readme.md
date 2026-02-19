# 🤖 RAG Chatbot

A Hybrid AI Chatbot built with Retrieval-Augmented Generation (RAG) architecture that answers questions based on your own documents and falls back to general knowledge when needed.

## 📌 Project Overview

This chatbot can:
- Read and understand your own documents (TXT, PDF)
- Store and retrieve information using a Vector Database
- Answer questions based on your documents using Groq AI
- Fall back to general knowledge if the answer is not in your documents
- Auto-update the vector store when documents are added or modified

---

## 🏗️ Architecture
```
User → Streamlit UI → FastAPI Backend → RAG Pipeline → ChromaDB + Groq LLM → Response
```

### Three Layers:
- **Frontend** — Streamlit chat interface
- **Backend** — FastAPI server handling requests
- **RAG Pipeline** — Document loading, chunking, embedding, retrieval and generation

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| Backend | FastAPI + Uvicorn |
| RAG Orchestration | LangChain |
| Vector Database | ChromaDB |
| Embeddings | HuggingFace (all-MiniLM-L6-v2) |
| LLM | Groq (llama-3.1-8b-instant) |
| PDF Support | PyPDF |

---

## 📁 Project Structure
```
chatbot_project/
├── app.py              # Frontend - Streamlit UI
├── main.py             # Backend - FastAPI server
├── rag_pipeline.py     # RAG Pipeline - Core logic
├── requirements.txt    # Project dependencies
├── .env                # API keys (not committed)
├── .gitignore          # Git ignore rules
├── data/               # Your documents (TXT, PDF)
│   └── sample.txt
└── chroma_db/          # Vector store (auto generated)
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.11
- Groq API Key (get it from https://console.groq.com)

### Step 1 — Clone the repository
```bash
git clone https://github.com/Pawanmalik-CS/chatbot_rag.git
cd chatbot_rag
```

### Step 2 — Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Create `.env` file
```
GROQ_API_KEY=your_groq_api_key_here
```

### Step 5 — Add your documents
Add any `.txt` or `.pdf` files to the `data/` folder.

---

## 🚀 Running the Project

**Terminal 1 — Start Backend:**
```bash
uvicorn main:app --host 127.0.0.1 --port 8000
```

**Terminal 2 — Start Frontend:**
```bash
streamlit run app.py
```

Then open your browser at `http://localhost:8501`

---

## ✨ Features

- 🎨 **Dark themed UI** with animated thinking dots and typing effect
- 💬 **Chat history** displayed in sidebar
- 🗑️ **Clear chat** button
- 📄 **Auto document ingestion** — just drop files in `data/` folder
- 🔄 **Auto vector store rebuild** when documents change
- 🤖 **Hybrid responses** — uses your docs first, falls back to general knowledge
- 🛡️ **Safe responses** — declines harmful or sensitive topics

---

## 📦 Dependencies

See [requirements.txt](https://github.com/Pawanmalik-CS/chatbot_rag/blob/master/requirements.txt)

---

## 🔮 Upcoming Features

- [ ] PDF upload from UI
- [ ] Multiple document collections
- [ ] Chat history persistence
- [ ] User authentication

---


##RAG Mode — When you ask something related to your documents in the data/ folder, it searches the vector database and answers from your documents
General Mode — When you ask something not in your documents (like "how are you" or "what is Python"), it falls back to Groq's general knowledge and answers normally

So it's hybrid because it combines both your custom data and general AI knowledge in one chatbot — giving the best of both worlds! 🚀

## 👨‍💻 Author

**Pawan Malik**
- GitHub: [@Pawanmalik-CS](https://github.com/Pawanmalik-CS)