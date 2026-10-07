// src/components/RecommendationCard.jsx

const TYPE_ICONS = {
  Beach:      '🏖️',
  Historical: '🏛️',
  Nature:     '🌿',
  Adventure:  '🧗',
  City:       '🏙️',
};

export default function RecommendationCard({ rec, meta, delay = 0, isCompare, onToggleCompare, onExplore }) {
  const typeClass = `type-${rec.destination_type}`;
  const typeIcon  = TYPE_ICONS[rec.destination_type] || '🗺️';

  const budgetBadgeClass =
    rec.budget_status === 'Within budget' ? 'badge-success'
    : rec.budget_status === 'Above budget' ? 'badge-warning'
    : 'badge-accent';

  // Extract top 3 spots cleanly
  const topSpots = (rec.tourist_spots || []).slice(0, 3);
  const remainingSpotsCount = (rec.total_spots || rec.tourist_spots?.length || 0) - topSpots.length;

  return (
    <div
      className={`dest-card-desktop ${isCompare ? 'card-selected' : ''}`}
      style={{ animationDelay: `${delay}s` }}
    >
      {/* ── Top Header Row ── */}
      <div className="card-top-row">
        <div className="card-rank-badge">#{rec.rank}</div>
        <div className="card-top-badges">
          <span className={`dest-type-badge ${typeClass}`}>
            {typeIcon} {rec.destination_type}
          </span>
          <button
            type="button"
            className={`btn-compare-pill ${isCompare ? 'active' : ''}`}
            onClick={(e) => {
              e.stopPropagation();
              onToggleCompare && onToggleCompare(rec);
            }}
            title="Compare up to 3 destinations"
          >
            {isCompare ? '✓ In Compare' : '+ Compare'}
          </button>
        </div>
      </div>

      {/* ── Destination Identity ── */}
      <div className="card-identity-block">
        <h3
          className="dest-card-title"
          onClick={() => onExplore && onExplore(rec)}
          title="Click to view full trip plan & itinerary"
        >
          {rec.destination}
        </h3>
        <div className="dest-location-row">
          <span>📍 {rec.state}</span>
          <span className="dest-dot-sep">•</span>
          <span className="dest-season-text">{rec.in_peak_season ? '🌤️ Peak Season' : 'Off-Peak'}</span>
        </div>
      </div>

      {/* ── Compatibility Score Meter ── */}
      <div className="card-compat-bar-box">
        <div className="compat-bar-header">
          <span className="compat-title">Group Compatibility</span>
          <span className="compat-percentage">{rec.group_compatibility.toFixed(1)}%</span>
        </div>
        <div className="compat-meter-track">
          <div
            className="compat-meter-fill"
            style={{ width: `${Math.min(100, Math.max(0, rec.group_compatibility))}%` }}
          />
        </div>
      </div>

      {/* ── 3-Column Metrics Grid ── */}
      <div className="card-metrics-grid">
        <div className="metric-box">
          <span className="metric-lbl">⭐ Rating</span>
          <span className="metric-val">{rec.average_rating.toFixed(1)} / 5</span>
        </div>
        <div className="metric-box">
          <span className="metric-lbl">💰 Est. Stay/Night</span>
          <span className="metric-val">
            {rec.predicted_accommodation_cost != null
              ? `₹${Math.round(rec.predicted_accommodation_cost).toLocaleString('en-IN')}`
              : 'N/A'}
          </span>
          {rec.predicted_accommodation_cost != null && (
            <span className="metric-sub-detail">
              ≈ ₹{Math.round(rec.predicted_accommodation_cost * (meta?.trip_nights || 2)).toLocaleString('en-IN')} ({meta?.trip_days || 3}d)
            </span>
          )}
        </div>
        <div className="metric-box">
          <span className="metric-lbl">💳 Budget</span>
          <span className={`metric-val ${rec.budget_status === 'Within budget' ? 'text-green' : 'text-amber'}`}>
            {rec.budget_status === 'Within budget' ? '✓ Within' : '⚠ Over'}
          </span>
        </div>
      </div>

      {/* ── Key Tourist Spots Pills ── */}
      <div className="card-spots-section">
        <div className="spots-pills-row">
          {topSpots.map((spot, idx) => (
            <span key={spot.name || idx} className="spot-micro-pill" title={spot.characteristics}>
              ✦ {spot.name}
            </span>
          ))}
          {remainingSpotsCount > 0 && (
            <span className="spot-more-pill">+{remainingSpotsCount} more</span>
          )}
        </div>
      </div>

      {/* ── Action Button ── */}
      <div className="card-footer-action">
        <button
          type="button"
          className="btn-card-explore"
          onClick={() => onExplore && onExplore(rec)}
        >
          <span>View Full Trip Plan</span>
          <span className="btn-explore-arrow">→</span>
        </button>
      </div>
    </div>
  );
}
