import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const chatAPI = {
    /**
     * Send a message to the chatbot
     * @param {string} message - User message
     * @param {string} sessionId - Session identifier
     * @returns {Promise} Response from the chatbot
     */
    sendMessage: async (message, sessionId) => {
        try {
            const response = await apiClient.post('/chat', {
                message,
                session_id: sessionId,
            });
            return response.data;
        } catch (error) {
            console.error('Error sending message:', error);
            throw error;
        }
    },

    /**
     * Get greeting message for a session
     * @param {string} sessionId - Session identifier
     * @returns {Promise} Greeting message
     */
    getGreeting: async (sessionId) => {
        try {
            const response = await apiClient.get(`/chat/greeting/${sessionId}`);
            return response.data;
        } catch (error) {
            console.error('Error getting greeting:', error);
            throw error;
        }
    },

    /**
     * Check API health
     * @returns {Promise} Health status
     */
    healthCheck: async () => {
        try {
            const response = await apiClient.get('/health');
            return response.data;
        } catch (error) {
            console.error('Error checking health:', error);
            throw error;
        }
    },
};

export default apiClient;
