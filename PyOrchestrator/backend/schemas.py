from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict
from enum import Enum
import time

class ExecutionEventType(str, Enum):
    LOG = "log"
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"
    AGENT_THOUGHT = "agent_thought"
    STEP_COMPLETE = "step_complete"
    ERROR = "error"
    JOB_STARTED = "job_started"
    JOB_FINISHED = "job_finished"
    JOB_CANCELLED = "job_cancelled"

class Agent(BaseModel):
    name: str
    model: str
    system_prompt: str
    skills: List[str] = Field(default_factory=list)
    temperature: float = 0.7
    
class WorkflowStep(BaseModel):
    id: str
    agent_name: str
    instruction: str
    input_vars: List[str] = Field(default_factory=list)
    output_vars: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    
class ExecutionEvent(BaseModel):
    type: ExecutionEventType
    timestamp: float = Field(default_factory=time.time)
    step_id: Optional[str] = None
    content: Any

class Workflow(BaseModel):
    name: str = "Unknown"
    steps: List[WorkflowStep]
