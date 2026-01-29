# Setup Guide for Agents-and-Workflows

This guide outlines the steps to set up the **Agents-and-Workflows** environment from scratch on your local machine.

## Prerequisites

*   **Operating System**: macOS (Recommended), Linux, or Windows (WSL recommended).
*   **VS Code**: [Visual Studio Code](https://code.visualstudio.com/) or [VS Code Insiders](https://code.visualstudio.com/insiders/).
*   **Python**: Python 3.11 or higher installed.
*   **Extensions**:
    *   **GitHub Copilot**: For agent interactions.
    *   (Optional) **Continue**: If using Continue as your AI assistant.

## 1. Environment Initialization (RAG System)

The project uses a Retrieval-Augmented Generation (RAG) system running as a Model Context Protocol (MCP) server. This requires a Python environment setup.

1.  **Open a Terminal** in the root of the `Agents-and-Workflows` repository.
2.  **Run the Setup Script**:
    This script creates a shared virtual environment (default: `~/Library/Application Support/Code - Insiders/rag_env`) and installs necessary dependencies (`chromadb`, `mcp`, `numpy`, etc.).

    ```bash
    ./scripts/rag/setup-rag.sh
    ```

3.  **Verify Installation**:
    If successful, you should see:
    > RAG environment setup complete!

## 2. Populate the RAG Database

Before the agents can "remember" or "search" your codebase, you need to ingest the files into the local vector database.

1.  **Run Ingestion**:
    ```bash
    ./scripts/rag/rag_ingest
    ```
    This scans the current directory (respecting `.gitignore`) and populates the ChromaDB database.

    *Note: You should re-run this command periodically or after significant code changes to keep the RAG index up-to-date.*

## 3. Configure VS Code MCP

VS Code needs to know how to connect to the local RAG MCP server.

1.  **Check Configuration**:
    Ensure the `.vscode/mcp.json` file exists in your project root. It should look like this:

    ```json
    {
      "servers": {
        "RAG": {
          "command": "bash",
          "args": [
            "-c",
            "if [ -f 'scripts/rag/start-rag-mcp.sh' ]; then bash 'scripts/rag/start-rag-mcp.sh'; elif [ -f '.github/rag/start-rag-mcp.sh' ]; then bash '.github/rag/start-rag-mcp.sh'; else echo 'RAG startup script not found in current project' >&2; exit 1; fi"
          ],
          "env": {
            "PYTHONUNBUFFERED": "1"
          },
          "cwd": "${workspaceFolder}"
        }
      }
    }
    ```

2.  **Restart VS Code / Reload Window**:
    After confirming the file exists, reload your VS Code window (`Cmd+Shift+P` -> `Developer: Reload Window`) to ensure the MCP server starts operation.

## 4. Verification

To verify that the setup is working:

1.  Open **GitHub Copilot Chat** (or your preferred MCP client).
2.  Ask a question that requires codebase context, or explicitly ask it to use the `rag_search` tool:
    > "Can you use the RAG tool to search for 'task.md references' in the codebase?"
3.  If the tool is called and returns results, your setup is complete!

## 5. Troubleshooting

*   **Python command not found**: Ensure `python3` is in your PATH. The setup script prefers `python3.11`.
*   **Dependencies fail to install**: Check for build errors. On macOS, you might need Xcode command line tools (`xcode-select --install`).
*   **MCP Server doesn't start**: Check the **Output** panel in VS Code and select "MCP" or "GitHub Copilot" to see logs. Ensure `scripts/rag/start-rag-mcp.sh` is executable (`chmod +x scripts/rag/start-rag-mcp.sh`).
*   **Database acts weird**: Reset it by running `./scripts/rag/rag_clean` and then re-ingesting.

## 6. Project Structure Overview

*   `custom-agents/`: Contains all agent definitions (`.agent.md`) and instructions.
*   `scripts/rag/`: Contains RAG system code, ingestion scripts, and MCP server logic.
*   `.vscode/mcp.json`: Configuration for the MCP server.
*   `agent-output/`: Directory where agents write their output artifacts.

## 7. Additional MCP Servers Setup

To enable the full range of agent capabilities (including mobile testing, browser automation, and sequential thinking), you need to configure additional MCP servers.

### Prerequisites

1.  **Node.js**: Install Node.js v18+ (LTS recommended).
    ```bash
    node -v
    npm -v
    ```
2.  **Homebrew** (macOS): Required for iOS Simulator tools.
3.  **Python 3.11**: Required for iOS Simulator python bindings.
4.  **pipx**: Recommended for installing python tools in isolated environments.
    ```bash
    brew install pipx
    pipx ensurepath
    ```

### iOS Simulator Setup (macOS only)

The `ios-simulator` MCP allows agents to interact with the iOS Simulator.

1.  **Install idb-companion**:
    ```bash
    brew install facebook/idb-companion
    ```
2.  **Install fb-idb**:
    ```bash
    pipx install fb-idb
    ```
3.  **Find Paths**:
    You will need the paths to `idb_companion` and the `fb-idb` python site-packages for the configuration.
    *   `IDB_COMPANION_PATH`: Usually `/opt/homebrew/bin/idb_companion` (Apple Silicon) or `/usr/local/bin/idb_companion` (Intel).
    *   `PYTHONPATH`: Find where pipx installed fb-idb. It usually looks like `~/.local/pipx/venvs/fb-idb/lib/python3.11/site-packages`.

### Context7 Setup (Upstash)

The `context7` MCP requires an API key.

1.  **Get API Key**: Obtain your Context7 API key from Upstash.
2.  **Add to VS Code Secrets**:
    The configuration uses `${input:CONTEXT7_API_KEY}`. When you first run it, VS Code might prompt you, or you can hardcode it in the config (not recommended for shared machines).

### Updated MCP Configuration

Update your `.vscode/mcp.json` to include these new servers along with the RAG server.

**Note on Paths**: Update `PATH`, `IDB_COMPANION_PATH`, and `PYTHONPATH` in the `ios-simulator` section to match your actual local paths.

```json
{
  "servers": {
    "RAG": {
      "command": "bash",
      "args": [
        "-c",
        "if [ -f 'scripts/rag/start-rag-mcp.sh' ]; then bash 'scripts/rag/start-rag-mcp.sh'; elif [ -f '.github/rag/start-rag-mcp.sh' ]; then bash '.github/rag/start-rag-mcp.sh'; else echo 'RAG startup script not found in current project' >&2; exit 1; fi"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      },
      "cwd": "${workspaceFolder}"
    },
    "microsoft/playwright-mcp": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "@playwright/mcp@latest"
      ],
      "gallery": "https://api.mcp.github.com",
      "version": "0.0.1-seed"
    },
    "io.github.ChromeDevTools/chrome-devtools-mcp": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "chrome-devtools-mcp@0.12.1"
      ],
      "gallery": "https://api.mcp.github.com",
      "version": "0.12.1"
    },
    "ios-simulator": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "-y",
        "ios-simulator-mcp"
      ],
      "env": {
        "PATH": "/usr/local/bin:/usr/bin:/bin:/opt/homebrew/bin",
        "IDB_COMPANION_PATH": "/opt/homebrew/bin/idb_companion",
        "PYTHONPATH": "${userHome}/.local/pipx/venvs/fb-idb/lib/python3.11/site-packages"
      }
    },
    "io.github.upstash/context7": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "@upstash/context7-mcp@1.0.31"
      ],
      "env": {
        "CONTEXT7_API_KEY": "${input:CONTEXT7_API_KEY}"
      },
      "gallery": "https://api.mcp.github.com",
      "version": "1.0.31"
    },
    "sequential-thinking": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-sequential-thinking"
      ]
    }
  },
  "inputs": [
    {
      "id": "CONTEXT7_API_KEY",
      "type": "promptString",
      "description": "Enter your Upstash Context7 API Key",
      "password": true
    }
  ]
}
```
