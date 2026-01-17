import { useEffect, useRef } from 'react';
import { Terminal } from 'xterm';
import { FitAddon } from 'xterm-addon-fit';
import 'xterm/css/xterm.css';

interface TerminalComponentProps {
    websocketUrl?: string;
    onStatusChange?: (status: 'idle' | 'running') => void;
}

export default function TerminalComponent({ websocketUrl = 'ws://localhost:8000/ws', onStatusChange }: TerminalComponentProps) {
    const terminalRef = useRef<HTMLDivElement>(null);
    const xtermRef = useRef<Terminal | null>(null);
    const wsRef = useRef<WebSocket | null>(null);

    useEffect(() => {
        if (!terminalRef.current) return;

        // Initialize XTerm
        const term = new Terminal({
            cursorBlink: true,
            fontSize: 14,
            fontFamily: 'Menlo, Monaco, "Courier New", monospace',
            theme: {
                background: '#0a0a0a',
                foreground: '#00ff00',
            },
        });

        const fitAddon = new FitAddon();
        term.loadAddon(fitAddon);
        term.open(terminalRef.current);
        fitAddon.fit();
        xtermRef.current = term;

        term.writeln('🚀 PyOrchestra Terminal');
        term.writeln('Connecting to WebSocket...');

        // WebSocket Connection
        const ws = new WebSocket(websocketUrl);
        wsRef.current = ws;

        ws.onopen = () => {
            term.writeln('✅ Connected to backend');
        };

        ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                const timestamp = new Date(data.timestamp * 1000).toLocaleTimeString();

                // Color-coded output based on event type
                switch (data.type) {
                    case 'log':
                        term.writeln(`\x1b[36m[${timestamp}] LOG:\x1b[0m ${data.content}`);
                        break;
                    case 'agent_thought':
                        term.writeln(`\x1b[35m[${timestamp}] AGENT:\x1b[0m ${data.content}`);
                        break;
                    case 'tool_call':
                        term.writeln(`\x1b[33m[${timestamp}] TOOL:\x1b[0m ${data.content}`);
                        break;
                    case 'step_complete':
                        term.writeln(`\x1b[32m[${timestamp}] ✓ STEP COMPLETE\x1b[0m`);
                        break;
                    case 'error':
                        term.writeln(`\x1b[31m[${timestamp}] ERROR:\x1b[0m ${data.content}`);
                        if (onStatusChange) onStatusChange('idle');
                        break;
                    case 'job_started':
                        term.writeln(`\x1b[1;32m[${timestamp}] 🎬 ${data.content}\x1b[0m`);
                        break;
                    case 'job_finished':
                        term.writeln(`\x1b[1;32m[${timestamp}] 🎉 ${data.content}\x1b[0m`);
                        if (onStatusChange) onStatusChange('idle');
                        break;
                    default:
                        term.writeln(`[${timestamp}] ${JSON.stringify(data)}`);
                }
            } catch (e) {
                term.writeln(`[RAW] ${event.data}`);
            }
        };

        ws.onerror = () => {
            term.writeln('\x1b[31m❌ WebSocket error\x1b[0m');
        };

        ws.onclose = () => {
            term.writeln('\x1b[33m⚠️  WebSocket disconnected\x1b[0m');
        };

        // Cleanup
        return () => {
            ws.close();
            term.dispose();
        };
    }, [websocketUrl]);

    return <div ref={terminalRef} style={{ height: '100%', width: '100%' }} />;
}
