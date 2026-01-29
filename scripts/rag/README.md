# RAG System & MCP Server

This directory contains the Retrieval-Augmented Generation (RAG) system for the agent ecosystem, implemented as a Model Context Protocol (MCP) server.

## Contents

- **`mcp_server.py`**: The core MCP server that exposes the `rag_search` tool.
- **`rag_core.py`**: Handles ChromaDB interactions and embeddings.
- **`ingest.py`**: Scans the codebase and populates the vector database.
- **`setup-rag.sh`**: Sets up the Python virtual environment and installs dependencies.
- **`rag_ingest`**: Wrapper script to run ingestion.
- **`start-rag-mcp.sh`**: Startup script for the MCP server.

## Helper Scripts

All helper scripts are self-contained and can be run from this directory or the project root.

### Setup
The RAG system uses a centralized virtual environment shared across all your projects to save space and time.

**Run Setup**: Run the setup script from any project repository to initialize/update the shared environment:

- **Primary Repository:** `bash scripts/rag/setup-rag.sh`
- **Synced Projects:** `bash .github/rag/setup-rag.sh`

This will create/update the virtual environment in `~/Library/Application Support/Code - Insiders/rag_env`. You only need to run this once per machine (or when dependencies change).

### Ingestion (Indexing)

You can ingest the entire workspace or specific files/folders.

**Full Workspace Scan:**
Runs a complete scan of the project (respecting `.gitignore` and common excludes).
```bash
./scripts/rag/rag_ingest
```

**Targeted Ingestion:**
Pass specific files or directories as arguments.
```bash
./scripts/rag/rag_ingest path/to/file.py path/to/folder/
```

*Note: For synced projects, the script is located at `.github/rag/rag_ingest`.*

### Cleaning (Reset)

If your RAG database is cluttered or out of date, you can wipe it clean.

**Clean Database:**
```bash
./scripts/rag/rag_clean
```
This will remove the ChromaDB directory. You should run `rag_ingest` afterwards to rebuild it.

### Manual Search (via MCP)
Can be run via an MCP client.

## VS Code Configuration
To use this MCP server automatically in VS Code (with an MCP client extension), add the following to your `${workspaceFolder}/.vscode/mcp.json`. 

**Safe Configuration Features:**
-   **Portable**: Works in both the primary repository and any synced projects.
-   **Zero-Config Sync**: Once synced via `sync-agents.sh`, this configuration works out-of-the-box in the target repo.
-   **Project-Scoped**: STRICTLY looks for the script in the current project or `.github` folder. Fails safely if not found, preventing it from accidentally checking out other projects.
-   **Centralized**: Automatically uses the shared virtual environment in `~/Library/Application Support/Code - Insiders/rag_env`.

```json
{
  "mcpServers": {
    "rag-search": {
      "command": "bash",
      "args": [
        "-c",
        "if [ -f 'scripts/rag/start-rag-mcp.sh' ]; then bash 'scripts/rag/start-rag-mcp.sh'; elif [ -f '.github/rag/start-rag-mcp.sh' ]; then bash '.github/rag/start-rag-mcp.sh'; else echo 'RAG startup script not found in current project' >&2; exit 1; fi"
      ],
      "env": { "PYTHONUNBUFFERED": "1" },
      "cwd": "${workspaceFolder}"
    }
  }
}
```

## Manual Client Configuration
If you are using a different MCP client, configure it to run the startup script using the same logic above to ensure portability.
