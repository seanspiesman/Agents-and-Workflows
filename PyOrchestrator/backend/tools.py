import subprocess
import os
import json
from typing import Dict, Any, List
from pathlib import Path

class ToolExecutor:
    """Handles execution of native tools."""
    
    @staticmethod
    async def execute_tool(tool_name: str, arguments: Dict[str, Any], on_file_update=None) -> str:
        """
        Executes a tool by name with given arguments.
        Returns the result as a string.
        """
        tools = {
            "execute_shell": ToolExecutor.execute_shell,
            "read_file": ToolExecutor.read_file,
            "write_file": ToolExecutor.write_file,
            "list_directory": ToolExecutor.list_directory,
        }
        
        if tool_name not in tools:
            return f"Error: Unknown tool '{tool_name}'"
        
        try:
            result = await tools[tool_name](**arguments)
            
            # Post-execution hooks
            if tool_name == "write_file" and on_file_update:
                path = arguments.get("path")
                if path:
                    await on_file_update(path, "created/modified")
                    
            return result
        except Exception as e:
            return f"Error executing {tool_name}: {str(e)}"
    
    @staticmethod
    async def execute_shell(command: str, timeout: int = 30, cwd: str = None) -> str:
        """
        Executes a shell command with timeout.
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=cwd
            )
            
            output = result.stdout
            if result.stderr:
                output += f"\n[STDERR]: {result.stderr}"
            if result.returncode != 0:
                output += f"\n[EXIT CODE]: {result.returncode}"
                
            return output or "Command executed successfully (no output)"
        except subprocess.TimeoutExpired:
            return f"Error: Command timed out after {timeout} seconds"
        except Exception as e:
            return f"Error: {str(e)}"
    
    @staticmethod
    async def read_file(path: str) -> str:
        """Reads a file and returns its contents."""
        try:
            with open(path, 'r') as f:
                content = f.read()
            return f"File: {path}\n\n{content}"
        except FileNotFoundError:
            return f"Error: File not found: {path}"
        except Exception as e:
            return f"Error reading file: {str(e)}"
    
    @staticmethod
    async def write_file(path: str, content: str) -> str:
        """Writes content to a file."""
        try:
            # Create parent directories if they don't exist
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            
            with open(path, 'w') as f:
                f.write(content)
            return f"Successfully wrote to {path}"
        except Exception as e:
            return f"Error writing file: {str(e)}"
    
    @staticmethod
    async def list_directory(path: str = ".") -> str:
        """Lists contents of a directory."""
        try:
            items = os.listdir(path)
            output = f"Contents of {path}:\n"
            for item in sorted(items):
                full_path = os.path.join(path, item)
                item_type = "DIR" if os.path.isdir(full_path) else "FILE"
                output += f"  [{item_type}] {item}\n"
            return output
        except Exception as e:
            return f"Error listing directory: {str(e)}"

# Tool definitions for LLM (to be included in system prompts)
TOOL_DEFINITIONS = [
    {
        "name": "execute_shell",
        "description": "Execute a shell command",
        "parameters": {
            "command": "The shell command to execute",
            "timeout": "Timeout in seconds (default: 30)",
            "cwd": "Working directory (optional)"
        }
    },
    {
        "name": "read_file",
        "description": "Read contents of a file",
        "parameters": {
            "path": "Path to the file to read"
        }
    },
    {
        "name": "write_file",
        "description": "Write content to a file",
        "parameters": {
            "path": "Path to the file to write",
            "content": "Content to write to the file"
        }
    },
    {
        "name": "list_directory",
        "description": "List contents of a directory",
        "parameters": {
            "path": "Directory path (default: current directory)"
        }
    }
]
