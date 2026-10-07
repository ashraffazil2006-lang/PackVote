// src/components/FoodSection.jsx
export default function FoodSection({ food = [], restaurants = [], destinationName }) {
  return (
    <div className="food-wrapper">
      {/* ── Must-Try Local Delicacies ── */}
      <div className="food-subblock">
        <div className="block-header">
          <h3 className="section-heading">🍛 Must-Try Local Delicacies & Cuisine</h3>
          <p className="section-subheading">
            Authentic culinary specialties of {destinationName} you shouldn't miss.
          </p>
        </div>
        {food.length === 0 ? (
          <div className="empty-substate">Food guide unavailable for this destination.</div>
        ) : (
          <div className="food-cards-grid">
            {food.map((dish, i) => (
              <div key={i} className="dish-card">
                <div className="dish-top">
                  <div className="dish-emoji">{dish.emoji || '🍲'}</div>
                  <div className="dish-headings">
                    <div className="dish-title-row">
                      <span className="dish-name">{dish.name}</span>
                      {dish.must_try && (
                        <span className="must-try-tag">⭐ Must Try</span>
                      )}
                    </div>
                    <span className="dish-type">{dish.type || 'Regional Specialty'}</span>
                  </div>
                </div>
                <p className="dish-description">{dish.description}</p>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* ── Recommended Restaurants ── */}
      <div className="food-subblock" style={{ marginTop: 36 }}>
        <div className="block-header">
          <h3 className="section-heading">🍽️ Top Recommended Dining & Restaurants</h3>
          <p className="section-subheading">
            Best dining spots in {destinationName} spanning traditional feasts, scenic views, and street delicacies.
          </p>
        </div>
        {restaurants.length === 0 ? (
          <div className="empty-substate">Restaurant recommendations being compiled.</div>
        ) : (
          <div className="restaurant-cards-grid">
            {restaurants.map((place, i) => (
              <div key={i} className="restaurant-card">
                <div className="restaurant-card-header">
                  <div>
                    <h4 className="restaurant-name">{place.name}</h4>
                    <div className="restaurant-meta-row">
                      <span className="restaurant-cuisine">🍴 {place.cuisine}</span>
                      <span className="restaurant-price">{place.price_range}</span>
                    </div>
                  </div>
                  {place.rating && (
                    <div className="restaurant-rating">
                      ⭐ {Number(place.rating).toFixed(1)}
                    </div>
                  )}
                </div>
                {place.specialty && (
                  <div className="restaurant-specialty">
                    <strong>Specialty:</strong> {place.specialty}
                  </div>
                )}
                {place.area && (
                  <div className="restaurant-area">
                    📍 <span>{place.area}</span>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
