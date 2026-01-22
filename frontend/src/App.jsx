import { useState, useEffect } from 'react'
import Chat from './components/Chat'
import Settings from './components/Settings'
import './App.css'

function App() {
  const [isOpen, setIsOpen] = useState(false)
  const [isMinimized, setIsMinimized] = useState(false)
  const [contextMessage, setContextMessage] = useState(null)

  const [currentView, setCurrentView] = useState('chat'); // chat, settings

  // Notify parent (Zabbix Frame) about resize requirements
  useEffect(() => {
    const isExpanded = isOpen && !isMinimized;
    window.parent.postMessage({
      type: 'zabbix-agent-resize',
      expanded: isExpanded
    }, '*');
  }, [isOpen, isMinimized]);

  // Listen for context analysis requests from parent
  useEffect(() => {
    const handleMessage = (event) => {
      console.log("App received message:", event.data);

      if (event.data && event.data.type === 'analyze-context') {
        const { contextType, data } = event.data;

        console.log("Context analysis request:", contextType, data);

        // Build a message for the AI
        let message = '';
        if (data.name) {
          message = `Analiza esta información de Zabbix:\n\n${data.name}`;
        } else if (data.text) {
          message = `Analiza esta información de Zabbix:\n\n${data.text}`;
        } else {
          message = 'Analiza esta información de Zabbix';
        }

        console.log("Setting context message:", message);
        setContextMessage(message);
        setCurrentView('chat');
        setIsOpen(true);
        setIsMinimized(false);
      }
    };

    window.addEventListener('message', handleMessage);
    return () => window.removeEventListener('message', handleMessage);
  }, []);

  return (
    <div className="app-container">

      {/* Chat Window */}
      {isOpen && !isMinimized && (
        <div className="chat-window">
          {/* Header */}
          <div className="chat-header">
            <div className="chat-title">
              <span className="chat-title-icon">⚡</span>
              Zabbix AI Agent
            </div>
            <div className="chat-controls">
              <button
                onClick={() => setCurrentView(currentView === 'chat' ? 'settings' : 'chat')}
                className="control-btn"
                title={currentView === 'chat' ? "Configuración" : "Volver al Chat"}
                style={{ marginRight: '5px' }}
              >
                {currentView === 'chat' ? '⚙️' : '💬'}
              </button>
              <button onClick={() => setIsMinimized(true)} className="control-btn" title="Minimizar">
                −
              </button>
              <button onClick={() => setIsOpen(false)} className="control-btn close" title="Cerrar">
                ×
              </button>
            </div>
          </div>

          {/* Content */}
          <div className="chat-content">
            {currentView === 'chat' ? (
              <Chat contextMessage={contextMessage} onMessageSent={() => setContextMessage(null)} />
            ) : (
              <div style={{ height: '100%', overflowY: 'auto' }}>
                <Settings />
              </div>
            )}
          </div>
        </div>
      )}

      {/* Launcher Bubble */}
      <button
        onClick={() => {
          if (isMinimized) {
            setIsMinimized(false)
          } else {
            setIsOpen(!isOpen)
          }
        }}
        className="launcher-btn"
      >
        <div className="launcher-icon">
          {isOpen && !isMinimized ? '×' : '💬'}
        </div>
      </button>

    </div>
  )
}

export default App
