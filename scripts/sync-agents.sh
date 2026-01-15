#!/bin/bash

# Sync Agents Script
# Syncs the custom-agents folder from Agents-and-Workflows to all .github folders in Documents

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

# Find all .github directories in Documents
# We want to find the .github folder itself.
echo -e "${YELLOW}Searching for .github folders...${NC}"
TARGET_DIRS=()
# Simpler find command: find directories named .github, exclude node_modules
while IFS= read -r -d '' dir; do
    TARGET_DIRS+=("$dir")
done < <(find "$DOCUMENTS_DIR" -type d -name ".github" -not -path "*/node_modules/*" -print0 2>/dev/null)

# Display found directories
if [ ${#TARGET_DIRS[@]} -eq 0 ]; then
    echo -e "${YELLOW}No .github folders found in Documents.${NC}"
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
    
    # Parent project directory (dirname of .github)
    PROJECT_ROOT="$(dirname "$target_dir")"
    
    # 1. Update .gitignore
    GITIGNORE_FILE="$PROJECT_ROOT/.gitignore"
    if [ ! -f "$GITIGNORE_FILE" ]; then
        echo -e "  Creating .gitignore and adding .github"
        echo ".github" > "$GITIGNORE_FILE"
    else
        # Check if .github is already ignored
        if ! grep -q "^.github" "$GITIGNORE_FILE" && ! grep -q "^/.github" "$GITIGNORE_FILE"; then
            echo -e "  Adding .github to .gitignore"
            # Ensure newline before appending if file not empty
            if [ -s "$GITIGNORE_FILE" ] && [ "$(tail -c1 "$GITIGNORE_FILE" | wc -l)" -eq 0 ]; then
                echo "" >> "$GITIGNORE_FILE"
            fi
            echo ".github" >> "$GITIGNORE_FILE"
        else
            echo -e "  .github already in .gitignore"
        fi
    fi

    local_fail=0
    
    # 2. Iterate through folders in custom-agents and sync them
    for item in "$SOURCE_DIR"/*; do
        basename_item=$(basename "$item")
        
        # Skip files in root if any (only sync directories typically)
        if [ ! -d "$item" ]; then
            continue
        fi

        target_sub_dir="$target_dir/$basename_item"
        mkdir -p "$target_sub_dir"

        if [ "$basename_item" == "workflows" ]; then
            # SAFE SYNC for workflows: Do NOT delete existing files (GitHub Actions)
            echo -e "  Syncing ${basename_item} (safe mode)..."
            if rsync -av "$item/" "$target_sub_dir/"; then
                echo -e "    ✓ ${basename_item} synced"
            else
                echo -e "    ${RED}✗ ${basename_item} sync failed${NC}"
                local_fail=1
            fi
        else
            # STRICT SYNC for others: Delete unknown files
            echo -e "  Syncing ${basename_item} (strict mode)..."
            if rsync -av --delete "$item/" "$target_sub_dir/"; then
                echo -e "    ✓ ${basename_item} synced"
            else
                echo -e "    ${RED}✗ ${basename_item} sync failed${NC}"
                local_fail=1
            fi
        fi
    done

    if [ $local_fail -eq 0 ]; then
        ((SUCCESS_COUNT++))
    else
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
