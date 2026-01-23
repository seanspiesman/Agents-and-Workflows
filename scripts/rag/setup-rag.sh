#!/bin/bash
# scripts/setup-rag.sh

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$HOME/Library/Application Support/Code - Insiders/rag_env"

echo -e "${YELLOW}Setting up RAG environment...${NC}"

# Check for Python 3.11 (preferred for compatibility)
if command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3.11"
elif command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    echo "python3 could not be found. Please install Python 3."
    exit 1
fi

echo -e "${YELLOW}Using Python: $PYTHON_CMD${NC}"

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}Creating virtual environment at $VENV_DIR...${NC}"
    $PYTHON_CMD -m venv "$VENV_DIR"
else
    echo -e "${GREEN}Virtual environment already exists.${NC}"
fi

# Activate venv
source "$VENV_DIR/bin/activate"

# Upgrade pip
echo -e "${YELLOW}Upgrading pip...${NC}"
pip install --upgrade pip

# Install requirements
if [ -f "$SCRIPT_DIR/requirements.txt" ]; then
    echo -e "${YELLOW}Installing requirements...${NC}"
    pip install -r "$SCRIPT_DIR/requirements.txt"
else
    echo "requirements.txt not found!"
    exit 1
fi

echo -e "${GREEN}RAG environment setup complete!${NC}"
echo -e "To use manually: source .venv/bin/activate"
