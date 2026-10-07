// src/components/TravelerInput.jsx
const PREFERENCE_OPTIONS = [
  { id: 'Beach',      emoji: '🏖️' },
  { id: 'Historical', emoji: '🏛️' },
  { id: 'Nature',     emoji: '🌿' },
  { id: 'Adventure',  emoji: '🧗' },
  { id: 'City',       emoji: '🏙️' },
];

export default function TravelerInput({ travelers, onUpdate, onAdd, onRemove }) {
  const togglePref = (travelerIndex, pref) => {
    const current = travelers[travelerIndex].preferences;
    const updated = current.includes(pref)
      ? current.filter((p) => p !== pref)
      : [...current, pref];
    onUpdate(travelerIndex, updated);
  };

  return (
    <div>
      {travelers.map((traveler, i) => (
        <div key={i} className="traveler-item">
          <div className="traveler-header">
            <span className="traveler-label">
              <div className="traveler-avatar">{i + 1}</div>
              Traveler {i + 1}
            </span>
            {travelers.length > 1 && (
              <button className="remove-btn" onClick={() => onRemove(i)} aria-label={`Remove traveler ${i + 1}`}>
                ✕ Remove
              </button>
            )}
          </div>
          <div className="pref-chips">
            {PREFERENCE_OPTIONS.map(({ id, emoji }) => (
              <button
                key={id}
                className={`pref-chip ${traveler.preferences.includes(id) ? 'selected' : ''}`}
                onClick={() => togglePref(i, id)}
                type="button"
              >
                {emoji} {id}
              </button>
            ))}
          </div>
          {traveler.preferences.length === 0 && (
            <p style={{ fontSize: '0.75rem', color: 'var(--color-danger)', marginTop: 6 }}>
              ⚠ Select at least one preference
            </p>
          )}
        </div>
      ))}

      {travelers.length < 10 && (
        <button className="add-traveler-btn" onClick={onAdd} type="button">
          ＋ Add Traveler
        </button>
      )}
    </div>
  );
}
