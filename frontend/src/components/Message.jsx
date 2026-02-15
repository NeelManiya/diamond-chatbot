import React from 'react';
import '../styles/chat.css';

const Message = ({ message, isBot }) => {
    const formatTime = (timestamp) => {
        const date = new Date(timestamp);
        return date.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    return (
        <div className={`message-wrapper ${isBot ? 'bot' : 'user'}`}>
            <div className={`message ${isBot ? 'bot-message' : 'user-message'}`}>
                <div className="message-content">{message.content}</div>
                <div className="message-time">
                    {formatTime(message.timestamp)}
                </div>
            </div>
        </div>
    );
};

export default Message;
