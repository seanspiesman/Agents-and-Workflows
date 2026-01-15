#!/bin/bash

# Define source and destination
SOURCE_DIR="./agents"
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

# Copy contents
echo "Copying contents from $SOURCE_DIR to $DEST_DIR..."
cp -R "$SOURCE_DIR/" "$DEST_DIR/"

if [ $? -eq 0 ]; then
    echo "Successfully copied agents to prompts directory."
else
    echo "Error: Failed to copy files."
    exit 1
fi
