// src/components/Navbar.jsx
import { useState } from 'react';

export default function Navbar({ currentView, onNavigate, backendOk, theme, onToggleTheme }) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleLinkClick = (e, sectionId) => {
    e.preventDefault();
    setMobileMenuOpen(false);
    if (onNavigate) {
      onNavigate('landing', sectionId);
    }
  };

  const handlePlanClick = () => {
    setMobileMenuOpen(false);
    if (onNavigate) {
      onNavigate('planner');
    }
  };

  return (
    <nav className="desktop-navbar">
      <div className="navbar-container">
        {/* ── [PACKVOTE LOGO] ── */}
        <div
          className="navbar-brand-desktop"
          onClick={(e) => handleLinkClick(e, 'hero')}
          role="button"
          tabIndex={0}
        >
          <div className="navbar-logo-box">✈️</div>
          <div className="navbar-logo-title">PACKVOTE</div>
        </div>

        {/* ── Navigation Links: Overview  How It Works  Destinations  About  Contact ── */}
        <div className="navbar-nav-links">
          <a
            href="#hero"
            className={`nav-item-link ${currentView === 'landing' ? 'active' : ''}`}
            onClick={(e) => handleLinkClick(e, 'hero')}
          >
            Overview
          </a>
          <a
            href="#how-it-works"
            className="nav-item-link"
            onClick={(e) => handleLinkClick(e, 'how-it-works')}
          >
            How It Works
          </a>
          <a
            href="#destinations"
            className="nav-item-link"
            onClick={(e) => handleLinkClick(e, 'destinations')}
          >
            Destinations
          </a>
          <a
            href="#about"
            className="nav-item-link"
            onClick={(e) => handleLinkClick(e, 'about')}
          >
            About
          </a>
          <a
            href="#contact"
            className="nav-item-link"
            onClick={(e) => handleLinkClick(e, 'contact')}
          >
            Contact
          </a>
          <a
            href="#analytics"
            className={`nav-item-link nav-analytics-link ${currentView === 'analytics' ? 'active' : ''}`}
            onClick={(e) => {
              e.preventDefault();
              setMobileMenuOpen(false);
              if (onNavigate) onNavigate('analytics');
            }}
          >
            📊 ML Analytics
          </a>
        </div>

        {/* ── Right Actions: Theme Toggle + Status + Plan Trip ── */}
        <div className="navbar-right-cluster">
          {/* Light / Dark Mode Toggle */}
          <button
            className="btn-theme-toggle"
            onClick={onToggleTheme}
            aria-label={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
            title={theme === 'dark' ? 'Switch to Light Theme' : 'Switch to Dark Theme'}
          >
            <span className="theme-toggle-icon">{theme === 'dark' ? '☀️' : '🌙'}</span>
          </button>

          {backendOk !== null && (
            <div
              className="navbar-status-pill"
              title={backendOk ? '8 ML Models Online' : 'Backend Offline'}
            >
              <span className={`status-dot ${backendOk ? 'online' : 'offline'}`} />
              <span className="status-label">{backendOk ? '8 Models Live' : 'API Offline'}</span>
            </div>
          )}

          {currentView === 'planner' && (
            <button
              className="btn-nav-overview"
              onClick={(e) => handleLinkClick(e, 'hero')}
            >
              ← Overview
            </button>
          )}

          <button
            className="btn-plan-trip-nav"
            onClick={handlePlanClick}
          >
            Plan Your Trip →
          </button>

          {/* Mobile hamburger menu toggle */}
          <button
            className="navbar-mobile-btn"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            aria-label="Toggle Navigation"
          >
            {mobileMenuOpen ? '✕' : '☰'}
          </button>
        </div>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="navbar-drawer-mobile animate-fadeIn">
          <a href="#hero" className="drawer-link" onClick={(e) => handleLinkClick(e, 'hero')}>Overview</a>
          <a href="#how-it-works" className="drawer-link" onClick={(e) => handleLinkClick(e, 'how-it-works')}>How It Works</a>
          <a href="#destinations" className="drawer-link" onClick={(e) => handleLinkClick(e, 'destinations')}>Destinations</a>
          <a href="#about" className="drawer-link" onClick={(e) => handleLinkClick(e, 'about')}>About</a>
          <a href="#contact" className="drawer-link" onClick={(e) => handleLinkClick(e, 'contact')}>Contact</a>
          <a
            href="#analytics"
            className="drawer-link"
            style={{ color: 'var(--color-primary-light)', fontWeight: 700 }}
            onClick={(e) => {
              e.preventDefault();
              setMobileMenuOpen(false);
              if (onNavigate) onNavigate('analytics');
            }}
          >
            📊 ML Analytics & Graphs
          </a>
          <button className="mobile-theme-toggle-btn" onClick={onToggleTheme}>
            {theme === 'dark' ? '☀️ Switch to Light Theme' : '🌙 Switch to Dark Theme'}
          </button>
          <button className="btn-plan-trip-nav" style={{ width: '100%', marginTop: 8 }} onClick={handlePlanClick}>
            Plan Your Trip →
          </button>
        </div>
      )}
    </nav>
  );
}
