import React, { useState } from 'react';
import { Graph } from 'react-d3-graph';
import axios from 'axios';
import './App.css';

function InputAutomaton() {
    const [nodes, setNodes] = useState([]);
    const [links, setLinks] = useState([]);
    const [selectedNode, setSelectedNode] = useState(null);
    const [initialState, setInitialState] = useState('');
    const [finalStates, setFinalStates] = useState('');
    const [probabilityThreshold, setProbabilityThreshold] = useState('');

    const addNode = () => {
        const newNode = {
            id: `Node ${nodes.length + 1}`,
            x: 400,
            y: 300
        };
        setNodes([...nodes, newNode]);
    };

    const addLink = () => {
        if (!selectedNode) {
            alert('Select a node first');
            return;
        }
        const targetNode = prompt('Enter target node:');
        if (targetNode) {
            const newLink = { source: selectedNode, target: targetNode, action: '', probability: '' };
            setLinks([...links, newLink]);
        }
    };

    const updateLink = (index, field, value) => {
        const updatedLinks = [...links];
        updatedLinks[index][field] = value;
        setLinks(updatedLinks);
    };

    const handleNodeClick = (nodeId) => {
        setSelectedNode(nodeId);
    };

    const sendAutomaton = () => {
        const automaton = {
            nodes,
            links,
            initialState,
            finalStates: finalStates.split(',').map(s => s.trim()),
            probabilityThreshold
        };
        axios.post('http://localhost:5000/api/automaton', automaton)
            .then(response => {
                alert(response.data);
            })
            .catch(error => {
                console.error('There was an error sending the automaton!', error);
            });
    };

    const graphData = {
        nodes,
        links: links.map(link => ({
            ...link,
            label: `Action: ${link.action}, Prob: ${link.probability}`
        }))
    };

    const graphConfig = {
        node: { color: 'lightblue', size: 400, fontSize: 16 },
        link: { renderLabel: true, fontSize: 12 }
    };

    return (
        <div className="container">
            <h1>Quantum Automaton</h1>
            <div>
                <button onClick={addNode}>Add State</button>
                <button onClick={addLink}>Add Transition</button>
                <button onClick={sendAutomaton}>Send Automaton</button>
            </div>
            <div className="input-container">
                <label>
                    Initial State:
                    <input
                        type="text"
                        value={initialState}
                        onChange={(e) => setInitialState(e.target.value)}
                    />
                </label>
                <label>
                    Final States (comma separated):
                    <input
                        type="text"
                        value={finalStates}
                        onChange={(e) => setFinalStates(e.target.value)}
                    />
                </label>
                <label>
                    Probability Threshold:
                    <input
                        type="text"
                        value={probabilityThreshold}
                        onChange={(e) => setProbabilityThreshold(e.target.value)}
                    />
                </label>
            </div>
            <div className="graph-container">
                <Graph
                    id="graph-id"
                    data={graphData}
                    config={graphConfig}
                    onClickNode={handleNodeClick}
                />
            </div>
            <div className="link-list">
                {links.map((link, index) => (
                    <div key={index} className="link-item">
                        <span>{link.source} -> {link.target}</span>
                        <input
                            type="text"
                            placeholder="Action"
                            value={link.action}
                            onChange={(e) => updateLink(index, 'action', e.target.value)}
                        />
                        <input
                            type="text"
                            placeholder="Probability"
                            value={link.probability}
                            onChange={(e) => updateLink(index, 'probability', e.target.value)}
                        />
                    </div>
                ))}
            </div>
        </div>
    );
}

export default InputAutomaton;