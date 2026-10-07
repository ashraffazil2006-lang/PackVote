// src/components/SpotDetailGrid.jsx
import { useState, useMemo } from 'react';

const CATEGORIES = ['All', 'Beach', 'Nature', 'Heritage', 'Adventure', 'Scenic', 'Temple', 'Lake', 'Waterfall', 'Fort'];

const KNOWN_TAGS = [
  'beach', 'nature', 'historical', 'adventure', 'scenic', 'heritage',
  'cultural', 'temple', 'photography', 'lake', 'mountain', 'waterfall',
  'family', 'wildlife', 'trekking', 'fort', 'palace'
];

function extractTags(spot) {
  if (Array.isArray(spot.tags) && spot.tags.length > 0) {
    return spot.tags;
  }
  const raw = (spot.characteristics || '').trim();
  if (!raw) return ['Sightseeing'];
  if (raw.includes(',')) {
    return raw.split(',').map(t => t.trim()).filter(Boolean);
  }
  // If concatenated without commas like "adventureheritagecultural"
  const lower = raw.toLowerCase();
  const matched = KNOWN_TAGS.filter(k => lower.includes(k)).map(k => k.charAt(0).toUpperCase() + k.slice(1));
  return matched.length > 0 ? matched : [raw];
}

export default function SpotDetailGrid({ spots = [], destinationName }) {
  const [search, setSearch] = useState('');
  const [activeCategory, setActiveCategory] = useState('All');

  // Filter out any synthetic View Point placeholders
  const verifiedSpots = useMemo(() => {
    return (spots || []).filter(s => {
      if (!s || !s.name) return false;
      return !s.name.toLowerCase().match(/\bview\s*point\s*\d+/);
    });
  }, [spots]);

  const filtered = useMemo(() => {
    return verifiedSpots.filter((s) => {
      const nameMatch = (s.name || '').toLowerCase().includes(search.toLowerCase());
      const charMatch = (s.characteristics || '').toLowerCase().includes(search.toLowerCase());
      const addrMatch = (s.address || '').toLowerCase().includes(search.toLowerCase());
      const matchesSearch = nameMatch || charMatch || addrMatch;

      if (!matchesSearch) return false;
      if (activeCategory === 'All') return true;

      const tags = extractTags(s);
      return tags.some(t => t.toLowerCase().includes(activeCategory.toLowerCase())) ||
        (s.characteristics || '').toLowerCase().includes(activeCategory.toLowerCase());
    });
  }, [verifiedSpots, search, activeCategory]);

  return (
    <div className="spots-grid-wrapper">
      <div className="spots-grid-header">
        <div>
          <h3 className="section-heading">📍 Verified Tourist Spots & Attractions</h3>
          <p className="section-subheading">
            Explore {verifiedSpots.length} authentic, famous tourist attractions in {destinationName}.
          </p>
        </div>

        <div className="spots-filter-bar">
          <input
            type="text"
            className="form-input spots-search-input"
            placeholder="🔎 Search spots by name, area, or category..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
      </div>

      <div className="category-chips-row">
        {CATEGORIES.map((cat) => (
          <button
            key={cat}
            className={`cat-chip-btn ${activeCategory === cat ? 'active' : ''}`}
            onClick={() => setActiveCategory(cat)}
          >
            {cat}
          </button>
        ))}
      </div>

      <div className="spots-count-indicator">
        Showing <strong>{filtered.length}</strong> of {verifiedSpots.length} verified places
      </div>

      {filtered.length === 0 ? (
        <div className="empty-substate">No verified tourist attractions match your search criteria.</div>
      ) : (
        <div className="detailed-spots-grid">
          {filtered.map((spot, i) => {
            const tags = extractTags(spot);
            const address = spot.address || `${spot.name}, ${destinationName}, India`;
            const mapsUrl = spot.maps_url || `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(spot.name + ' ' + (destinationName || '') + ' India')}`;
            const entryFee = spot.entry_fee !== undefined ? spot.entry_fee : 0;
            const bestTime = spot.best_time || 'Anytime';

            return (
              <div key={spot.name || i} className="detailed-spot-card">
                <div className="spot-card-top">
                  <div className="spot-number">#{i + 1}</div>
                  <div className="spot-title-area">
                    <h4 className="spot-name">{spot.name}</h4>
                    <div className="spot-tags-row">
                      {tags.slice(0, 3).map((tag, tIdx) => (
                        <span key={tIdx} className="spot-tag-chip">
                          {tag}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>

                {/* Human-readable Address / Location */}
                <div className="spot-address-row">
                  <span className="spot-address-icon">📍</span>
                  <span className="spot-address-text">{address}</span>
                </div>

                {/* Card Meta & Maps Action */}
                <div className="spot-card-footer">
                  <div className="spot-meta-chips">
                    <span className="spot-meta-badge">
                      🎫 {entryFee > 0 ? `₹${entryFee}` : 'Free Entry'}
                    </span>
                    <span className="spot-meta-badge">
                      ⏰ {bestTime}
                    </span>
                  </div>

                  <a
                    href={mapsUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="btn-spot-maps"
                    title={`View ${spot.name} on Google Maps`}
                  >
                    🗺️ View on Maps ↗
                  </a>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
