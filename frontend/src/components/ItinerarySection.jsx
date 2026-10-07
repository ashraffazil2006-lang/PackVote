// src/components/ItinerarySection.jsx
import { useState } from 'react';

export default function ItinerarySection({ itinerary, destinationName }) {
  const [selectedPlan, setSelectedPlan] = useState('3_day');

  const plan3 = itinerary?.['3_day'] || [];
  const plan5 = itinerary?.['5_day'] || [];
  const activePlan = selectedPlan === '5_day' && plan5.length > 0 ? plan5 : plan3;

  return (
    <div className="itinerary-wrapper">
      <div className="itinerary-header">
        <div>
          <h3 className="section-heading">🗓️ Day-by-Day Travel Itinerary</h3>
          <p className="section-subheading">
            Curated daily flow for {destinationName || 'this destination'} covering mornings, afternoons, and evenings.
          </p>
        </div>
        <div className="plan-toggle">
          <button
            className={`plan-toggle-btn ${selectedPlan === '3_day' ? 'active' : ''}`}
            onClick={() => setSelectedPlan('3_day')}
          >
            ⚡ 3-Day Plan
          </button>
          {plan5.length > 0 && (
            <button
              className={`plan-toggle-btn ${selectedPlan === '5_day' ? 'active' : ''}`}
              onClick={() => setSelectedPlan('5_day')}
            >
              🌴 5-Day Plan
            </button>
          )}
        </div>
      </div>

      {activePlan.length === 0 ? (
        <div className="empty-substate">Custom itinerary being synthesized for this destination.</div>
      ) : (
        <div className="itinerary-cards-grid">
          {activePlan.map((dayItem, idx) => (
            <div key={idx} className="day-card">
              <div className="day-card-header">
                <div className="day-badge">Day {dayItem.day || idx + 1}</div>
                <div className="day-title">{dayItem.title}</div>
              </div>
              <div className="day-timeline">
                {dayItem.morning && (
                  <div className="timeline-slot">
                    <div className="timeline-marker morning">🌅</div>
                    <div className="timeline-body">
                      <div className="timeline-label morning">Morning</div>
                      <div className="timeline-desc">{dayItem.morning}</div>
                    </div>
                  </div>
                )}
                {dayItem.afternoon && (
                  <div className="timeline-slot">
                    <div className="timeline-marker afternoon">☀️</div>
                    <div className="timeline-body">
                      <div className="timeline-label afternoon">Afternoon</div>
                      <div className="timeline-desc">{dayItem.afternoon}</div>
                    </div>
                  </div>
                )}
                {dayItem.evening && (
                  <div className="timeline-slot">
                    <div className="timeline-marker evening">🌙</div>
                    <div className="timeline-body">
                      <div className="timeline-label evening">Evening & Night</div>
                      <div className="timeline-desc">{dayItem.evening}</div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
