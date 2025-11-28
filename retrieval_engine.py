import pandas as pd
import chromadb
from chromadb.utils import embedding_functions
from src.config import DATA_PATH, CHROMA_PATH

class FactRetriever:
    def __init__(self):
        # Initialize ChromaDB 
        self.client = chromadb.PersistentClient(path=CHROMA_PATH)
        
        
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        
        self.collection = self.client.get_or_create_collection(
            name="gov_facts",
            embedding_function=self.embedding_fn
        )
        
       
        if self.collection.count() == 0:
            self.ingest_data()

    def ingest_data(self):
        """Reads CSV and stores embeddings in ChromaDB."""
        print("--- Ingesting Data into Vector DB ---")
        df = pd.read_csv(DATA_PATH)
        
        documents = df['fact_text'].tolist()
        ids = [str(x) for x in df['id'].tolist()]
        metadatas = [{"source": src} for src in df['source'].tolist()]
        
        self.collection.add(
            documents=documents,
            ids=ids,
            metadatas=metadatas
        )
        print(f"--- Ingested {len(documents)} facts ---")

    def retrieve(self, query, k=3):
        """Retrieves top-k similar facts AND their distance scores."""
        results = self.collection.query(
            query_texts=[query],
            n_results=k,
           
            include=["documents", "distances"] 
        )
        
        return results['documents'][0], results['distances'][0]