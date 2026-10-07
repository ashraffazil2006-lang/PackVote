// src/components/BudgetInput.jsx
import React from 'react';

const ACCOMMODATION_TYPES = [
  'Hotel', 'GuestHouse', 'Homestay', 'Luxury Camps', 'Boutique Hotel', 'Resort', 'Hostel'
];

const DURATION_PRESETS = [
  { days: 2, nights: 1, label: '2 Days / 1 Night' },
  { days: 3, nights: 2, label: '3 Days / 2 Nights' },
  { days: 4, nights: 3, label: '4 Days / 3 Nights' },
  { days: 5, nights: 4, label: '5 Days / 4 Nights' },
  { days: 7, nights: 6, label: '7 Days / 6 Nights' },
  { days: 10, nights: 9, label: '10 Days / 9 Nights' },
];

const ACCOM_GUIDES = {
  Hostel: 'Dorm / Backpacker stay · ₹600 - ₹1,800 / night',
  Homestay: 'Authentic local home · ₹1,200 - ₹3,000 / night',
  GuestHouse: 'Cozy budget rooms · ₹1,000 - ₹2,500 / night',
  Hotel: 'Standard 3★/4★ hotel · ₹3,000 - ₹7,000 / night',
  'Boutique Hotel': 'Heritage / boutique · ₹5,000 - ₹12,000 / night',
  Resort: 'Full amenities & pool · ₹6,000 - ₹20,000 / night',
  'Luxury Camps': 'Glamping & tent resorts · ₹4,500 - ₹15,000 / night',
};

const NIGHTLY_PRESETS = [1500, 3000, 5000, 8000];
const TOTAL_PRESETS = [6000, 10000, 15000, 25000];

