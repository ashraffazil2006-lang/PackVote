// src/components/Header.jsx
export default function Header({ backendOk }) {
  return (
    <header className="header">
      <div className="header-inner">
        <a className="logo" href="/">
          <div className="logo-icon">✈️</div>
          <div>
            <div className="logo-text">PACKVOTE</div>
            <div className="header-subtitle">Group Travel Intelligence</div>
          </div>
        </a>

        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          {backendOk !== null && (
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 6,
                fontSize: '0.75rem',
                color: backendOk ? 'var(--color-success)' : 'var(--color-danger)',
              }}
            >
              <div
                style={{
                  width: 7,
                  height: 7,
                  borderRadius: '50%',
                  background: 'currentColor',
                  boxShadow: backendOk ? '0 0 6px var(--color-success)' : 'none',
                }}
              />
              {backendOk ? 'ML Online' : 'Backend Offline'}
            </div>
          )}
          <div className="header-badge">🤖 ML-Powered</div>
        </div>
      </div>
    </header>
  );
}
