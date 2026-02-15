import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import '../styles/chat.css'; // Reuse existing styles for consistency

const Insight = () => {
    const [stats, setStats] = useState(null);
    const [logs, setLogs] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const statsRes = await axios.get('http://localhost:8000/insight/stats');
                setStats(statsRes.data);

                const logsRes = await axios.get('http://localhost:8000/insight/logs');
                setLogs(logsRes.data.logs);
            } catch (error) {
                console.error("Error fetching insight data:", error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
        const interval = setInterval(fetchData, 5000); // Refresh every 5 seconds
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="chat-container">
            <div className="chat-header">
                <h1>System Insights</h1>
                <Link to="/" style={{ color: 'white', textDecoration: 'none', marginLeft: '20px', fontSize: '14px' }}>Back to Chat</Link>
            </div>
            
            <div className="messages-area" style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '20px' }}>
                {loading ? (
                    <p>Loading insights...</p>
                ) : (
                    <>
                        <div className="stats-card" style={{ background: '#f5f5f5', padding: '15px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
                            <h2 style={{ borderBottom: '1px solid #ddd', paddingBottom: '10px', marginBottom: '10px' }}>Knowledge Base Stats</h2>
                            {stats ? (
                                <ul style={{ listStyle: 'none', padding: 0 }}>
                                    {Object.entries(stats).map(([key, value]) => (
                                        <li key={key} style={{ padding: '5px 0' }}>
                                            <strong>{key.replace(/_/g, ' ').toUpperCase()}:</strong> {JSON.stringify(value)}
                                        </li>
                                    ))}
                                </ul>
                            ) : (
                                <p>No stats available</p>
                            )}
                        </div>

                        <div className="logs-card" style={{ background: '#1e1e1e', color: '#00ff00', padding: '15px', borderRadius: '8px', fontFamily: 'monospace', height: '400px', overflowY: 'auto' }}>
                            <h2 style={{ color: 'white', borderBottom: '1px solid #444', paddingBottom: '10px', marginBottom: '10px' }}>System Logs</h2>
                            <div className="logs-content">
                                {logs.map((log, index) => (
                                    <div key={index} style={{ whiteSpace: 'pre-wrap', marginBottom: '4px' }}>{log}</div>
                                ))}
                            </div>
                        </div>
                    </>
                )}
            </div>
        </div>
    );
};

export default Insight;
