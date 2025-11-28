🔍 TrueCheck: LLM-Powered RAG Fact Checker

📌 Project Overview

TrueCheck is a Retrieval-Augmented Generation (RAG) system designed to verify claims against a trusted knowledge base of Indian Government policies. It features a hybrid pipeline using spaCy for entity extraction, ChromaDB for semantic retrieval, and a Local LLM (Mistral via Ollama) for reasoning and verification.

🚀 Key Features

Strict Verification: Classifies claims as ✅ True, ❌ False, or 🤷‍♂️ Unverifiable.

Cost-Optimized: Implements a Relevance Score Threshold (0.5) to filter out vague/unrelated claims before calling the LLM, saving compute resources.

Local & Privacy-First: Fully capable of running offline using Ollama (Mistral) and SentenceTransformers.

Transparent Logic: Displays the exact retrieved evidence and the "Distance Score" for every query.

🛠️ Tech Stack

Frontend: Streamlit

Embeddings: all-MiniLM-L6-v2 (SentenceTransformers)

Vector DB: ChromaDB (Persistent storage)

LLM: Mistral (via Ollama) or GPT-4o-mini (Configurable)

NLP: spaCy (en_core_web_sm)

⚙️ Setup Instructions

1. Prerequisites

Python 3.9+

Ollama installed and running.

2. Install Dependencies

pip install -r requirements.txt
python -m spacy download en_core_web_sm


3. Start Local LLM

Ensure your local Ollama instance is running with the Mistral model:

ollama run mistral


(Keep this terminal window open)

4. Run the Application

streamlit run app.py


The app will launch at http://localhost:8501.

📂 Project Structure

fact_checker_assignment/
├── app.py                 # Main Streamlit UI application
├── .env                   # Configuration (API Keys if using OpenAI)
├── requirements.txt       # Python dependencies
├── README.md              # Documentation
├── data/
│   └── facts.csv          # Trusted Knowledge Base (Verified Facts)
└── src/
    ├── config.py          # Path configurations
    ├── extractor.py       # spaCy Entity Extraction
    ├── retrieval_engine.py# ChromaDB Vector Search Logic
    └── verifier_llm.py    # LLM Verification Agent (Ollama/OpenAI)


🧪 How It Works (Pipeline)

User Input: Accepts a natural language claim.

Metadata Extraction: src/extractor.py uses spaCy to identify key entities (Dates, Organizations, Policies).

Vector Retrieval: src/retrieval_engine.py converts the claim to vector embeddings and queries ChromaDB.

Optimization: If the Distance Score > 0.5, the system flags the claim as "Unverifiable" immediately, skipping the LLM.

LLM Verification: If the score is valid, src/verifier_llm.py sends the claim + evidence to Mistral to generate a verdict (True/False) with reasoning.

