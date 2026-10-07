// src/components/WeatherSection.jsx
const MONTH_NAMES = [
  'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
];

export default function WeatherSection({ weather = [], destinationName, bestTime = '' }) {
  const currentMonthIdx = new Date().getMonth();
  const currentMonthName = MONTH_NAMES[currentMonthIdx];

  return (
    <div className="weather-wrapper">
      <div className="weather-header">
        <div>
          <h3 className="section-heading">🌤️ Climate & Best Time to Visit</h3>
          <p className="section-subheading">
            Seasonal temperature guide for {destinationName}. Current month is highlighted.
          </p>
        </div>
        {bestTime && (
          <div className="best-time-banner">
            <span className="best-time-icon">📅</span>
            <div>
              <div className="best-time-label">Prime Visiting Window</div>
              <div className="best-time-val">{bestTime}</div>
            </div>
          </div>
        )}
      </div>

      {weather.length === 0 ? (
        <div className="empty-substate">Weather information unavailable.</div>
      ) : (
        <div className="weather-months-grid">
          {weather.map((m, idx) => {
            const isCurrent = m.month?.toLowerCase() === currentMonthName.toLowerCase();
            return (
              <div key={idx} className={`weather-month-card ${isCurrent ? 'current-month' : ''}`}>
                {isCurrent && <div className="now-chip">Current Month</div>}
                <div className="month-name">{m.month}</div>
                <div className="month-emoji">{m.emoji || '☀️'}</div>
                <div className="month-temps">
                  <span className="temp-high">{m.temp_high ?? '—'}°C</span>
                  <span className="temp-sep">/</span>
                  <span className="temp-low">{m.temp_low ?? '—'}°C</span>
                </div>
                <div className="month-desc" title={m.description}>
                  {m.description}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
