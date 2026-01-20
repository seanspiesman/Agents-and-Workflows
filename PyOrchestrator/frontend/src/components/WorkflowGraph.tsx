import { useCallback, useEffect, useState } from 'react';
import ReactFlow, {
    Node,
    Edge,
    Controls,
    Background,
    useNodesState,
    useEdgesState,
    MarkerType,
} from 'reactflow';
import 'reactflow/dist/style.css';

interface WorkflowGraphProps {
    workflowData?: any;
    activeStepId?: string;
}

export default function WorkflowGraph({ workflowData, activeStepId }: WorkflowGraphProps) {
    const [nodes, setNodes, onNodesChange] = useNodesState([]);
    const [edges, setEdges, onEdgesChange] = useEdgesState([]);

    useEffect(() => {
        if (!workflowData || !workflowData.steps) return;

        // Convert workflow steps to React Flow nodes
        const newNodes: Node[] = workflowData.steps.map((step: any, index: number) => ({
            id: step.id,
            type: 'default',
            position: { x: 250, y: index * 150 },
            data: {
                label: `${step.agent_name}\n${step.instruction.substring(0, 30)}...`
            },
            style: {
                background: step.id === activeStepId ? '#00ff88' : '#1a1a1a',
                color: step.id === activeStepId ? '#000' : '#fff',
                border: '2px solid #00ff88',
                borderRadius: '8px',
                padding: '10px',
                width: 200,
            },
        }));

        // Convert dependencies to edges
        const newEdges: Edge[] = [];
        workflowData.steps.forEach((step: any) => {
            step.dependencies?.forEach((depId: string) => {
                newEdges.push({
                    id: `${depId}-${step.id}`,
                    source: depId,
                    target: step.id,
                    type: 'smoothstep',
                    animated: step.id === activeStepId,
                    style: { stroke: '#00ff88' },
                    markerEnd: {
                        type: MarkerType.ArrowClosed,
                        color: '#00ff88',
                    },
                });
            });
        });

        setNodes(newNodes);
        setEdges(newEdges);
    }, [workflowData, activeStepId, setNodes, setEdges]);

    return (
        <div style={{ height: '400px', background: '#0a0a0a', borderRadius: '12px', border: '1px solid #00ff88' }}>
            <ReactFlow
                nodes={nodes}
                edges={edges}
                onNodesChange={onNodesChange}
                onEdgesChange={onEdgesChange}
                fitView
            >
                <Background color="#00ff88" gap={16} />
                <Controls />
            </ReactFlow>
        </div>
    );
}
