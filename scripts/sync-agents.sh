#!/bin/bash

# Sync Agents Script
# Syncs the custom-agents folder from Agents-and-Workflows to all .github/agents folders in Documents

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Source directory (this repository's custom-agents folder)
SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/custom-agents"
DOCUMENTS_DIR="$HOME/Documents"

echo -e "${YELLOW}======================================${NC}"
echo -e "${YELLOW}Agent Folder Sync Tool${NC}"
echo -e "${YELLOW}======================================${NC}"
echo ""
echo -e "Source: ${GREEN}${SOURCE_DIR}${NC}"
echo -e "Searching in: ${GREEN}${DOCUMENTS_DIR}${NC}"
echo ""

# Check if source directory exists
if [ ! -d "$SOURCE_DIR" ]; then
    echo -e "${RED}Error: Source directory not found: ${SOURCE_DIR}${NC}"
    exit 1
fi

# Find all .github/agents directories in Documents
echo -e "${YELLOW}Searching for .github/agents folders...${NC}"
TARGET_DIRS=()
while IFS= read -r -d '' dir; do
    TARGET_DIRS+=("$dir")
done < <(find "$DOCUMENTS_DIR" -type d -path "*/.github/agents" -print0 2>/dev/null)

# Display found directories
if [ ${#TARGET_DIRS[@]} -eq 0 ]; then
    echo -e "${YELLOW}No .github/agents folders found in Documents.${NC}"
    exit 0
fi

echo -e "${GREEN}Found ${#TARGET_DIRS[@]} target folder(s):${NC}"
for dir in "${TARGET_DIRS[@]}"; do
    echo "  - $dir"
done
echo ""

# Ask for confirmation
read -p "Do you want to sync agents to these folders? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Sync cancelled.${NC}"
    exit 0
fi

# Sync to each target
echo ""
echo -e "${YELLOW}Starting sync...${NC}"
SUCCESS_COUNT=0
FAIL_COUNT=0

for target_dir in "${TARGET_DIRS[@]}"; do
    echo ""
    echo -e "${YELLOW}Syncing to:${NC} $target_dir"
    
    # Create backup if target exists
    if [ -d "$target_dir" ]; then
        backup_dir="${target_dir}.backup.$(date +%Y%m%d_%H%M%S)"
        echo -e "  Creating backup: ${backup_dir}"
        cp -R "$target_dir" "$backup_dir"
    fi
    
    # Create parent directory if needed
    mkdir -p "$(dirname "$target_dir")"
    
    # Sync using rsync (preserves structure, deletes files not in source)
    if rsync -av --delete "$SOURCE_DIR/" "$target_dir/"; then
        echo -e "  ${GREEN}✓ Synced successfully${NC}"
        ((SUCCESS_COUNT++))
    else
        echo -e "  ${RED}✗ Sync failed${NC}"
        ((FAIL_COUNT++))
    fi
done

# Summary
echo ""
echo -e "${YELLOW}======================================${NC}"
echo -e "${YELLOW}Sync Complete${NC}"
echo -e "${YELLOW}======================================${NC}"
echo -e "${GREEN}Successful: ${SUCCESS_COUNT}${NC}"
if [ $FAIL_COUNT -gt 0 ]; then
    echo -e "${RED}Failed: ${FAIL_COUNT}${NC}"
fi
echo ""
echo -e "${YELLOW}Note: Backups were created with .backup.[timestamp] suffix${NC}"
