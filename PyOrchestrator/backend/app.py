from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, WebSocket, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from engine import ExecutionEngine, WebSocketManager
import asyncio
import os
from pathlib import Path
from typing import List, Dict, Any, Optional


app = FastAPI(title="PyOrchestra")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ws_manager = WebSocketManager()
engine = ExecutionEngine(ws_manager)

from typing import Dict, Any, Optional

class RequestRun(BaseModel):
    workflow_path: str
    inputs: Optional[Dict[str, Any]] = None

@app.get("/")
def health_check():
    return {"status": "ok", "service": "pyorchestra-backend"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            # Keep alive loop
            await websocket.receive_text()
    except Exception:
        ws_manager.disconnect(websocket)

@app.post("/execute")
async def execute_workflow(request: RequestRun):
    """
    Triggers a workflow execution in the background.
    """
    # Create task manually to store reference
    task = asyncio.create_task(engine.run_workflow(request.workflow_path, request.inputs))
    engine.current_task = task
    return {"status": "started", "workflow": request.workflow_path}


def scan_files(directory: str, extension: str) -> List[str]:
    """Recursively find files with specific extension."""
    files_list = []
    base_path = Path(directory)
    if not base_path.exists():
        return []
        
    for path in base_path.rglob(f"*{extension}"):
        # relative path from the directory being scanned? 
        # Actually user probably wants relative to backend so they can just pass it
        # But for UI display we might want just the name. 
        # Let's return the relative path from project root or backend.
        # Since engine searches relative to backend (or parent), let's try to normalize.
        try:
           # Get path relative to the backend folder (which is where app.py is running)
           # current cwd is backend/
           rel = os.path.relpath(path, os.getcwd())
           files_list.append(rel)
        except Exception:
           files_list.append(str(path))
           
    return sorted(files_list)

@app.get("/options")
def get_options(workflows_dir: Optional[str] = None, prompts_dir: Optional[str] = None):
    """Returns available workflows and prompts."""
    # Compute project root from app.py location
    backend_dir = Path(__file__).parent
    project_root = backend_dir.parent.parent
    
    # Use provided dirs or defaults
    wf_dir = Path(workflows_dir) if workflows_dir else project_root / "custom-agents" / "workflows"
    pr_dir = Path(prompts_dir) if prompts_dir else project_root / "ZeroToHeroPrompts"
    
    workflows = scan_files(str(wf_dir), ".workflow.md")
    prompts = scan_files(str(pr_dir), ".md")
    
    return {
        "workflows": workflows,
        "prompts": prompts,
        "workflows_dir": str(wf_dir),
        "prompts_dir": str(pr_dir)
    }

@app.post("/stop")
async def stop_workflow():
    """
    Stops the currently running workflow.
    """
    await engine.stop_workflow()
    return {"status": "stopped"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
