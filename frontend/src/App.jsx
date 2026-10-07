// src/App.jsx
import { useState, useEffect } from 'react';
import './App.css';
import Navbar from './components/Navbar';
import LandingPage from './pages/LandingPage';
import Home from './pages/Home';
import DestinationModal from './components/DestinationModal';
import MLAnalyticsDashboard from './components/MLAnalyticsDashboard';
import VoiceAssistant from './components/VoiceAssistant';
import { checkHealth } from './services/api';

export default function App() {
  const [currentView, setCurrentView] = useState(() => {
    if (window.location.hash === '#plan') return 'planner';
    if (window.location.hash === '#analytics') return 'analytics';
    return 'landing';
  });
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem('packvote_theme') || 'dark';
  });
  const [backendOk, setBackendOk] = useState(null);
  const [selectedModalDest, setSelectedModalDest] = useState(null);

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('packvote_theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => (prev === 'dark' ? 'light' : 'dark'));
  };

  useEffect(() => {
    checkHealth()
      .then(() => setBackendOk(true))
      .catch(() => setBackendOk(false));
  }, []);

  const handleNavigate = (view, sectionId) => {
    setCurrentView(view);
    if (view === 'planner') {
      window.location.hash = '#plan';
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } else if (view === 'analytics') {
      window.location.hash = '#analytics';
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } else {
      window.location.hash = sectionId ? `#${sectionId}` : '#';
      if (sectionId) {
        setTimeout(() => {
          const el = document.getElementById(sectionId);
          if (el) {
            el.scrollIntoView({ behavior: 'smooth', block: 'start' });
          } else {
            window.scrollTo({ top: 0, behavior: 'smooth' });
          }
        }, 50);
      } else {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    }
  };

  return (
    <div className="app">
      <Navbar
        currentView={currentView}
        onNavigate={handleNavigate}
        backendOk={backendOk}
        theme={theme}
        onToggleTheme={toggleTheme}
      />

      {backendOk === false && (
        <div style={{ maxWidth: 1280, margin: '16px auto', padding: '0 24px', width: '100%' }}>
          <div className="error-alert">
            <span className="error-icon">⚠️</span>
            <div className="error-content">
              <div className="error-title">Backend Unavailable</div>
              <div className="error-msg">
                Cannot connect to the PACKVOTE API on port 8000. Please start the backend:
                <code style={{ display: 'block', marginTop: 6, padding: '4px 8px', background: 'rgba(0,0,0,0.3)', borderRadius: 4 }}>
                  python -m uvicorn backend.app.main:app --port 8000
                </code>
              </div>
            </div>
          </div>
        </div>
      )}

      {currentView === 'planner' ? (
        <Home onNavigate={handleNavigate} />
      ) : currentView === 'analytics' ? (
        <MLAnalyticsDashboard
          onPlanTrip={() => handleNavigate('planner')}
          onBackToOverview={() => handleNavigate('landing')}
        />
      ) : (
        <LandingPage
          onPlanTrip={() => handleNavigate('planner')}
          onExploreDestination={(destName) => setSelectedModalDest(destName)}
          onNavigate={handleNavigate}
        />
      )}

      {/* Global Destination Modal (callable from Landing Page or anywhere) */}
      {selectedModalDest && (
        <DestinationModal
          destinationName={selectedModalDest}
          onClose={() => setSelectedModalDest(null)}
          onSelectDestination={(destName) => setSelectedModalDest(destName)}
        />
      )}

      <footer className="footer">
        <div className="footer-inner-content">
          <div className="footer-col-brand">
            <div className="footer-brand-logo">
              <span className="footer-icon">✈️</span>
              <span className="footer-title">PACKVOTE</span>
            </div>
            <p className="footer-tagline">
              Democratizing group travel with algorithmic fairness and multi-model machine learning.
            </p>
            <div className="footer-status-pill">
              <span className={`status-dot ${backendOk ? 'online' : 'offline'}`} />
              <span>FastAPI 8-Model Consensus Engine: {backendOk ? 'Online' : 'Offline'}</span>
            </div>
          </div>

          <div className="footer-links-grid">
            <div className="footer-nav-col">
              <h4 className="footer-col-title">Navigation</h4>
              <a href="#hero" onClick={(e) => { e.preventDefault(); handleNavigate('landing', 'hero'); }}>Home</a>
              <a href="#how-it-works" onClick={(e) => { e.preventDefault(); handleNavigate('landing', 'how-it-works'); }}>How It Works</a>
              <a href="#features" onClick={(e) => { e.preventDefault(); handleNavigate('landing', 'features'); }}>Features</a>
              <a href="#destinations" onClick={(e) => { e.preventDefault(); handleNavigate('landing', 'destinations'); }}>Destinations</a>
            </div>

            <div className="footer-nav-col">
              <h4 className="footer-col-title">Platform</h4>
              <button
                className="footer-link-btn"
                onClick={() => handleNavigate('planner')}
              >
                Launch Trip Planner →
              </button>
              <a href="#about" onClick={(e) => { e.preventDefault(); handleNavigate('landing', 'about'); }}>About PACKVOTE</a>
              <a href="#contact" onClick={(e) => { e.preventDefault(); handleNavigate('landing', 'contact'); }}>Contact & Support</a>
              <a href="http://localhost:8000/api/docs" target="_blank" rel="noreferrer">API Documentation ↗</a>
            </div>

            <div className="footer-nav-col">
              <h4 className="footer-col-title">ML Stack</h4>
              <span>Random Forest (200 trees)</span>
              <span>K-Means Clustering</span>
              <span>SVD Collaborative Filter</span>
              <span>TF-IDF Cosine Similarity</span>
            </div>
          </div>
        </div>

        <div className="footer-bottom-bar">
          <p>
            © {new Date().getFullYear()} <span className="footer-logo">PACKVOTE</span>. Built with FastAPI · React · scikit-learn · Python.
          </p>
        </div>
      </footer>

      {/* AI Voice Assistant Floating Launcher & Window */}
      <VoiceAssistant
        onNavigate={handleNavigate}
        onOpenDestination={(destName) => setSelectedModalDest(destName)}
        onToggleTheme={toggleTheme}
        currentTheme={theme}
      />
    </div>
  );
}
