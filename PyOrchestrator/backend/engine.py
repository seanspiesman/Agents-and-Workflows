import asyncio
import json
import re
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from fastapi import WebSocket
from schemas import Workflow, ExecutionEvent, ExecutionEventType, Agent
from router import ModelRouter
from parser import Parser
from tools import ToolExecutor

class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, event: ExecutionEvent):
        message = event.model_dump_json()
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                # Handle disconnection gracefully
                pass

class ExecutionEngine:
    def __init__(self, ws_manager: WebSocketManager):
        self.ws_manager = ws_manager
        self.router = ModelRouter()
        self.tool_executor = ToolExecutor()
        self.context: Dict[str, Any] = {} # Variable store
        self.current_task: Optional[asyncio.Task] = None
        
    @staticmethod
    def _load_resources(resource_paths: List[str], resource_type: str = "skill") -> str:
        """
        Loads content from skill/instruction/collection paths.
        Supports both file paths and directories (reads SKILL.md/README.md inside).
        """
        loaded_content = []
        for path in resource_paths:
            try:
                resource_path = Path(path)
                if resource_path.is_dir():
                    # Look for common resource files
                    for filename in ["SKILL.md", "README.md", "content.md", "index.md"]:
                        candidate = resource_path / filename
                        if candidate.exists():
                            content = candidate.read_text()
                            loaded_content.append(f"## [{resource_type.upper()}] {resource_path.name}\n{content}")
                            break
                elif resource_path.is_file():
                    content = resource_path.read_text()
                    loaded_content.append(f"## [{resource_type.upper()}] {resource_path.stem}\n{content}")
            except Exception as e:
                print(f"Warning: Could not load {resource_type} from {path}: {e}")
        return "\n\n".join(loaded_content)

    async def run_workflow(self, workflow_path: str, inputs: Dict[str, Any] = None):
        """
        Executes a workflow from a file path.
        """
        try:
            # 0. Merge inputs into context
            if inputs:
                self.context.update(inputs)

            workflow = Parser.parse_workflow(workflow_path)
            
            await self.ws_manager.broadcast(ExecutionEvent(
                type=ExecutionEventType.JOB_STARTED,
                content=f"Starting workflow: {workflow.name}"
            ))

            for step in workflow.steps:
                # Check for cancellation
                if asyncio.current_task().cancelled():
                    raise asyncio.CancelledError()

                # 1. Resolve Inputs
                prompt = step.instruction
                for var in step.input_vars:
                    # Naive strict replacement ${Var} -> value
                    key = var.replace("${", "").replace("}", "")
                    if key in self.context:
                        prompt = prompt.replace(var, str(self.context[key]))
                
                await self.ws_manager.broadcast(ExecutionEvent(
                    type=ExecutionEventType.LOG,
                    step_id=step.id,
                    content=f"Phase: {step.agent_name} - {prompt[:50]}..."
                ))

                # 2. Get Agent
                agent_file = None
                # Search for agent file
                potential_paths = [
                    f"../custom-agents/agents/{step.agent_name.lower()}.agent.md",
                    f"../../custom-agents/agents/{step.agent_name.lower()}.agent.md",
                    f"custom-agents/agents/{step.agent_name.lower()}.agent.md"
                ]
                
                agent = None
                for path in potential_paths:
                    if os.path.exists(path):
                        try:
                            agent = Parser.parse_agent(path)
                            break
                        except Exception as e:
                            print(f"Error parsing agent {path}: {e}")
                
                # Fallback if agent file not found
                if not agent:
                    agent = Agent(
                        name=step.agent_name,
                        model="m4-max", # Default fallback
                        system_prompt=f"You are the {step.agent_name}. Execute the task."
                    )
                
                # Determine Model ID based on Agent Config or Hardcoded Override
                # (Keeping your mac/local logic for now, but ideally this comes from .agent.md)
                model_name = "m4-max" 
                if "3090" in step.agent_name or "3090" in agent.model:
                     model_name = "devstral-3090"
                elif "Mac" in step.agent_name or "m4" in agent.model:
                     model_name = "m4-max"

                # Construct System Prompt with Tools
                from tools import TOOL_DEFINITIONS
                output_dir = os.path.abspath("agent-output")
                tool_instructions = f"""
You have access to the following tools:
{json.dumps(TOOL_DEFINITIONS, indent=2)}

OUTPUT DIRECTORY: {output_dir}
All files you create should be saved to this directory or its subdirectories.

To use a tool, you MUST output a line in the format:
TOOL_CALL: tool_name({{"arg": "value", ...}})

Examples:
TOOL_CALL: write_file({{"path": "{output_dir}/strategy/Product-Brief.md", "content": "# Product Brief\\n..."}})
TOOL_CALL: read_file({{"path": "{output_dir}/strategy/Product-Brief.md"}})
TOOL_CALL: execute_shell({{"command": "ls -la {output_dir}"}})

IMPORTANT: Always create files before trying to read them in subsequent steps.
Only use one tool per response unless instructed otherwise.
"""
                # Load Skills referenced by agent
                skills_content = ""
                if agent.skills:
                    skills_content = self._load_resources(agent.skills, "skill")
                    if skills_content:
                        skills_content = "\n\n# SKILLS & KNOWLEDGE\n" + skills_content
                
                final_system_prompt = agent.system_prompt + "\n\n" + tool_instructions + skills_content
                
                messages = [
                    {"role": "system", "content": final_system_prompt},
                    {"role": "user", "content": prompt}
                ]

                # 3. Call Router
                try:
                    response = await self.router.chat_completion(
                        model=model_name, 
                        messages=messages
                    )
                except Exception as e:
                    await self.ws_manager.broadcast(ExecutionEvent(
                        type=ExecutionEventType.ERROR,
                        step_id=step.id,
                        content=str(e)
                    ))
                    return

                # DEBUG: Log raw response
                print(f"[DEBUG] Agent: {step.agent_name}")
                print(f"[DEBUG] Response (first 500 chars): {response[:500]}")
                
                # 4. Check for tool calls in response
                tool_calls = self._extract_tool_calls(response)
                print(f"[DEBUG] Extracted tool calls: {tool_calls}")
                if tool_calls:
                    for tool_call in tool_calls:
                        await self.ws_manager.broadcast(ExecutionEvent(
                            type=ExecutionEventType.TOOL_CALL,
                            step_id=step.id,
                            content=f"{tool_call['name']}({tool_call['arguments']})"
                        ))
                        
                        # Define callback
                        async def on_file_update(path, status):
                            await self.ws_manager.broadcast(ExecutionEvent(
                                type=ExecutionEventType.LOG,
                                step_id=step.id,
                                content=f"FILE_UPDATE: {path} ({status})"
                            ))

                        tool_result = await self.tool_executor.execute_tool(
                            tool_call['name'],
                            tool_call['arguments'],
                            on_file_update=on_file_update
                        )
                        
                        await self.ws_manager.broadcast(ExecutionEvent(
                            type=ExecutionEventType.TOOL_RESULT,
                            step_id=step.id,
                            content=tool_result
                        ))
                        
                        # Append tool result to response
                        response += f"\n\n[Tool Result]: {tool_result}"

                # 5. Store Outputs
                # Naively map the entire response to the first output variable
                if step.output_vars:
                    # Just taking the first var for now
                    first_var = step.output_vars[0].replace("${", "").replace("}", "")
                    self.context[first_var] = response

                await self.ws_manager.broadcast(ExecutionEvent(
                    type=ExecutionEventType.STEP_COMPLETE,
                    step_id=step.id,
                    content=response
                ))

            await self.ws_manager.broadcast(ExecutionEvent(
                type=ExecutionEventType.JOB_FINISHED,
                content="Workflow completed successfully."
            ))

        except asyncio.CancelledError:
            await self.ws_manager.broadcast(ExecutionEvent(
                type=ExecutionEventType.JOB_CANCELLED,
                content="Workflow execution cancelled by user."
            ))

        except Exception as e:
            await self.ws_manager.broadcast(ExecutionEvent(
                type=ExecutionEventType.ERROR,
                content=f"Workflow failed: {str(e)}"
            ))
        
        finally:
            self.current_task = None
            
    async def stop_workflow(self):
        """
        Stops the currently running workflow.
        """
        if self.current_task:
            self.current_task.cancel()
            try:
                await self.current_task
            except asyncio.CancelledError:
                pass

    def _extract_tool_calls(self, response: str) -> List[Dict[str, Any]]:
        """
        Extract tool calls from LLM response.
        Simple pattern: TOOL_CALL: function_name({"arg": "value"})
        """
        tool_calls = []
        pattern = r'TOOL_CALL:\s*(\w+)\((.*?)\)'
        matches = re.finditer(pattern, response, re.DOTALL)
        
        for match in matches:
            function_name = match.group(1)
            args_str = match.group(2).strip()
            
            try:
                # Try to parse as JSON
                arguments = json.loads(args_str)
                tool_calls.append({
                    "name": function_name,
                    "arguments": arguments
                })
            except json.JSONDecodeError:
                # If not JSON, treat as plain dict-like string
                pass
        
        return tool_calls

