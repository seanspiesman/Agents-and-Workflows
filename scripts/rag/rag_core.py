import os
import chromadb
from chromadb.config import Settings
from openai import OpenAI

class RAGSystem:
    def __init__(self, db_path=None, collection_name="agent_memory"):
        if db_path is None:
            # Default to project_root/agent-output/memory/chroma_db
            # Assuming this script is in scripts/rag/rag_core.py
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.abspath(os.path.join(current_dir, '../..'))
            self.db_path = os.path.join(project_root, "agent-output/memory/chroma_db")
        else:
            self.db_path = db_path
            
        self.collection_name = collection_name
        
        # Initialize Client
        self.client = chromadb.PersistentClient(path=self.db_path)
        
        
        # Connection Configuration
        self.local_base_url = "http://192.168.4.213:1234/v1"
        self.remote_base_url = "https://lmstudio.spiesmanhosting.ddns.net/v1"
        self.api_key = "waoMhQOuqpJh9saflSoT6b4EUaZTFoPWdxVg5vSySBZM57Fw4YscLcC7dxrqItDVrtSKeJ1GLP9pIAqvxaKDz4AePHbGORDcl41sd8ZaRaLHelFthmWCuxaHl6iDGSp2St6e0TTH5BHVJYl8cR28Msf9TiEGPBs1g21eaEhYfww5EgKoEbsCFGTj3zbTU4x3oveDOSPzbpU1yZeAS2orjY3BfBq0Cg8y0zawZsrfLOBTJcGkkYGKmv4CpAsYjLtx5KYKj6w2mrfCZhGLrpMFWyHrb43tTsQeaQt0VlcBtEIxu0RUh095t0v6rMBmci12ejQ7B0TL43rBBmUmOHrHG8itgfwy0L2zH6ZbkMbCpyLu89RksElmqKcvz2iPOy1DKpekIRL7Ex5WwojhsVgCieUQC0X54rjEbxZCdjalPosCr97lkaaAahsbMvz7c7oh0EDt6smForI20gvTB9rPEOjX910OElcJaJjehgDJB7wsGYoreda0lfTH9dYaoA2X"
        
        # Initialize Remote Embedding Client (with Fallback)
        self.embedding_model = "text-embedding-embeddinggemma-300m"
        self.openai_client = self._initialize_client()
        
        # Get or Create Collection
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def _initialize_client(self):
        """
        Try to connect to local endpoint first. If it fails, fallback to remote.
        """
        import requests
        
        print(f"Testing local RAG connection: {self.local_base_url}...")
        try:
            # Short timeout to check connectivity
            response = requests.get(f"{self.local_base_url}/models", timeout=2.0)
            if response.status_code == 200:
                print("Local connection confirmed.")
                return OpenAI(base_url=self.local_base_url, api_key="lm-studio")
        except Exception as e:
            print(f"Local connection failed ({e}).")
        
        print(f"Falling back to remote connection: {self.remote_base_url}...")
        return OpenAI(
            base_url=self.remote_base_url,
            api_key=self.api_key,
            default_headers={"X-Api-Key": self.api_key}
        )
        

    def _get_embeddings(self, texts):
        if not texts:
            return []
        try:
            response = self.openai_client.embeddings.create(
                input=texts,
                model=self.embedding_model
            )
            return [data.embedding for data in response.data]
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            return []

    def embed_text(self, text):
        embeddings = self._get_embeddings([text])
        if not embeddings:
            raise RuntimeError("Failed to generate embeddings. Check connection to local/remote LLM service.")
        return embeddings[0]

    def add_documents(self, documents, metadatas, ids):
        embeddings = self._get_embeddings(documents)
        
        if not embeddings:
            print("Failed to generate embeddings, skipping add_documents.")
            return

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
