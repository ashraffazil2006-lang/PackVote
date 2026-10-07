// src/pages/Home.jsx
import { useState } from 'react';
import TravelerInput from '../components/TravelerInput';
import BudgetInput from '../components/BudgetInput';
import RecommendationList from '../components/RecommendationList';
import Loading from '../components/Loading';
import { getRecommendations } from '../services/api';

const DEFAULT_TRAVELER = () => ({ preferences: [] });

export default function Home({ onNavigate }) {
  const [travelers, setTravelers] = useState([DEFAULT_TRAVELER(), DEFAULT_TRAVELER()]);
  const [budgetMode, setBudgetMode] = useState('per_night'); // 'per_night' | 'total_trip'
  const [budget, setBudget] = useState(5000);
  const [totalTripBudget, setTotalTripBudget] = useState(10000);
  const [tripDays, setTripDays] = useState(3);
  const [tripNights, setTripNights] = useState(2);
  const [accomType, setAccomType] = useState('Hotel');
  const [topN, setTopN] = useState(6);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [meta, setMeta] = useState(null);
  const [error, setError] = useState(null);
  const [isEditingForm, setIsEditingForm] = useState(false);

  const addTraveler = () => setTravelers(t => [...t, DEFAULT_TRAVELER()]);
  const removeTraveler = (i) => setTravelers(t => t.filter((_, idx) => idx !== i));
  const updateTraveler = (i, prefs) =>
    setTravelers(t => t.map((tr, idx) => idx === i ? { ...tr, preferences: prefs } : tr));

  const effectiveNightlyBudget = budgetMode === 'total_trip'
    ? Math.max(100, Math.round(totalTripBudget / (tripNights || 1)))
    : budget;

  const canSubmit = travelers.length > 0 && travelers.every(t => t.preferences.length > 0) && effectiveNightlyBudget > 0;

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!canSubmit) return;
    setLoading(true);
    setError(null);

    try {
      const payload = {
        travelers: travelers.map(t => ({ preferences: t.preferences })),
        budget_per_person: effectiveNightlyBudget,
        accommodation_type: accomType,
        top_n: topN,
      };
      const data = await getRecommendations(payload);
      setResults(data.recommendations);
      setMeta({
        total_travelers:   data.total_travelers,
        budget_per_person: effectiveNightlyBudget,
        accommodation_type: data.accommodation_type,
        budget_mode: budgetMode,
        total_trip_budget: budgetMode === 'total_trip' ? totalTripBudget : (budget * tripNights),
        trip_days: tripDays,
        trip_nights: tripNights,
      });
      setIsEditingForm(false);

      // Smooth scroll down to results
      setTimeout(() => {
        const el = document.getElementById('results-section-anchor');
        if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 50);
    } catch (err) {
      setError(err.message || 'Something went wrong. Please check backend connection.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="planner-page-wrapper">
      <div className="desktop-container">
        {/* ── Section 6: Compact ML Hero / Information Section ── */}
        <div className="planner-ml-banner">
          <div className="ml-banner-left">
            <span className="ml-banner-badge">🤖 8-Model AI Ensemble</span>
            <h2 className="ml-banner-title">Group Travel Intelligence</h2>
            <p className="ml-banner-sub">ML-powered destination recommendations tailored for your entire group</p>
          </div>

          <div className="ml-banner-right">
            <div className="ml-stats-trio">
              <div className="ml-stat-item">
                <span className="ml-stat-num">5,000+</span>
                <span className="ml-stat-lbl">Travelers</span>
              </div>
              <div className="ml-stat-sep" />
              <div className="ml-stat-item">
                <span className="ml-stat-num">2,000+</span>
                <span className="ml-stat-lbl">Tourist Spots</span>
              </div>
              <div className="ml-stat-sep" />
              <div className="ml-stat-item">
                <span className="ml-stat-num">20</span>
                <span className="ml-stat-lbl">Destinations</span>
              </div>
            </div>
            <div className="ml-consensus-tag">⚡ Vectorized ML Consensus (~60ms)</div>
          </div>
        </div>

        {/* ── Section 7: Compact Edit Group Details Bar (When Results Exist) ── */}
        {results && (
          <div className="planner-nav-bar-compact">
            <button
              type="button"
              className="btn-edit-group-compact"
              onClick={() => setIsEditingForm(!isEditingForm)}
            >
              <span>{isEditingForm ? '✕ Close Group Form' : '← Edit Group Details / Budget'}</span>
            </button>
            <div className="planner-nav-summary">
              Showing recommendations for <strong>{travelers.length} travelers</strong> · Budget: <strong>₹{budget.toLocaleString('en-IN')}/person</strong> ({accomType})
            </div>
          </div>
        )}

        {/* ── Group Details & Budget Form (Shown if no results yet, or toggled via Edit) ── */}
        {(!results || isEditingForm) && (
          <div className="planner-form-container-desktop animate-fadeIn">
            <div className="form-card-desktop">
              <div className="form-card-header">
                <div className="form-header-icon">👥</div>
                <div>
                  <h3 className="form-header-title">
                    {results ? 'Edit Group Travel Preferences' : 'Group Details & Preferences'}
                  </h3>
                  <p className="form-header-sub">
                    Select interests for each traveler and set your per-person nightly stay budget.
                  </p>
                </div>
              </div>

              <form onSubmit={handleSubmit}>
                <div className="form-section-block">
                  <label className="desktop-form-label">Group Members & Travel Tastes</label>
                  <TravelerInput
                    travelers={travelers}
                    onUpdate={updateTraveler}
                    onAdd={addTraveler}
                    onRemove={removeTraveler}
                  />
                </div>

                <div className="form-section-block">
                  <BudgetInput
                    budget={budget}
                    accommodationType={accomType}
                    onBudgetChange={setBudget}
                    onAccomChange={setAccomType}
                    budgetMode={budgetMode}
                    onBudgetModeChange={setBudgetMode}
                    tripDays={tripDays}
                    tripNights={tripNights}
                    onDurationChange={(d, n) => { setTripDays(d); setTripNights(n); }}
                    totalTripBudget={totalTripBudget}
                    onTotalBudgetChange={setTotalTripBudget}
                  />
                </div>

                <div className="form-section-block" style={{ marginTop: 14 }}>
                  <label className="desktop-form-label" htmlFor="topn-select-desktop">
                    Number of Recommendations
                  </label>
                  <select
                    id="topn-select-desktop"
                    className="desktop-form-select"
                    value={topN}
                    onChange={e => setTopN(Number(e.target.value))}
                  >
                    {[3, 4, 5, 6, 7, 8, 9, 10].map(n => (
                      <option key={n} value={n}>{n} destinations</option>
                    ))}
                  </select>
                </div>

                {error && (
                  <div className="error-alert" style={{ margin: '14px 0' }}>
                    <span className="error-icon">⚠️</span>
                    <div className="error-content">
                      <div className="error-title">Error</div>
                      <div className="error-msg">{error}</div>
                    </div>
                    <button className="error-dismiss" onClick={() => setError(null)}>✕</button>
                  </div>
                )}

                <div className="form-action-row">
                  <button
                    type="submit"
                    className="btn-submit-planner"
                    disabled={!canSubmit || loading}
                  >
                    {loading ? (
                      <>
                        <div style={{ width: 16, height: 16, border: '2px solid rgba(255,255,255,0.3)', borderTopColor: 'white', borderRadius: '50%', animation: 'spin 0.6s linear infinite' }} />
                        Analyzing with 8 ML Models...
                      </>
                    ) : (
                      <>✨ Get Recommendations</>
                    )}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* ── Results Anchor & Destination Grid ── */}
        <div id="results-section-anchor">
          {loading ? (
            <div style={{ padding: '60px 0' }}>
              <Loading />
            </div>
          ) : results ? (
            <RecommendationList recommendations={results} meta={meta} onNavigate={onNavigate} />
          ) : null}
        </div>
      </div>
    </div>
  );
}
