import pytest
import os
from backend.parser import Parser
from backend.schemas import Workflow, Agent

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')

def test_parse_agent_valid():
    """Test parsing a valid agent file."""
    agent_path = os.path.join(FIXTURES_DIR, 'test.agent.md')
    agent = Parser.parse_agent(agent_path)
    
    assert agent.name == "TestAgent"
    assert agent.model == "gpt-4"
    assert agent.temperature == 0.5
    assert len(agent.skills) > 0
    assert "Test Agent" in agent.system_prompt

def test_parse_workflow_valid():
    """Test parsing a valid workflow file."""
    workflow_path = os.path.join(FIXTURES_DIR, 'test.workflow.md')
    workflow = Parser.parse_workflow(workflow_path)
    
    assert workflow.name == "Test Workflow"
    assert len(workflow.steps) == 2
    
    # Verify first step
    step1 = workflow.steps[0]
    assert step1.agent_name == "TestAgent"
    assert "${InputData}" in step1.input_vars
    assert "${AnalysisResult}" in step1.output_vars
    
def test_parse_agent_invalid_format():
    """Test parsing an invalid agent file."""
    # Create temporary invalid file
    invalid_path = os.path.join(FIXTURES_DIR, 'invalid.agent.md')
    with open(invalid_path, 'w') as f:
        f.write("Invalid content without frontmatter")
    
    with pytest.raises(ValueError):
        Parser.parse_agent(invalid_path)
    
    # Cleanup
    os.remove(invalid_path)
