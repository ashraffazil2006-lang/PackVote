// src/pages/LandingPage.jsx
import { useState } from 'react';

const CATEGORIES = [
  { id: 'Beach', name: 'Beach Escapes', icon: '🏖️', count: '4 Hubs', examples: 'Goa, Andaman, Gokarna' },
  { id: 'Nature', name: 'Nature & Backwaters', icon: '🌿', count: '5 Hubs', examples: 'Kerala, Coorg, Munnar' },
  { id: 'Adventure', name: 'Adventure & Treks', icon: '🧗', count: '4 Hubs', examples: 'Leh Ladakh, Manali, Rishikesh' },
  { id: 'Historical', name: 'Heritage & Culture', icon: '🏛️', count: '5 Hubs', examples: 'Jaipur, Varanasi, Hampi' },
  { id: 'City', name: 'City Breaks', icon: '🏙️', count: '2 Hubs', examples: 'Udaipur, Shimla, Mysore' },
];

const TOP_DESTINATIONS = [
  {
    name: 'Kerala Backwaters',
    state: 'Kerala',
    type: 'Nature',
    typeIcon: '🌿',
    rating: 4.8,
    spotsCount: 60,
    budgetPerNight: 4800,
    tagline: 'Cruise scenic palm-fringed canals on traditional houseboats & savor authentic Sadya feasts.',
    highlights: ['Alleppey Backwaters', 'Vembanad Lake', 'Kumarakom'],
    sentiment: '98% Positive',
    bestTime: 'Oct - Mar',
  },
  {
    name: 'Goa',
    state: 'Goa',
    type: 'Beach',
    typeIcon: '🏖️',
    rating: 4.7,
    spotsCount: 30,
    budgetPerNight: 3500,
    tagline: 'Sun-drenched coastal beaches, vibrant water sports, Portuguese architecture & seafood.',
    highlights: ['Palolem Beach', 'Baga Beach', 'Fort Aguada'],
    sentiment: '96% Positive',
    bestTime: 'Nov - Feb',
  },
  {
    name: 'Leh Ladakh',
    state: 'Jammu & Kashmir',
    type: 'Adventure',
    typeIcon: '🧗',
    rating: 4.9,
    spotsCount: 30,
    budgetPerNight: 5500,
    tagline: 'High-altitude Himalayan passes, ancient Buddhist monasteries & azure Pangong Lake.',
    highlights: ['Pangong Tso', 'Nubra Valley', 'Khardung La'],
    sentiment: '99% Positive',
    bestTime: 'May - Sep',
  },
  {
    name: 'Manali',
    state: 'Himachal Pradesh',
    type: 'Adventure',
    typeIcon: '🏔️',
    rating: 4.6,
    spotsCount: 30,
    budgetPerNight: 4200,
    tagline: 'Snow-capped Solang Valley, Rohtang Pass, riverside pine woods & adventure sports.',
    highlights: ['Solang Valley', 'Rohtang Pass', 'Hadimba Temple'],
    sentiment: '95% Positive',
    bestTime: 'Oct - Jun',
  },
  {
    name: 'Jaipur',
    state: 'Rajasthan',
    type: 'Historical',
    typeIcon: '🏛️',
    rating: 4.7,
    spotsCount: 30,
    budgetPerNight: 3800,
    tagline: 'The iconic Pink City featuring majestic Amer Fort, Hawa Mahal & royal Rajasthani thali.',
    highlights: ['Amer Fort', 'Hawa Mahal', 'City Palace'],
    sentiment: '97% Positive',
    bestTime: 'Oct - Mar',
  },
  {
    name: 'Varanasi',
    state: 'Uttar Pradesh',
    type: 'Historical',
    typeIcon: '🕉️',
    rating: 4.6,
    spotsCount: 30,
    budgetPerNight: 2800,
    tagline: 'Timeless spiritual capital with mystical Ganga Aarti, sacred ghats & ancient lanes.',
    highlights: ['Dashashwamedh Ghat', 'Kashi Vishwanath', 'Assi Ghat'],
    sentiment: '96% Positive',
    bestTime: 'Oct - Mar',
  },
];

