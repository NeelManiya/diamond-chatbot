import React, { useState } from 'react';
import '../styles/chat.css';

const MessageInput = ({ onSendMessage, disabled }) => {
    const [message, setMessage] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if (message.trim() && !disabled) {
            onSendMessage(message);
            setMessage('');
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit(e);
        }
    };

    return (
        <form className="message-input-container" onSubmit={handleSubmit}>
            <div className="message-input-wrapper">
                <input
                    type="text"
                    className="message-input"
                    placeholder="Type a message..."
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    onKeyPress={handleKeyPress}
                    disabled={disabled}
                />
                <button
                    type="submit"
                    className="send-button"
                    disabled={!message.trim() || disabled}
                >
                    <svg
                        viewBox="0 0 24 24"
                        width="24"
                        height="24"
                        fill="currentColor"
                    >
                        <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" />
                    </svg>
                </button>
            </div>
        </form>
    );
};

export default MessageInput;
