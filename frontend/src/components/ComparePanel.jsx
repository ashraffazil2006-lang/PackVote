// src/components/ComparePanel.jsx
export default function ComparePanel({ destinations, onRemove, onClear }) {
  if (!destinations || destinations.length < 2) return null;

  const fields = [
    { label: 'Compatibility',       key: 'group_compatibility',      fmt: v => `${v.toFixed(1)}/100` },
    { label: 'Preference Match',    key: 'group_preference_match',   fmt: v => `${v.toFixed(1)}%` },
    { label: 'Suitability',         key: 'suitability',              fmt: v => `${v.toFixed(1)}%` },
    { label: 'Sentiment',           key: 'sentiment_score',          fmt: v => v != null ? `${v.toFixed(0)}%` : '—' },
    { label: 'Seasonal Fit',        key: 'seasonal_score',           fmt: v => v != null ? `${v.toFixed(0)}%` : '—' },
    { label: 'Predicted Exp.',      key: 'predicted_experience',     fmt: v => `${v.toFixed(2)}/5` },
    { label: 'Avg Rating',          key: 'average_rating',           fmt: v => `${v.toFixed(2)}/5` },
    { label: 'Budget Status',       key: 'budget_status',            fmt: v => v },
    { label: 'Est. Stay / Night',   key: 'predicted_accommodation_cost', fmt: v => v != null ? `₹${Math.round(v).toLocaleString('en-IN')}` : 'N/A' },
    { label: 'Best Time',           key: 'best_time',                fmt: v => v },
    { label: 'Peak Season Now',     key: 'in_peak_season',           fmt: v => v ? '✅ Yes' : '❌ No' },
    { label: 'Tourist Spots',       key: 'total_spots',              fmt: v => `${v} spots` },
  ];

  const getBest = (key) => {
    const numericKeys = ['group_compatibility','group_preference_match','suitability','sentiment_score','seasonal_score','predicted_experience','average_rating','budget_fit'];
    if (!numericKeys.includes(key)) return null;
    const vals = destinations.map(d => d[key] ?? -Infinity);
    return Math.max(...vals);
  };

  return (
    <div className="compare-panel animate-fadeUp">
      <div className="compare-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <span style={{ fontSize: '1.1rem' }}>⚖️</span>
          <span style={{ fontWeight: 700, fontSize: '1rem' }}>Side-by-Side Comparison</span>
          <span className="badge badge-primary">{destinations.length} destinations</span>
        </div>
        <button className="compare-clear-btn" onClick={onClear}>Clear All</button>
      </div>

      <div className="compare-table-wrapper">
        <table className="compare-table">
          <thead>
            <tr>
              <th>Metric</th>
              {destinations.map((d, i) => (
                <th key={i}>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 4, alignItems: 'center' }}>
                    <span>{d.destination}</span>
                    <span style={{ fontSize: '0.7rem', color: 'var(--color-text-faint)', fontWeight: 400 }}>{d.state}</span>
                    <button
                      onClick={() => onRemove(d)}
                      style={{ background: 'none', color: 'var(--color-danger)', fontSize: '0.7rem', cursor: 'pointer', border: '1px solid rgba(239,68,68,0.3)', borderRadius: 4, padding: '1px 6px' }}
                    >✕</button>
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {fields.map(({ label, key, fmt }) => {
              const best = getBest(key);
              return (
                <tr key={key}>
                  <td className="compare-metric-label">{label}</td>
                  {destinations.map((d, i) => {
                    const val = d[key];
                    const isBest = best !== null && val === best && destinations.length > 1;
                    return (
                      <td
                        key={i}
                        className={`compare-cell ${isBest ? 'compare-cell-best' : ''}`}
                      >
                        {val != null ? fmt(val) : '—'}
                        {isBest && <span style={{ marginLeft: 5, fontSize: '0.7rem' }}>🏆</span>}
                      </td>
                    );
                  })}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
