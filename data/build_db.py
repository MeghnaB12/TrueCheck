import os
import pandas as pd
import chromadb
from chromadb.utils import embedding_functions

# --- Configuration ---

DATA_PATH = "data/facts.csv"
DB_PATH = "./chroma_db"
COLLECTION_NAME = "government_facts"

def build_database():
    print(f"🔄 Loading data from {DATA_PATH}...")
    
    if not os.path.exists(DATA_PATH):
        print(f"❌ Error: {DATA_PATH} not found!")
        print("Please ensure 'data/facts.csv' exists in the repository.")
        return

    # 1. Load Data
    try:
        df = pd.read_csv(DATA_PATH)
        
        # Robust column detection: Check for 'fact', 'content', or use the first column
        if 'fact' in df.columns:
            documents = df['fact'].tolist()
        elif 'content' in df.columns:
            documents = df['content'].tolist()
        else:
            print(f"⚠️ Column 'fact' not found. Using first column: '{df.columns[0]}'")
            documents = df.iloc[:, 0].tolist()
            
        # Create simple IDs
        ids = [f"id_{i}" for i in range(len(documents))]
        
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return

    # 2. Initialize ChromaDB
    print(f"⚙️ Initializing Vector Database at {DB_PATH}...")
    client = chromadb.PersistentClient(path=DB_PATH)
    
    # Use default embedding function (all-MiniLM-L6-v2)
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    
    # 3. Create or Reset Collection
    try:
        client.delete_collection(name=COLLECTION_NAME)
        print("🗑️  Cleared existing collection to ensure fresh data.")
    except ValueError:
        pass # Collection didn't exist yet, which is fine

    collection = client.create_collection(name=COLLECTION_NAME, embedding_function=ef)

    # 4. Add Data
    print(f"📥 Indexing {len(documents)} facts into vector store...")
    collection.add(
        documents=documents,
        ids=ids
    )

    print(f"✅ Success! Database built at {DB_PATH}")
    print("🚀 You can now run 'streamlit run app.py'")

if __name__ == "__main__":
    build_database()