const ML_MODELS = [
  { name: 'Random Forest Regressor', tag: 'Consensus Ranking', desc: 'Ensemble of 200 trees evaluating group agreement across multi-dimensional criteria' },
  { name: 'K-Means Clustering', tag: 'Group Segmentation', desc: 'Clusters diverse individual group interests into cohesive traveler preference archetypes' },
  { name: 'SVD Collaborative Filtering', tag: 'Matrix Factorization', desc: 'Latent taste vectors matching group preferences against verified travel patterns' },
  { name: 'K-Nearest Neighbors (KNN)', tag: 'Hub Archetypes', desc: 'Multi-class classifier mapping group activity profiles to nearest destination hubs' },
  { name: 'Naive Bayes Classifier', tag: 'Budget Viability', desc: 'Probabilistic validation assessing whether destination costs fit the group budget' },
  { name: 'Decision Tree Regressor', tag: 'Satisfaction Split', desc: 'Feature splits calculating transparent, explainable group satisfaction metrics' },
  { name: 'Linear Regression', tag: 'Cost Estimation', desc: 'Accurately predicts nightly stay rates across hotel, hostel, and homestay tiers' },
  { name: 'TF-IDF Cosine Similarity', tag: 'Content Matching', desc: 'Computes deep semantic similarities between spots, activities, and regional attractions' },
];

