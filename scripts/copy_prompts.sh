#!/bin/bash

# Define source and destination
# Resolve absolute path to custom-agents
SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/custom-agents"
DEST_DIR="/Users/work/Library/Application Support/Code - Insiders/User/prompts"

# Check if source directory exists
if [ ! -d "$SOURCE_DIR" ]; then
    echo "Error: Source directory '$SOURCE_DIR' does not exist."
    exit 1
fi

# Create destination directory if it doesn't exist
if [ ! -d "$DEST_DIR" ]; then
    echo "Creating destination directory: $DEST_DIR"
    mkdir -p "$DEST_DIR"
fi

# Sync contents using rsync to preserve structure and update efficiently
echo "Syncing contents from $SOURCE_DIR to $DEST_DIR..."
# -a: archive mode (preserves permissions, timestamps, etc.)
# -v: verbose
# --delete: remove files in dest that are not in source (clean sync)
rsync -av --delete "$SOURCE_DIR/" "$DEST_DIR/"

if [ $? -eq 0 ]; then
    echo "Successfully synced custom-agents to prompts directory."
else
    echo "Error: Failed to sync files."
    exit 1
fi
