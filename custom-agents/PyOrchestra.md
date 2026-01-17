# PROMPT: Bootstrap Custom Agent Platform

**Role**: Senior Systems Architect & Full-Stack Engineer  
**Objective**: Build a production-grade, locally hosted Autonomous Agent Platform with a Web UI, supporting Multi-GPU execution and MCP integration.

## Context
I have a localized workflow system defined in Markdown ([.agent.md](file:///Users/work/Documents/GitHub/Agents-and-Workflows/custom-agents/agents/qa.agent.md) and [.workflow.md](file:///Users/work/Documents/GitHub/Agents-and-Workflows/custom-agents/workflows/BugFix.workflow.md) files). I typically use VS Code extensions (Continue, Cline) but they lack the autonomy and multi-model routing I need. I possess two powerful local inference servers:
1.  **M4 Max** (Mac): `http://localhost:1234/v1` (High Context, Reasoning)
2.  **RTX 3090** (Linux): `http://192.168.1.119:1234/v1` (Fast, Coding)

## The Task
Generate the complete scaffolding and core implementation for a custom application: **"The Orchestrator"**.

### 1. Technology Stack
*   **Backend**: Python **FastAPI** (Async, WebSockets for streaming).
*   **Frontend**: **React** (Vite) + **TailwindCSS** (Dark Mode, Cyberpunk/Terminal aesthetic).
*   **LLM Interface**: **LiteLLM** or **OpenAI-Python** used polymorphically.
*   **Tooling**: Native Python tools + **Model Context Protocol (MCP)** client support.

### 2. Core Features to Implement
*   **Workflow Parser**: A robust regex/markdown parser that converts my existing [ZeroToHero.workflow.md](file:///Users/work/Documents/GitHub/Agents-and-Workflows/custom-agents/workflows/ZeroToHero.workflow.md) into an executable Directed Acyclic Graph (DAG) or sequential list.
*   **Agent Loader**: Dynamically loads `custom-agents/*.agent.md` and identifying System Prompts.
*   **Routing Engine**: A configuration system that routes specific Agents to specific API Endpoints (M4 vs 3090).
*   **Live Dashboard**: A Web UI that shows:
    *   The current active Phase/Step.
    *   A live scrolling terminal of Agent thoughts & Tool outputs.
    *   Token usage metrics per model.

### 3. Specific Deliverables
Please generate the following file structure and key code components:

```text
orchestrator/
├── backend/
│   ├── app.py              # FastAPI entry
│   ├── engine.py           # The Core Loop
│   ├── router.py           # Model Routing
│   ├── mcp_client.py       # MCP Integration
│   └── tools.py            # Native Tools
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Terminal.tsx
│   │   │   ├── ModelSelector.tsx
│   │   │   └── WorkflowVisualizer.tsx
│   │   └── App.tsx
├── config.yaml             # Initial config
└── requirements.txt
```

### 4. Critical Constraints
*   **Robustness**: The backend must recover from Model API timeouts.
*   **Tooling**: Ensure `execute_shell_command` is non-blocking or handles long-running processes (like `npm install`) gracefully via WebSocket updates.
*   **Aesthetics**: The UI should look like a professional mission control center.

---

**Begin by analyzing the architecture, critiquing potential bottlenecks (specifically reasoning loop latency vs WebSocket broadcast), and then writing the Foundation Code.**
