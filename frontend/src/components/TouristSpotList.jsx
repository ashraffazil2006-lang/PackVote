// src/components/TouristSpotList.jsx
import { useState } from 'react';

const CHAR_ICONS = {
  beach:      '🏖️',
  scenic:     '🌅',
  nature:     '🌿',
  waterfall:  '💧',
  historical: '🏛️',
  heritage:   '🏺',
  temple:     '⛩️',
  fort:       '🏰',
  adventure:  '🧗',
  trekking:   '🥾',
  mountain:   '⛰️',
  valley:     '🏔️',
  lake:       '🏞️',
  wildlife:   '🦁',
  cultural:   '🎭',
  family:     '👨‍👩‍👧‍👦',
  amusement:  '🎡',
  photography:'📸',
  default:    '📍',
};

function getIcon(characteristics = '') {
  const chars = characteristics.toLowerCase();
  for (const [key, icon] of Object.entries(CHAR_ICONS)) {
    if (key !== 'default' && chars.includes(key)) return icon;
  }
  return CHAR_ICONS.default;
}

function SpotChip({ spot }) {
  const icon = getIcon(spot.characteristics);
  return (
    <div
      className="spot-chip"
      title={spot.characteristics || spot.name}
    >
      <span>{icon}</span>
      <span>{spot.name}</span>
      {spot.characteristics && (
        <span style={{ opacity: 0.55, fontSize: '0.68rem' }}>
          · {spot.characteristics.split(',').slice(0, 2).join(', ')}
        </span>
      )}
    </div>
  );
}

export default function TouristSpotList({ spots, totalSpots }) {
  const [showAll, setShowAll]     = useState(false);
  const [filter, setFilter]       = useState('');

  if (!spots || spots.length === 0) return null;

  const filtered = filter.trim()
    ? spots.filter(s =>
        s.name.toLowerCase().includes(filter.toLowerCase()) ||
        (s.characteristics || '').toLowerCase().includes(filter.toLowerCase())
      )
    : spots;

  const INITIAL_SHOW = 8;
  const visible = showAll ? filtered : filtered.slice(0, INITIAL_SHOW);
  const hasMore  = filtered.length > INITIAL_SHOW && !showAll;

  return (
    <div className="spots-section">
      <div className="spots-title" style={{ justifyContent: 'space-between', flexWrap: 'wrap', gap: 8 }}>
        <span style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          📍 Tourist Attractions
          <span
            className="badge badge-accent"
            style={{ fontSize: '0.7rem', padding: '2px 8px' }}
          >
            {filtered.length}{filter ? ` of ${spots.length}` : ''} spots
          </span>
        </span>
        {spots.length > 5 && (
          <input
            type="text"
            placeholder="Filter spots…"
            value={filter}
            onChange={e => { setFilter(e.target.value); setShowAll(false); }}
            style={{
              background: 'var(--color-surface)',
              border: '1px solid var(--color-border)',
              borderRadius: 6,
              padding: '4px 10px',
              color: 'var(--color-text)',
              fontSize: '0.78rem',
              width: 160,
            }}
          />
        )}
      </div>

      {filtered.length === 0 ? (
        <div style={{ fontSize: '0.8rem', color: 'var(--color-text-faint)', padding: '8px 0' }}>
          No spots match "{filter}"
        </div>
      ) : (
        <>
          <div className="spots-list">
            {visible.map((spot, i) => (
              <SpotChip key={i} spot={spot} />
            ))}
          </div>

          {hasMore && (
            <button
              onClick={() => setShowAll(true)}
              style={{
                marginTop: 10,
                background: 'transparent',
                border: '1px solid var(--color-border-bright)',
                borderRadius: 6,
                color: 'var(--color-text-muted)',
                fontSize: '0.78rem',
                padding: '5px 14px',
                cursor: 'pointer',
                transition: 'all 0.15s',
              }}
              onMouseEnter={e => e.target.style.borderColor = 'var(--color-accent)'}
              onMouseLeave={e => e.target.style.borderColor = 'var(--color-border-bright)'}
            >
              Show {filtered.length - INITIAL_SHOW} more ▾
            </button>
          )}
          {showAll && filtered.length > INITIAL_SHOW && (
            <button
              onClick={() => setShowAll(false)}
              style={{
                marginTop: 10,
                background: 'transparent',
                border: '1px solid var(--color-border-bright)',
                borderRadius: 6,
                color: 'var(--color-text-muted)',
                fontSize: '0.78rem',
                padding: '5px 14px',
                cursor: 'pointer',
              }}
            >
              Show less ▴
            </button>
          )}
        </>
      )}
    </div>
  );
}
