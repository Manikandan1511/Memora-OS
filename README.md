<div align="center">

# 🧠 Memora OS
### Your Personal AI Memory Operating System

*"Never lose an idea again. Build a second brain that remembers, connects, and evolves your knowledge."*

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?logo=react)
![ChromaDB](https://img.shields.io/badge/VectorDB-ChromaDB-orange)
![Neo4j](https://img.shields.io/badge/Graph-Neo4j-018BFF?logo=neo4j)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)

</div>

---

# 🚀 Overview

Memora OS is an AI-powered Memory Operating System designed to become your personal **Second Brain**.

Instead of simply storing notes, Memora understands relationships between ideas, tracks how your thoughts evolve over time, retrieves forgotten knowledge when needed, and allows natural conversations with your entire knowledge base.

Unlike traditional note-taking applications, Memora transforms scattered information into an interconnected knowledge network powered by Artificial Intelligence.

---

# ✨ Features

## 📝 Intelligent Memory Storage

- Save notes instantly
- Store thoughts, ideas, documents, and conversations
- Semantic vector indexing
- Fast retrieval

---

## 🔍 AI Semantic Search

Search memories using natural language.

Example:

> "Show me the ideas I had about startup funding."

instead of searching exact keywords.

---

## 🧠 Knowledge Graph

Every memory becomes a node.

Related memories are automatically connected using Neo4j, allowing AI to understand relationships between ideas.

Example

```
Blockchain
     │
     ├──── Smart Contracts
     │
     ├──── Ethereum
     │
     └──── Solidity
```

---

## 📈 Memory Evolution

Track how an idea grows over time.

```
Initial Idea
      │
      ▼
Research
      │
      ▼
Prototype
      │
      ▼
Final Product
```

---

## 💬 Chat With Your Brain

Instead of searching manually, simply ask:

> "What project ideas have I worked on recently?"

or

> "Summarize everything I know about Machine Learning."

The AI understands context and retrieves the most relevant memories.

---

## ⏳ Timeline View

Visualize memories chronologically.

```
Yesterday

• AI Project Idea
• Blockchain Notes

Today

• Meeting Notes
• Startup Research
```

---

## 🔗 Automatic Memory Linking

Memora automatically detects related concepts and creates meaningful relationships between memories.

No manual tagging required.

---

## ⚡ Fast Vector Search

Uses Sentence Transformers + ChromaDB for semantic similarity search.

Even if your wording changes, Memora still understands what you mean.

---

# 🏗 Architecture

```
                  User
                    │
                    ▼
             React Frontend
                    │
                    ▼
              FastAPI Backend
                    │
     ┌──────────────┼───────────────┐
     ▼              ▼               ▼

 ChromaDB       Neo4j Graph      AI Model
(Vector DB)      Database       (Gemini / Local LLM)

     │
     ▼

 Memory Retrieval
 Relationship Discovery
 AI Reasoning
```

---

# 🛠 Tech Stack

## Frontend

- React
- Vite
- Tailwind CSS
- ShadCN UI
- Framer Motion

---

## Backend

- FastAPI
- Python

---

## AI

- Sentence Transformers
- Embedding Generation
- Semantic Search
- LLM Integration

---

## Databases

- ChromaDB
- Neo4j

---

# 📂 Project Structure

```
Memora-OS
│
├── backend
│   ├── app
│   │   ├── api
│   │   ├── models
│   │   ├── services
│   │   ├── database
│   │   └── main.py
│
├── frontend
│   ├── src
│   ├── components
│   ├── pages
│   └── assets
│
├── vectordb
│
├── README.md
│
└── requirements.txt
```

---

# 📸 Screenshots

```
📌 Add screenshots here

Dashboard

Search

Timeline

Knowledge Graph

Chat Interface
```

---

# ⚙ Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/Memora-OS.git

cd Memora-OS
```

---

## Backend

```bash
cd backend

python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

---

# 🚀 API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | /api/v1/memory | Save Memory |
| POST | /api/v1/memory/search | Semantic Search |
| POST | /api/v1/memory/timeline | Timeline |
| GET | /api/v1/evolution/{id} | Memory Evolution |
| POST | /api/v1/brain/ask | AI Chat |

---

# 🎯 Roadmap

- [x] Semantic Search

- [x] Vector Database

- [x] Knowledge Graph

- [x] Memory Timeline

- [x] AI Chat

- [ ] OCR Support

- [ ] PDF Understanding

- [ ] Voice Notes

- [ ] Mobile Application

- [ ] Browser Extension

- [ ] Multi-user Collaboration

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository

2. Create your feature branch

3. Commit your changes

4. Push to your branch

5. Open a Pull Request

---

# 📊 Why Memora?

Traditional Notes

❌ Keyword Search

❌ No Relationships

❌ Static Information

❌ No Memory Evolution

❌ No AI Understanding

---

Memora OS

✅ Semantic Search

✅ Knowledge Graph

✅ AI Reasoning

✅ Context Awareness

✅ Memory Evolution

✅ Second Brain

---

# 🌟 Future Vision

Memora aims to become an intelligent operating system for human knowledge.

Imagine an AI that not only remembers everything you've learned but also connects ideas, uncovers forgotten insights, and helps you think more effectively.

Our vision is to transform personal knowledge management into an intelligent cognitive companion.

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Manikandan**

Computer Science Engineering

AI & Full Stack Developer

---

<div align="center">

### ⭐ If you found this project useful, please consider giving it a Star!

Made with ❤️ using FastAPI, React, Neo4j & ChromaDB

</div>
