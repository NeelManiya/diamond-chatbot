import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ChatContainer from './components/ChatContainer';
import Insight from './pages/Insight';
import './styles/chat.css';

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<ChatContainer />} />
                <Route path="/insight" element={<Insight />} />
            </Routes>
        </Router>
    );
}

export default App;
