import { useState, useEffect } from 'react';
import {
    ChevronRight,
    ChevronDown,
    Terminal,
    Cpu,
    FileText,
    AlertCircle,
    CheckCircle,
    Play,
    StopCircle
} from 'lucide-react';

interface LogEntry {
    type: string;
    content: string;
    timestamp: number;
    step_id?: string;
}

interface ActivityLogProps {
    websocketUrl?: string;
    onStatusChange?: (status: 'idle' | 'running') => void;
}

export default function ActivityLog({ websocketUrl = 'ws://localhost:8000/ws', onStatusChange }: ActivityLogProps) {
    const [events, setEvents] = useState<LogEntry[]>([]);
    const [expandedSteps, setExpandedSteps] = useState<Set<string>>(new Set());
    const [connectionStatus, setConnectionStatus] = useState<'connected' | 'disconnected'>('disconnected');

    useEffect(() => {
        const ws = new WebSocket(websocketUrl);

        ws.onopen = () => setConnectionStatus('connected');
        ws.onclose = () => setConnectionStatus('disconnected');

        ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);

                // Handle status updates
                if (data.type === 'job_finished' || data.type === 'error' || data.type === 'job_cancelled') {
                    if (onStatusChange) onStatusChange('idle');
                }

                // Auto-expand new steps
                if (data.step_id && !expandedSteps.has(data.step_id)) {
                    setExpandedSteps(prev => new Set(prev).add(data.step_id));
                }

                setEvents(prev => [...prev, data]);
            } catch (e) {
                console.error("Failed to parse WS message", e);
            }
        };

        return () => ws.close();
    }, [websocketUrl]);

    // Group events by step_id
    const groupedEvents = events.reduce((acc, event) => {
        const key = event.step_id || 'system';
        if (!acc[key]) acc[key] = [];
        acc[key].push(event);
        return acc;
    }, {} as Record<string, LogEntry[]>);

    const toggleStep = (stepId: string) => {
        setExpandedSteps(prev => {
            const next = new Set(prev);
            if (next.has(stepId)) next.delete(stepId);
            else next.add(stepId);
            return next;
        });
    };

    return (
        <div className="bg-[#1e1e1e] text-gray-300 font-mono text-sm h-full overflow-y-auto p-4 rounded-lg border border-[#333]">
            <div className="flex justify-between items-center mb-4 pb-2 border-b border-[#333]">
                <span className="flex items-center gap-2">
                    <Terminal size={16} />
                    Mission Control
                </span>
                <span className={`text-xs ${connectionStatus === 'connected' ? 'text-green-500' : 'text-red-500'}`}>
                    {connectionStatus === 'connected' ? '● Live' : '○ Offline'}
                </span>
            </div>

            <div className="space-y-4">
                {Object.entries(groupedEvents).map(([stepId, stepEvents]) => {
                    const isSystem = stepId === 'system';
                    const isExpanded = expandedSteps.has(stepId);

                    // Find generic description from LOG events
                    const titleEvent = stepEvents.find(e => e.type === 'log' && e.content.startsWith('Phase:'));
                    const title = titleEvent
                        ? titleEvent.content.replace('Phase: ', '')
                        : (isSystem ? 'System Notifications' : `Step: ${stepId}`);

                    return (
                        <div key={stepId} className="border border-[#333] rounded overflow-hidden">
                            {/* Header */}
                            <div
                                onClick={() => toggleStep(stepId)}
                                className="bg-[#252526] p-2 flex items-center gap-2 cursor-pointer hover:bg-[#2d2d2d] transition-colors"
                            >
                                {isExpanded ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
                                {isSystem ? <Cpu size={14} className="text-blue-400" /> : <Play size={14} className="text-green-400" />}
                                <span className="font-semibold truncate">{title}</span>
                            </div>

                            {/* Body */}
                            {isExpanded && (
                                <div className="bg-[#1e1e1e] p-2 space-y-2 border-t border-[#333]">
                                    {stepEvents.map((ev, idx) => (
                                        <LogItem key={idx} event={ev} />
                                    ))}
                                </div>
                            )}
                        </div>
                    );
                })}
            </div>
        </div>
    );
}

function LogItem({ event }: { event: LogEntry }) {
    switch (event.type) {
        case 'agent_thought':
            return (
                <div className="pl-4 text-gray-400 text-xs italic">
                    🤔 {event.content}
                </div>
            );
        case 'tool_call':
            return (
                <div className="pl-4 text-yellow-500">
                    🛠️ Executing: <span className="font-semibold">{event.content}</span>
                </div>
            );
        case 'tool_result':
            return (
                <div className="pl-6 text-gray-500 text-xs border-l-2 border-[#333] ml-4">
                    Result: {event.content.slice(0, 200)}{event.content.length > 200 ? '...' : ''}
                </div>
            );
        case 'step_complete':
            return (
                <div className="pl-4 text-green-500 font-bold">
                    <CheckCircle size={14} className="inline mr-2" />
                    Step Completed
                </div>
            );
        case 'error':
            return (
                <div className="pl-4 text-red-500 bg-red-900/10 p-2 rounded">
                    <AlertCircle size={14} className="inline mr-2" />
                    {event.content}
                </div>
            );
        case 'job_cancelled':
            return (
                <div className="pl-4 text-orange-500 font-bold">
                    <StopCircle size={14} className="inline mr-2" />
                    Cancelled
                </div>
            );
        case 'log':
            if (event.content.startsWith('FILE_UPDATE:')) {
                return (
                    <div className="pl-4 text-blue-400 font-semibold bg-blue-900/10 p-1 rounded my-1">
                        <FileText size={14} className="inline mr-2" />
                        {event.content}
                    </div>
                );
            }
            if (event.content.startsWith('Phase:')) return null; // Skip header logs
            return <div className="pl-4 text-gray-400">{event.content}</div>;

        case 'job_started':
        case 'job_finished':
            return <div className="text-center text-xs text-gray-600 uppercase tracking-widest my-2">- {event.content} -</div>;

        default:
            return <div className="pl-4 text-gray-500">{event.content}</div>;
    }
}
