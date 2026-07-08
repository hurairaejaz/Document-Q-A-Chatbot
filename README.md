# 📄 AI Document Q&A Chatbot

An intelligent Document Question-Answering application that enables users to upload PDF documents and ask natural language questions about their content. The system uses **Retrieval-Augmented Generation (RAG)** with **LangChain**, **FAISS**, **Google Gemini**, and **FastAPI** to provide accurate, context-aware answers.

---

## 🚀 Features

* 📂 Upload PDF documents
* 🧠 AI-powered Question Answering
* 🔍 Semantic Search using Vector Embeddings
* ⚡ Fast Retrieval with ChromaDb Vector Database
* 💬 Conversational Question Answering
* 📑 Multiple Document Support
* 🌐 Modern Responsive Web Interface
* 🛡 Error Handling & Validation

---

## 🏗 System Architecture

```
                 +----------------------+
                 |      User            |
                 +----------+-----------+
                            |
                            v
                +-----------------------+
                |      Frontend         |
                |      (Streamlit)      |
                +-----------+-----------+
                            |
                    REST API Requests
                            |
                            v
                +-----------------------+
                |      FastAPI Backend  |
                +-----------+-----------+
                            |
           +----------------+----------------+
           |                                 |
           v                                 v
   PDF Processing                  AI Question Answering
           |                                 |
           v                                 |
      LangChain Loader                       |
           |                                 |
           v                                 |
     Text Chunking                           |
           |                                 |
           v                                 |
 Google Embeddings --------------------------+
           |
           v
     FAISS Vector Store
           |
           v
   Relevant Context Retrieval
           |
           v
      GROQ LLM
           |
           v
      Final AI Response
```

---

# 📁 Project Structure

```
AI-Document-QA-Chatbot/
│
├── backend/
│   ├── database.py
│   ├── config.py
|   ├── embeddings.py
│   ├── llm.py
|   ├── pdf_loader.py
│   ├── rag.py
├── uploads/
├── chroma_db/
├── frontend/
│   ├── app.py
│── requirements.txt
├── .env
├── README.md


```

---

# 🛠 Technologies Used

### Backend

* Python 
* FastAPI
* Uvicorn
* LangChain
* GROQ API
* Chromadb
* PyPDF
* Pydantic

### Frontend

*streamlit

### AI & Machine Learning

* Retrieval-Augmented Generation (RAG)
* Embeddings
* Semantic Search

---

# ⚙ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/yourusername/AI-Document-QA-Chatbot.git

cd AI-Document-QA-Chatbot
```

---

## 2. Create Virtual Environment

Windows

```bash
python -m venv .venv

venv\Scripts\activate
```


## 3. Install Dependencies

```bash
pip install -r backend/requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file in the project root.

```env
GROK_API_KEY=GROQ_API_KEY
```

Replace the key with  GROQo API Key.

---

## 5. Run the Backend

```bash
cd backend

uvicorn app:app --reload
```

Server runs on

```
http://127.0.0.1:8000
```

---

## 6. Launch the Frontend

Open

```
http://localhost:8501
```



# 💡 How It Works

### Step 1

Upload one or more PDF documents.

↓

### Step 2

Documents are converted into text.

↓

### Step 3

Text is divided into manageable chunks.

↓

### Step 4

Embeddings are generated using  Embeddings.

↓

### Step 5

Embeddings are stored in a chromadb vector database.

↓

### Step 6

When a user asks a question:

* User query is converted into embeddings
* Relevant document chunks are retrieved
* Retrieved context is passed to Gemini
* Groq generates an accurate answer

---

# 🔌 API Endpoints

## Upload Document

```
POST /upload
```

Uploads a PDF document and indexes it.

---

## Ask Question

```
POST /ask
```

Example Request

```json
{
    "question": "What is Machine Learning?"
}
```

Example Response

```json
{
    "answer": "Machine Learning is a subset of Artificial Intelligence that enables systems to learn from data without explicit programming."
}
```

---

## Health Check

```
GET /
```

Returns API status.

---

# 📷 Application Workflow

```
Upload PDF
      │
      ▼
Extract Text
      │
      ▼
Chunk Text
      │
      ▼
Generate Embeddings
      │
      ▼
Store in FAISS
      │
      ▼
Ask Question
      │
      ▼
Similarity Search
      │
      ▼
Gemini Generates Answer
      │
      ▼
Display Response
```

---

# 📌 Future Improvements

* Multi-file Chat
* Conversation Memory
* User Authentication
* Chat History
* Citation-Based Answers
* Source Highlighting
* Cloud Deployment (AWS, Azure, GCP)
* Admin Dashboard
* Mobile Application

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a new feature branch.
3. Commit your changes.
4. Push your branch.
5. Open a Pull Request.

---


# 👨‍💻 Author

**Huraira Ejaz**

Software Engineer



GitHub: https://github.com/hurairaejaz

LinkedIn: https://linkedin.com/in/hurairaejaz

---

# ⭐ Support

If you found this project useful, please consider giving it a ⭐ on GitHub. Your support helps improve and maintain the project.
