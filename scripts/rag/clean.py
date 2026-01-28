import os
import shutil
import argparse
from rag_core import RAGSystem

def clean_database(force=False):
    """
    Removes the RAG database directory.
    """
    # Initialize RAGSystem just to get the db_path
    # We don't want to create the collection if it doesn't exist, but __init__ might.
    # actually __init__ creates the client but doesn't necessarily create collection until we ask?
    # Looking at rag_core.py: 
    # self.client = chromadb.PersistentClient(path=self.db_path)
    # self.collection = self.client.get_or_create_collection(...)
    # So simply instantiating it might create stuff. 
    # Let's just use the logic from rag_core.py to find the path without instantiating if possible, 
    # OR just instantiate it and then close/delete.
    
    # Replicating path logic to avoid side effects of instantiation if possible, 
    # but reusing logic is better.
    # Let's try to just import the path logic or instantiate. 
    # Instantiating is safe enough, we are about to delete it anyway.
    
    rag = RAGSystem()
    db_path = rag.db_path
    
    print(f"RAG Database Path: {db_path}")
    
    if not os.path.exists(db_path):
        print("Database directory does not exist. Nothing to clean.")
        return

    if not force:
        response = input(f"Are you sure you want to DELETE the entire RAG database at {db_path}? (y/N): ")
        if response.lower() != 'y':
            print("Operation cancelled.")
            return

    print(f"Removing database at {db_path}...")
    try:
        shutil.rmtree(db_path)
        print("Database successfully removed.")
        print("Run 'rag_ingest' to repopulate the database.")
    except Exception as e:
        print(f"Error removing database: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean the RAG database.")
    parser.add_argument('--force', action='store_true', help='Skip confirmation prompt')
    args = parser.parse_args()
    
    clean_database(force=args.force)
