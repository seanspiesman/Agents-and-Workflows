import os
import glob
import uuid
import hashlib
import time
from rag_core import RAGSystem

# Setup debug logging
def log_debug(msg):
    with open(os.path.join(os.path.dirname(__file__), 'rag_debug.log'), 'a') as f:
        f.write(f"{msg}\n")


# Configuration
IGNORE_DIRS = {'.git', '.venv', 'node_modules', '__pycache__', '.idea', '.vscode', 'dist', 'build', 'coverage', "bun","obj"}
INCLUDE_EXTENSIONS = {
    # Documentation
    '.md', '.txt', '.rst',
    # Config/Data
    '.json', '.yaml', '.yml', '.toml', '.xml', '.ini', '.env.example',
    # Scripts
    '.sh', '.bash', '.zsh', '.bat', '.ps1',
    # Python
    '.py',
    # Web/JS
    '.js', '.ts', '.jsx', '.tsx', '.mjs', '.cjs',
    '.html', '.css', '.scss', '.less', '.vue', '.svelte',
    # .NET/C#
    '.cs', '.fs', '.csproj', '.sln',
    # Mobile/Native
    '.swift', '.kt', '.java', '.dart',
    '.c', '.cpp', '.h', '.m', '.mm', '.go', '.rs', '.php', '.rb',
    '.lua', '.sql'
}

def should_ignore(path):
    parts = path.split(os.sep)
    for part in parts:
        if part in IGNORE_DIRS:
            return True
    return False

def calculate_file_hash(filepath):
    """Calculate MD5 hash of a file."""
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            buf = f.read(65536)
            while len(buf) > 0:
                hasher.update(buf)
                buf = f.read(65536)
        return hasher.hexdigest()
    except Exception as e:
        print(f"Error calculating hash for {filepath}: {e}")
        return None

def get_files_to_ingest(root_dir):
    """
    Get files using git ls-files if possible, otherwise fallback to os.walk/glob.
    """
    import subprocess
    
    files = []
    use_git = False
    
    # Try git ls-files first
    if os.path.exists(os.path.join(root_dir, '.git')):
        try:
            # git ls-files --cached --others --exclude-standard
            result = subprocess.run(
                ['git', 'ls-files', '-c', '-o', '--exclude-standard'],
                cwd=root_dir,
                capture_output=True,
                text=True,
                check=True
            )
            git_files = result.stdout.splitlines()
            print(f"Git identified {len(git_files)} tracked/unignored files.")
            
            for f in git_files:
                abs_path = os.path.join(root_dir, f)
                if os.path.exists(abs_path):
                     # Still check extension whitelist to avoid binary junk
                    _, ext = os.path.splitext(abs_path)
                    if ext in INCLUDE_EXTENSIONS:
                        files.append(abs_path)
            
            use_git = True
        except Exception as e:
            print(f"Git lookup failed, falling back to manual scan: {e}")
    
    if not use_git:
        # Fallback to manual glob
        for ext in INCLUDE_EXTENSIONS:
            found = glob.glob(os.path.join(root_dir, '**', f'*{ext}'), recursive=True)
            for f in found:
                if not should_ignore(f):
                     files.append(f)
                     
    return files

def chunk_file(file_path, chunk_size=1000, overlap=100):
    """
    Simple chunking strategy. 
    For code/markdown, splitting by paragraphs or sections is better, 
    but fixed size with overlap is a robust good-enough start.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        print(f"Skipping {file_path}: {e}")
        return []

    chunks = []
    start = 0
    text_len = len(text)

    while start < text_len:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += (chunk_size - overlap)
    
    return chunks

def run_ingest(files=None, root_dir=None, clean=False, tag=None):
    """
    Programmatic entry point for ingestion.
    :param files: List of absolute file paths to ingest.
    :param root_dir: Root directory of the project (default: 2 levels up).
    :param clean: If True, wipe the database before ingestion.
    :param tag: Optional tag to add to metadata (e.g. 'zerotohero').
    """
    if clean:
        print("Cleaning RAG database before ingestion...")
        from clean import clean_database
        clean_database(force=True)

    print("Initializing RAG System...")
    rag = RAGSystem()
    
    if root_dir is None:
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    
    target_files = []
    
    if files:
        log_debug(f"Incremental Ingestion: Processing {len(files)} target(s)...")
        for f in files:
            abs_path = os.path.abspath(f)
            log_debug(f"Checking path: {abs_path}")
            if not os.path.exists(abs_path):
                log_debug(f"Warning: Target not found: {f}")
                continue
            
            if os.path.isdir(abs_path):
                log_debug(f"Scanning directory: {abs_path}")
                # Recursively find files in this directory
                for root, _, filenames in os.walk(abs_path):
                    if should_ignore(root):
                        continue
                    for filename in filenames:
                        file_abs = os.path.join(root, filename)
                        _, ext = os.path.splitext(file_abs)
                        if ext in INCLUDE_EXTENSIONS:
                            target_files.append(file_abs)
            else:
                # Quick extension check for single files
                _, ext = os.path.splitext(abs_path)
                if ext in INCLUDE_EXTENSIONS:
                    target_files.append(abs_path)
                else:
                    log_debug(f"Skipping {f}: Extension {ext} not in whitelist.")
    else:
        log_debug(f"Full Scan: Scanning directory: {root_dir}")
        target_files = get_files_to_ingest(root_dir)
    
    log_debug(f"Found {len(target_files)} files to ingest.")
    
    documents = []
    metadatas = []
    ids = []
    
    for i, file_path in enumerate(target_files):
        log_debug(f"Processing ({i+1}/{len(target_files)}): {file_path}")
        
        # Calculate file metadata
        file_hash = calculate_file_hash(file_path)
        last_modified = os.path.getmtime(file_path)
        
        chunks = chunk_file(file_path)
        if not chunks:
            continue
            
        rel_path = os.path.relpath(file_path, root_dir)
        
        for j, chunk in enumerate(chunks):
            doc_id = f"{rel_path}::{j}"
            documents.append(chunk)
            metadata = {
                "source": rel_path, 
                "chunk_index": j,
                "file_hash": file_hash if file_hash else "",
                "last_modified": last_modified
            }
            if tag:
                metadata["tag"] = tag
            
            metadatas.append(metadata)
            ids.append(doc_id)
            
        # Batch insert every 10 files to avoid memory explosion
        if len(documents) > 100:
            rag.add_documents(documents, metadatas, ids)
            documents = []
            metadatas = []
            ids = []

    # Final flush
    if documents:
        rag.add_documents(documents, metadatas, ids)

    log_debug("Ingestion Complete.")
    return len(target_files)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Ingest files into the RAG system.")
    parser.add_argument('files', metavar='FILE', type=str, nargs='*', help='Specific files to ingest. If empty, scans all.')
    parser.add_argument('--clean', action='store_true', help='Clean the database before ingestion')
    parser.add_argument('--tag', type=str, help='Tag to apply to ingested documents', default=None)
    args = parser.parse_args()

    # Pass args.files (list of strings) directly to run_ingest
    run_ingest(files=args.files, clean=args.clean, tag=args.tag)

if __name__ == "__main__":
    main()
