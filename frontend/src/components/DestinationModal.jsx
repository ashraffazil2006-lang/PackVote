// src/components/DestinationModal.jsx
import { useState, useEffect } from 'react';
import { getDestinationDetails } from '../services/api';
import ItinerarySection from './ItinerarySection';
import FoodSection from './FoodSection';
import StaySection from './StaySection';
import WeatherSection from './WeatherSection';
import SpotDetailGrid from './SpotDetailGrid';

const TABS = [
  { id: 'itinerary', label: '🗺️ Itinerary & Timeline' },
  { id: 'spots',     label: '📍 Tourist Spots' },
  { id: 'food',      label: '🍛 Food & Dining' },
  { id: 'stays',     label: '🏨 Stays & Hotels' },
  { id: 'weather',   label: '🌤️ Weather' },
  { id: 'guide',     label: '💡 Travel Guide & Transit' },
  { id: 'similar',   label: '🤖 Similar Destinations' },
];

export default function DestinationModal({ destinationName, recommendation, onClose, onSelectDestination }) {
  const [activeTab, setActiveTab] = useState('itinerary');
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let mounted = true;
    setLoading(true);
    setError(null);

    getDestinationDetails(destinationName)
      .then((res) => {
        if (mounted) {
          setData(res.data);
          setLoading(false);
        }
      })
      .catch((err) => {
        if (mounted) {
          setError(err.message || 'Failed to load trip details');
          setLoading(false);
        }
      });

    return () => {
      mounted = false;
    };
  }, [destinationName]);

  // Handle escape key
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onClose]);

  if (!destinationName) return null;

  const overview = data?.overview || {};
  const meta = data?.meta || {};
  const howToReach = data?.how_to_reach || {};
  const tips = data?.tips || [];
  const nearby = data?.nearby || [];
  const similar = data?.similar_destinations || [];

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-dialog" onClick={(e) => e.stopPropagation()}>
        {/* ── Modal Close Button ── */}
        <button className="modal-close-btn" onClick={onClose} aria-label="Close dialog">
          ✕
        </button>

        {/* ── Modal Hero Banner ── */}
        <div className="modal-hero">
          <div className="modal-hero-content">
            <div className="modal-eyebrow">
              <span className="badge badge-primary">📍 {meta.state || recommendation?.state || 'India'}</span>
              <span className="badge badge-accent">🏷️ {meta.destination_type || recommendation?.destination_type || 'Travel'}</span>
              {recommendation?.group_compatibility && (
                <span className="badge badge-success">
                  ⭐ {recommendation.group_compatibility.toFixed(1)}% Match
                </span>
              )}
            </div>

            <h2 className="modal-destination-title">{data?.destination || destinationName}</h2>
            <p className="modal-tagline">
              {overview.tagline || meta.description || recommendation?.why_this_destination || 'Explore complete guide and travel timeline.'}
            </p>

            {/* Key Facts Quick Bar */}
            <div className="modal-quick-facts">
              {overview.avg_trip_days && (
                <div className="quick-fact-item">
                  <span className="qf-icon">⏱️</span>
                  <div>
                    <div className="qf-label">Recommended Trip</div>
                    <div className="qf-val">{overview.avg_trip_days} Days</div>
                  </div>
                </div>
              )}
              {overview.budget_per_day && (
                <div className="quick-fact-item">
                  <span className="qf-icon">💰</span>
                  <div>
                    <div className="qf-label">Daily Budget</div>
                    <div className="qf-val">₹{overview.budget_per_day.budget?.toLocaleString('en-IN')} - ₹{overview.budget_per_day.mid?.toLocaleString('en-IN')} / day</div>
                  </div>
                </div>
              )}
              {meta.best_time && (
                <div className="quick-fact-item">
                  <span className="qf-icon">📅</span>
                  <div>
                    <div className="qf-label">Best Visiting Season</div>
                    <div className="qf-val">{meta.best_time}</div>
                  </div>
                </div>
              )}
              {overview.language && (
                <div className="quick-fact-item">
                  <span className="qf-icon">🗣️</span>
                  <div>
                    <div className="qf-label">Languages</div>
                    <div className="qf-val">{overview.language}</div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* ── Tab Navigation Bar ── */}
        <div className="modal-tabs-bar">
          <div className="modal-tabs-scroller">
            {TABS.map((tab) => (
              <button
                key={tab.id}
                className={`modal-tab-button ${activeTab === tab.id ? 'active' : ''}`}
                onClick={() => setActiveTab(tab.id)}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        {/* ── Modal Body Area ── */}
        <div className="modal-body-scrollable">
          {loading ? (
            <div className="modal-loading-state">
              <div className="modal-spinner" />
              <div className="modal-loading-text">Synthesizing travel intelligence for {destinationName}...</div>
            </div>
          ) : error ? (
            <div className="modal-error-state">
              <div style={{ fontSize: '2rem', marginBottom: 12 }}>⚠️</div>
              <div style={{ fontWeight: 600, marginBottom: 6 }}>Could not load details</div>
              <div style={{ color: 'var(--color-text-faint)', fontSize: '0.85rem' }}>{error}</div>
            </div>
          ) : (
            <>
              {/* ── Tab 1: Itinerary ── */}
              {activeTab === 'itinerary' && (
                <ItinerarySection
                  itinerary={data.itinerary}
                  destinationName={data.destination}
                />
              )}

              {/* ── Tab 2: Tourist Spots ── */}
              {activeTab === 'spots' && (
                <SpotDetailGrid
                  spots={data.tourist_spots || []}
                  destinationName={data.destination}
                />
              )}

              {/* ── Tab 3: Food & Dining ── */}
              {activeTab === 'food' && (
                <FoodSection
                  food={data.food || []}
                  restaurants={data.restaurants || []}
                  destinationName={data.destination}
                />
              )}

              {/* ── Tab 4: Stays & Hotels ── */}
              {activeTab === 'stays' && (
                <StaySection
                  accommodation={data.accommodation || []}
                  destinationName={data.destination}
                />
              )}

              {/* ── Tab 5: Weather ── */}
              {activeTab === 'weather' && (
                <WeatherSection
                  weather={data.weather || []}
                  destinationName={data.destination}
                  bestTime={meta.best_time}
                />
              )}

              {/* ── Tab 6: Travel Guide & Transit ── */}
              {activeTab === 'guide' && (
                <div className="guide-wrapper">
                  <h3 className="section-heading">💡 Travel Logistics & Transit Guide</h3>
                  <p className="section-subheading">Essential connectivity and on-ground practical advice for {data.destination}.</p>

                  <div className="guide-grid">
                    {/* How to Reach */}
                    <div className="guide-card">
                      <h4 className="guide-card-title">✈️ How to Reach</h4>
                      <div className="guide-card-items">
                        {howToReach.flight && (
                          <div className="transit-item">
                            <span className="transit-icon">🛫</span>
                            <div>
                              <strong>By Air:</strong> {howToReach.flight}
                            </div>
                          </div>
                        )}
                        {howToReach.train && (
                          <div className="transit-item">
                            <span className="transit-icon">🚆</span>
                            <div>
                              <strong>By Train:</strong> {howToReach.train}
                            </div>
                          </div>
                        )}
                        {howToReach.bus && (
                          <div className="transit-item">
                            <span className="transit-icon">🚌</span>
                            <div>
                              <strong>By Bus / Road:</strong> {howToReach.bus}
                            </div>
                          </div>
                        )}
                      </div>
                    </div>

                    {/* Local Transport */}
                    <div className="guide-card">
                      <h4 className="guide-card-title">🛵 Local Commute & Transit</h4>
                      <div className="local-transit-chips">
                        {(howToReach.local_transport || ['Auto-rickshaws', 'Local Taxis', 'Walking']).map((t, idx) => (
                          <span key={idx} className="transit-chip">
                            ✓ {t}
                          </span>
                        ))}
                      </div>
                    </div>

                    {/* Pro Travel Tips */}
                    <div className="guide-card full-width">
                      <h4 className="guide-card-title">📝 Practical Pro-Tips</h4>
                      <ul className="tips-list">
                        {tips.map((tip, i) => (
                          <li key={i} className="tip-item">
                            <span className="tip-bullet">💡</span>
                            <span>{tip}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    {/* Nearby Getaways */}
                    {nearby.length > 0 && (
                      <div className="guide-card full-width">
                        <h4 className="guide-card-title">🚗 Nearby Add-on Getaways</h4>
                        <div className="nearby-chips">
                          {nearby.map((nb, i) => (
                            <span key={i} className="nearby-chip">
                              📍 {nb}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* ── Tab 7: Similar Destinations (TF-IDF ML Model) ── */}
              {activeTab === 'similar' && (
                <div className="similar-wrapper">
                  <div className="block-header">
                    <h3 className="section-heading">🤖 AI-Identified Similar Destinations</h3>
                    <p className="section-subheading">
                      Derived from our trained TF-IDF & Cosine Similarity ML model matching landscape, activities, and geographical affinity.
                    </p>
                  </div>

                  {similar.length === 0 ? (
                    <div className="empty-substate">No similar destination recommendations calculated.</div>
                  ) : (
                    <div className="similar-cards-grid">
                      {similar.map((sim, i) => (
                        <div key={i} className="similar-card">
                          <div className="similar-card-top">
                            <div className="similar-dest-name">{sim.destination}</div>
                            <span className="similarity-badge">
                              {sim.similarity_score}% Match
                            </span>
                          </div>
                          <div className="similar-meta">
                            <span>📍 {sim.state}</span>
                            <span>🏷️ {sim.type}</span>
                            {sim.rating > 0 && <span>⭐ {sim.rating.toFixed(1)}/5</span>}
                          </div>
                          <button
                            className="similar-explore-btn"
                            onClick={() => {
                              if (onSelectDestination) {
                                onSelectDestination(sim.destination);
                              }
                            }}
                          >
                            Explore This Destination →
                          </button>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}
