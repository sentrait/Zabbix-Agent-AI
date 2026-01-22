import { useState, useRef, useEffect } from 'react'
import ReactMarkdown from 'react-markdown'
import './Chat.css'

const API_URL = import.meta.env.VITE_API_URL || '/ai-backend/api';

export default function Chat({ contextMessage, onMessageSent }) {
    const [messages, setMessages] = useState(() => {
        const saved = localStorage.getItem('zabbix_ai_chat_history');
        return saved ? JSON.parse(saved) : [
            { role: 'assistant', content: 'Hello! I am your Zabbix AI Assistant. How can I help you check your infrastructure today?' }
        ];
    });
    const [input, setInput] = useState('')
    const [loading, setLoading] = useState(false)
    const messagesEndRef = useRef(null)

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
    }

    useEffect(() => {
        scrollToBottom()
        localStorage.setItem('zabbix_ai_chat_history', JSON.stringify(messages));
    }, [messages])

    const clearHistory = () => {
        const initial = [{ role: 'assistant', content: 'Chat history cleared.' }];
        setMessages(initial);
        localStorage.setItem('zabbix_ai_chat_history', JSON.stringify(initial));
    }

    // Handle context messages from parent
    useEffect(() => {
        if (contextMessage && contextMessage.trim()) {
            handleSendMessage(contextMessage);
            // Clear the context after sending
            if (onMessageSent) {
                setTimeout(() => onMessageSent(), 100);
            }
        }
    }, [contextMessage]);

    const handleSendMessage = async (messageText) => {
        const msgToSend = messageText.trim();
        if (!msgToSend) return;

        const userMsg = { role: 'user', content: msgToSend };
        setMessages(prev => [...prev, userMsg]);
        // Only clear input if the message originated from the input field
        if (messageText === input) {
            setInput('');
        }
        setLoading(true);

        try {
            const res = await fetch(`${API_URL}/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: userMsg.content })
            })
            const data = await res.json()

            // Handle potential multiple messages or complex responses
            let responseContent = data.reply;
            if (typeof data.reply === 'object') {
                responseContent = JSON.stringify(data.reply);
            }

            setMessages(prev => [...prev, { role: 'assistant', content: responseContent }])
        } catch (err) {
            setMessages(prev => [...prev, { role: 'assistant', content: "Error connecting to AI service. Please check backend connection." }])
        }
        setLoading(false)
    }

    const handleSubmit = (e) => {
        e.preventDefault();
        handleSendMessage(input);
    }

    return (
        <div className="chat-container">
            <div className="messages">
                {messages.map((msg, idx) => (
                    <div key={idx} className={`message ${msg.role}`}>
                        <div className="message-avatar">{msg.role === 'assistant' ? '🤖' : '👤'}</div>
                        <div className="message-bubble">
                            {msg.role === 'assistant' ? (
                                <ReactMarkdown className="markdown-content">{msg.content}</ReactMarkdown>
                            ) : (
                                msg.content
                            )}
                        </div>
                    </div>
                ))}
                {loading && (
                    <div className="message assistant">
                        <div className="message-avatar">🤖</div>
                        <div className="message-bubble loading">
                            <div className="dot"></div>
                            <div className="dot"></div>
                            <div className="dot"></div>
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            <div className="input-area">
                <form onSubmit={handleSubmit} style={{ position: 'relative', display: 'flex', alignItems: 'flex-end' }}>
                    <textarea
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={(e) => {
                            if (e.key === 'Enter' && !e.shiftKey) {
                                e.preventDefault();
                                handleSubmit(e);
                            }
                        }}
                        placeholder="Escribe tu consulta... (Shift+Enter para nueva línea)"
                        className="chat-input"
                        rows="1"
                        style={{ resize: 'none', overflow: 'hidden', minHeight: '44px' }}
                    />
                    <button type="submit" disabled={loading || !input.trim()} className="send-btn" style={{ marginBottom: '6px' }}>
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <line x1="22" y1="2" x2="11" y2="13"></line>
                            <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                        </svg>
                    </button>
                    <button type="button" onClick={clearHistory} className="send-btn" style={{ marginBottom: '6px', marginLeft: '5px', backgroundColor: '#ef4444' }} title="Borrar Historial">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <polyline points="3 6 5 6 21 6"></polyline>
                            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                        </svg>
                    </button>
                </form>
            </div>
        </div>
    )
}
