import React, { useState } from 'react';
import { 
  Bot, 
  Send, 
  Sparkles, 
  X, 
  HelpCircle, 
  Crosshair, 
  ShieldCheck 
} from 'lucide-react';

export default function AiAssistant({ 
  knowledgeBase = [], 
  isOpen, 
  onToggle, 
  onHighlightEntities 
}) {
  const [messages, setMessages] = useState([
    {
      sender: 'assistant',
      text: 'Namaste Officer. I am your KavachNet Case Assistant for DL-2026-0412. Ask me any question regarding suspects, call records, vehicle sightings, or financial accounts.',
      cited_entities: []
    }
  ]);
  const [inputVal, setInputVal] = useState('');

  const quickChips = [
    'What connects Rakesh to this case?',
    'How many people are connected to him?',
    'Why is burner phone +91 98710 44219 linked?',
    'What happened before the disappearance?',
    'Show the strongest connection'
  ];

  const handleSend = (queryText) => {
    const text = queryText || inputVal;
    if (!text.trim()) return;

    // Add user message
    const newMessages = [...messages, { sender: 'user', text }];
    setMessages(newMessages);
    setInputVal('');

    // Rule-based knowledge base matcher
    const normalized = text.toLowerCase();
    let bestMatch = null;

    for (const item of knowledgeBase) {
      for (const trigger of item.triggers) {
        if (normalized.includes(trigger.toLowerCase())) {
          bestMatch = item;
          break;
        }
      }
      if (bestMatch) break;
    }

    setTimeout(() => {
      if (bestMatch) {
        setMessages((prev) => [
          ...prev,
          {
            sender: 'assistant',
            text: bestMatch.answer,
            cited_entities: bestMatch.cited_entities,
            confidence: bestMatch.confidence
          }
        ]);
        if (onHighlightEntities && bestMatch.cited_entities) {
          onHighlightEntities(bestMatch.cited_entities);
        }
      } else {
        setMessages((prev) => [
          ...prev,
          {
            sender: 'assistant',
            text: `Based on synthetic case records for DL-2026-0412: 18 entities are indexed across telecom towers, ANPR toll sightings, and bank statements. Try asking: "What connects Rakesh to this case?" or "What happened before the disappearance?".`,
            cited_entities: []
          }
        ]);
      }
    }, 400);
  };

  if (!isOpen) {
    return (
      <button className="assistant-drawer-btn" onClick={onToggle}>
        <Sparkles size={18} />
        <span>Ask AI Assistant</span>
      </button>
    );
  }

  return (
    <div className="assistant-panel">
      {/* Header */}
      <div className="assistant-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <Bot size={20} color="#60a5fa" />
          <div>
            <div style={{ fontWeight: 700, fontSize: '0.88rem' }}>AI Investigative Assistant</div>
            <div style={{ fontSize: '0.7rem', color: '#94a3b8' }}>Case: DL-2026-0412 (Local KB)</div>
          </div>
        </div>
        <button 
          onClick={onToggle}
          style={{ background: 'transparent', border: 'none', color: 'white', cursor: 'pointer' }}
        >
          <X size={18} />
        </button>
      </div>

      {/* Chat Body */}
      <div className="assistant-chat-body">
        {messages.map((msg, idx) => (
          <div key={idx} className={`chat-bubble ${msg.sender}`}>
            <div style={{ marginBottom: msg.cited_entities?.length > 0 ? '0.45rem' : '0' }}>
              {msg.text}
            </div>

            {msg.confidence && (
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.3rem', fontSize: '0.72rem', color: 'var(--info-blue)', fontWeight: 600, marginTop: '0.3rem' }}>
                <ShieldCheck size={12} />
                <span>Association Confidence: {msg.confidence}%</span>
              </div>
            )}

            {msg.cited_entities && msg.cited_entities.length > 0 && (
              <button
                onClick={() => onHighlightEntities(msg.cited_entities)}
                style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '0.3rem',
                  fontSize: '0.72rem',
                  fontWeight: 600,
                  color: 'var(--info-blue)',
                  background: 'var(--info-blue-bg)',
                  border: '1px solid var(--info-blue-border)',
                  padding: '0.25rem 0.5rem',
                  borderRadius: 'var(--radius-sm)',
                  cursor: 'pointer',
                  marginTop: '0.4rem'
                }}
              >
                <Crosshair size={12} />
                Highlight ({msg.cited_entities.length}) Entities on Graph
              </button>
            )}
          </div>
        ))}
      </div>

      {/* Quick Chips */}
      <div className="chat-chips-area">
        {quickChips.map((chip, idx) => (
          <button 
            key={idx} 
            className="query-chip"
            onClick={() => handleSend(chip)}
          >
            {chip}
          </button>
        ))}
      </div>

      {/* Input Area */}
      <div className="assistant-input-area">
        <input
          type="text"
          className="assistant-input"
          placeholder="Ask a question about this case..."
          value={inputVal}
          onChange={(e) => setInputVal(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
        />
        <button className="assistant-send-btn" onClick={() => handleSend()}>
          <Send size={15} />
        </button>
      </div>
    </div>
  );
}
