# 🩺 MediBot — AI Medical Chatbot

MediBot is an **AI-powered medical chatbot** that uses **Retrieval-Augmented Generation (RAG)** to answer medical questions using information retrieved from a curated medical knowledge base.

Instead of relying entirely on the language model's internal knowledge, MediBot retrieves relevant information from medical documents stored in a **FAISS vector database** and provides that context to the language model before generating an answer.

> ⚠️ **Disclaimer:** MediBot is an educational/research project and is **not a substitute for professional medical advice, diagnosis, or treatment.** Always consult a qualified healthcare professional for medical concerns.

---

## ✨ Features

* 🤖 AI-powered medical question answering
* 🔎 Retrieval-Augmented Generation (RAG)
* 📚 Answers grounded in medical PDF documents
* 🧠 Semantic search using Hugging Face embeddings
* ⚡ Fast similarity search using FAISS
* 💬 Interactive chat interface using Streamlit
* 🗂️ Persistent vector database
* 🛡️ Prompt designed to reduce hallucinations by restricting responses to retrieved context
* 🔗 Source-document retrieval through LangChain

---

## 🏗️ How MediBot Works

MediBot follows a simple RAG pipeline:

```text
                    Medical PDFs
                         │
                         ▼
                  PDF Document Loader
                         │
                         ▼
                  Text Chunking
                         │
                         ▼
              Hugging Face Embeddings
                         │
                         ▼
                   FAISS Vector DB
                         │
                         │
User Question ───────────┘
       │
       ▼
 Semantic Similarity Search
       │
       ▼
 Relevant Medical Context
       │
       ▼
     Qwen 2.5
       │
       ▼
   Final Response
       │
       ▼
 Streamlit Chat Interface
```

---

## 🧠 RAG Pipeline

### 1. Load Medical Documents

Medical PDF files placed inside the `data/` directory are loaded using LangChain's `PyPDFLoader` and `DirectoryLoader`.

### 2. Split Documents

The extracted text is divided into smaller chunks using `RecursiveCharacterTextSplitter`.

Current configuration:

```text
Chunk size: 500
Chunk overlap: 50
```

### 3. Generate Embeddings

Each text chunk is converted into a numerical vector using:

```text
sentence-transformers/all-MiniLM-L6-v2
```

### 4. Store Embeddings

The generated embeddings are stored in a local **FAISS** vector database.

```text
vectorstore/db_faiss
```

### 5. Retrieve Relevant Information

When a user asks a question, MediBot searches the FAISS database and retrieves the most relevant chunks.

The current retrieval configuration returns the top **3** relevant documents.

### 6. Generate the Answer

The retrieved context is passed to:

```text
Qwen/Qwen2.5-1.5B-Instruct
```

through Hugging Face and LangChain.

The prompt instructs the model to answer only using the provided context and avoid making up information.

---

## 🛠️ Tech Stack

| Technology                | Purpose                            |
| ------------------------- | ---------------------------------- |
| 🐍 Python                 | Core programming language          |
| 🎈 Streamlit              | Web-based chat interface           |
| 🦜 LangChain              | RAG pipeline and LLM orchestration |
| 🤗 Hugging Face           | Embeddings and LLM integration     |
| 🧠 Qwen 2.5 1.5B Instruct | Language model                     |
| 🔢 FAISS                  | Vector similarity search           |
| 🔤 Sentence Transformers  | Text embeddings                    |
| 📄 PyPDF                  | PDF document processing            |
| 🌱 python-dotenv          | Environment variable management    |

The repository's dependency file includes LangChain, FAISS CPU, Streamlit, Sentence Transformers, Transformers, PyTorch, Hugging Face Hub, and related packages.

---

## 📂 Project Structure

```text
MediBot/
│
├── data/
│   └── *.pdf
│
├── vectorstore/
│   └── db_faiss/
│       ├── index.faiss
│       └── index.pkl
│
├── chatbot.py
├── create_memory_for_llm.py
├── connect_memory_with_llm.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

### File Description

#### `create_memory_for_llm.py`

Creates the knowledge base used by MediBot.

The script:

1. Loads PDFs from `data/`
2. Splits documents into chunks
3. Generates embeddings
4. Creates the FAISS vector database
5. Saves the vector store locally

The current implementation uses `PyPDFLoader`, 500-character chunks with 50-character overlap, `all-MiniLM-L6-v2`, and FAISS.

#### `connect_memory_with_llm.py`

Connects the FAISS vector database to the language model and creates the LangChain `RetrievalQA` pipeline.

It retrieves the top 3 relevant documents before generating an answer.

#### `chatbot.py`

Provides the Streamlit user interface.

It:

* Loads the FAISS vector database
* Initializes the embedding model
* Connects to Qwen through Hugging Face
* Creates the RetrievalQA chain
* Maintains chat history using Streamlit session state
* Displays responses through the Streamlit chat interface.

---

# 🚀 Getting Started

## 1. Clone the Repository

```bash
git clone https://github.com/Tanishq-lalani/MediBot.git

