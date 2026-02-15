import { Link } from 'react-router-dom';

const ChatHeader = () => {
    return (
        <div className="chat-header">
            <div className="header-content">
                <div className="bot-avatar">
                    <svg viewBox="0 0 24 24" width="40" height="40" fill="white">
                        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z" />
                    </svg>
                </div>
                <div className="bot-info">
                    <h2 className="bot-name">Diamond Assistant</h2>
                    <p className="bot-status">
                        <span className="status-indicator"></span>
                        Online
                    </p>
                </div>
            </div>
            <Link to="/insight" className="insight-link" style={{ color: 'white', textDecoration: 'none', padding: '5px 10px', background: 'rgba(255,255,255,0.2)', borderRadius: '4px', fontSize: '0.8rem' }}>
                Insights
            </Link>
        </div>
    );
};

export default ChatHeader;
