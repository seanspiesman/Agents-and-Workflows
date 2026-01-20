---
name: Test Workflow
description: Simple test workflow for validation
---

# Test Workflow

## Step 1: Analysis
*   **Agent:** [TestAgent](./test.agent.md)
    *   **Input:** `${InputData}`
    *   **Instruction:** "Analyze the input data"
    *   **Output:** `${AnalysisResult}`

## Step 2: Processing
*   **Agent:** [TestAgent](./test.agent.md)
    *   **Input:** `${AnalysisResult}`
    *   **Instruction:** "Process the analysis results"
    *   **Output:** `${FinalReport}`
