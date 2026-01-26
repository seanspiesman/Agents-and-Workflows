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

### Manual Search (via MCP)
Can be run via an MCP client.

## VS Code Configuration
To use this MCP server automatically in VS Code (with an MCP client extension), add the following to your `${workspaceFolder}/.vscode/mcp.json`. 

**Universal Configuration Features:**
-   **Portable**: Works in both the primary repository and any synced projects.
-   **Zero-Config Sync**: Once synced via `sync-agents.sh`, this configuration works out-of-the-box in the target repo.
-   **Smart Discovery**: Uses Mac's Spotlight (`mdfind`) as a fallback to locate the RAG script if the server starts in a different directory.
-   **Centralized**: Automatically uses the shared virtual environment in `~/Library/Application Support/Code - Insiders/rag_env`.

```json
{
  "mcpServers": {
    "rag-search": {
      "command": "bash",
      "args": [
        "-c",
        "for p in 'scripts/rag/start-rag-mcp.sh' '.github/rag/start-rag-mcp.sh'; do if [ -f \"$p\" ]; then bash \"$p\"; exit; fi; done; SCRIPT=$(mdfind \"kMDItemFSName == 'start-rag-mcp.sh'\" | xargs ls -ut 2>/dev/null | head -n 1); if [ -n \"$SCRIPT\" ]; then bash \"$SCRIPT\"; else echo 'RAG startup script not found' >&2; exit 1; fi"
      ],
      "env": { "PYTHONUNBUFFERED": "1" }
    }
  }
}
```

## Manual Client Configuration
If you are using a different MCP client, configure it to run the startup script using the same logic above to ensure portability.
