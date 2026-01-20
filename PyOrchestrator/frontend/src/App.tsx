import { useState, useEffect, useCallback } from 'react';
import ActivityLog from './components/ActivityLog';
import './App.css';

interface OptionsData {
  workflows: string[];
  prompts: string[];
  workflows_dir?: string;
  prompts_dir?: string;
}

function App() {
  const [workflowPath, setWorkflowPath] = useState('');
  const [guideFile, setGuideFile] = useState('');
  const [options, setOptions] = useState<OptionsData>({ workflows: [], prompts: [] });
  const [status, setStatus] = useState<'idle' | 'running'>('idle');

  // Custom directory paths
  const [workflowsDir, setWorkflowsDir] = useState('');
  const [promptsDir, setPromptsDir] = useState('');
  const [showSettings, setShowSettings] = useState(false);

  const fetchOptions = useCallback(() => {
    const params = new URLSearchParams();
    if (workflowsDir) params.append('workflows_dir', workflowsDir);
    if (promptsDir) params.append('prompts_dir', promptsDir);

    fetch(`http://localhost:8000/options?${params.toString()}`)
      .then(res => res.json())
      .then(data => {
        setOptions(data);
        if (data.workflows.length > 0 && !workflowPath) setWorkflowPath(data.workflows[0]);
        // Update directory fields with resolved paths if not already set
        if (data.workflows_dir && !workflowsDir) setWorkflowsDir(data.workflows_dir);
        if (data.prompts_dir && !promptsDir) setPromptsDir(data.prompts_dir);
      })
      .catch(err => console.error("Failed to fetch options", err));
  }, [workflowsDir, promptsDir, workflowPath]);

  useEffect(() => {
    fetchOptions();
  }, []);

  const handleExecute = async () => {
    setStatus('running');
    try {
      const inputs = guideFile ? { "GuideFile": guideFile } : {};

      const response = await fetch('http://localhost:8000/execute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          workflow_path: workflowPath,
          inputs: inputs
        }),
      });

      if (response.ok) {
        console.log('Workflow started');
      }
    } catch (error) {
      console.error('Failed to start workflow:', error);
      setStatus('idle');
    }
  };

  const handleStop = async () => {
    try {
      await fetch('http://localhost:8000/stop', { method: 'POST' });
      setStatus('idle');
    } catch (error) {
      console.error('Failed to stop workflow:', error);
    }
  };

  return (
    <div className="container">
      <div className="header">
        <h1>🎯 PyOrchestra</h1>
        <p className="subtitle">Autonomous Agent Platform</p>
        <button
          className="settings-toggle"
          onClick={() => setShowSettings(!showSettings)}
        >
          ⚙️ {showSettings ? 'Hide Settings' : 'Settings'}
        </button>
      </div>

      {showSettings && (
        <div className="settings-panel">
          <div className="settings-row">
            <label>Workflows Directory:</label>
            <input
              type="text"
              value={workflowsDir}
              onChange={e => setWorkflowsDir(e.target.value)}
              className="input"
              placeholder="e.g., /path/to/workflows"
            />
          </div>
          <div className="settings-row">
            <label>Prompts Directory:</label>
            <input
              type="text"
              value={promptsDir}
              onChange={e => setPromptsDir(e.target.value)}
              className="input"
              placeholder="e.g., /path/to/prompts"
            />
          </div>
          <button onClick={fetchOptions} className="button refresh-button">
            🔄 Refresh Options
          </button>
        </div>
      )}

      <div className="controls">
        <select
          value={workflowPath}
          onChange={(e) => setWorkflowPath(e.target.value)}
          className="input select-input"
        >
          <option value="" disabled>Select Workflow</option>
          {options.workflows.map(wf => (
            <option key={wf} value={wf}>{wf.split('/').pop()?.replace('.workflow.md', '')}</option>
          ))}
        </select>

        <select
          value={guideFile}
          onChange={(e) => setGuideFile(e.target.value)}
          className="input select-input"
        >
          <option value="">No Guide File (Optional)</option>
          {options.prompts.map(p => (
            <option key={p} value={p}>{p.split('/').pop()?.replace('.md', '')}</option>
          ))}
        </select>

        <div className="button-group">
          <button
            onClick={handleExecute}
            disabled={!workflowPath || status === 'running'}
            className="button"
          >
            {status === 'running' ? '⏳ Running' : '▶️ Execute'}
          </button>
          {status === 'running' && (
            <button
              onClick={handleStop}
              className="button stop-button"
            >
              ⏹ Stop
            </button>
          )}
        </div>
      </div>

      <div className="terminal-container">
        <ActivityLog onStatusChange={(s) => setStatus(s)} />
      </div>
    </div>
  );
}

export default App;
