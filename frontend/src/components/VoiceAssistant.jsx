// src/components/VoiceAssistant.jsx
import React, { useState, useEffect, useRef } from 'react';
import { sendAssistantMessage } from '../services/api';

const DEFAULT_SUGGESTIONS = [
  'Plan a 3-day beach trip for 2',
  'Show ML Analytics',
  'Tell me about Goa',
  'Explain how consensus works',
  'Explain budget per night',
];

export default function VoiceAssistant({
  onNavigate,
  onOpenDestination,
  onToggleTheme,
  currentTheme,
  onApplyPlanParams,
}) {
  const [isOpen, setIsOpen] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [voiceMuted, setVoiceMuted] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(false);
  const [suggestions, setSuggestions] = useState(DEFAULT_SUGGESTIONS);

  const [messages, setMessages] = useState([
    {
      id: 'welcome',
      sender: 'assistant',
      text: "Hi! I'm your PACKVOTE AI Voice Assistant. Speak or type to plan group trips, explore destinations, or inspect our 8 ML models!",
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    },
  ]);

  const recognitionRef = useRef(null);
  const chatScrollRef = useRef(null);

  // Initialize Web Speech Recognition
  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      const recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = true;
      recognition.lang = 'en-IN'; // Indian English

      recognition.onstart = () => {
        setIsListening(true);
      };

      recognition.onresult = (event) => {
        let currentTranscript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
          currentTranscript += event.results[i][0].transcript;
        }
        setTranscript(currentTranscript);
      };

      recognition.onerror = (event) => {
        console.warn('Speech recognition error:', event.error);
        setIsListening(false);
      };

      recognition.onend = () => {
        setIsListening(false);
        // If we captured speech, auto-send it
        setTranscript((finalText) => {
          if (finalText && finalText.trim().length > 1) {
            handleSendMessage(finalText.trim());
          }
          return '';
        });
      };

      recognitionRef.current = recognition;
    }

    return () => {
      if (window.speechSynthesis) {
        window.speechSynthesis.cancel();
      }
    };
  }, []);

  // Auto-scroll chat
  useEffect(() => {
    if (chatScrollRef.current) {
      chatScrollRef.current.scrollTop = chatScrollRef.current.scrollHeight;
    }
  }, [messages, loading]);

  // Text-to-Speech synthesizer
  const speakReply = (text) => {
    if (voiceMuted || !window.speechSynthesis) return;

    window.speechSynthesis.cancel(); // Stop any active speech

    // Strip emojis or extra formatting for smooth spoken output
    const cleanText = text.replace(/[\u{1F600}-\u{1F64F}\u{1F300}-\u{1F5FF}\u{1F680}-\u{1F6FF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}]/gu, '');
    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.rate = 1.0;
    utterance.pitch = 1.0;

    // Pick an English voice if available
    const voices = window.speechSynthesis.getVoices();
    const preferredVoice = voices.find(v => v.lang.includes('en-IN') || v.lang.includes('en-US') || v.lang.includes('en-GB'));
    if (preferredVoice) {
      utterance.voice = preferredVoice;
    }

    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);

    window.speechSynthesis.speak(utterance);
  };

  const startVoiceInput = () => {
    if (isSpeaking && window.speechSynthesis) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
    }

    if (recognitionRef.current) {
      try {
        setTranscript('');
        recognitionRef.current.start();
      } catch (err) {
        // Recognition might already be running
        recognitionRef.current.stop();
      }
    } else {
      setMessages(prev => [
        ...prev,
        {
          id: Date.now().toString(),
          sender: 'assistant',
          text: "Voice speech recognition isn't supported in this browser. You can type any question or click a suggestion chip below!",
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        },
      ]);
    }
  };

  const stopVoiceInput = () => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
    }
  };

  const handleSendMessage = async (textToSend) => {
    const query = textToSend || inputText;
    if (!query || !query.trim()) return;

    const userMsg = {
      id: Date.now().toString(),
      sender: 'user',
      text: query,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages(prev => [...prev, userMsg]);
    setInputText('');
    setLoading(true);

    try {
      const response = await sendAssistantMessage(query);
      const data = response.data || {};
      const replyText = data.reply || "I didn't quite catch that. Could you please rephrase?";

      const botMsg = {
        id: (Date.now() + 1).toString(),
        sender: 'assistant',
        text: replyText,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };

      setMessages(prev => [...prev, botMsg]);
      if (data.suggestions) {
        setSuggestions(data.suggestions);
      }

      // Execute app actions if present
      if (data.action) {
        handleActionExecution(data.action);
      }

      // Speak response
      speakReply(replyText);
    } catch (err) {
      const errorMsg = {
        id: (Date.now() + 1).toString(),
        sender: 'assistant',
        text: "Sorry, I am having trouble connecting to the travel intelligence service. Please check your network.",
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  const handleActionExecution = (action) => {
    if (!action) return;

    if (action.type === 'NAVIGATE' && onNavigate) {
      onNavigate(action.target);
    } else if (action.type === 'SET_THEME' && onToggleTheme) {
      if (action.theme !== currentTheme) {
        onToggleTheme();
      }
    } else if (action.type === 'OPEN_DESTINATION' && onOpenDestination) {
      onOpenDestination(action.destination);
    } else if (action.type === 'SET_PLANNER_AND_SUBMIT' && onNavigate) {
      if (onApplyPlanParams) {
        onApplyPlanParams(action);
      }
      onNavigate('planner');
    }
  };

  const stopSpeaking = () => {
    if (window.speechSynthesis) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
    }
  };

  return (
    <>
      {/* ── 1. Floating Trigger Button (Bottom-Right) ── */}
      {!isOpen && (
        <div className="voice-assistant-launcher-wrapper animate-fadeIn">
          <button
            type="button"
            className="btn-voice-assistant-orb"
            onClick={() => setIsOpen(true)}
            aria-label="Open AI Voice Assistant"
          >
            <div className="orb-glowing-ring" />
            <span className="orb-icon">🎙️</span>
            <span className="orb-label-badge">Ask AI</span>
          </button>
        </div>
      )}

      {/* ── 2. Expanded Voice Assistant Window ── */}
      {isOpen && (
        <div className="voice-assistant-panel animate-slideUp">
          {/* Header */}
          <div className="vap-header">
            <div className="vap-header-title-box">
              <span className="vap-ai-avatar">🤖</span>
              <div>
                <h3 className="vap-title">PACKVOTE AI Voice</h3>
                <span className="vap-status">
                  <span className="vap-online-dot" /> Speech & Travel Copilot
                </span>
              </div>
            </div>

            <div className="vap-header-controls">
              {/* Voice Mute Toggle */}
              <button
                type="button"
                className="vap-btn-icon"
                onClick={() => {
                  setVoiceMuted(!voiceMuted);
                  if (!voiceMuted) stopSpeaking();
                }}
                title={voiceMuted ? "Unmute Voice" : "Mute Voice"}
              >
                {voiceMuted ? '🔇' : '🔊'}
              </button>

              {/* Minimize / Close */}
              <button
                type="button"
                className="vap-btn-icon"
                onClick={() => {
                  stopSpeaking();
                  stopVoiceInput();
                  setIsOpen(false);
                }}
                title="Close Assistant"
              >
                ✕
              </button>
            </div>
          </div>

          {/* Active Voice Waveform Area */}
          <div className={`vap-voice-status-bar ${isListening ? 'listening' : isSpeaking ? 'speaking' : ''}`}>
            {isListening ? (
              <div className="vap-wave-container">
                <span className="wave-bar bar-1" />
                <span className="wave-bar bar-2" />
                <span className="wave-bar bar-3" />
                <span className="wave-bar bar-4" />
                <span className="wave-bar bar-5" />
                <span className="wave-text">Listening... Speak now</span>
              </div>
            ) : isSpeaking ? (
              <div className="vap-wave-container">
                <span className="wave-bar bar-speaking b1" />
                <span className="wave-bar bar-speaking b2" />
                <span className="wave-bar bar-speaking b3" />
                <span className="wave-text">PACKVOTE Speaking...</span>
                <button type="button" className="vap-stop-audio-btn" onClick={stopSpeaking}>
                  Stop
                </button>
              </div>
            ) : (
              <div className="vap-idle-hint">
                <span>Tap the microphone to speak, or select a suggestion</span>
              </div>
            )}
          </div>

          {/* Live Transcript Banner if listening */}
          {isListening && transcript && (
            <div className="vap-live-transcript animate-fadeIn">
              <em>"{transcript}"</em>
            </div>
          )}

          {/* Chat Messages Body */}
          <div className="vap-messages-scroll" ref={chatScrollRef}>
            {messages.map((m) => (
              <div key={m.id} className={`vap-msg-row ${m.sender}`}>
                <div className="vap-bubble">
                  <div className="vap-bubble-txt">{m.text}</div>
                  <span className="vap-bubble-time">{m.timestamp}</span>
                </div>
              </div>
            ))}
            {loading && (
              <div className="vap-msg-row assistant">
                <div className="vap-bubble vap-loading-bubble">
                  <span className="dot dot-1" />
                  <span className="dot dot-2" />
                  <span className="dot dot-3" />
                </div>
              </div>
            )}
          </div>

          {/* Quick Suggestions Chips */}
          <div className="vap-suggestions-row">
            {suggestions.map((s, idx) => (
              <button
                key={idx}
                type="button"
                className="vap-sug-chip"
                onClick={() => handleSendMessage(s)}
              >
                ✦ {s}
              </button>
            ))}
          </div>

          {/* Input Controls Footer */}
          <form
            className="vap-input-footer"
            onSubmit={(e) => {
              e.preventDefault();
              handleSendMessage();
            }}
          >
            {/* Big Mic Button */}
            <button
              type="button"
              className={`vap-mic-btn ${isListening ? 'active' : ''}`}
              onClick={isListening ? stopVoiceInput : startVoiceInput}
              title={isListening ? "Stop Listening" : "Start Speaking"}
            >
              {isListening ? '🛑' : '🎙️'}
            </button>

            {/* Text Input Fallback */}
            <input
              type="text"
              className="vap-text-input"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Ask anything or click 🎙️ to talk..."
            />

            <button
              type="submit"
              className="vap-send-btn"
              disabled={!inputText.trim()}
              title="Send"
            >
              ➤
            </button>
          </form>
        </div>
      )}
    </>
  );
}
