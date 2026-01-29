import os
import argparse
from rag_core import RAGSystem
from ingest import get_files_to_ingest, calculate_file_hash

def get_db_file_states(rag):
    """
    Query the database to get the state of all files.
    Returns a dictionary: {rel_path: {"file_hash": hash, "last_modified": timestamp}}
    """
    try:
        # Fetch all metadata from the collection
        # Note: ChromaDB get() without ids returns everything. 
        # For large datasets, this might be slow, but it's the most direct way to get all source files.
        result = rag.collection.get(include=["metadatas"])
        
        db_files = {}
        if result and result['metadatas']:
            for meta in result['metadatas']:
                if 'source' in meta:
                    source = meta['source']
                    # We only need one chunk to know the file's state in DB
                    # If multiple chunks have different states, something is wrong, but we'll take the latest seen.
                    if source not in db_files:
                        db_files[source] = {
                            "file_hash": meta.get("file_hash", ""),
                            "last_modified": meta.get("last_modified", 0)
                        }
        return db_files
    except Exception as e:
        print(f"Error querying database: {e}")
        return {}

def check_status(root_dir=None, verbose=False):
    if root_dir is None:
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    
    print(f"Checking RAG status for project root: {root_dir}")
    
    # 1. Get Local Files
    print("Scanning local files...")
    local_files_abs = get_files_to_ingest(root_dir)
    local_files = {}
    for f in local_files_abs:
        rel_path = os.path.relpath(f, root_dir)
        local_files[rel_path] = f
        
    # 2. Get DB Files
    print("Querying RAG database...")
    rag = RAGSystem()
    db_files = get_db_file_states(rag)
    
    # 3. Compare
    new_files = []
    deleted_files = []
    stale_files = []
    uptodate_files = []
    unknown_state_files = [] 
    
    # Check Local against DB
    for rel_path, abs_path in local_files.items():
        if rel_path not in db_files:
            new_files.append(rel_path)
        else:
            db_state = db_files[rel_path]
            db_hash = db_state.get("file_hash")
            
            if not db_hash:
                # If DB hash is missing, it's essentially stale/unknown because we can't verify it
                unknown_state_files.append(rel_path)
                continue
                
            local_hash = calculate_file_hash(abs_path)
            
            if local_hash != db_hash:
                stale_files.append(rel_path)
            else:
                uptodate_files.append(rel_path)
                
    # Check DB against Local (for deletions)
    for rel_path in db_files:
        if rel_path not in local_files:
            deleted_files.append(rel_path)
            
    # 4. Report
    print("\n=== RAG Status Report ===")
    print(f"Total Local Files: {len(local_files)}")
    print(f"Total DB Files:    {len(db_files)}")
    print("-------------------------")
    print(f"Up-to-date: {len(uptodate_files)}")
    print(f"New:        {len(new_files)}")
    print(f"Stale:      {len(stale_files)}")
    print(f"Deleted:    {len(deleted_files)}")
    print(f"Unknown:    {len(unknown_state_files)} (Missing metadata in DB)")
    print("=========================")
    
    if verbose or (len(new_files) + len(stale_files) + len(deleted_files) + len(unknown_state_files) > 0):
        if new_files:
            print("\n[NEW] Files (Need Ingestion):")
            for f in new_files[:20]: print(f"  + {f}")
            if len(new_files) > 20: print(f"  ... and {len(new_files) - 20} more")
            
        if stale_files:
            print("\n[STALE] Files (Content Changed):")
            for f in stale_files[:20]: print(f"  * {f}")
            if len(stale_files) > 20: print(f"  ... and {len(stale_files) - 20} more")
            
        if deleted_files:
            print("\n[DELETED] Files (In DB but not Disk):")
            for f in deleted_files[:20]: print(f"  - {f}")
            if len(deleted_files) > 20: print(f"  ... and {len(deleted_files) - 20} more")
            
        if unknown_state_files:
            print("\n[UNKNOWN] Files (Legacy Data - Re-ingest Recommended):")
            for f in unknown_state_files[:20]: print(f"  ? {f}")
            if len(unknown_state_files) > 20: print(f"  ... and {len(unknown_state_files) - 20} more")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check the freshness of the RAG database.")
    parser.add_argument('-v', '--verbose', action='store_true', help='Show detailed file lists')
    args = parser.parse_args()
    
    check_status(verbose=args.verbose)
