#!/bin/bash
# scripts/start-rag-mcp.sh
set -e

# Get directories
# Get directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Environment Discovery
GLOBAL_VENV="$HOME/Library/Application Support/Code - Insiders/rag_env"
LOCAL_VENV="$(dirname "$(dirname "$SCRIPT_DIR")")/.venv"

if [ -d "$GLOBAL_VENV" ]; then
    VENV_DIR="$GLOBAL_VENV"
elif [ -d "$LOCAL_VENV" ]; then
    VENV_DIR="$LOCAL_VENV"
else
    echo "RAG environment not found (checked $GLOBAL_VENV and $LOCAL_VENV)" >&2
    echo "Please run scripts/rag/setup-rag.sh first" >&2
    exit 1
fi

# Run the MCP server using the venv python
"$VENV_DIR/bin/python" "$SCRIPT_DIR/mcp_server.py"
