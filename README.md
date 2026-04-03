# 🎓 College AI Assistant (Production-Ready RAG System)

## 📌 Overview
College AI Assistant is a **context-aware AI question–answering system** built for **real college usage**.  
It answers queries from students and parents related to **courses, fees, admissions, campus, placements, achievements, and students** using **verified college data only**.

The system follows a **Retrieval-Augmented Generation (RAG)** approach to ensure:
- No hallucinated answers  
- Controlled token usage  
- Complete and readable responses  

This project is designed for **practical deployment**, not just as a demo.

---

## 🎯 Problem Statement
College websites usually contain information spread across multiple pages and documents.  
Students and parents repeatedly ask common questions such as:
- What courses are offered?
- What is the fee structure?
- How are placements?
- Tell me about the college and students

This project solves that problem by providing a **single AI assistant** that:
- Understands natural language queries  
- Retrieves only relevant college information  
- Generates clear, factual answers  

---

## 🧠 Design Philosophy
- ❌ No custom ML model training  
- ❌ No sending full datasets to the AI  
- ❌ No blind dependency on prompts  

Instead:
- ✅ Backend-controlled logic  
- ✅ Context-first retrieval  
- ✅ AI used only for language generation  

---

## 🏗️ High-Level Architecture

User (HTML / Frontend)
        ↓
FastAPI (Python)
        ↓
Query Normalization + Synonym Mapping
        ↓
Semantic Retrieval (FAISS Vector Search)
        ↓
Top Relevant Context Chunks
        ↓
LLM (NVIDIA / LLaMA)
        ↓
Final Answer

---

## 🔑 Key Features

### 1. Context-Only Answers
- AI responds strictly using verified college data
- If information is unavailable, it replies:
  "Please contact the college office for this information."

### 2. Query Normalization & Synonym Handling
Handles real-world queries such as:
- AI → Artificial Intelligence  
- fees → fee structure / cost  
- B.Tech → Bachelor of Technology  
- placement 2026, hostel fees, direct admission  

### 3. Semantic Search with FAISS
- College data is converted into vector embeddings
- Queries are matched by **meaning**, not keywords
- Works well with long or imperfect questions

### 4. Dynamic Token Management
- Short questions → short answers  
- Long descriptive questions → longer answers  
- Prevents token waste and truncated replies  

### 5. Auto-Continuation Safety
- Detects incomplete answers
- Automatically continues generation
- Ensures no half sentences reach users

### 6. Strict System Rules
- Context-only answers
- No assumptions or external facts
- Simple English for students and parents

---

## 🧪 Example Queries
- What B.Tech courses are offered?
- Tell me about the college and students
- Is the college affiliated with AKTU?
- How is the campus environment?
- What are the placement opportunities?

---

## 🛠️ Tech Stack

### Backend
- Python
- FastAPI
- Uvicorn

### AI & Search
- Sentence Transformers
- FAISS (CPU)
- NVIDIA / LLaMA API

### Utilities
- python-dotenv
- requests
- numpy

---

## 📂 Project Structure

ai-service/
│
├── app/
│   ├── main.py               # FastAPI entry point
│   ├── config.py             # Configuration & environment handling
│   ├── routes/
│   │   └── chat.py           # /api/ask endpoint
│   ├── services/
│   │   ├── retriever.py      # Context retrieval logic
│   │   ├── llm.py            # LLM call + continuation handling
│   │   ├── token_manager.py # Dynamic token control
│   │   └── normalizer.py    # Synonym & query normalization
│   ├── data/
│   │   └── college_data.py  # Verified college information
│
├── requirements.txt
├── .env                      # API keys (not committed)
├── run.sh
└── README.md

---

## ▶️ How to Run Locally

source venv/Scripts/activate  
./run.sh

Open:
http://127.0.0.1:8001/docs

---

## 🔒 Security & Safety
- API keys stored securely in .env
- .env and venv/ excluded from version control
- No sensitive data sent to the AI
- Only selected context is shared with the LLM

---

## 🚀 Deployment & Server Setup

If you are deploying this project to a Linux VPS (e.g., DigitalOcean, AWS, Render), follow these optimized steps to ensure stability and efficiency.

### 🥇 Option 1: CPU-only Install (RECOMMENDED)
Since most cloud servers (without GPUs) don't need heavy CUDA drivers, use this method to save disk space and RAM.

1. **Clean start:**
   ```bash
   rm -rf venv
   python3 -m venv venv
   source venv/bin/activate
   ```
2. **Install PyTorch (CPU version):**
   ```bash
   pip install torch --index-url https://download.pytorch.org/whl/cpu
   ```
3. **Install other dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### 🥈 Option 2: Space Optimization
If your server is running out of disk space, run these cleanup commands:
```bash
sudo apt clean
rm -rf ~/.cache/pip
rm -rf /tmp/*
```
*Expected: Frees up ~1GB+ of space.*

### 🥉 Option 3: Server Specifications
For a smooth production experience with FAISS and LLM models:
- **Disk Space:** 15–20GB minimum.
- **RAM:** 2GB minimum (4GB recommended).

---

## 🛠️ Running 24/7 with `tmux`
To keep the bot running even after you close your terminal session:

1. **Start a new session:**
   ```bash
   tmux new -s allen-bot
   ```
2. **Run the server:**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8001
   ```
3. **Detach (Leave it running):**
   Press `Ctrl + B`, then let go and press `D`.
4. **Reconnect later:**
   ```bash
   tmux attach -t allen-bot
   ```

---

*Powered by ⚡ Rizq Technologies*
