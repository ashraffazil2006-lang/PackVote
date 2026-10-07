// src/components/StaySection.jsx
import { useState } from 'react';

const TIER_COLORS = {
  Hostel:         { bg: 'rgba(16,185,129,0.15)', text: '#34d399', border: 'rgba(16,185,129,0.3)' },
  Budget:         { bg: 'rgba(16,185,129,0.15)', text: '#34d399', border: 'rgba(16,185,129,0.3)' },
  Hotel:          { bg: 'rgba(59,130,246,0.15)', text: '#60a5fa', border: 'rgba(59,130,246,0.3)' },
  Homestay:       { bg: 'rgba(245,158,11,0.15)', text: '#fbbf24', border: 'rgba(245,158,11,0.3)' },
  Houseboat:      { bg: 'rgba(6,182,212,0.15)',  text: '#22d3ee', border: 'rgba(6,182,212,0.3)' },
  'Boutique Hotel': { bg: 'rgba(168,85,247,0.15)', text: '#c084fc', border: 'rgba(168,85,247,0.3)' },
  Resort:         { bg: 'rgba(168,85,247,0.15)', text: '#c084fc', border: 'rgba(168,85,247,0.3)' },
  Luxury:         { bg: 'rgba(234,179,8,0.15)',  text: '#facc15', border: 'rgba(234,179,8,0.3)' },
};

export default function StaySection({ accommodation = [], destinationName }) {
  const [sortBy, setSortBy] = useState('recommended');

  const sorted = [...accommodation].sort((a, b) => {
    if (sortBy === 'price_asc') return (a.price_per_night || 0) - (b.price_per_night || 0);
    if (sortBy === 'price_desc') return (b.price_per_night || 0) - (a.price_per_night || 0);
    if (sortBy === 'rating') return (b.rating || 0) - (a.rating || 0);
    return 0;
  });

  return (
    <div className="stay-wrapper">
      <div className="stay-header">
        <div>
          <h3 className="section-heading">🏨 Accommodation & Stay Options</h3>
          <p className="section-subheading">
            Curated stays in {destinationName} for all budgets — backpacker hostels to scenic resorts.
          </p>
        </div>
        <div className="stay-sort-controls">
          <span style={{ fontSize: '0.78rem', color: 'var(--color-text-faint)' }}>Sort:</span>
          <select
            className="form-select"
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            style={{ width: 'auto', padding: '6px 28px 6px 12px', fontSize: '0.8rem' }}
          >
            <option value="recommended">⭐ Recommended</option>
            <option value="price_asc">💰 Price: Low to High</option>
            <option value="price_desc">💎 Price: High to Low</option>
            <option value="rating">🌟 Top Rated</option>
          </select>
        </div>
      </div>

      {sorted.length === 0 ? (
        <div className="empty-substate">Stay listings currently being aggregated.</div>
      ) : (
        <div className="stay-cards-grid">
          {sorted.map((item, idx) => {
            const style = TIER_COLORS[item.type] || { bg: 'rgba(255,255,255,0.06)', text: 'var(--color-text-muted)', border: 'var(--color-border)' };
            return (
              <div key={idx} className="stay-card">
                <div className="stay-card-top">
                  <div>
                    <span
                      className="stay-type-badge"
                      style={{ background: style.bg, color: style.text, borderColor: style.border }}
                    >
                      {item.type}
                    </span>
                    <h4 className="stay-name">{item.name}</h4>
                  </div>
                  {item.rating && (
                    <div className="stay-rating-chip">
                      ⭐ {Number(item.rating).toFixed(1)}
                    </div>
                  )}
                </div>

                <div className="stay-price-row">
                  <div className="stay-price-val">
                    ₹{Number(item.price_per_night || 0).toLocaleString('en-IN')}
                  </div>
                  <span className="stay-price-period">/ night</span>
                </div>

                {item.highlights && item.highlights.length > 0 && (
                  <div className="stay-highlights">
                    {item.highlights.map((h, i) => (
                      <span key={i} className="stay-highlight-chip">
                        ✓ {h}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