export default function BudgetInput({
  budget,
  accommodationType,
  onBudgetChange,
  onAccomChange,
  budgetMode = 'per_night',
  onBudgetModeChange,
  tripDays = 3,
  tripNights = 2,
  onDurationChange,
  totalTripBudget = 10000,
  onTotalBudgetChange,
}) {
  const isTotalTrip = budgetMode === 'total_trip';
  const effectiveNightly = isTotalTrip
    ? Math.max(100, Math.round(totalTripBudget / (tripNights || 1)))
    : budget;

  const handleModeSwitch = (mode) => {
    if (onBudgetModeChange) {
      onBudgetModeChange(mode);
    }
  };

  const handleDurationSelect = (e) => {
    const selected = DURATION_PRESETS.find(
      d => `${d.days}-${d.nights}` === e.target.value
    );
    if (selected && onDurationChange) {
      onDurationChange(selected.days, selected.nights);
    }
  };

  return (
    <div className="budget-control-block">
      {/* ── Mode Selection Segmented Tabs ── */}
      <div className="budget-mode-header">
        <label className="desktop-form-label" style={{ marginBottom: 6 }}>
          Budget Specification Type
        </label>
        <div className="budget-mode-tabs" role="tablist">
          <button
            type="button"
            className={`budget-mode-tab ${!isTotalTrip ? 'active' : ''}`}
            onClick={() => handleModeSwitch('per_night')}
            aria-selected={!isTotalTrip}
          >
            🌙 Per Night Budget (₹/night)
          </button>
          <button
            type="button"
            className={`budget-mode-tab ${isTotalTrip ? 'active' : ''}`}
            onClick={() => handleModeSwitch('total_trip')}
            aria-selected={isTotalTrip}
          >
            🎒 Overall Trip Budget (₹ total)
          </button>
        </div>
      </div>

      <div className="budget-fields-layout">
        {/* If Total Trip Budget Mode */}
        {isTotalTrip ? (
          <div className="budget-fields-grid">
            <div className="form-group">
              <label className="form-label" htmlFor="total-budget-input">
                🎒 Total Trip Budget (₹ / person)
              </label>
              <input
                id="total-budget-input"
                type="number"
                className="form-input"
                value={totalTripBudget}
                min={500}
                max={500000}
                step={500}
                onChange={(e) => onTotalBudgetChange && onTotalBudgetChange(Number(e.target.value))}
                placeholder="e.g. 6000"
              />
              <div className="budget-preset-chips">
                {TOTAL_PRESETS.map((p) => (
                  <button
                    key={p}
                    type="button"
                    className={`budget-preset-chip ${totalTripBudget === p ? 'active' : ''}`}
                    onClick={() => onTotalBudgetChange && onTotalBudgetChange(p)}
                  >
                    ₹{p.toLocaleString('en-IN')}
                  </button>
                ))}
              </div>
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="trip-duration-select">
                🗓️ Trip Duration
              </label>
              <select
                id="trip-duration-select"
                className="form-select"
                value={`${tripDays}-${tripNights}`}
                onChange={handleDurationSelect}
              >
                {DURATION_PRESETS.map((d) => (
                  <option key={`${d.days}-${d.nights}`} value={`${d.days}-${d.nights}`}>
                    {d.label}
                  </option>
                ))}
              </select>
              <div className="budget-calc-banner">
                <span className="bcalc-icon">💡</span>
                <span>
                  Nightly stay allowance: <strong>₹{effectiveNightly.toLocaleString('en-IN')} / night</strong>
                  <span className="bcalc-sub"> (₹{totalTripBudget.toLocaleString('en-IN')} ÷ {tripNights} {tripNights === 1 ? 'night' : 'nights'})</span>
                </span>
              </div>
            </div>
          </div>
        ) : (
          /* Per Night Budget Mode */
          <div className="budget-fields-grid">
            <div className="form-group">
              <label className="form-label" htmlFor="budget-input">
                💰 Nightly Stay Budget (₹ / person / night)
              </label>
              <input
                id="budget-input"
                type="number"
                className="form-input"
                value={budget}
                min={100}
                max={100000}
                step={100}
                onChange={(e) => onBudgetChange(Number(e.target.value))}
                placeholder="e.g. 5000"
              />
              <div className="budget-preset-chips">
                {NIGHTLY_PRESETS.map((p) => (
                  <button
                    key={p}
                    type="button"
                    className={`budget-preset-chip ${budget === p ? 'active' : ''}`}
                    onClick={() => onBudgetChange(p)}
                  >
                    ₹{p.toLocaleString('en-IN')}/night
                  </button>
                ))}
              </div>
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="trip-duration-preview">
                🗓️ Intended Trip Length
              </label>
              <select
                id="trip-duration-preview"
                className="form-select"
                value={`${tripDays}-${tripNights}`}
                onChange={handleDurationSelect}
              >
                {DURATION_PRESETS.map((d) => (
                  <option key={`${d.days}-${d.nights}`} value={`${d.days}-${d.nights}`}>
                    {d.label}
                  </option>
                ))}
              </select>
              <div className="budget-calc-banner">
                <span className="bcalc-icon">💡</span>
                <span>
                  Estimated {tripDays}-day stay: <strong>₹{(budget * tripNights).toLocaleString('en-IN')} total</strong>
                  <span className="bcalc-sub"> (₹{budget.toLocaleString('en-IN')} × {tripNights} nights)</span>
                </span>
              </div>
            </div>
          </div>
        )}

        {/* ── Accommodation Type Selector ── */}
        <div className="form-group" style={{ marginTop: 10 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 5 }}>
            <label className="form-label" htmlFor="accom-select" style={{ marginBottom: 0 }}>
              🏨 Preferred Accommodation Type
            </label>
            <span className="accom-hint-pill">
              {ACCOM_GUIDES[accommodationType] || 'Standard Stay'}
            </span>
          </div>
          <select
            id="accom-select"
            className="form-select"
            value={accommodationType}
            onChange={(e) => onAccomChange(e.target.value)}
          >
            {ACCOMMODATION_TYPES.map((t) => (
              <option key={t} value={t}>{t}</option>
            ))}
          </select>
        </div>

        {/* ── Clarification Callout Note ── */}
        <div className="budget-clarify-callout">
          <span className="bcc-icon">🤖</span>
          <span className="bcc-text">
            <strong>How PACKVOTE evaluates your budget:</strong> Our Linear Regression ML model estimates the actual market cost of <strong>1 room per night</strong> in each destination. If that nightly rate is ≤ your stay budget, the destination is marked <strong>Within Budget</strong>.
          </span>
        </div>
      </div>
    </div>
  );
}
