import re
import yaml
import os
from typing import List, Dict, Tuple, Optional
from schemas import Agent, Workflow, WorkflowStep

class Parser:
    @staticmethod
    def parse_agent(file_path: str) -> Agent:
        """
        Parses a .agent.md file into an Agent object.
        """
        with open(file_path, 'r') as f:
            content = f.read()
            
        # Split Frontmatter (YAML) and System Prompt
        parts = content.split('---')
        if len(parts) < 3:
            raise ValueError(f"Invalid agent file format: {file_path}")
            
        frontmatter_yaml = parts[1]
        system_prompt = "---".join(parts[2:]).strip()
        
        metadata = yaml.safe_load(frontmatter_yaml)
        
        name = metadata.get('name', 'Unknown')
        model = metadata.get('model', 'gpt-3.5-turbo') 
        skills = metadata.get('skills', [])
        
        normalized_skills = []
        base_dir = os.path.dirname(file_path)
        for skill in skills:
            abs_path = os.path.normpath(os.path.join(base_dir, skill))
            normalized_skills.append(abs_path)

        return Agent(
            name=name,
            model=model,
            system_prompt=system_prompt,
            skills=normalized_skills,
            temperature=metadata.get('temperature', 0.7)
        )

    @staticmethod
    def parse_workflow(file_path: str) -> Workflow:
        """
        Enhanced parser that supports multiple workflow formats:
        1. Original format: * **Agent:** [Name] with **Instruction:** lines
        2. Phase-based format: ### Phase X with **Primary Agent**: sections
        """
        # Resolve file path if it doesn't exist
        if not os.path.exists(file_path):
            # Try searching in parent directories (up to 2 levels)
            for i in range(1, 3):
                parent_path = os.path.join("../" * i, file_path)
                if os.path.exists(parent_path):
                    file_path = parent_path
                    break
        
        with open(file_path, 'r') as f:
            content = f.read()
            
        # Extract frontmatter if present
        parts = content.split('---')
        metadata = {}
        if len(parts) >= 3:
            try:
                metadata = yaml.safe_load(parts[1]) or {}
            except:
                metadata = {}
            body = "---".join(parts[2:])
        else:
            body = content
            # Try to extract name from first H1
            h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            if h1_match:
                metadata['name'] = h1_match.group(1).strip()

        # Try phase-based parsing first (user's format)
        steps = Parser._parse_phase_format(body)
        
        # Fallback to original format if no phases found
        if not steps:
            steps = Parser._parse_original_format(body)
            
        return Workflow(
            name=metadata.get('name', 'Untitled Workflow'),
            steps=steps
        )
    
    @staticmethod
    def _parse_phase_format(body: str) -> List[WorkflowStep]:
        """
        Parse phase-based workflow format like:
        ### Phase 1: Strategy (Roadmap, Researcher, Critic)
        - **Primary Agent**: Roadmap
        - **Goal**: Define what to build
        - **Actions**:
            1. Context Analysis
            2. Vision Definition
        - **Input**: `file.md`
        - **Output**: `report.md`
        """
        steps = []
        
        # Find all phases
        phase_pattern = r'###\s+Phase\s+(\d+)[:\s]+([^\n\(]+)(?:\(([^\)]+)\))?'
        phase_matches = list(re.finditer(phase_pattern, body, re.IGNORECASE))
        
        if not phase_matches:
            return []
        
        for i, match in enumerate(phase_matches):
            phase_num = match.group(1)
            phase_name = match.group(2).strip()
            agents_in_parens = match.group(3) or ""
            
            # Get the content until next phase or end
            start_pos = match.end()
            end_pos = phase_matches[i + 1].start() if i + 1 < len(phase_matches) else len(body)
            phase_content = body[start_pos:end_pos]
            
            # Extract primary agent(s)
            agent_match = re.search(r'\*\*Primary\s+Agents?\*\*[:\s]+([^\n]+)', phase_content, re.IGNORECASE)
            if agent_match:
                agent_name = agent_match.group(1).strip()
                # Clean up agent name - take first one if comma-separated
                agent_name = agent_name.split(',')[0].strip()
                agent_name = re.sub(r'\(.*?\)', '', agent_name).strip()
            elif agents_in_parens:
                # Use first agent from parentheses
                agent_name = agents_in_parens.split(',')[0].strip()
            else:
                agent_name = "Orchestrator"
            
            # Extract goal as instruction
            goal_match = re.search(r'\*\*Goal\*\*[:\s]+([^\n]+)', phase_content, re.IGNORECASE)
            instruction = goal_match.group(1).strip() if goal_match else phase_name
            
            # Also look for Actions to enrich the instruction
            actions_match = re.search(r'\*\*Actions\*\*[:\s]*\n((?:\s+\d+\..*\n?)+)', phase_content, re.IGNORECASE)
            if actions_match:
                actions_text = actions_match.group(1)
                action_items = re.findall(r'\d+\.\s+\*\*([^*]+)\*\*', actions_text)
                if action_items:
                    instruction += " Steps: " + ", ".join(action_items[:3])  # First 3 actions
            
            # Extract inputs
            input_vars = []
            input_matches = re.findall(r'\*\*Input\*\*[:\s]+`?([^`\n]+)`?', phase_content, re.IGNORECASE)
            for inp in input_matches:
                input_vars.append(f"${{{inp.strip()}}}")
            
            # Extract outputs
            output_vars = []
            output_matches = re.findall(r'\*\*Output\*\*[:\s]+`?([^`\n]+)`?', phase_content, re.IGNORECASE)
            for out in output_matches:
                output_vars.append(f"${{{out.strip()}}}")
            
            # Create step
            step = WorkflowStep(
                id=f"phase_{phase_num}",
                agent_name=agent_name,
                instruction=instruction,
                input_vars=input_vars,
                output_vars=output_vars,
                dependencies=[f"phase_{int(phase_num) - 1}"] if int(phase_num) > 0 else []
            )
            steps.append(step)
        
        return steps
    
    @staticmethod
    def _parse_original_format(body: str) -> List[WorkflowStep]:
        """
        Parse original format:
        * **Agent:** [Name](path)
            * **Input:** ${var}
            * **Instruction:** "Do something"
            * **Output:** ${result}
        """
        steps = []
        lines = body.split('\n')
        current_step = {}
        
        for line in lines:
            line = line.strip()
            
            # Detect Agent Step - multiple patterns
            agent_patterns = [
                r'\*\s+\*\*Agent:\*\*\s+\[(.*?)\]',  # * **Agent:** [Name]
                r'\*\*Agent\*\*[:\s]+\[(.*?)\]',     # **Agent**: [Name]
                r'-\s+\*\*Agent:\*\*\s+\[(.*?)\]',   # - **Agent:** [Name]
            ]
            
            for pattern in agent_patterns:
                agent_match = re.search(pattern, line)
                if agent_match:
                    if current_step:
                        steps.append(WorkflowStep(**current_step))
                    
                    agent_name = agent_match.group(1)
                    current_step = {
                        "id": f"step_{len(steps) + 1}",
                        "agent_name": agent_name,
                        "instruction": "",
                        "input_vars": [],
                        "output_vars": [],
                        "dependencies": [f"step_{len(steps)}"] if steps else []
                    }
                    break

            # Detect Instruction
            instr_patterns = [
                r'\*\s+\*\*Instruction:\*\*\s+"(.*?)"',
                r'\*\*Instruction\*\*[:\s]+"(.*?)"',
                r'\*\s+\*\*Instruction:\*\*\s+(.+)',
            ]
            for pattern in instr_patterns:
                instr_match = re.search(pattern, line)
                if instr_match and current_step:
                    current_step["instruction"] = instr_match.group(1).strip().strip('"')
                    break

            # Detect Input
            input_match = re.search(r'\*\*Input:?\*\*[:\s]+(.+)', line, re.IGNORECASE)
            if input_match and current_step:
                raw_inputs = input_match.group(1).split(',')
                current_step["input_vars"] = [x.strip().strip('`') for x in raw_inputs]
                
            # Detect Output
            output_match = re.search(r'\*\*Output:?\*\*[:\s]+(.+)', line, re.IGNORECASE)
            if output_match and current_step:
                raw_outputs = output_match.group(1).split(',')
                current_step["output_vars"] = [x.strip().strip('`') for x in raw_outputs]

        # Add last step
        if current_step:
            steps.append(WorkflowStep(**current_step))
            
        return steps
