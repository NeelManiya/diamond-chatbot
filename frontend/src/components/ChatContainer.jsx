import React, { useState, useEffect } from 'react';
import ChatHeader from './ChatHeader';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import { chatAPI } from '../services/api';
import '../styles/chat.css';

const ChatContainer = () => {
    const [messages, setMessages] = useState([]);
    const [isTyping, setIsTyping] = useState(false);
    const [sessionId] = useState(() => `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`);
    const [error, setError] = useState(null);

    useEffect(() => {
        // Load greeting message on mount
        loadGreeting();
    }, []);

    const loadGreeting = async () => {
        try {
            setIsTyping(true);
            const response = await chatAPI.getGreeting(sessionId);

            setMessages([{
                content: response.message,
                timestamp: response.timestamp || new Date().toISOString(),
                isBot: true
            }]);
        } catch (err) {
            console.error('Error loading greeting:', err);
            setError('Failed to connect to the chatbot. Please check if the backend is running.');
            // Fallback greeting
            setMessages([{
                content: 'Hello! Welcome to our diamond store. I\'m here to help you find the perfect diamond. How can I assist you today?',
                timestamp: new Date().toISOString(),
                isBot: true
            }]);
        } finally {
            setIsTyping(false);
        }
    };

    const handleSendMessage = async (messageText) => {
        // Add user message immediately
        const userMessage = {
            content: messageText,
            timestamp: new Date().toISOString(),
            isBot: false
        };

        setMessages(prev => [...prev, userMessage]);
        setIsTyping(true);
        setError(null);

        try {
            // Send message to backend
            const response = await chatAPI.sendMessage(messageText, sessionId);

            // Add bot response
            const botMessage = {
                content: response.message,
                timestamp: response.timestamp || new Date().toISOString(),
                isBot: true
            };

            setMessages(prev => [...prev, botMessage]);
        } catch (err) {
            console.error('Error sending message:', err);
            setError('Failed to get response. Please try again.');

            // Add error message
            const errorMessage = {
                content: 'Sorry, I\'m having trouble connecting right now. Please try again in a moment.',
                timestamp: new Date().toISOString(),
                isBot: true
            };

            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setIsTyping(false);
        }
    };

    return (
        <div className="chat-container">
            <ChatHeader />

            {error && (
                <div className="error-banner">
                    {error}
                </div>
            )}

            <MessageList messages={messages} isTyping={isTyping} />
            <MessageInput onSendMessage={handleSendMessage} disabled={isTyping} />
        </div>
    );
};

export default ChatContainer;