cd MediBot
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Hugging Face

Create a `.env` file in the root directory:

```env
HF_TOKEN=your_huggingface_token
```

Your application reads the Hugging Face token from the environment using `python-dotenv`.

> Never commit your `.env` file or API tokens to GitHub.

---

# 📚 Build the Vector Database

Before running the chatbot, make sure your medical PDF documents are placed inside:

```text
data/
```

Then run:

```bash
python create_memory_for_llm.py
```

This will:

```text
PDF files
   ↓
Text extraction
   ↓
Text chunks
   ↓
Embeddings
   ↓
FAISS
   ↓
vectorstore/db_faiss
```

The generated vector database is stored inside:

```text
vectorstore/db_faiss/
```

---

# ▶️ Run MediBot

Start the Streamlit application:

```bash
streamlit run chatbot.py
```

Streamlit will provide a local URL similar to:

```text
http://localhost:8501
```

Open it in your browser and start asking medical questions.

---

# 💬 Example

You can ask questions such as:

```text
What are the common symptoms of diabetes?
```

or:

```text
What are the symptoms mentioned in the medical documents for hypertension?
```

MediBot retrieves relevant information from the vector database and uses that context to generate the response.

---

# 🔐 Environment Variables

| Variable   | Description            | Required |
| ---------- | ---------------------- | -------- |
| `HF_TOKEN` | Hugging Face API token | ✅        |

Example:

```env
HF_TOKEN=hf_xxxxxxxxxxxxxxxxx
```

---

# ⚙️ Configuration

### Embedding Model

```python
sentence-transformers/all-MiniLM-L6-v2
```

### Language Model

```python
Qwen/Qwen2.5-1.5B-Instruct
```

### Vector Database

```text
FAISS
```

### Retrieved Documents

```python
search_kwargs={"k": 3}
```

### Text Chunking

```text
Chunk size: 500
Chunk overlap: 50
```

---

# 🧩 Architecture

```text
┌─────────────────────────┐
│     Medical PDF Files   │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│      PyPDFLoader        │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ RecursiveCharacter      │
│ Text Splitter           │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ Hugging Face Embeddings │
│ all-MiniLM-L6-v2        │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│       FAISS DB          │
└────────────┬────────────┘
             │
             │ Retrieval
             ▼
┌─────────────────────────┐
│    Relevant Context     │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ Qwen 2.5 1.5B Instruct  │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│   Streamlit Chat UI     │
└─────────────────────────┘
```

---

# 🎯 Why RAG?

A traditional LLM can generate an answer based on its pretrained knowledge.

MediBot instead follows:

```text
User Question
      ↓
Retrieve relevant medical information
      ↓
Provide retrieved information to LLM
      ↓
Generate grounded response
```

This approach helps reduce unsupported answers because the custom prompt explicitly instructs the model to use the supplied context and say it does not know when the information is unavailable.

---

# 🚧 Future Improvements

Some potential improvements for MediBot include:

* [ ] Add citations to retrieved medical sources
* [ ] Display source documents in the Streamlit UI
* [ ] Add conversation memory across sessions
* [ ] Improve prompt engineering
* [ ] Add medical safety guardrails
* [ ] Add document upload directly through the UI
* [ ] Support multiple medical knowledge bases
* [ ] Add authentication
* [ ] Deploy the application
* [ ] Add evaluation metrics for RAG quality
* [ ] Add automated tests
* [ ] Improve retrieval with hybrid search
* [ ] Add reranking for retrieved documents
* [ ] Add conversation summarization for long chats

---

# ⚠️ Medical Disclaimer

MediBot is an **educational and technical demonstration of Retrieval-Augmented Generation for healthcare-related information**.

It should **not** be used to:

* Diagnose medical conditions
* Replace a doctor or healthcare professional
* Recommend prescription medication
* Make emergency medical decisions
* Replace professional medical treatment

For medical emergencies or serious health concerns, consult a qualified healthcare professional or emergency service.

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a new branch

```bash
git checkout -b feature/your-feature
```

3. Make your changes
4. Commit your changes

```bash
git commit -m "Add your feature"
```

5. Push the branch

```bash
git push origin feature/your-feature
```

6. Open a Pull Request

---

# 👨‍💻 Author

**Tanishq Lalani**

GitHub: [@Tanishq-lalani](https://github.com/Tanishq-lalani)

---

# ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

---

## 📄 License

This project is intended for educational and research purposes.
