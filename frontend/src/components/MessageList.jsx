import React, { useEffect, useRef } from 'react';
import Message from './Message';
import TypingIndicator from './TypingIndicator';
import '../styles/chat.css';

const MessageList = ({ messages, isTyping }) => {
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages, isTyping]);

    return (
        <div className="message-list">
            {messages.map((message, index) => (
                <Message
                    key={index}
                    message={message}
                    isBot={message.isBot}
                />
            ))}
            {isTyping && (
                <div className="message-wrapper bot">
                    <div className="message bot-message typing">
                        <TypingIndicator />
                    </div>
                </div>
            )}
            <div ref={messagesEndRef} />
        </div>
    );
};

export default MessageList;
