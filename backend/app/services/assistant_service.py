"""
backend/app/services/assistant_service.py
AI Voice Assistant service for PACKVOTE.
Parses natural language queries, handles travel planning actions,
provides destination facts, and answers ML/budget questions.
"""
import re
import logging
from typing import Dict, Any, List, Optional
from backend.app.services.destination_service import (
    find_canonical_name,
    get_destination_full_details,
    get_all_destinations_summary,
)

logger = logging.getLogger(__name__)

TASTE_KEYWORDS = {
    "beach": "Beach",
    "beaches": "Beach",
    "coastal": "Beach",
    "sea": "Beach",
    "ocean": "Beach",
    "nature": "Nature",
    "greenery": "Nature",
    "scenic": "Nature",
    "hills": "Nature",
    "mountain": "Nature",
    "mountains": "Nature",
    "adventure": "Adventure",
    "trekking": "Adventure",
    "rafting": "Adventure",
    "hiking": "Adventure",
    "sports": "Adventure",
    "historical": "Historical",
    "heritage": "Historical",
    "history": "Historical",
    "fort": "Historical",
    "palace": "Historical",
    "monuments": "Historical",
    "temple": "Historical",
    "city": "City",
    "urban": "City",
    "shopping": "City",
    "nightlife": "City",
}

ACCOM_KEYWORDS = {
    "hostel": "Hostel",
    "homestay": "Homestay",
    "guesthouse": "GuestHouse",
    "guest house": "GuestHouse",
    "hotel": "Hotel",
    "resort": "Resort",
    "boutique": "Boutique Hotel",
    "camp": "Luxury Camps",
    "camps": "Luxury Camps",
}


