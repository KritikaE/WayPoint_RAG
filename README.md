# WayPoint RAG

A RAG-powered assistant for answering Visa dispute and chargeback policy questions using grounded answers from Visa guidelines.

## 🚀 Live Demo

- **Frontend:** https://way-point-rag.vercel.app/
- **Backend API Docs:** https://waypoint-rag.onrender.com/docs

## 🧠 How It Works

```text
User Question
      ↓
React Frontend
      ↓
FastAPI Backend
      ↓
Visa Policy Retrieval
      ↓
LLM + Retrieved Context
      ↓
Grounded Answer
```

WayPoint RAG retrieves relevant sections from Visa dispute and chargeback guidelines before generating an answer. This helps keep responses grounded in the source material rather than relying solely on the LLM's general knowledge.

## ✨ Features

- 💬 Natural-language dispute and chargeback queries
- 🔎 Semantic retrieval from Visa guidelines
- 🧠 Context-grounded LLM responses
- 📚 Source and page references
- ⚡ FastAPI backend
- ⚛️ React + Vite frontend
- ☁️ Cloud deployment with Vercel and Render

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React, Vite |
| Backend | Python, FastAPI |
| AI | RAG, Embeddings, LLM |
| Retrieval | Semantic Search |
| Deployment | Vercel, Render |

## 📚 Knowledge Base

The knowledge base is built using:

**Visa Dispute Management Guidelines for Visa Merchants — June 2024**

The retrieved source content is provided to the LLM as context so that answers can reference the relevant Visa policy sections and page numbers.

## 🏗️ Architecture

```text
                    ┌──────────────────┐
                    │      User        │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  React + Vite    │
                    │    Frontend      │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  FastAPI Backend │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │    Semantic      │
                    │    Retrieval     │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Visa Guidelines  │
                    │ Knowledge Base   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ LLM + Retrieved  │
                    │     Context      │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Grounded Answer  │
                    │    + Sources     │
                    └──────────────────┘
```

## 🎯 Use Cases

WayPoint RAG can help users quickly understand questions related to:

- Visa dispute conditions
- Chargeback scenarios
- Dispute reason codes
- Merchant responsibilities
- Required documentation
- Dispute timeframes
- Visa policy requirements