export default function LandingPage({ onPlanTrip, onExploreDestination, onNavigate }) {
  const [selectedCategory, setSelectedCategory] = useState('All');

  const scrollTo = (id) => {
    const el = document.getElementById(id);
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

  const filteredDestinations = selectedCategory === 'All'
    ? TOP_DESTINATIONS
    : TOP_DESTINATIONS.filter(d => d.type === selectedCategory);

  return (
    <div className="landing-page-root">
      {/* ═════════════════════════════════════════════
          1. HERO SECTION (Structured like reference)
          ═════════════════════════════════════════════ */}
      <section id="hero" className="rent-hero">
        <div className="desktop-container">
          <div className="rent-hero-inner">
            {/* Top Pill Badge */}
            <div className="rent-hero-badge">
              <span>●</span>
              <span>8-MODEL ML GROUP TRAVEL CONSENSUS</span>
            </div>

            {/* Main Headline */}
            <h1 className="rent-hero-title">
              Plan Together.<br />
              <span className="text-gradient">Travel Smarter.</span>
            </h1>

            {/* Subtitle */}
            <p className="rent-hero-subtitle">
              PACKVOTE uses Machine Learning to understand your group's preferences, budget, interests,
              and travel history to recommend destinations that everyone can enjoy.
            </p>

            {/* Interactive Hero Quick-Planner Bar (Like Reference Search Bar) */}
            <div className="rent-search-bar" onClick={onPlanTrip}>
              <div className="rsb-item">
                <span className="rsb-icon">👥</span>
                <div className="rsb-text">
                  <div className="rsb-label">Group Size</div>
                  <div className="rsb-val">2 - 10 Travelers</div>
                </div>
              </div>
              <div className="rsb-divider" />
              <div className="rsb-item">
                <span className="rsb-icon">💰</span>
                <div className="rsb-text">
                  <div className="rsb-label">Budget</div>
                  <div className="rsb-val">₹5,000 / person</div>
                </div>
              </div>
              <div className="rsb-divider" />
              <div className="rsb-item">
                <span className="rsb-icon">🏨</span>
                <div className="rsb-text">
                  <div className="rsb-label">Stay Type</div>
                  <div className="rsb-val">Hotel / Resort</div>
                </div>
              </div>
              <button
                type="button"
                className="rsb-btn"
                onClick={(e) => {
                  e.stopPropagation();
                  onPlanTrip();
                }}
              >
                Plan Your Trip →
              </button>
            </div>

            {/* Preference Chips Row */}
            <div className="rent-hero-tags">
              <span className="rent-tags-label">Popular Tastes:</span>
              {['🏖️ Beach', '🌿 Nature', '🧗 Adventure', '🏛️ Historical', '🏙️ City'].map(tag => (
                <button
                  key={tag}
                  type="button"
                  className="rent-tag-pill"
                  onClick={onPlanTrip}
                >
                  {tag}
                </button>
              ))}
            </div>

            {/* Bottom Stats Row (Like Reference Hero Stats) */}
            <div className="rent-hero-stats">
              <div className="rhs-stat">
                <div className="rhs-num">8</div>
                <div className="rhs-label">ML Models</div>
              </div>
              <div className="rhs-stat">
                <div className="rhs-num">20</div>
                <div className="rhs-label">Indian Hubs</div>
              </div>
              <div className="rhs-stat">
                <div className="rhs-num">440+</div>
                <div className="rhs-label">Tourist Spots</div>
              </div>
              <div className="rhs-stat">
                <div className="rhs-num">~60ms</div>
                <div className="rhs-label">Consensus</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ═════════════════════════════════════════════
          2. TRAVEL CATEGORIES (Like Reference Category Grid)
          ═════════════════════════════════════════════ */}
      <section className="rent-section">
        <div className="desktop-container">
          <div className="rent-section-head">
            <h2 className="rent-section-title">Explore Travel Styles</h2>
            <p className="rent-section-sub">Choose from diverse Indian holiday archetypes calibrated across our ML models.</p>
          </div>

          <div className="rent-categories-grid">
            {CATEGORIES.map(cat => (
              <div
                key={cat.id}
                className={`rent-cat-card ${selectedCategory === cat.id ? 'active' : ''}`}
                onClick={() => {
                  setSelectedCategory(selectedCategory === cat.id ? 'All' : cat.id);
                  scrollTo('destinations');
                }}
              >
                <div className="rcc-icon">{cat.icon}</div>
                <div className="rcc-name">{cat.name}</div>
                <div className="rcc-count">{cat.examples}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ═════════════════════════════════════════════
          3. HOW IT WORKS (3 Step Cards)
          ═════════════════════════════════════════════ */}
      <section id="how-it-works" className="rent-section bg-subtle">
        <div className="desktop-container">
          <div className="rent-section-head text-center">
            <span className="rent-eyebrow">STEP-BY-STEP PROCESS</span>
            <h2 className="rent-section-title">How PACKVOTE Works</h2>
            <p className="rent-section-sub">
              Eliminate group friction and find the mathematically optimal trip for everyone.
            </p>
          </div>

          <div className="rent-steps-grid">
            <div className="rent-step-card">
              <div className="rsc-badge">01</div>
              <div className="rsc-icon">👥</div>
              <h3 className="rsc-title">1. Input Group Preferences</h3>
              <p className="rsc-desc">
                Add each group member, select individual travel tastes (Beach, Nature, Heritage, Adventure, City), and set a per-person budget in INR.
              </p>
            </div>

            <div className="rent-step-card highlight">
              <div className="rsc-badge">02</div>
              <div className="rsc-icon">🧠</div>
              <h3 className="rsc-title">2. 8-Model ML Consensus</h3>
              <p className="rsc-desc">
                Our ensemble runs Random Forest, K-Means, SVD collaborative filtering, KNN, and Naive Bayes in parallel to score group satisfaction.
              </p>
            </div>

            <div className="rent-step-card">
              <div className="rsc-badge">03</div>
              <div className="rsc-icon">🗺️</div>
              <h3 className="rsc-title">3. Tailored Itinerary & Stays</h3>
              <p className="rsc-desc">
                Receive ranked destinations with group compatibility percentages, 3-day and 5-day itineraries, regional dining, and 12-month weather.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* ═════════════════════════════════════════════
          4. POPULAR DESTINATIONS (Like Reference Listings Grid)
          ═════════════════════════════════════════════ */}
      <section id="destinations" className="rent-section">
        <div className="desktop-container">
          <div className="rent-listings-header">
            <div>
              <h2 className="rent-section-title">Popular Destinations</h2>
              <p className="rent-section-sub">Top Indian vacation hubs with complete itineraries, food guides, and accommodations.</p>
            </div>

            <div className="rent-filter-row">
              {['All', 'Beach', 'Nature', 'Adventure', 'Historical'].map(f => (
                <button
                  key={f}
                  type="button"
                  className={`rent-filter-chip ${selectedCategory === f ? 'active' : ''}`}
                  onClick={() => setSelectedCategory(f)}
                >
                  {f}
                </button>
              ))}
            </div>
          </div>

          <div className="rent-listings-grid">
            {filteredDestinations.map(dest => (
              <div
                key={dest.name}
                className="rent-listing-card"
                onClick={() => onExploreDestination && onExploreDestination(dest.name)}
              >
                {/* Visual Header Banner */}
                <div className="rlc-banner">
                  <span className="rlc-type-badge">{dest.typeIcon} {dest.type}</span>
                  <span className="rlc-rating-badge">⭐ {dest.rating}</span>
                </div>

                {/* Card Body */}
                <div className="rlc-body">
                  <div className="rlc-location">📍 {dest.state}, India · <span className="text-green">{dest.bestTime}</span></div>
                  <h3 className="rlc-title">{dest.name}</h3>
                  <p className="rlc-desc">{dest.tagline}</p>

                  <div className="rlc-spots-pills">
                    {dest.highlights.map(h => (
                      <span key={h} className="rlc-spot-pill">✦ {h}</span>
                    ))}
                  </div>

                  <div className="rlc-footer">
                    <div className="rlc-price">
                      ₹{dest.budgetPerNight.toLocaleString('en-IN')}
                      <span>/night avg</span>
                    </div>
                    <button
                      type="button"
                      className="btn-rlc-action"
                      onClick={(e) => {
                        e.stopPropagation();
                        onExploreDestination && onExploreDestination(dest.name);
                      }}
                    >
                      View Trip Plan →
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ═════════════════════════════════════════════
          5. ML PIPELINE ARCHITECTURE SECTION
          ═════════════════════════════════════════════ */}
      <section className="rent-section bg-subtle">
        <div className="desktop-container">
          <div className="rent-section-head text-center">
            <span className="rent-eyebrow">DATA SCIENCE & ARCHITECTURE</span>
            <h2 className="rent-section-title">The 8 Machine Learning Models</h2>
            <p className="rent-section-sub">
              Trained on 5,000+ synthetic traveler profiles and verified reviews running in vectorized batch consensus.
            </p>
          </div>

          <div className="rent-models-grid">
            {ML_MODELS.map((m, idx) => (
              <div key={m.name} className="rent-model-box">
                <div className="rmb-top">
                  <span className="rmb-idx">0{idx + 1}</span>
                  <span className="rmb-tag">{m.tag}</span>
                </div>
                <h4 className="rmb-name">{m.name}</h4>
                <p className="rmb-desc">{m.desc}</p>
              </div>
            ))}
          </div>

          {/* Interactive ML Analytics CTA Banner */}
          <div className="landing-analytics-cta">
            <div className="lac-left">
              <span className="lac-icon">📊</span>
              <div>
                <h4 className="lac-title">Interactive K-Means Clusters & Multi-Model Evaluation</h4>
                <p className="lac-desc">
                  Inspect the live 2D feature scatter distribution, cluster volume shares, and Linear Regression vs. Random Forest cost curves.
                </p>
              </div>
            </div>
            <button
              type="button"
              className="btn-lac-action"
              onClick={() => onNavigate && onNavigate('analytics')}
            >
              Open ML Analytics Dashboard →
            </button>
          </div>
        </div>
      </section>

      {/* ═════════════════════════════════════════════
          6. ABOUT SECTION
          ═════════════════════════════════════════════ */}
      <section id="about" className="rent-section">
        <div className="desktop-container">
          <div className="rent-about-grid">
            <div>
              <span className="rent-eyebrow">ABOUT PACKVOTE</span>
              <h2 className="rent-section-title">Solving Group Travel Conflict</h2>
              <p className="rent-about-p">
                Group travel is one of the most rewarding adventures in life, yet planning it often descends into deadlock. One person wants peaceful backwaters, another craves Himalayan trekking, and someone else is restricted by budget.
              </p>
              <p className="rent-about-p">
                <strong>PACKVOTE</strong> solves this by aggregating individual preferences into mathematical consensus. Using multi-model machine learning, it calculates destination compatibility scores that honor everyone's bucket list without bias.
              </p>
              <div className="rent-about-bullets">
                <div>✓ Democratic consensus voting eliminates compromises</div>
                <div>✓ Fast vectorized inference returns results in under ~60ms</div>
                <div>✓ End-to-end trip plans including dining, stays, and transit</div>
              </div>
            </div>

            <div className="rent-about-stats-card">
              <div className="rasc-item">
                <div className="rasc-num">20</div>
                <div className="rasc-label">Travel Hubs Covered</div>
              </div>
              <div className="rasc-item">
                <div className="rasc-num">440+</div>
                <div className="rasc-label">Cataloged Attractions</div>
              </div>
              <div className="rasc-item">
                <div className="rasc-num">8</div>
                <div className="rasc-label">Trained ML Algorithms</div>
              </div>
              <div className="rasc-item">
                <div className="rasc-num">0</div>
                <div className="rasc-label">Group Compromises</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ═════════════════════════════════════════════
          7. CONTACT SECTION
          ═════════════════════════════════════════════ */}
      <section id="contact" className="rent-section bg-subtle">
        <div className="desktop-container">
          <div className="rent-contact-grid">
            <div>
              <span className="rent-eyebrow">GET IN TOUCH</span>
              <h2 className="rent-section-title">Questions or Custom Requests?</h2>
              <p className="rent-section-sub" style={{ marginBottom: 20 }}>
                We continuously expand PACKVOTE's machine learning consensus models and destination catalogs.
              </p>
              <div className="rent-contact-items">
                <div>📧 <strong>Email:</strong> support@packvote.travel</div>
                <div>📍 <strong>Coverage:</strong> All 28 States & Union Territories of India</div>
                <div>⚡ <strong>Status:</strong> All 8 ML Models Active & Operational</div>
              </div>
            </div>

            <div className="rent-contact-form-box">
              <h4 style={{ fontSize: 16, fontWeight: 700, marginBottom: 12 }}>Send a Message</h4>
              <input type="text" className="rent-input" placeholder="Your Name" />
              <input type="email" className="rent-input" placeholder="Your Email" />
              <textarea rows={3} className="rent-input" placeholder="Your message..." />
              <button
                type="button"
                className="btn-rent-primary"
                style={{ width: '100%' }}
                onClick={() => alert('Thank you! Your feedback has been received.')}
              >
                Send Message →
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* ═════════════════════════════════════════════
          8. BOTTOM CTA
          ═════════════════════════════════════════════ */}
      <section className="rent-bottom-cta">
        <div className="desktop-container">
          <div className="rent-cta-box">
            <h2 className="rent-cta-title">Ready to Plan Your Next Group Trip?</h2>
            <p className="rent-cta-sub">
              Enter your group's preferences and budget to receive tailored, conflict-free recommendations in seconds.
            </p>
            <button
              type="button"
              className="btn-rent-cta"
              onClick={onPlanTrip}
            >
              Plan Your Trip Now →
            </button>
          </div>
        </div>
      </section>
    </div>
  );
}