def process_assistant_message(user_message: str, current_state: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Process speech/text input from user and return conversational reply + UI action.
    """
    text = (user_message or "").strip().lower()
    if not text:
        return {
            "reply": "I'm listening! You can ask me to plan a trip, explain our ML models, or show destination details.",
            "action": None,
            "suggestions": [
                "Plan a 3-day beach trip for 2",
                "Show ML Analytics",
                "Tell me about Goa",
                "Explain how budget works",
            ],
        }

    # 1. Navigation / Theme commands
    if any(k in text for k in ["dark mode", "switch to dark", "night mode"]):
        return {
            "reply": "Switched to dark theme for comfortable night viewing.",
            "action": {"type": "SET_THEME", "theme": "dark"},
            "suggestions": ["Plan a trip", "Show ML Analytics"],
        }
    if any(k in text for k in ["light mode", "switch to light", "day mode"]):
        return {
            "reply": "Switched to light theme.",
            "action": {"type": "SET_THEME", "theme": "light"},
            "suggestions": ["Plan a trip", "Show ML Analytics"],
        }

    if any(k in text for k in ["analytics", "graphs", "charts", "scatter plot", "cluster plot", "prediction curve"]):
        return {
            "reply": "Opening the ML Analytics Dashboard. Here you can explore our K-Means 2D scatter clusters and multi-model stay prediction curves.",
            "action": {"type": "NAVIGATE", "target": "analytics"},
            "suggestions": ["Explain K-Means clusters", "Explain the 8 ML models", "Plan a group trip"],
        }

    if any(k in text for k in ["overview", "go to home", "landing page", "homepage"]):
        return {
            "reply": "Navigating back to the PACKVOTE Overview page.",
            "action": {"type": "NAVIGATE", "target": "landing"},
            "suggestions": ["Plan Your Trip", "View ML Analytics", "Explore Destinations"],
        }

    # 2. Trip Planning Intent (e.g. "plan a trip for 3 people with beach and adventure budget 5000")
    if any(k in text for k in ["plan", "recommend", "trip for", "suggest a trip", "looking for a trip"]):
        # Extract number of travelers
        travelers_count = 2
        match_travelers = re.search(r'(\d+)\s*(people|travelers|friends|persons|members|of us)', text)
        if match_travelers:
            travelers_count = max(1, min(6, int(match_travelers.group(1))))
        elif "solo" in text or "alone" in text:
            travelers_count = 1

        # Extract tastes
        matched_tastes = set()
        for word, taste in TASTE_KEYWORDS.items():
            if re.search(r'\b' + re.escape(word) + r'\b', text):
                matched_tastes.add(taste)
        tastes_list = list(matched_tastes) if matched_tastes else ["Beach", "Nature"]

        # Extract budget
        extracted_budget = 5000
        budget_match = re.search(r'(\d+[\d,]*)\s*(k|thousand|inr|rs|rupees|budget)?', text)
        if budget_match:
            raw_b = budget_match.group(1).replace(",", "")
            try:
                b_val = int(raw_b)
                if "k" in text:
                    b_val = b_val * 1000 if b_val < 100 else b_val
                if 500 <= b_val <= 100000:
                    extracted_budget = b_val
            except Exception:
                pass

        # Extract accommodation type
        accom_type = "Hotel"
        for word, a_type in ACCOM_KEYWORDS.items():
            if word in text:
                accom_type = a_type
                break

        # Generate travelers array
        travelers_payload = []
        for i in range(travelers_count):
            travelers_payload.append({"preferences": tastes_list})

        reply_str = (
            f"I have configured a trip for {travelers_count} traveler{'s' if travelers_count > 1 else ''} "
            f"interested in {', '.join(tastes_list)}, with a nightly stay budget of ₹{extracted_budget:,} for {accom_type}. "
            f"Redirecting you to recommendations now!"
        )

        return {
            "reply": reply_str,
            "action": {
                "type": "SET_PLANNER_AND_SUBMIT",
                "travelers_count": travelers_count,
                "preferences": tastes_list,
                "budget": extracted_budget,
                "accom_type": accom_type,
            },
            "suggestions": [
                "Show ML Analytics",
                "Explain how consensus works",
                "Compare top destinations",
            ],
        }

    # 3. Questions about Machine Learning & Consensus
    if any(k in text for k in ["how it works", "consensus", "8 models", "machine learning", "algorithm"]):
        return {
            "reply": (
                "PACKVOTE uses an ensemble of 8 Machine Learning models, including SVD Collaborative Filtering, "
                "Random Forest, and K-Means Clustering. Our consensus formula combines 65% group average satisfaction, "
                "15% anti-misery minimum fairness, 10% budget feasibility, and 10% seasonal fit."
            ),
            "action": {"type": "NAVIGATE", "target": "analytics"},
            "suggestions": ["Show ML Analytics", "Explain K-Means clusters", "Plan a group trip"],
        }

    if any(k in text for k in ["kmeans", "k-means", "clusters", "archetype"]):
        return {
            "reply": (
                "Our K-Means algorithm groups travel destinations into 4 archetypes: "
                "Cluster 0: Coastal & Beach Escapes, "
                "Cluster 1: Himalayan Mountain Adventures, "
                "Cluster 2: Royal Heritage Hubs, and "
                "Cluster 3: Spiritual & Nature Sanctuaries. Check out the 2D scatter plot in ML Analytics!"
            ),
            "action": {"type": "NAVIGATE", "target": "analytics"},
            "suggestions": ["View K-Means Scatter Plot", "Plan a trip", "Explain budget prediction"],
        }

    if any(k in text for k in ["budget", "cost per night", "overall trip", "per night"]):
        return {
            "reply": (
                "PACKVOTE features a dual-mode budget engine. You can enter a nightly rate per person, "
                "or enter your total trip budget with days and nights, and we automatically calculate the stay allowance. "
                "Our Linear Regression model predicts actual hotel rates per night and compares them with your allowance."
            ),
            "action": {"type": "NAVIGATE", "target": "planner"},
            "suggestions": ["Plan a trip with ₹5000 budget", "Show ML Analytics", "Best budget destinations"],
        }

    # 4. Questions about specific destinations (e.g. "Tell me about Goa", "What food in Kerala?")
    all_dests = get_all_destinations_summary()
    found_dest_name = None
    for d in all_dests:
        dest_name = d.get("destination") or d.get("name") or ""
        if not dest_name:
            continue
        dest_lower = dest_name.lower()
        # Direct substring match
        if dest_lower in text:
            found_dest_name = dest_name
            break
        # Keyword token match (e.g., 'goa', 'kerala', 'jaipur', 'manali')
        for word in dest_lower.split():
            clean_word = word.strip(".,;:()")
            if len(clean_word) >= 3 and clean_word not in ["and", "the", "caves", "city", "ruins", "temples", "beach", "beaches", "valley"]:
                if re.search(r'\b' + re.escape(clean_word) + r'\b', text):
                    found_dest_name = dest_name
                    break
        if found_dest_name:
            break

    if found_dest_name:
        details = get_destination_full_details(found_dest_name) or {}
        overview = details.get("overview", {})
        tagline = overview.get("tagline", "")
        meta = details.get("meta", {})
        best_time = meta.get("best_time") or details.get("best_time") or "winter months"
        foods = details.get("food", [])
        food_names = [f.get("name") for f in foods[:2] if isinstance(f, dict) and f.get("name")]
        spots = details.get("tourist_spots", []) or details.get("spots", [])
        spot_names = [s.get("name") for s in spots[:2] if isinstance(s, dict) and s.get("name")]

        spoken_parts = []
        if tagline:
            spoken_parts.append(f"{found_dest_name} is known for {tagline}.")
        else:
            spoken_parts.append(f"{found_dest_name} is one of India's top travel destinations.")
        spoken_parts.append(f"The best time to visit is {best_time}.")
        if spot_names:
            spoken_parts.append(f"Top sights include {', '.join(spot_names)}.")
        if food_names:
            spoken_parts.append(f"Don't miss regional specialties like {', '.join(food_names)}.")
        spoken_parts.append("I am opening the full 7-tab trip plan for you now.")

        return {
            "reply": " ".join(spoken_parts),
            "action": {
                "type": "OPEN_DESTINATION",
                "destination": found_dest_name,
            },
            "suggestions": [
                f"Show 3-day itinerary for {found_dest_name}",
                f"Nearby spots in {found_dest_name}",
                "Plan a group trip",
            ],
        }

    # 5. Food queries
    if any(k in text for k in ["food", "dishes", "eat", "dining", "cuisine"]):
        return {
            "reply": (
                "Every destination in PACKVOTE includes authentic regional dishes and top local restaurants. "
                "For example, Kerala features traditional Sadya and seafood curries, Jaipur serves royal Dal Baati Churma, "
                "and Varanasi offers iconic kachoris and Malaiyyo."
            ),
            "action": None,
            "suggestions": ["Tell me about Goa", "Tell me about Alleppey", "Tell me about Jaipur"],
        }

    # Default friendly conversational response
    return {
        "reply": (
            f"I heard: '{user_message}'. I can help you plan a conflict-free trip, explain our 8 ML models, "
            "show K-Means cluster charts, or give you day-by-day itineraries for top Indian destinations. What would you like to explore?"
        ),
        "action": None,
        "suggestions": [
            "Plan a 3-day beach trip for 2",
            "Show ML Analytics",
            "Tell me about Manali",
            "Tell me about Goa",
        ],
    }
