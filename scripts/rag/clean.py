import os
import shutil
import argparse
from rag_core import RAGSystem

def clean_database(force=False):
    """
    Removes the RAG database directory.
    """
    # Calculate path manually to avoid instantiating RAGSystem (which creates locks)
    # Assuming this script is in scripts/rag/clean.py
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, '../..'))
    db_path = os.path.join(project_root, "agent-output/memory/chroma_db")
    
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
