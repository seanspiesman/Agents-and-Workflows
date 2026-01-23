
import os
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

class RAGSystem:
    def __init__(self, db_path="agent-output/memory/chroma_db", collection_name="agent_memory"):
        self.db_path = db_path
        self.collection_name = collection_name
        
        # Initialize Client
        self.client = chromadb.PersistentClient(path=self.db_path)
        
        # Initialize Embedding Model
        # using a lightweight, high-performance model
        self.embedding_function = self._get_embedding_function()
        
        # Get or Create Collection
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def _get_embedding_function(self):
        # We wrap the sentence-transformer to match what Chroma expects if needed,
        # but Chroma has a default. However, we want specific control.
        model = SentenceTransformer('all-MiniLM-L6-v2')
        return model

    def embed_text(self, text):
        return self.embedding_function.encode(text).tolist()

    def add_documents(self, documents, metadatas, ids):
        # Embeddings are handled automatically by Chroma if we don't provide them, 
        # OR we can pre-compute. Let's let Chroma handle it with a custom embedding function 
        # or just pass embeddings. For simplicity/efficiency, we'll implement a simple wrapper 
        # or just use raw embeddings if we were batching hard. 
        # actually, let's just use the default chroma embedding function or pass the model.
        # But wait, to ensure consistency, let's explicitly compute embeddings 
        # so we don't depend on chroma's default changing.
        
        embeddings = self.embedding_function.encode(documents).tolist()
        
        self.collection.upsert(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )

    def query(self, query_text, n_results=5):
        query_embedding = self.embed_text(query_text)
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        return results
