# 🔍 TrueCheck: LLM-Powered RAG Fact Checker

![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg) ![Python](https://img.shields.io/badge/Python-3.9%2B-yellow) ![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red) ![Ollama](https://img.shields.io/badge/LLM-Mistral%20%2F%20Ollama-orange)

## 📌 Project Overview

**TrueCheck** is a Retrieval-Augmented Generation (RAG) system designed to verify claims against a trusted knowledge base of Indian Government policies. It features a hybrid pipeline using **spaCy** for entity extraction, **ChromaDB** for semantic retrieval, and a **Local LLM** (Mistral via Ollama) for reasoning and verification.

---

## 🚀 Key Features

* ✅ **Strict Verification:** Classifies claims clearly as **True**, **False**, or **Unverifiable**.
* ⚡ **Cost-Optimized:** Implements a **Relevance Score Threshold (0.5)** to filter out vague or unrelated claims *before* calling the LLM, saving compute resources and reducing latency.
* 🔒 **Local & Privacy-First:** Fully capable of running offline using **Ollama (Mistral)** and **SentenceTransformers**, ensuring data stays local.
* 🧠 **Transparent Logic:** Displays the exact retrieved evidence and the specific "Distance Score" for every query to ensure explainability.

---

## 🧪 How It Works (Pipeline)

```mermaid
graph TD
    A[User Input] --> B[Entity Extractor (spaCy)]
    B --> C{Relevance Check}
    C -- "Distance Score > 0.5" --> D[Strict Filter: 'Unverifiable']
    C -- "Distance Score <= 0.5" --> E[Vector DB (ChromaDB)]
    E --> F[Retrieved Context]
    F --> G[LLM Reasoner (Mistral/Ollama)]
    G --> H[Final Verdict & Evidence]
