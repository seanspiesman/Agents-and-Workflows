# Project: PyOrchestra - Autonomous Agent Platform

**Role**: Senior Systems Architect & Full-Stack Engineer
**Objective**: Build a production-grade, locally hosted Autonomous Agent Platform with a Web UI, supporting Multi-GPU execution and MCP integration.

---

## 1. System Architecture & Data Structures

### 1.1 Core Entities (Pydantic / TypeScript Interfaces)

We must define strict contracts between the Backend (Python) and Frontend (TypeScript).

**`Agent` Schema:**
*   `name`: str (Unique identifier)
*   `model`: str (e.g., "gpt-4", "deepseek-coder-v2")
*   `system_prompt`: str
*   `skills`: List[str] (Paths to skill files)
*   `temperature`: float

**`WorkflowStep` Schema:**
*   `id`: str
*   `agent_name`: str
*   `instruction`: str
*   `input_vars`: List[str] (e.g., `["${RepoUrl}"]`)
*   `output_vars`: List[str] (e.g., `["${AnalysisReport}"]`)
*   `dependencies`: List[str] (IDs of previous steps)

**`ExecutionEvent` Schema (WebSocket):**
*   `type`: "log" | "tool_call" | "tool_result" | "agent_thought" | "step_complete" | "error"
*   `timestamp`: float
*   `step_id`: str
*   `content`: Any

### 1.2 Tech Stack
*   **Backend**: Python 3.11+, FastAPI (Async), LiteLLM (Model Gateway)
*   **Frontend**: React (Vite), TailwindCSS, ShadcnUI (optional), XTerm.js (for terminal)
*   **Storage**: SQLite (for run logs), File System (for agents/workflows)

---

## 2. Phase 1: Backend Core (The Engine)

### 2.1 Setup & Dependencies

1.  **Initialize Project**:
    ```bash
    mkdir -p orchestrator/backend
    cd orchestrator/backend
    python -m venv venv
    source venv/bin/activate
    ```

2.  **Dependencies (`requirements.txt`)**:
    *   `fastapi`, `uvicorn[standard]`, `websockets`
    *   `litellm` (Unified LLM Interface)
    *   `pydantic`, `pydantic-settings`
    *   `pytest`, `pytest-asyncio` (Testing)

### 2.2 Core Components

#### A. Global Router (`router.py`)
*   **Responsibility**: Route requests to the correct model server based on the Agent's config.
*   **Logic**:
    *   `"devstral-3090"` -> `http://192.168.1.119:1234/v1`
    *   `"gpt-4"` -> OpenAI API
    *   **Fallback**: If primary fails, retry once, then fail step.

#### B. Execution Engine (`engine.py`)
*   **Responsibility**: The main event loop.
*   **Logic**:
    1.  Load Workflow (DAG).
    2.  Topological Sort steps.
    3.  Iterate steps:
        *   Resolve Inputs (`${Var}`).
        *   Instantiate Agent.
        *   Call LLM via `Router`.
        *   Execute Tools (if called).
        *   Broadcast events via `WebSocketManager`.
        *   Store Outputs.

### 2.3 Unit Testing Strategy (Backend)

**Goal**: 90% Code Coverage on Core Logic.

1.  **Test Router (`tests/test_router.py`)**:
    *   **Case**: Mock LiteLLM. Verify routing logic sends request to correct URL.
    *   **Case**: Simulate Timeout. Verify Retry logic.

2.  **Test Parser (`tests/test_parser.py`)**:
    *   **Case**: Load `ZeroToHero.workflow.md`. Verify graph structure (correct nodes and edges).
    *   **Case**: Malformed Markdown. Verify `ValidationError` is raised.

3.  **Test Engine (`tests/test_engine.py`)**:
    *   **Case**: "Mock Execution". Run a 3-step workflow with a Mock LLM that simply echoes input. Verify variable passing (`Step1 Output` -> `Step2 Input`).

---

## 3. Phase 2: Frontend Command Center

### 3.1 Setup

1.  **Initialize**:
    ```bash
    cd orchestrator
    npm create vite@latest frontend -- --template react-ts
    cd frontend
    npm install -D tailwindcss postcss autoprefixer
    npx tailwindcss init -p
    ```

### 3.2 Core Components

#### A. Terminal Component (`Terminal.tsx`)
*   **Lib**: `xterm.js` + `xterm-addon-fit`.
*   **Logic**: Connect to `ws://localhost:8000/ws`. Render logs with specific colors (Cyan=Agent, Green=Tool, Red=Error).

#### B. Workflow Visualizer (`WorkflowVisualizer.tsx`)
*   **Lib**: `reactflow` (highly recommended for DAGs).
*   **Logic**: Fetch workflow structure JSON. Render nodes. Highlight "Active" node in Yellow, "Completed" in Green.

### 3.3 Unit Testing Strategy (Frontend)

**Goal**: Verify interactivity and state.

1.  **Test Terminal (`src/components/__tests__/Terminal.test.tsx`)**:
    *   **Tool**: `vitest` + `react-testing-library`.
    *   **Case**: Mock WebSocket server. Send a "log" message. Assert text appears in the document.

2.  **Test Workflow State (`src/__tests__/App.test.tsx`)**:
    *   **Case**: Click "Start Workflow". Assert API call is made. Assert status indicator changes to "Running".

---

## 4. Phase 3: Agent & Workflow Parsing

### 4.1 The Parsers

*   **Agent Parser**:
    *   Read Frontmatter (YAML).
    *   Extract System Prompt (Content after `---`).
*   **Workflow Parser**:
    *   Parse custom syntax:
        *   `* **Agent:** [Name](./path)`
        *   `* **Input:** ${Var}`

### 4.2 Integration Testing

1.  **End-to-End Test (`tests/test_e2e.py`)**:
    *   **Setup**: Spin up FastAPI `TestClient`.
    *   **Action**: POST `/workflows/execute` with a dummy workflow.
    *   **Assert**:
        1.  Receive 200 OK.
        2.  WebSocket receives "Job Started".
        3.  WebSocket receives "Step 1 Complete".
        4.  WebSocket receives "Job Finished".

---

## 5. Quality Gates & CI/CD

Before merging any code or considering a phase "Complete", run:

1.  **Backend Linting**:
    ```bash
    ruff check .
    mypy .
    ```
2.  **Backend Tests**:
    ```bash
    pytest --cov=app --cov-report=term-missing
    # Fail if coverage < 80%
    ```
3.  **Frontend Linting**:
    ```bash
    npm run lint
    ```
4.  **Frontend Tests**:
    ```bash
    npm run test
    ```

---

## 6. Implementation Checklist

### Step 1: Foundation
- [ ] Create Directory Structure.
- [ ] Set up `backend/venv` and `frontend/package.json`.
- [ ] Create shared types (Pydantic models).

### Step 2: Backend Logic
- [ ] Implement `Parser` for `.agent.md` files.
- [ ] Implement `Parser` for `.workflow.md` files. (Unit Test this heavily!)
- [ ] Implement `Router` logic for LLMs.

### Step 3: API & Engine
- [ ] Create `FastAPI` app with `/execute` endpoint.
- [ ] Implement `WebSocket` broadcaster.
- [ ] Build the `Engine` loop (Topological sort + Execution).

### Step 4: Frontend UI
- [ ] Build `Terminal` component.
- [ ] Build `WorkflowList` and `WorkflowVisualizer`.
- [ ] Connect Frontend to WebSocket.

### Step 5: Integration
- [ ] Run the "ZeroToHero" workflow through the full system.
