# 🧠 Legal QA System with Fine-Tuned LLMs and RAG

A scalable Legal Question Answering (QA) system that combines fine-tuned open-source Language Models (LLaMA, Mistral) with Retrieval-Augmented Generation (RAG) to deliver accurate, explainable answers from 100K+ U.S. legal documents.

---

## 🚀 Overview

This project aims to democratize access to legal information by enabling users to ask legal questions and receive answers grounded in real legal texts. The system combines:

- **Fine-tuned LLMs** using Low-Rank Adaptation (LoRA)
- **Semantic search** with SentenceTransformers + FAISS
- **RAG pipelines** to combine retrieval + generation

---

## 🧰 Tech Stack

| Module             | Technology                                      |
|-------------------|--------------------------------------------------|
| Language Models    | LLaMA, Mistral (via HuggingFace Transformers)   |
| Fine-Tuning        | LoRA (via PEFT, bitsandbytes)                   |
| Embeddings         | SentenceTransformers                            |
| Vector Store       | FAISS                                            |
| Backend (optional) | Streamlit / FastAPI                             |
| Preprocessing      | spaCy, PyMuPDF                                  |

---

## 📦 Features

- ⚡ **4× Memory Efficient**: LoRA tuning reduces GPU footprint for training/deployment
- 🔍 **Semantic Search**: Real-time retrieval of relevant legal paragraphs
- 💬 **Answer Grounding**: LLM outputs cite actual case law & statutory references
- 🛠️ **End-to-End Pipeline**: From document ingestion to user query generation

---

## 🧪 Example Usage (WIP)

```python
from legal_qa_pipeline import LegalRAG

qa = LegalRAG()
response = qa.ask("What are Miranda rights?")
print(response)
