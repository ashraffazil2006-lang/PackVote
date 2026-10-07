"""
create_destination_intelligence.py
Generates destination_intelligence.json — rich trip data for all 20 destinations.
Covers: food, restaurants, accommodation, 3-day & 5-day itinerary,
        monthly weather, travel tips, nearby destinations.
"""
import json
from pathlib import Path

OUT = Path("d:/PACKVOTE/data")
OUT.mkdir(parents=True, exist_ok=True)

INTELLIGENCE = {

  "Goa Beaches": {
    "overview": {
      "tagline": "Sun, sand, and soulful vibes on India's golden coast",
      "best_for": ["Couples", "Friend Groups", "Solo Travellers"],
      "avg_trip_days": 4,
      "budget_per_day": {"budget": 1500, "mid": 4000, "luxury": 12000},
      "language": "Konkani, English, Hindi",
      "currency": "INR",
      "timezone": "IST (UTC+5:30)"
    },
    "how_to_reach": {
      "flight": "Goa International Airport (Dabolim/Mopa) — direct flights from all major cities",
      "train": "Madgaon (Margao) & Vasco da Gama railway stations",
      "bus": "Kadamba Transport Corporation runs buses from Mumbai, Pune, Bangalore",
      "local_transport": ["Rented scooter (₹300/day)", "Auto-rickshaw", "Taxi (Goa Miles app)", "Bicycle"]
    },
    "food": [
      {"name": "Fish Curry Rice", "type": "Main Course", "description": "Goa's soul food — tangy coconut-based curry with fresh local fish served over fluffy rice", "emoji": "🍛", "must_try": True},
      {"name": "Bebinca", "type": "Dessert", "description": "Traditional 16-layer Goan cake made with coconut milk, eggs, and sugar — a Portuguese legacy", "emoji": "🍰", "must_try": True},
      {"name": "Prawn Balchão", "type": "Main Course", "description": "Spicy pickled prawn preparation with vinegar and red chilies — a fiery Goan classic", "emoji": "🦐", "must_try": True},
      {"name": "Feni", "type": "Drink", "description": "Goa's local cashew or coconut spirit — try it in a cocktail at beach shacks", "emoji": "🥃", "must_try": False},
      {"name": "Xacuti", "type": "Main Course", "description": "Chicken or lamb in a complex roasted coconut and poppy seed gravy", "emoji": "🍗", "must_try": True},
      {"name": "Pork Vindaloo", "type": "Main Course", "description": "Fiery pork curry with Kashmiri chilies and vinegar — the dish that inspired all Vindaloos", "emoji": "🌶️", "must_try": True}
    ],
    "restaurants": [
      {"name": "Fisherman's Wharf", "cuisine": "Seafood / Goan", "price_range": "₹₹₹", "specialty": "Crab Xec Xec and freshly caught Kingfish", "area": "Cavelossim Beach", "rating": 4.5},
      {"name": "Gunpowder", "cuisine": "South Indian", "price_range": "₹₹", "specialty": "Kori Rotti and Coorg specialties", "area": "Assagao", "rating": 4.4},
      {"name": "Thalassa", "cuisine": "Greek / Mediterranean", "price_range": "₹₹₹₹", "specialty": "Mezze platters with sunset ocean views", "area": "Vagator", "rating": 4.6},
      {"name": "Martin's Corner", "cuisine": "Goan / Seafood", "price_range": "₹₹", "specialty": "Pomfret Recheado and Sausage Pulao", "area": "Betalbatim", "rating": 4.3},
      {"name": "Britto's", "cuisine": "Multi-cuisine / Beach", "price_range": "₹₹", "specialty": "Lobster thermidor and beach party ambience", "area": "Baga Beach", "rating": 4.2},
      {"name": "A Reverie", "cuisine": "European / Fusion", "price_range": "₹₹₹₹", "specialty": "Smoked duck breast and truffled mushroom risotto", "area": "Panaji", "rating": 4.7}
    ],
    "accommodation": [
      {"name": "Zostel Goa", "type": "Hostel", "price_per_night": 650, "highlights": ["Beach walk 5 mins", "Social rooftop", "Dorm & private rooms"], "rating": 4.1},
      {"name": "Varca Beach Resort", "type": "Hotel", "price_per_night": 3500, "highlights": ["Private beach", "Swimming pool", "Breakfast included"], "rating": 4.2},
      {"name": "Coconut Creek", "type": "Boutique Hotel", "price_per_night": 6500, "highlights": ["Portuguese architecture", "Garden pool", "Cycling tours"], "rating": 4.5},
      {"name": "Alila Diwa Goa", "type": "Resort", "price_per_night": 14000, "highlights": ["Infinity pool", "Spa", "Ayurvedic treatments", "Private beach access"], "rating": 4.7},
      {"name": "Airbnb Homestay Anjuna", "type": "Homestay", "price_per_night": 1800, "highlights": ["Goan family experience", "Home-cooked meals", "Local guided tours"], "rating": 4.3}
    ],
    "itinerary": {
      "3_day": [
        {"day": 1, "title": "North Goa — Beaches & Forts", "morning": "Arrive, check in. Head to Baga Beach for breakfast at a beach shack", "afternoon": "Calangute Beach → Fort Aguada → Sinquerim Beach", "evening": "Sunset at Vagator. Dinner at Thalassa with ocean views"},
        {"day": 2, "title": "Old Goa & Culture", "morning": "Basilica of Bom Jesus (UNESCO) → Se Cathedral → Fontainhas Latin Quarter", "afternoon": "Panjim market → Dudhsagar Waterfalls excursion (2hrs)", "evening": "Casino night cruise on Mandovi River or live music at Baga"},
        {"day": 3, "title": "South Goa — Serenity", "morning": "Palolem Beach (pristine, quiet) → Kayaking through mangroves", "afternoon": "Cotigao Wildlife Sanctuary walk → Agonda Beach", "evening": "Farewell seafood feast at Martin's Corner"}
      ],
      "5_day": [
        {"day": 1, "title": "Arrival & North Beaches", "morning": "Check in. Baga Beach breakfast", "afternoon": "Calangute → Anjuna Flea Market (Wed only)", "evening": "Sunset at Chapora Fort. Night at Tito's Lane"},
        {"day": 2, "title": "Old Goa Heritage", "morning": "Basilica of Bom Jesus → Se Cathedral", "afternoon": "Fontainhas walk → Panaji Ferry Cruise", "evening": "Casino Royale night cruise"},
        {"day": 3, "title": "Adventure Day", "morning": "Dudhsagar Falls trek (book jeep safari)", "afternoon": "Spice plantation tour with lunch", "evening": "Beach bonfire at Vagator"},
        {"day": 4, "title": "South Goa Tranquility", "morning": "Palolem Beach → kayaking", "afternoon": "Agonda Beach → Cotigao Wildlife", "evening": "Silent noise party Palolem (seasonal)"},
        {"day": 5, "title": "Water Sports & Farewell", "morning": "Parasailing / jet ski at Baga", "afternoon": "Last minute shopping at Mapusa Market", "evening": "Farewell sunset dinner at Fisherman's Wharf"}
      ]
    },
    "weather": [
      {"month": "Jan", "temp_high": 32, "temp_low": 20, "description": "Ideal — sunny skies, peak season", "emoji": "☀️"},
      {"month": "Feb", "temp_high": 33, "temp_low": 21, "description": "Excellent — warm with cool evenings", "emoji": "☀️"},
      {"month": "Mar", "temp_high": 34, "temp_low": 23, "description": "Good — getting hotter, still pleasant", "emoji": "🌤️"},
      {"month": "Apr", "temp_high": 36, "temp_low": 25, "description": "Hot — fewer tourists, good deals", "emoji": "🌤️"},
      {"month": "May", "temp_high": 34, "temp_low": 26, "description": "Pre-monsoon — humid, some showers", "emoji": "🌦️"},
      {"month": "Jun", "temp_high": 30, "temp_low": 24, "description": "Monsoon — heavy rain, most hotels close", "emoji": "🌧️"},
      {"month": "Jul", "temp_high": 29, "temp_low": 24, "description": "Peak monsoon — beaches unsafe", "emoji": "⛈️"},
      {"month": "Aug", "temp_high": 29, "temp_low": 24, "description": "Monsoon continues — green landscapes", "emoji": "🌧️"},
      {"month": "Sep", "temp_high": 30, "temp_low": 24, "description": "Monsoon tapering — quiet & lush", "emoji": "🌦️"},
      {"month": "Oct", "temp_high": 32, "temp_low": 23, "description": "Post-monsoon — season opening", "emoji": "⛅"},
      {"month": "Nov", "temp_high": 32, "temp_low": 21, "description": "Peak season begins — perfect weather", "emoji": "☀️"},
      {"month": "Dec", "temp_high": 31, "temp_low": 20, "description": "Best month — Christmas & NYE parties", "emoji": "🎄"}
    ],
    "tips": [
      "Rent a scooter — it's the best way to explore Goa (₹300-400/day)",
      "Book Dudhsagar Falls jeep safari in advance (limited slots)",
      "Avoid Goa June–September (monsoon season — most beaches unsafe)",
      "Carry cash — many beach shacks don't accept cards",
      "Bargain at Anjuna Flea Market — starting prices are 3x the fair price",
      "Night cabs are expensive — use Goa Miles app or pre-negotiate"
    ],
    "nearby": ["Gokarna (5 hrs)", "Hampi (7 hrs)", "Coorg (8 hrs)"]
  },

  "Kerala Backwaters": {
    "overview": {
      "tagline": "Float through paradise on God's Own Country's emerald waterways",
      "best_for": ["Couples", "Families", "Nature Lovers", "Wellness Seekers"],
      "avg_trip_days": 5,
      "budget_per_day": {"budget": 1200, "mid": 3500, "luxury": 10000},
      "language": "Malayalam, English",
      "currency": "INR",
      "timezone": "IST (UTC+5:30)"
    },
    "how_to_reach": {
      "flight": "Cochin International Airport (COK) — nearest major airport, 85km from Alleppey",
      "train": "Alleppey (Alappuzha) railway station — well connected to Mumbai, Delhi, Chennai",
      "bus": "KSRTC buses from Kochi (1.5 hrs), Trivandrum (3 hrs)",
      "local_transport": ["Houseboat (essential experience)", "Auto-rickshaw", "Boat ferry", "Bicycle along canals"]
    },
    "food": [
      {"name": "Kerala Sadya", "type": "Feast", "description": "Grand vegetarian feast on banana leaf with 20+ dishes — served at weddings and Onam. An unmissable experience.", "emoji": "🍃", "must_try": True},
      {"name": "Karimeen Pollichathu", "type": "Main Course", "description": "Pearl spot fish marinated in spices and grilled in banana leaf — Kerala's signature fish dish", "emoji": "🐟", "must_try": True},
      {"name": "Appam with Stew", "type": "Breakfast", "description": "Lacy rice hoppers served with creamy coconut milk vegetable or chicken stew — perfect Kerala morning", "emoji": "🥞", "must_try": True},
      {"name": "Prawn Moilee", "type": "Main Course", "description": "Delicate golden curry of prawns in thin coconut milk with green chilies — light and aromatic", "emoji": "🦐", "must_try": True},
      {"name": "Puttu & Kadala Curry", "type": "Breakfast", "description": "Steamed rice cylinders served with spiced black chickpea curry — authentic Kerala breakfast", "emoji": "🫙", "must_try": True},
      {"name": "Kerala Prawn Biryani", "type": "Main Course", "description": "Fragrant rice layered with prawns, fried onions, and aromatic spices in dum style", "emoji": "🍚", "must_try": False}
    ],
    "restaurants": [
      {"name": "Chakara Restaurant", "cuisine": "Kerala Seafood", "price_range": "₹₹₹", "specialty": "Karimeen Pollichathu and Crab Masala", "area": "Marari Beach", "rating": 4.6},
      {"name": "Harbour Restaurant", "cuisine": "Continental & Kerala", "price_range": "₹₹₹", "specialty": "Freshwater fish from the backwaters", "area": "Alleppey town", "rating": 4.4},
      {"name": "Tharavadu", "cuisine": "Traditional Kerala", "price_range": "₹₹", "specialty": "Full Kerala Sadya served on banana leaf", "area": "Kochi", "rating": 4.5},
      {"name": "Dhe Puttu", "cuisine": "Kerala Street Food", "price_range": "₹", "specialty": "50+ varieties of Puttu — must visit", "area": "Kochi", "rating": 4.3},
      {"name": "Malabar Junction", "cuisine": "Malabar / Kerala", "price_range": "₹₹₹₹", "specialty": "Malabar Prawn Curry and Thalassery Biryani", "area": "Fort Kochi", "rating": 4.5},
      {"name": "Houseboat Dining", "cuisine": "Kerala Home-style", "price_range": "₹₹₹", "specialty": "Fresh catch cooked by your houseboat crew", "area": "Alleppey Backwaters", "rating": 4.7}
    ],
    "accommodation": [
      {"name": "Zostel Alleppey", "type": "Hostel", "price_per_night": 550, "highlights": ["Canal-side location", "Social common area", "Boat tour bookings"], "rating": 4.1},
      {"name": "Lake Palace Resort", "type": "Hotel", "price_per_night": 4200, "highlights": ["Backwater views", "Ayurvedic spa", "Canoe rides included"], "rating": 4.3},
      {"name": "Punnamada Lake Resort", "type": "Resort", "price_per_night": 8500, "highlights": ["Private pool villas", "Houseboat included", "Yoga sessions"], "rating": 4.6},
      {"name": "Kettuvallam Houseboat", "type": "Houseboat", "price_per_night": 6000, "highlights": ["Sleep on the water", "Full board meals", "Crew cooks fresh fish", "Sunrise & sunset views"], "rating": 4.8},
      {"name": "Canal Side Homestay", "type": "Homestay", "price_per_night": 1400, "highlights": ["Kerala family experience", "Home-cooked sadya", "Village walks"], "rating": 4.4}
    ],
    "itinerary": {
      "3_day": [
        {"day": 1, "title": "Arrival in Kochi — Fort Kochi Exploration", "morning": "Fly into Kochi. Visit Chinese Fishing Nets and Fort Kochi beach walk", "afternoon": "Dutch Palace → Jewish Synagogue → Mattancherry spice market", "evening": "Kathakali dance performance. Dinner at Malabar Junction"},
        {"day": 2, "title": "Alleppey — The Venice of the East", "morning": "Drive to Alleppey (1.5 hrs). Board overnight houseboat at noon", "afternoon": "Float through paddy fields and coconut groves on Vembanad Lake", "evening": "Watch sunset from houseboat deck. Fresh fish dinner cooked by crew. Sleep on water"},
        {"day": 3, "title": "Backwater Village Life & Departure", "morning": "Early morning canoe through narrow village canals", "afternoon": "Kumarakom Bird Sanctuary walk → Pathiramanal Island visit", "evening": "Return to Kochi. Farewell Kerala Sadya dinner"}
      ],
      "5_day": [
        {"day": 1, "title": "Fort Kochi Heritage", "morning": "Chinese Fishing Nets → St Francis Church (oldest European church in India)", "afternoon": "Mattancherry Palace → Jewish Quarter", "evening": "Kathakali performance → dinner at Tharavadu"},
        {"day": 2, "title": "Munnar Tea Hills", "morning": "Drive to Munnar (3 hrs). Cheeyappara Waterfalls en route", "afternoon": "Tea Museum → Eravikulam National Park (Nilgiri Tahr)", "evening": "Stay in Munnar — cool mountain air, evening walk through tea gardens"},
        {"day": 3, "title": "Munnar to Alleppey", "morning": "Top Station viewpoint at sunrise → Mattupetty Dam", "afternoon": "Drive to Alleppey (4 hrs). Board houseboat at 1pm", "evening": "Sunset cruise on Vembanad Lake. Fresh fish dinner on deck"},
        {"day": 4, "title": "Deep Backwaters", "morning": "Early morning canoe through Kuttanad (below sea level rice fields)", "afternoon": "Alappuzha Beach → Ambalappuzha Temple", "evening": "Cooking class — learn to make Kerala Sadya"},
        {"day": 5, "title": "Kovalam Beach Finale", "morning": "Drive to Kovalam (3 hrs). Lighthouse Beach swim", "afternoon": "Ayurvedic massage at beach resort", "evening": "Seafood sunset dinner. Return to Trivandrum for departure"}
      ]
    },
    "weather": [
      {"month": "Jan", "temp_high": 31, "temp_low": 22, "description": "Ideal — clear skies, perfect houseboat weather", "emoji": "☀️"},
      {"month": "Feb", "temp_high": 32, "temp_low": 23, "description": "Excellent — warm and dry", "emoji": "☀️"},
      {"month": "Mar", "temp_high": 34, "temp_low": 25, "description": "Good — getting warm, still recommended", "emoji": "🌤️"},
      {"month": "Apr", "temp_high": 35, "temp_low": 26, "description": "Hot — pre-monsoon heat, fewer tourists", "emoji": "🌤️"},
      {"month": "May", "temp_high": 33, "temp_low": 26, "description": "Pre-monsoon — occasional showers", "emoji": "🌦️"},
      {"month": "Jun", "temp_high": 29, "temp_low": 24, "description": "SW Monsoon arrives — heavy rain, backwaters swell beautifully", "emoji": "🌧️"},
      {"month": "Jul", "temp_high": 28, "temp_low": 23, "description": "Heavy monsoon — Nehru Trophy Boat Race season (Aug)", "emoji": "⛈️"},
      {"month": "Aug", "temp_high": 28, "temp_low": 23, "description": "Nehru Trophy Boat Race — dramatic and exciting if you plan for it", "emoji": "🚣"},
      {"month": "Sep", "temp_high": 29, "temp_low": 24, "description": "Onam festival — best time for Sadya and cultural events", "emoji": "🌦️"},
      {"month": "Oct", "temp_high": 30, "temp_low": 24, "description": "Post-monsoon — lush green, clear canals", "emoji": "⛅"},
      {"month": "Nov", "temp_high": 31, "temp_low": 23, "description": "Peak season begins — perfect weather", "emoji": "☀️"},
      {"month": "Dec", "temp_high": 31, "temp_low": 22, "description": "Best month — Christmas in Kerala is magical", "emoji": "🎄"}
    ],
    "tips": [
      "Book houseboats 2-3 months in advance for peak season (Nov-Feb)",
      "Overnight houseboat is essential — don't just take a day trip",
      "The Nehru Trophy Snake Boat Race (second Saturday of August) is spectacular",
      "Try the village cycle tour in Kumarakom — through paddy fields and canal bridges",
      "Carry insect repellent — the canal areas have mosquitoes at dusk",
      "Onam festival (August-September) offers the most authentic cultural experience"
    ],
    "nearby": ["Munnar (3 hrs)", "Kovalam (3 hrs)", "Thekkady (3 hrs)", "Kochi (1.5 hrs)"]
  },

  "Taj Mahal": {
    "overview": {
      "tagline": "Witness the world's greatest monument to love at sunrise",
      "best_for": ["Couples", "History Buffs", "Families", "First-time India Visitors"],
      "avg_trip_days": 3,
      "budget_per_day": {"budget": 1000, "mid": 3000, "luxury": 8000},
      "language": "Hindi, Urdu, English",
      "currency": "INR",
      "timezone": "IST (UTC+5:30)"
    },
    "how_to_reach": {
      "flight": "Agra Airport (AGR) — limited flights. Better: fly to Delhi (250km), take Gatimaan Express (100 mins)",
      "train": "Agra Cantonment & Agra Fort stations — Shatabdi/Gatimaan Express from Delhi in under 2 hrs",
      "bus": "Yamuna Expressway buses from Delhi (4 hrs). Volvo AC buses available",
      "local_transport": ["Tuk-tuk (₹100-200 for short trips)", "E-rickshaw near Taj", "Pre-paid taxi", "Cycle rickshaw in old city"]
    },
    "food": [
      {"name": "Petha", "type": "Sweet / Snack", "description": "Agra's iconic translucent white sweet made from ash gourd — try angoori (grape) and kesar (saffron) varieties", "emoji": "🍬", "must_try": True},
      {"name": "Bedai & Jalebi", "type": "Breakfast", "description": "Crispy fried bread with spiced potato curry and hot jalebis — perfect Agra morning at Deviram's", "emoji": "🥐", "must_try": True},
      {"name": "Mughlai Biryani", "type": "Main Course", "description": "Slow-cooked aromatic rice with meat, saffron and dried fruits — Mughal-era recipe unchanged for 400 years", "emoji": "🍚", "must_try": True},
      {"name": "Dalmoth", "type": "Snack", "description": "Agra's crunchy spiced lentil snack — perfect tea-time munchies to take home", "emoji": "🥜", "must_try": False},
      {"name": "Gajak", "type": "Sweet", "description": "Sesame and jaggery brittle — a winter speciality from Agra and Mathura", "emoji": "🍫", "must_try": False},
      {"name": "Tandoori Chicken", "type": "Main Course", "description": "Clay oven-roasted chicken marinated in yogurt and spices — best at Peshawri restaurant", "emoji": "🍗", "must_try": True}
    ],
    "restaurants": [
      {"name": "Pind Balluchi", "cuisine": "North Indian / Mughlai", "price_range": "₹₹₹", "specialty": "Dal Makhani and Rogan Josh with Taj views", "area": "Fatehabad Road", "rating": 4.3},
      {"name": "Pinch of Spice", "cuisine": "North Indian", "price_range": "₹₹₹", "specialty": "Butter Chicken and award-winning Dal Tadka", "area": "Fatehabad Road", "rating": 4.5},
      {"name": "Esphahan", "cuisine": "Mughlai Fine Dining", "price_range": "₹₹₹₹", "specialty": "Dum Pukht Gosht and Shahi Tukda — in Oberoi hotel", "area": "The Oberoi Amarvilas", "rating": 4.8},
      {"name": "Sheroes Hangout Café", "cuisine": "Café / Continental", "price_range": "₹₹", "specialty": "Run by acid-attack survivors — great cause, great food", "area": "Taj Ganj", "rating": 4.4},
      {"name": "Deviram Sweets", "cuisine": "Indian Sweets / Breakfast", "price_range": "₹", "specialty": "The best Bedai-Jalebi breakfast in Agra since 1898", "area": "Sadar Bazaar", "rating": 4.6},
      {"name": "Mama Chicken", "cuisine": "North Indian / Mughlai", "price_range": "₹₹", "specialty": "Half Tandoori Chicken and Mutton Seekh Kebab", "area": "Taj Ganj", "rating": 4.2}
    ],
    "accommodation": [
      {"name": "Hotel Kamal", "type": "Budget", "price_per_night": 800, "highlights": ["Rooftop Taj view", "Walking distance to Taj", "Friendly staff"], "rating": 4.0},
      {"name": "Trident Agra", "type": "Hotel", "price_per_night": 5500, "highlights": ["Mughal garden architecture", "Pool", "Taj view from room"], "rating": 4.5},
      {"name": "ITC Mughal Resort", "type": "Resort", "price_per_night": 11000, "highlights": ["UNESCO awarded gardens", "Spa", "Multiple restaurants", "Taj view rooms"], "rating": 4.6},
      {"name": "The Oberoi Amarvilas", "type": "Luxury", "price_per_night": 45000, "highlights": ["Every room faces Taj Mahal", "World's best hotel view", "Butler service"], "rating": 4.9},
      {"name": "Zostel Agra", "type": "Hostel", "price_per_night": 500, "highlights": ["Budget backpacker hub", "Tour bookings", "Social dorms"], "rating": 3.9}
    ],
    "itinerary": {
      "3_day": [
        {"day": 1, "title": "The Taj — Sunrise to Sunset", "morning": "Taj Mahal at SUNRISE (5:30am) — most magical light. Buy tickets online the night before", "afternoon": "Agra Fort (UNESCO) — Red sandstone fortress with Taj views from towers", "evening": "Mehtab Bagh — garden across Yamuna River for sunset Taj reflection photo"},
        {"day": 2, "title": "Fatehpur Sikri & Surroundings", "morning": "Fatehpur Sikri ghost city (1hr drive) — Akbar's abandoned Mughal capital", "afternoon": "Itmad-ud-Daulah (Baby Taj) — smaller marble marvel predating Taj", "evening": "Shopping at Kinari Bazaar — marble inlay souvenirs and leather goods"},
        {"day": 3, "title": "Mathura & Vrindavan Day Trip", "morning": "Mathura (50km) — birthplace of Lord Krishna. Dwarkadheesh Temple", "afternoon": "Vrindavan — ISKCON temple and Banke Bihari Temple", "evening": "Return to Agra. Farewell Mughlai dinner at Esphahan"}
      ],
      "5_day": [
        {"day": 1, "title": "Taj Mahal — Sunrise Visit", "morning": "Taj at sunrise. Spend 2 hours inside exploring all corners and minarets", "afternoon": "Rest at hotel. Taj moonlight visit if full moon (ticketed separately)", "evening": "Agra Fort light and sound show"},
        {"day": 2, "title": "Agra Monuments", "morning": "Agra Fort interior — Jahangir's palace, Musamman Burj", "afternoon": "Itmad-ud-Daulah → Chini Ka Rauza", "evening": "Petha factory tour. Sheroes Café for dinner"},
        {"day": 3, "title": "Fatehpur Sikri", "morning": "Fatehpur Sikri ghost city full day tour", "afternoon": "Salim Chishti's Dargah (tie a thread for wishes)", "evening": "Sunset photography at Taj from Mehtab Bagh"},
        {"day": 4, "title": "Mathura & Vrindavan", "morning": "Mathura — Gita Mandir, Dwarkadheesh Temple", "afternoon": "Vrindavan — Banke Bihari, Prem Mandir at sunset", "evening": "Return. Mughlai cooking class"},
        {"day": 5, "title": "Crafts & Departure", "morning": "Visit marble inlay workshop — see artisans creating Taj replicas", "afternoon": "Sadar Bazaar shopping — leather goods, carpets, Petha boxes", "evening": "Farewell dinner at Pinch of Spice. Train to Delhi"}
      ]
    },
    "weather": [
      {"month": "Jan", "temp_high": 21, "temp_low": 7, "description": "Best weather — cool and foggy mornings (may obscure Taj)", "emoji": "🌫️"},
      {"month": "Feb", "temp_high": 25, "temp_low": 10, "description": "Excellent — clear skies, perfect for photography", "emoji": "☀️"},
      {"month": "Mar", "temp_high": 30, "temp_low": 15, "description": "Good — comfortable temperatures", "emoji": "🌤️"},
      {"month": "Apr", "temp_high": 37, "temp_low": 21, "description": "Hot — morning visits essential", "emoji": "🌤️"},
      {"month": "May", "temp_high": 43, "temp_low": 27, "description": "Very hot — avoid midday. Dawn and dusk only", "emoji": "🌡️"},
      {"month": "Jun", "temp_high": 41, "temp_low": 28, "description": "Scorching + monsoon starts — not recommended", "emoji": "🌡️"},
      {"month": "Jul", "temp_high": 34, "temp_low": 26, "description": "Monsoon — Taj looks dramatic in rain mist", "emoji": "🌧️"},
      {"month": "Aug", "temp_high": 33, "temp_low": 25, "description": "Monsoon continues — humidity high", "emoji": "🌧️"},
      {"month": "Sep", "temp_high": 33, "temp_low": 24, "description": "Post-monsoon — green surroundings", "emoji": "⛅"},
      {"month": "Oct", "temp_high": 32, "temp_low": 19, "description": "Good — season begins, comfortable", "emoji": "🌤️"},
      {"month": "Nov", "temp_high": 27, "temp_low": 13, "description": "Excellent — clear skies, peak tourist season", "emoji": "☀️"},
      {"month": "Dec", "temp_high": 23, "temp_low": 8, "description": "Very good — cool, clear, some morning fog", "emoji": "🌤️"}
    ],
    "tips": [
      "Visit at SUNRISE — the golden light on white marble is life-changing. Arrive by 5:30am",
      "Buy Taj tickets online at asi.payumoney.com — skip the queue (₹1100 for foreigners, ₹50 for Indians)",
      "Friday: Taj is closed for Juma prayers",
      "No food, tripods, or large bags allowed inside Taj complex",
      "Full moon nights: Taj Mahal moonlight viewing is ticketed separately — book 2 months early",
      "Avoid January fog — it completely obscures the Taj (beautiful in its own way but disappointing if you want photos)"
    ],
    "nearby": ["Mathura (50km)", "Vrindavan (55km)", "Fatehpur Sikri (37km)", "Bharatpur Bird Sanctuary (55km)"]
  },

  "Leh Ladakh": {
    "overview": {
      "tagline": "The land where mountains meet sky and stars touch earth",
      "best_for": ["Adventure Seekers", "Bikers", "Photographers", "Spiritual Travellers"],
      "avg_trip_days": 7,
      "budget_per_day": {"budget": 1500, "mid": 4000, "luxury": 9000},
      "language": "Ladakhi, Hindi, English",
      "currency": "INR",
      "timezone": "IST (UTC+5:30)"
    },
    "how_to_reach": {
      "flight": "Leh Kushok Bakula Rimpochee Airport — flights from Delhi (1hr), Mumbai (2hrs). Book well in advance",
      "road": "Manali–Leh Highway (478km, 2 days) — open May to October only. Srinagar–Leh Highway (434km)",
      "bus": "HRTC Volvo from Manali (seasonal). Private jeeps and Royal Enfield rentals",
      "local_transport": ["Rented Royal Enfield (₹800-1200/day)", "Shared jeep for Nubra/Pangong", "Local taxi union (fixed rates)", "Mountain bike (for fit travellers)"]
    },
    "food": [
      {"name": "Thukpa", "type": "Main Course", "description": "Hearty Tibetan noodle soup with vegetables or meat — perfect for cold Ladakhi evenings", "emoji": "🍜", "must_try": True},
      {"name": "Skyu", "type": "Main Course", "description": "Traditional thick pasta stew with root vegetables — ancient Ladakhi recipe for mountain winters", "emoji": "🍲", "must_try": True},
      {"name": "Butter Tea (Po Cha)", "type": "Drink", "description": "Salted yak butter tea — an acquired taste but essential for acclimatisation", "emoji": "🍵", "must_try": True},
      {"name": "Momos", "type": "Snack / Starter", "description": "Steamed or fried Tibetan dumplings with minced meat or vegetables — addictive at 3500m", "emoji": "🥟", "must_try": True},
      {"name": "Tsampa", "type": "Breakfast", "description": "Roasted barley flour mixed with butter tea or milk — the staple breakfast of Ladakhi nomads", "emoji": "🌾", "must_try": False},
      {"name": "Chhang", "type": "Drink", "description": "Local barley beer — mild and slightly sour. Consumed at festivals and monasteries", "emoji": "🍺", "must_try": False}
    ],
    "restaurants": [
      {"name": "Bon Appetit", "cuisine": "Multi-cuisine / Continental", "price_range": "₹₹₹", "specialty": "Wood-fired pizza and Ladakhi thukpa together — unlikely but excellent", "area": "Leh Market", "rating": 4.5},
      {"name": "The Open Hand", "cuisine": "Continental / Café", "price_range": "₹₹₹", "specialty": "Organic salads, amazing apple pie, and strong coffee", "area": "Main Leh Bazaar", "rating": 4.4},
      {"name": "Wok To Walk", "cuisine": "Tibetan / Chinese", "price_range": "₹₹", "specialty": "Gyuma (Ladakhi sausage) and steaming hot Skyu", "area": "Old Leh", "rating": 4.3},
      {"name": "Gesmo Restaurant", "cuisine": "Multi-cuisine", "price_range": "₹₹", "specialty": "Budget traveller staple — huge portions, kind owners", "area": "Fort Road", "rating": 4.2},
      {"name": "Lamayuru Restaurant", "cuisine": "Ladakhi / Indian", "price_range": "₹₹", "specialty": "Authentic Ladakhi Thukpa and Butter Tea experience", "area": "Changspa", "rating": 4.3},
      {"name": "Café Jeevan", "cuisine": "Indian / Snacks", "price_range": "₹", "specialty": "Fresh Momos and Ladakhi apricot jam on toast", "area": "Leh Old Town", "rating": 4.1}
    ],
    "accommodation": [
      {"name": "Zostel Leh", "type": "Hostel", "price_per_night": 700, "highlights": ["Mountain views", "Rooftop hangout", "Motorcycle trips organised"], "rating": 4.3},
      {"name": "The Grand Dragon", "type": "Hotel", "price_per_night": 7500, "highlights": ["Heated rooms", "Mountain views", "Altitude acclimatisation support"], "rating": 4.5},
      {"name": "Nimmu House", "type": "Boutique", "price_per_night": 9000, "highlights": ["500-year-old heritage property", "River views", "Organic garden meals"], "rating": 4.7},
      {"name": "Chamba Camp Diskit", "type": "Luxury Camp", "price_per_night": 18000, "highlights": ["Nubra Valley tent resort", "Sand dunes views", "Bactrian camel nearby", "Stargazing sessions"], "rating": 4.8},
      {"name": "Ladakhi Homestay", "type": "Homestay", "price_per_night": 900, "highlights": ["Live with a Ladakhi family", "Home-cooked Thukpa and Tsampa", "Monastery guidance"], "rating": 4.5}
    ],
    "itinerary": {
      "3_day": [
        {"day": 1, "title": "ACCLIMATISE in Leh — Do Not Rush!", "morning": "IMPORTANT: Rest completely on arrival day. Altitude sickness is real at 3500m. Walk slowly", "afternoon": "Easy Shanti Stupa walk for panoramic views (go slow)", "evening": "Leh Palace sunset photos from below. Early sleep at 9pm"},
        {"day": 2, "title": "Local Monasteries", "morning": "Hemis Monastery (largest in Ladakh) → Thiksey Monastery (stunning sunrise site)", "afternoon": "Shey Palace → Spituk Monastery with Indus River views", "evening": "Leh Market — buy pashmina shawls and turquoise jewellery"},
        {"day": 3, "title": "Magnetic Hill & Gurudwara", "morning": "Magnetic Hill (vehicles roll uphill) → Pathar Sahib Gurudwara", "afternoon": "Confluence of Indus & Zanskar rivers — colours are dramatic", "evening": "Diskit Village if energy allows. Early return and departure prep"}
      ],
      "5_day": [
        {"day": 1, "title": "Acclimatisation Day", "morning": "REST. Drink lots of water. Short 15-min Shanti Stupa walk maximum", "afternoon": "Leh Palace easy exploration — 1 hour max", "evening": "Early dinner of Thukpa. Sleep at 9pm"},
        {"day": 2, "title": "Monasteries Circuit", "morning": "Hemis → Thiksey → Shey Palace", "afternoon": "Stok Palace Museum → Stakna Monastery", "evening": "Leh bazaar stroll. Dinner at Bon Appetit"},
        {"day": 3, "title": "Nubra Valley — 2-Day Trip", "morning": "Khardung La Pass (world's highest motorable road — 5359m) — photo stop", "afternoon": "Descend to Nubra Valley. Diskit Monastery → Giant Maitreya Buddha statue", "evening": "Hunder Sand Dunes — camel ride on Bactrian double-humped camels at sunset"},
        {"day": 4, "title": "Pangong Lake — 134km Long!", "morning": "Drive from Nubra to Pangong Tso via Shyok River road (4 hrs)", "afternoon": "Pangong Lake — impossible blue-green colour. Walk along shore", "evening": "Camp at Pangong — shooting stars at 4350m. Best stargazing of your life"},
        {"day": 5, "title": "Return & Departure", "morning": "Sunrise at Pangong — colours change from blue to pink to teal. Drive back (5 hrs)", "afternoon": "Chang La Pass photo stop (3rd highest motorable road)", "evening": "Return Leh. Last Momos and Chhang beer. Night flight to Delhi"}
      ]
    },
    "weather": [
      {"month": "Jan", "temp_high": -2, "temp_low": -14, "description": "Frozen — Chadar Frozen River Trek for the brave. Minus 20°C nights", "emoji": "❄️"},
      {"month": "Feb", "temp_high": 1, "temp_low": -12, "description": "Very cold — Chadar Trek continues. Roads closed", "emoji": "❄️"},
      {"month": "Mar", "temp_high": 8, "temp_low": -5, "description": "Cold — roads begin to open, few tourists", "emoji": "🌨️"},
      {"month": "Apr", "temp_high": 15, "temp_low": 2, "description": "Shoulder season — Manali-Leh highway opens late April", "emoji": "⛅"},
      {"month": "May", "temp_high": 22, "temp_low": 7, "description": "Good — all passes open, pleasant days", "emoji": "🌤️"},
      {"month": "Jun", "temp_high": 27, "temp_low": 12, "description": "Excellent — peak season begins, all roads open", "emoji": "☀️"},
      {"month": "Jul", "temp_high": 30, "temp_low": 16, "description": "Best month — maximum sunshine, all routes accessible", "emoji": "☀️"},
      {"month": "Aug", "temp_high": 29, "temp_low": 16, "description": "Peak season — Hemis Festival (monastic dances). Crowded", "emoji": "☀️"},
      {"month": "Sep", "temp_high": 25, "temp_low": 10, "description": "Excellent — crowds thinning, perfect weather", "emoji": "🌤️"},
      {"month": "Oct", "temp_high": 15, "temp_low": 2, "description": "Season ending — passes close, fewer services", "emoji": "⛅"},
      {"month": "Nov", "temp_high": 4, "temp_low": -8, "description": "Cold — Manali highway closes, only flights", "emoji": "🌨️"},
      {"month": "Dec", "temp_high": -1, "temp_low": -13, "description": "Very cold — only for winter trek enthusiasts", "emoji": "❄️"}
    ],
    "tips": [
      "CRITICAL: Spend first 24hrs in Leh doing NOTHING — altitude sickness (AMS) kills the unprepared",
      "Drink 4-5 litres of water daily. Avoid alcohol for first 2 days",
      "Carry Diamox (acetazolamide) — consult your doctor before the trip",
      "Book Pangong & Nubra permits online at DC office website — foreigners need Inner Line Permit",
      "Carry CASH — ATMs in Leh are the last ones you'll see. No ATMs in Nubra or Pangong",
      "Rent Royal Enfield only if you have experience riding on mountain roads",
      "Fuel up in Leh — next petrol pump is 100+ km away on most routes"
    ],
    "nearby": ["Nubra Valley (120km)", "Pangong Lake (140km)", "Tso Moriri (220km)", "Zanskar Valley (230km)"]
  },

  "Jaipur City": {
    "overview": {
      "tagline": "Step into a royal Rajputana dream in the Pink City",
      "best_for": ["History Buffs", "Shoppers", "Families", "Couples", "Photographers"],
      "avg_trip_days": 3,
      "budget_per_day": {"budget": 1200, "mid": 3500, "luxury": 9000},
      "language": "Rajasthani, Hindi, English",
      "currency": "INR",
      "timezone": "IST (UTC+5:30)"
    },
    "how_to_reach": {
      "flight": "Jaipur International Airport (JAI) — direct flights from Delhi, Mumbai, Bangalore, Kolkata",
      "train": "Jaipur Junction — Shatabdi Express from Delhi (4.5 hrs), many overnight trains",
      "bus": "Luxury Volvo from Delhi (5 hrs via expressway — excellent road), RSRTC buses",
      "local_transport": ["Auto-rickshaw", "Cycle rickshaw in Walled City", "Uber/Ola available", "Heritage walk tours", "Hop-on hop-off bus"]
    },
    "food": [
      {"name": "Dal Baati Churma", "type": "Main Course", "description": "Rajasthan's iconic dish — baked wheat balls (baati) with five-lentil dal and sweet ground wheat churma. Cooked in ghee.", "emoji": "🫙", "must_try": True},
      {"name": "Laal Maas", "type": "Main Course", "description": "Fiery Rajasthani mutton curry with Mathania red chilies — not for the faint of heart but unforgettable", "emoji": "🌶️", "must_try": True},
      {"name": "Pyaaz Kachori", "type": "Breakfast / Snack", "description": "Crispy fried pastry stuffed with spiced onion filling — Jaipur's iconic street breakfast with tamarind chutney", "emoji": "🥐", "must_try": True},
      {"name": "Ghevar", "type": "Dessert", "description": "Disc-shaped deep-fried lattice cake soaked in sugar syrup and topped with rabri cream — a Rajasthani festival sweet", "emoji": "🍮", "must_try": True},
      {"name": "Ker Sangri", "type": "Side Dish", "description": "Wild desert berries and beans cooked with dried spices — unique to Rajasthan and impossible to find elsewhere", "emoji": "🌿", "must_try": False},
      {"name": "Mirchi Bada", "type": "Snack", "description": "Large green chili stuffed with potato, coated in gram flour batter and fried — Jodhpur export beloved in Jaipur", "emoji": "🌶️", "must_try": True}
    ],
    "restaurants": [
      {"name": "Laxmi Mishthan Bhandar (LMB)", "cuisine": "Rajasthani Vegetarian", "price_range": "₹₹", "specialty": "Dal Baati Churma and legendary Rajasthani Thali since 1954", "area": "Johari Bazaar", "rating": 4.5},
      {"name": "Suvarna Mahal", "cuisine": "Rajasthani Fine Dining", "price_range": "₹₹₹₹", "specialty": "Royal Laal Maas in the Rambagh Palace — dining in a kingdom", "area": "Rambagh Palace Hotel", "rating": 4.8},
      {"name": "Handi Restaurant", "cuisine": "Mughlai / North Indian", "price_range": "₹₹₹", "specialty": "Laal Maas cooked in traditional clay pot (handi)", "area": "MI Road", "rating": 4.4},
      {"name": "Peacock Rooftop Restaurant", "cuisine": "Multi-cuisine", "price_range": "₹₹₹", "specialty": "Panoramic Pink City views with Rajasthani cuisine", "area": "Hotel Pearl Palace", "rating": 4.3},
      {"name": "Rawat Mishtan Bhandar", "cuisine": "Rajasthani Street Food", "price_range": "₹", "specialty": "Pyaaz Kachori — the definitive version in Jaipur", "area": "Station Road", "rating": 4.6},
      {"name": "Bar Palladio", "cuisine": "Italian / Mediterranean", "price_range": "₹₹₹₹", "specialty": "Hand-made pasta in a Maharaja's garden — surreal setting", "area": "Narain Niwas", "rating": 4.7}
    ],
    "accommodation": [
      {"name": "Zostel Jaipur", "type": "Hostel", "price_per_night": 550, "highlights": ["Old City location", "Rooftop hangout", "Free walking tour"], "rating": 4.2},
      {"name": "Umaid Bhawan Heritage House", "type": "Heritage Hotel", "price_per_night": 4500, "highlights": ["100-yr old haveli", "Rooftop breakfast", "Heritage character"], "rating": 4.5},
      {"name": "Raj Palace Hotel", "type": "Heritage Palace", "price_per_night": 12000, "highlights": ["14th century royal palace", "Antique furniture", "Royal butler service"], "rating": 4.7},
      {"name": "Rambagh Palace", "type": "Luxury Palace", "price_per_night": 35000, "highlights": ["Former residence of Maharaja of Jaipur", "Peacock garden", "Polo ground"], "rating": 4.9},
      {"name": "Moustache Hostel", "type": "Hostel", "price_per_night": 600, "highlights": ["Great location", "Tour packages", "Rooftop café"], "rating": 4.3}
    ],
    "itinerary": {
      "3_day": [
        {"day": 1, "title": "The Forts — Amber & Nahargarh", "morning": "Amber Fort at opening time (9am) — elephant ride up (optional, ethical debate — tread carefully) or jeep", "afternoon": "Nahargarh Fort for panoramic city views → Jaigarh Fort (largest cannon on wheels)", "evening": "Hawa Mahal sunset glow. Johari Bazaar shopping for gems and textiles"},
        {"day": 2, "title": "City Palace & Pink City Bazaars", "morning": "City Palace complex — Diwan-i-Khas, Maharani's palace, museum", "afternoon": "Jantar Mantar UNESCO observatory → Albert Hall Museum", "evening": "Chokhi Dhani village resort — cultural show, camel rides, Rajasthani dinner"},
        {"day": 3, "title": "Markets & Departure", "morning": "Bapu Bazaar for textiles → Tripolia Bazaar for bangles → Nehru Bazaar for juttis (handmade shoes)", "afternoon": "Jal Mahal photo stop (palace in middle of lake)", "evening": "Rawat Kachori breakfast at 7am (yes, breakfast before leaving!). Train to Agra or Delhi"}
      ],
      "5_day": [
        {"day": 1, "title": "Amber Fort Full Day", "morning": "Amber Fort — arrive 9am, 3 hours minimum inside", "afternoon": "Panna Meena Ka Kund step-well → Amber village walk", "evening": "Jaigarh Fort sunset"},
        {"day": 2, "title": "Walled Pink City", "morning": "City Palace → Jantar Mantar observatory", "afternoon": "Hawa Mahal → Johari Bazaar gem shopping", "evening": "Light & Sound show at Amber Fort (Hindi/English shows)"},
        {"day": 3, "title": "Ranthambore Day Trip", "morning": "Early drive to Ranthambore Tiger Reserve (3 hrs)", "afternoon": "Safari — chance to see Bengal Tiger in Rajasthan's jungle", "evening": "Return to Jaipur. Laal Maas dinner at Handi"},
        {"day": 4, "title": "Art & Crafts Trail", "morning": "Block printing workshop in Sanganer village", "afternoon": "Blue pottery workshop → Gem museum", "evening": "Chokhi Dhani cultural evening"},
        {"day": 5, "title": "Stepwells & Markets", "morning": "Abhaneri stepwell (1hr from Jaipur) → Fateh Sagar Lake", "afternoon": "Bapu Bazaar final shopping spree", "evening": "Farewell thali at LMB"}
      ]
    },
    "weather": [
      {"month": "Jan", "temp_high": 22, "temp_low": 8, "description": "Best month — cool, clear, peak tourist season", "emoji": "☀️"},
      {"month": "Feb", "temp_high": 26, "temp_low": 11, "description": "Excellent — pleasant temperatures, clear skies", "emoji": "☀️"},
      {"month": "Mar", "temp_high": 32, "temp_low": 17, "description": "Good — warming up but comfortable", "emoji": "🌤️"},
      {"month": "Apr", "temp_high": 39, "temp_low": 23, "description": "Hot — morning visits essential for monuments", "emoji": "🌡️"},
      {"month": "May", "temp_high": 43, "temp_low": 28, "description": "Very hot — not recommended. 45°C days possible", "emoji": "🌡️"},
      {"month": "Jun", "temp_high": 41, "temp_low": 29, "description": "Extreme heat + dust storms before monsoon", "emoji": "🌪️"},
      {"month": "Jul", "temp_high": 35, "temp_low": 25, "description": "Monsoon — moderate rain, Jaipur looks lush", "emoji": "🌧️"},
      {"month": "Aug", "temp_high": 33, "temp_low": 24, "description": "Monsoon continues — Teej festival (swing festival) — colourful", "emoji": "🌧️"},
      {"month": "Sep", "temp_high": 34, "temp_low": 24, "description": "Post-monsoon — green and pleasant", "emoji": "⛅"},
      {"month": "Oct", "temp_high": 33, "temp_low": 20, "description": "Good — Diwali lights up the Pink City beautifully", "emoji": "🪔"},
      {"month": "Nov", "temp_high": 28, "temp_low": 14, "description": "Excellent — Pushkar Camel Fair nearby. Peak season", "emoji": "☀️"},
      {"month": "Dec", "temp_high": 22, "temp_low": 9, "description": "Best — Christmas markets, Jaipur Literature Festival prep", "emoji": "☀️"}
    ],
    "tips": [
      "Buy Amber Fort + City Palace combo ticket for savings",
      "Hire a local guide at Amber Fort — the hidden stories are extraordinary (₹500 for 2hrs)",
      "Bargain hard in bazaars — start at 40% of asking price",
      "Visit Amber Fort when it opens (9am) to beat crowds and heat",
      "Avoid May and June — Jaipur hits 45°C and is completely inhospitable",
      "Jaipur Literature Festival (January) — world's largest free literary festival. Plan around it"
    ],
    "nearby": ["Ajmer (130km)", "Pushkar (145km)", "Ranthambore (160km)", "Agra (240km)"]
  },

  "Rishikesh": {
    "overview": {
      "tagline": "Where the Himalayas meet the Ganges — yoga, rafting, and soul-searching",
      "best_for": ["Backpackers", "Adventure Seekers", "Yogis", "Spiritual Seekers"],
      "avg_trip_days": 4,
      "budget_per_day": {"budget": 800, "mid": 2500, "luxury": 7000},
      "language": "Hindi, Garhwali, English",
      "currency": "INR",
      "timezone": "IST (UTC+5:30)"
    },
    "how_to_reach": {
      "flight": "Jolly Grant Airport, Dehradun (35km). Fly to Dehradun, then taxi (45 mins)",
      "train": "Rishikesh Railway Station — trains from Delhi (Shatabdi to Haridwar then bus — 6hrs total)",
      "bus": "UPSRTC/Uttarakhand buses from Delhi ISBT (7 hrs). Volvo AC overnight buses comfortable",
      "local_transport": ["Walking (most of Rishikesh is walkable)", "Vikram (shared mini-jeep — ₹10)", "Auto-rickshaw", "River crossing by boat (₹10)"]
    },
    "food": [
      {"name": "Ganga Aarti Prasad", "type": "Spiritual Food", "description": "Blessed food distributed after the evening Ganga Aarti ceremony — simple but sacred", "emoji": "🙏", "must_try": True},
      {"name": "Rhododendron Juice", "type": "Drink", "description": "Fresh pink juice made from Buransh flowers — only available March-April in mountain season", "emoji": "🌸", "must_try": False},
      {"name": "Saatvik Thali", "type": "Main Course", "description": "Pure vegetarian Ayurvedic meal — no onion, no garlic, as served in ashrams. Deeply nourishing", "emoji": "🍱", "must_try": True},
      {"name": "Chai at Ram Jhula", "type": "Drink", "description": "Ginger-cardamom tea with views of the Ganges from a rooftop — the quintessential Rishikesh moment", "emoji": "☕", "must_try": True},
      {"name": "Chocolate Banana Pancakes", "type": "Breakfast", "description": "Backpacker cafés line the streets with these — perfect pre-rafting fuel", "emoji": "🥞", "must_try": False},
      {"name": "Bhandaras (Langars)", "type": "Free Community Meal", "description": "Free communal meals served at ashrams — simple daal-chawal served to all", "emoji": "🍲", "must_try": True}
    ],
    "restaurants": [
      {"name": "Little Buddha Café", "cuisine": "International / Israeli", "price_range": "₹₹", "specialty": "Shakshuka, hummus and mezze — beloved by Israeli backpackers for decades", "area": "Lakshman Jhula", "rating": 4.4},
      {"name": "Chotiwala Restaurant", "cuisine": "North Indian Vegetarian", "price_range": "₹", "specialty": "Iconic Ganga-side restaurant — Thali and Aloo Poori since 1958", "area": "Swarg Ashram", "rating": 4.2},
      {"name": "Ganga Beach Restaurant", "cuisine": "Indian / Continental", "price_range": "₹₹", "specialty": "Sitting on the beach with Ganges rushing past — the setting IS the dish", "area": "Tapovan", "rating": 4.3},
      {"name": "Café Dewa", "cuisine": "Café / Healthy", "price_range": "₹₹", "specialty": "Avocado toast, smoothie bowls, and yoga-studio atmosphere", "area": "Tapovan", "rating": 4.4},
      {"name": "Madras Café", "cuisine": "South Indian", "price_range": "₹", "specialty": "Crispy dosas and filter coffee at Rishikesh's hidden gem", "area": "Ram Jhula", "rating": 4.3},
      {"name": "Bistro Nirvana", "cuisine": "Italian / Café", "price_range": "₹₹", "specialty": "Wood-fired pizza by the Ganges — sounds odd, tastes divine", "area": "Lakshman Jhula", "rating": 4.2}
    ],
    "accommodation": [
      {"name": "Zostel Rishikesh", "type": "Hostel", "price_per_night": 450, "highlights": ["Ganges views", "Adventure sports desk", "Social rooftop"], "rating": 4.4},
      {"name": "Parmarth Niketan Ashram", "type": "Ashram", "price_per_night": 1200, "highlights": ["Daily yoga at sunrise", "Ganga Aarti front row", "Vegetarian meals included", "Meditation classes"], "rating": 4.5},
      {"name": "Divine Resort Rishikesh", "type": "Hotel", "price_per_night": 4000, "highlights": ["Ganges-facing rooms", "Yoga deck", "Ayurvedic spa"], "rating": 4.3},
      {"name": "Aloha on the Ganges", "type": "Luxury Resort", "price_per_night": 9500, "highlights": ["Private river beach", "Infinity pool over Ganges", "Helicopter transfers available"], "rating": 4.7},
      {"name": "Glamp on Ganges", "type": "Luxury Camp", "price_per_night": 6000, "highlights": ["Riverside glamping tents", "Bonfire evenings", "White-water views", "Star-gazing"], "rating": 4.6}
    ],
    "itinerary": {
      "3_day": [
        {"day": 1, "title": "Arrival, Aarti & the Bridges", "morning": "Check in. Walk across Lakshman Jhula suspension bridge", "afternoon": "Beatles Ashram (Maharishi Mahesh Yogi's — the Beatles meditated here in 1968)", "evening": "Dashashwamedh Ghat for GANGA AARTI at sunset — one of India's most moving ceremonies. Dine at Chotiwala"},
        {"day": 2, "title": "White-Water Rafting", "morning": "Rafting on the Ganges — choose 16km or 36km stretch with rapids up to Grade IV. Book with Aqua Terra or Red Chilli", "afternoon": "Bungee jumping at Jumpin Heights (highest in India — 83m) or Giant Swing", "evening": "Evening yoga class at Parmarth Niketan. Ganga Aarti again"},
        {"day": 3, "title": "Temples & Departure", "morning": "Sunrise yoga on the banks of Ganges", "afternoon": "Neelkanth Mahadev Temple trek (22km round trip) or jeep", "evening": "Triveni Ghat evening dip. Farewell chai at Ram Jhula viewpoint"}
      ],
      "5_day": [
        {"day": 1, "title": "Settle & Spirituality", "morning": "Arrive. Check in. Ram Jhula walk", "afternoon": "Beatles Ashram → Swarg Ashram walk", "evening": "Parmarth Ganga Aarti (most spectacular in Rishikesh)"},
        {"day": 2, "title": "White-Water Rafting Day", "morning": "36km rafting — Shivpuri to Rishikesh. Best rapids: Golf Course (IV), Crossfire (IV)", "afternoon": "Cliff jumping at Shivpuri beach", "evening": "Bonfire and guitar at Zostel. Campfire momos"},
        {"day": 3, "title": "Yoga & Meditation Immersion", "morning": "Sunrise yoga (6am) at Parmarth Niketan or Rishikul", "afternoon": "Ayurvedic massage and shirodhara oil therapy", "evening": "Meditation session at Vashishtha Cave (natural cave on Ganges bank)"},
        {"day": 4, "title": "Haridwar Day Trip", "morning": "Haridwar (25km) — Har Ki Pauri sacred ghat. Morning dip in Ganga", "afternoon": "Chandi Devi Temple ropeway → Mansa Devi Temple", "evening": "Haridwar Ganga Aarti (more dramatic than Rishikesh). Return"},
        {"day": 5, "title": "Neelkanth & Departure", "morning": "Neelkanth Mahadev Temple trek (7km up) — Lord Shiva's abode", "afternoon": "Rajaji National Park jeep safari (if time)", "evening": "Final chai at Ram Jhula. Bus to Delhi"}
      ]
    },
    "weather": [
      {"month": "Jan", "temp_high": 18, "temp_low": 6, "description": "Cool and clear — good for yoga, not rafting (water very cold)", "emoji": "🌤️"},
      {"month": "Feb", "temp_high": 22, "temp_low": 9, "description": "Pleasant — Mauni Amavasya pilgrimage season", "emoji": "☀️"},
      {"month": "Mar", "temp_high": 28, "temp_low": 14, "description": "Best — International Yoga Festival (March 1-7). Perfect weather", "emoji": "☀️"},
      {"month": "Apr", "temp_high": 33, "temp_low": 18, "description": "Good — rafting season at peak", "emoji": "☀️"},
      {"month": "May", "temp_high": 38, "temp_low": 23, "description": "Hot but rafting still excellent (water cool from glaciers)", "emoji": "🌤️"},
      {"month": "Jun", "temp_high": 35, "temp_low": 25, "description": "Monsoon approaching — last weeks of rafting season", "emoji": "🌦️"},
      {"month": "Jul", "temp_high": 29, "temp_low": 22, "description": "Monsoon — rafting BANNED (river dangerous). Temples beautiful", "emoji": "🌧️"},
      {"month": "Aug", "temp_high": 28, "temp_low": 22, "description": "Heavy rain — Janmashtami celebrations. No rafting", "emoji": "⛈️"},
      {"month": "Sep", "temp_high": 29, "temp_low": 21, "description": "Monsoon ends — Navratri. Rafting resumes slowly", "emoji": "🌦️"},
      {"month": "Oct", "temp_high": 30, "temp_low": 16, "description": "Excellent — Diwali lights on Ganga. Rafting fully open", "emoji": "🪔"},
      {"month": "Nov", "temp_high": 24, "temp_low": 11, "description": "Good — cool evenings, peak yoga retreat season", "emoji": "🌤️"},
      {"month": "Dec", "temp_high": 18, "temp_low": 6, "description": "Cold — New Year celebrations on Ganges. Spiritual winter", "emoji": "❄️"}
    ],
    "tips": [
      "Ganga Aarti at Parmarth Niketan (7pm) is non-negotiable — arrive 30 mins early for front rows",
      "Rafting season: Feb-June and Sept-Nov. NEVER raft during monsoon",
      "Book bungee at Jumpin Heights online — slots fill up weeks in advance",
      "Rishikesh is fully vegetarian and alcohol-free (by law in the sacred zone)",
      "The Beatles came here in 1968 — their ashram (Chaurasi Kutia) is now a graffiti art park (₹150 entry)",
      "Lakshman Jhula bridge: famous but now restricted due to safety — use alternate bridges"
    ],
    "nearby": ["Haridwar (25km)", "Dehradun (45km)", "Mussoorie (77km)", "Auli ski resort (250km)"]
  },

  "Manali": {
    "overview": {
      "tagline": "Himalayan paradise for skiers, trekkers, and honeymooners",
      "best_for": ["Couples", "Adventure Seekers", "Skiers", "Road-trippers"],
      "avg_trip_days": 5,
      "budget_per_day": {"budget": 1200, "mid": 3500, "luxury": 9000},
      "language": "Pahari, Hindi, English",
      "currency": "INR",
      "timezone": "IST (UTC+5:30)"
    },
    "how_to_reach": {
      "flight": "Bhuntar Airport (50km from Manali) — small airport, limited flights from Delhi/Chandigarh",
      "bus": "Volvo AC sleeper from Delhi (14 hrs overnight) — most popular option. ₹1200-2000",
      "road": "Drive from Delhi via NH-3 (560km, 12-14 hrs). Self-drive in a good 4WD or taxi hire",
      "local_transport": ["Local taxis (fixed rate chart at taxi union)", "Bike rental (₹500-800/day)", "Shared cabs to Rohtang and Solang", "Horse riding in Solang Valley"]
    },
    "food": [
      {"name": "Siddu", "type": "Main Course", "description": "Stuffed steamed wheat bread with walnut and poppy seed filling — Himachal's unique comfort food", "emoji": "🥐", "must_try": True},
      {"name": "Trout Fish Curry", "type": "Main Course", "description": "Fresh Himalayan river trout cooked in tomato and mustard gravy — caught from Beas River nearby", "emoji": "🐟", "must_try": True},
      {"name": "Chha Gosht", "type": "Main Course", "description": "Himachali marinated lamb in gramflour-based gravy with yogurt and spices — a mountain delicacy", "emoji": "🍖", "must_try": True},
      {"name": "Aktori", "type": "Dessert", "description": "Buckwheat pancakes sweet or savoury — traditional Lahaul-Spiti recipe", "emoji": "🥞", "must_try": False},
      {"name": "Apple Fresh Juice", "type": "Drink", "description": "Manali is India's apple capital — fresh-pressed juice at ₹30 a glass from roadside vendors", "emoji": "🍎", "must_try": True},
      {"name": "Momos & Thukpa", "type": "Snack", "description": "Tibetan-style dumplings and noodle soup — Manali Old Town has excellent Tibetan restaurants", "emoji": "🥟", "must_try": True}
    ],
    "restaurants": [
      {"name": "Johnson's Café", "cuisine": "Continental / Trout", "price_range": "₹₹₹", "specialty": "Beas River Trout cooked 4 ways — legendary in Manali", "area": "Circuit House Road", "rating": 4.6},
      {"name": "Drifter's Inn & Café", "cuisine": "Tibetan / International", "price_range": "₹₹", "specialty": "Yak cheese momos and excellent Tibetan butter tea", "area": "Old Manali", "rating": 4.4},
      {"name": "Café 1947", "cuisine": "Multicuisine", "price_range": "₹₹", "specialty": "Budget traveller favourite with good pasta and momos", "area": "Old Manali", "rating": 4.2},
      {"name": "Mayur Restaurant", "cuisine": "North Indian / Chinese", "price_range": "₹₹", "specialty": "Butter chicken and hakka noodles — tried and tested", "area": "Mall Road", "rating": 4.1},
      {"name": "Chopsticks", "cuisine": "Tibetan / Chinese", "price_range": "₹₹", "specialty": "Chilli chicken and garlic noodles — Manali's best Asian spot", "area": "Mall Road", "rating": 4.3},
      {"name": "Sher-E-Punjab Dhaba", "cuisine": "Punjabi / Indian", "price_range": "₹", "specialty": "Sarson da saag, makki di roti and endless lassi", "area": "Bypass Road", "rating": 4.4}
    ],
    "accommodation": [
      {"name": "Zostel Manali", "type": "Hostel", "price_per_night": 550, "highlights": ["Trek booking desk", "Social common area", "Mountain views"], "rating": 4.3},
      {"name": "Hotel Sunflower", "type": "Hotel", "price_per_night": 2800, "highlights": ["Beas river views", "Warm rooms", "Good value"], "rating": 4.2},
      {"name": "Solang Nature Resort", "type": "Resort", "price_per_night": 7500, "highlights": ["Base of Solang Valley", "Skiing access", "Mountain backdrop"], "rating": 4.4},
      {"name": "The Orchard Greens", "type": "Boutique", "price_per_night": 5500, "highlights": ["Apple orchard setting", "Wood-panelled rooms", "Fireplace"], "rating": 4.6},
      {"name": "Snow Valley Resorts", "type": "Resort", "price_per_night": 11000, "highlights": ["Ski-in ski-out in winter", "Spa", "Mountain view infinity pool (summer)"], "rating": 4.7}
    ],
    "itinerary": {
      "3_day": [
        {"day": 1, "title": "Arrival & Old Manali", "morning": "Arrive from overnight bus. Check in. Rest. Walk to Hadimba Devi Temple through deodar forest", "afternoon": "Old Manali lanes — handicraft shops, cafés, Tibetan quarter", "evening": "Mall Road stroll. Dinner at Johnson's Café"},
        {"day": 2, "title": "Rohtang Pass Adventure", "morning": "Rohtang Pass (3978m) — permit required (₹500, book online). Snow even in June", "afternoon": "Solang Valley — paragliding (₹2000), zorbing, horse riding", "evening": "Manikaran Gurudwara hot springs (1hr from Manali). Free langar dinner"},
        {"day": 3, "title": "Naggar & Departure", "morning": "Naggar Castle — 500-year-old fort now heritage hotel with views. Nicholas Roerich Art Gallery", "afternoon": "Kullu Valley drive — Bijli Mahadev Temple hike for panoramic view", "evening": "Mall Road farewell dinner. Night bus to Delhi"}
      ],
      "5_day": [
        {"day": 1, "title": "Arrival & Manali Town", "morning": "Rest after overnight journey. Hadimba Temple walk", "afternoon": "Tibetan Monastery → Van Vihar National Park walk", "evening": "Old Manali café hopping"},
        {"day": 2, "title": "Rohtang & Solang", "morning": "Rohtang Pass — depart 6am to beat traffic", "afternoon": "Solang Valley activities", "evening": "Manikaran hot springs"},
        {"day": 3, "title": "Spiti Valley Entry (Kaza)", "morning": "Drive towards Spiti via Kunzum Pass (if open, May-Oct)", "afternoon": "Kaza town — Key Monastery", "evening": "Stay in Kaza — stargazing at 3800m"},
        {"day": 4, "title": "Spiti Wonders", "morning": "Kibber (highest motorable village) → Langza (fossil hunting at 4400m)", "afternoon": "Dhankar Monastery perched on cliff", "evening": "Return to Kaza or Manali"},
        {"day": 5, "title": "Kullu & Departure", "morning": "Naggar Castle → Roerich Art Gallery", "afternoon": "River rafting on Beas at Pirdi (Grade III-IV)", "evening": "Night bus to Delhi"}
      ]
    },
    "weather": [
      {"month": "Jan", "temp_high": 4, "temp_low": -10, "description": "Snow season — excellent skiing at Solang. Roads may be blocked", "emoji": "❄️"},
      {"month": "Feb", "temp_high": 7, "temp_low": -7, "description": "Peak ski season. Snowfall heavy. Very cold nights", "emoji": "⛷️"},
      {"month": "Mar", "temp_high": 13, "temp_low": -2, "description": "Snow melting — beautiful landscapes. Spring flowers begin", "emoji": "🌨️"},
      {"month": "Apr", "temp_high": 19, "temp_low": 5, "description": "Good — Rohtang still closed. Apple blossom season", "emoji": "🌸"},
      {"month": "May", "temp_high": 24, "temp_low": 10, "description": "Excellent — Rohtang opens. Green valleys and snow peaks", "emoji": "☀️"},
      {"month": "Jun", "temp_high": 27, "temp_low": 14, "description": "Best month — all roads open, perfect weather, peak season", "emoji": "☀️"},
      {"month": "Jul", "temp_high": 26, "temp_low": 15, "description": "Monsoon season — landslides risk on Rohtang road", "emoji": "🌧️"},
      {"month": "Aug", "temp_high": 25, "temp_low": 14, "description": "Monsoon continues — rivers swell. Check road status daily", "emoji": "⛈️"},
      {"month": "Sep", "temp_high": 22, "temp_low": 10, "description": "Excellent — post-monsoon, clear blue skies, less crowded", "emoji": "🌤️"},
      {"month": "Oct", "temp_high": 16, "temp_low": 4, "description": "Good — season closing. Apple harvest festival", "emoji": "🍎"},
      {"month": "Nov", "temp_high": 9, "temp_low": -3, "description": "Cold — Rohtang closes. Early snow at higher elevations", "emoji": "🌨️"},
      {"month": "Dec", "temp_high": 4, "temp_low": -8, "description": "Ski season begins. Christmas in snow — magical", "emoji": "🎄"}
    ],
    "tips": [
      "Book Rohtang Pass permit ONLINE at himachal.nic.in — only 800 vehicles allowed daily",
      "Drive or take a night Volvo from Delhi — avoid daytime buses (endless stops)",
      "Carry warm layers even in June — temperature drops sharply after sunset",
      "Paragliding at Solang Valley (₹1500-2500) and Billing (₹2500) are must-dos",
      "Old Manali is 2km from Mall Road — the cafés, guesthouses, and vibe are infinitely better",
      "Manali-Leh Highway: rent Royal Enfield here (₹1000/day) for the Leh road trip"
    ],
    "nearby": ["Solang Valley (14km)", "Rohtang Pass (51km)", "Naggar (22km)", "Spiti Valley (195km)"]
  }
}

# Add remaining 13 destinations with compact but complete data
REMAINING = {
  "Hampi Ruins": {"overview": {"tagline": "Boulders, ruins, and timeless wonder — the empire that once was", "best_for": ["History Buffs","Photographers","Backpackers"], "avg_trip_days": 3, "budget_per_day": {"budget":800,"mid":2500,"luxury":6000}, "language":"Kannada, English", "currency":"INR", "timezone":"IST"}, "food": [{"name":"Bisi Bele Bath","type":"Main","description":"Karnataka's one-pot rice, lentil and vegetable dish with ghee and cashews","emoji":"🍲","must_try":True},{"name":"Set Dosa","type":"Breakfast","description":"Soft spongy dosas served in a set of three — Hampi's staple breakfast","emoji":"🥞","must_try":True},{"name":"Jolada Rotti","type":"Main","description":"Sorghum flatbread with spicy chutney — Uttara Karnataka tradition","emoji":"🫓","must_try":True}], "restaurants": [{"name":"Mango Tree Restaurant","cuisine":"Multi-cuisine","price_range":"₹₹","specialty":"Riverside dining on boulders with bananas","area":"Tungabhadra riverbank","rating":4.4},{"name":"Laughing Buddha","cuisine":"Israeli/Indian","price_range":"₹₹","specialty":"Shakshuka and masala chai overlooking ruins","area":"Virupapur Gadde","rating":4.3}], "accommodation": [{"name":"Hampi's Boulders Resort","type":"Boutique","price_per_night":8500,"highlights":["Built among 500m.y.o. boulders","Pool","Yoga sessions"],"rating":4.7},{"name":"Kishkinda Trust","type":"Eco-lodge","price_per_night":2500,"highlights":["Supporting local artisans","Organic meals"],"rating":4.4}], "itinerary": {"3_day": [{"day":1,"title":"Royal Enclosure","morning":"Vitthala Temple at sunrise — stone chariot photo","afternoon":"Hampi Bazaar → Lotus Mahal → Elephant Stables","evening":"Sunset at Matanga Hill — 360° view of ruins"},{"day":2,"title":"Virupapur Gadde","morning":"Cross river by coracle boat → hippy village walk","afternoon":"Anjaneya Hill (Hanuman birthplace) — 570 steps","evening":"Sunset at Tungabhadra Dam"},{"day":3,"title":"Southern Ruins","morning":"Achyutaraya Temple → Queen's Bath","afternoon":"Underground Shiva Temple → Pattabhirama Temple","evening":"Departure"}]}, "tips": ["Rent a cycle (₹80/day) — best way to explore scattered ruins","Virupapur Gadde across the river is where backpackers stay (no motored vehicles)","Carry lots of water — Hampi is extremely hot and exposed","Sunrise at Matanga Hill is legendary — climb in pitch dark with a torch"], "nearby": ["Hospet (13km)","Badami (140km)","Mysore (340km)"], "weather": [{"month":"Jan","temp_high":29,"temp_low":16,"description":"Ideal — cool and clear","emoji":"☀️"},{"month":"Oct","temp_high":32,"temp_low":22,"description":"Good — post monsoon green","emoji":"🌤️"},{"month":"Jul","temp_high":27,"temp_low":22,"description":"Monsoon — dramatic skies","emoji":"🌧️"}]},
  "Ajanta Ellora Caves": {"overview": {"tagline": "2000-year-old rock-cut masterpieces that will humble your soul", "best_for": ["History Buffs","Art Lovers","Families"], "avg_trip_days": 2, "budget_per_day": {"budget":1000,"mid":2500,"luxury":6000}, "language":"Marathi, Hindi, English", "currency":"INR", "timezone":"IST"}, "food": [{"name":"Varhadi Mutton","type":"Main","description":"Vidarbha-style spicy mutton curry with garam masala — Aurangabad specialty","emoji":"🍖","must_try":True},{"name":"Naan Qalia","type":"Main","description":"Aurangabad's Mughal naan with slow-cooked lamb — Hyderabadi influence","emoji":"🫓","must_try":True},{"name":"Shahi Tukda","type":"Dessert","description":"Royal bread pudding with condensed milk and silver leaf — Mughal legacy","emoji":"🍮","must_try":True}], "restaurants": [{"name":"Bhoj Restaurant","cuisine":"Maharashtrian","price_range":"₹₹","specialty":"Maharashtrian Thali with 15 dishes","area":"Aurangabad","rating":4.3},{"name":"Tandoor Restaurant","cuisine":"Mughlai","price_range":"₹₹₹","specialty":"Naan Qalia and Mughlai biryani","area":"Aurangabad","rating":4.4}], "accommodation": [{"name":"MTDC Resort Ajanta","type":"Hotel","price_per_night":3500,"highlights":["Near cave entrance","AC rooms","Restaurant"],"rating":4.1},{"name":"Lemon Tree Hotel","type":"Hotel","price_per_night":5500,"highlights":["Pool","Restaurant","Airport pickup"],"rating":4.4}], "itinerary": {"3_day": [{"day":1,"title":"Ellora Caves","morning":"Kailash Temple (Cave 16) — world's largest rock-cut monolith. Spend 3 hrs minimum","afternoon":"Buddhist and Jain cave groups at Ellora","evening":"Bibi Ka Maqbara (mini Taj) at sunset"},{"day":2,"title":"Ajanta Caves","morning":"Early bus to Ajanta (100km). Cave 1, 2, 9, 10, 16, 17 — stunning Buddhist frescoes","afternoon":"Cave 26 — giant reclining Buddha","evening":"Return Aurangabad. Daulatabad Fort visit"},{"day":3,"title":"Departure","morning":"Aurangabad Markets — Bidriware and Paithani silk sarees","afternoon":"Departure","evening":""}]}, "tips": ["Ellora and Ajanta are 100km apart — visit on separate days","Hire a guide at caves (₹500) — the stories behind paintings are extraordinary","Photography allowed at Ellora, restricted at Ajanta — respect the rules","Visit Ajanta early — the site gets very hot by midday"], "nearby": ["Aurangabad (100km from Ajanta)","Shirdi (120km)","Nashik (190km)"], "weather": [{"month":"Nov","temp_high":30,"temp_low":16,"description":"Best — cool and dry","emoji":"☀️"},{"month":"Jan","temp_high":28,"temp_low":12,"description":"Excellent","emoji":"☀️"},{"month":"Jul","temp_high":26,"temp_low":21,"description":"Monsoon — green hills","emoji":"🌧️"}]},
  "Khajuraho Temples": {"overview": {"tagline": "Ancient erotic sculptures hiding profound spiritual wisdom", "best_for": ["History Buffs","Couples","Photographers"], "avg_trip_days": 2, "budget_per_day": {"budget":1000,"mid":2500,"luxury":5000}, "language":"Hindi, Bundeli, English", "currency":"INR", "timezone":"IST"}, "food": [{"name":"Bafla","type":"Main","description":"Bundeli version of baati — baked wheat balls in pure ghee with dal","emoji":"🫙","must_try":True},{"name":"Poha Jalebi","type":"Breakfast","description":"Flattened rice breakfast with crispy jalebis — MP morning tradition","emoji":"🥐","must_try":True}], "restaurants": [{"name":"Rajput Restaurant","cuisine":"Indian","price_range":"₹₹","specialty":"MP Thali with bafla and dal","area":"Temple Road","rating":4.2},{"name":"Mediterraneo Restaurant","cuisine":"Continental","price_range":"₹₹₹","specialty":"Italian-inspired food near temples","area":"Khajuraho town","rating":4.3}], "accommodation": [{"name":"Hotel Harmony","type":"Budget","price_per_night":1500,"highlights":["Walking distance to temples","Rooftop views"],"rating":4.0},{"name":"Ramada Khajuraho","type":"Hotel","price_per_night":7000,"highlights":["Pool","Garden views","Restaurant"],"rating":4.4}], "itinerary": {"3_day": [{"day":1,"title":"Western Temples","morning":"Western Group sunrise — Kandariya Mahadeva (tallest temple), Lakshmana","afternoon":"Sound & Light show evening — Hindi or English narration","evening":""},{"day":2,"title":"Eastern & Southern","morning":"Eastern Jain temples → Chaturbhuja Temple with giant Vishnu","afternoon":"Panna National Park safari (tigers and Ken River crocodiles)","evening":"Raneh Falls waterfall walk"},{"day":3,"title":"Departure","morning":"Archaeological Museum — miniature sculptures","afternoon":"Departure","evening":""}]}, "tips": ["Western group temples are free with ASI ticket. Others separate","Hire a guide who explains the Tantric philosophy — without context, you see only erotic art","Khajuraho Dance Festival (February-March) is spectacular — classical dance against temple backdrop","Panna Tiger Reserve safaris often sighted — book early"], "nearby": ["Panna NP (25km)","Orchha (175km)","Varanasi (400km)"], "weather": [{"month":"Jan","temp_high":22,"temp_low":7,"description":"Best — clear and cool","emoji":"☀️"},{"month":"Feb","temp_high":26,"temp_low":10,"description":"Dance Festival month","emoji":"🌤️"},{"month":"Jul","temp_high":28,"temp_low":22,"description":"Monsoon — green and lush","emoji":"🌧️"}]},
  "Coorg": {"overview": {"tagline": "Karnataka's coffee highlands — Scotland of India", "best_for": ["Nature Lovers","Couples","Coffee Enthusiasts"], "avg_trip_days": 3, "budget_per_day": {"budget":1200,"mid":3500,"luxury":9000}, "language":"Kodava, Kannada, English", "currency":"INR", "timezone":"IST"}, "food": [{"name":"Pandi Curry","type":"Main","description":"Coorg's iconic pork curry with Kachampuli vinegar — Kodava warrior food","emoji":"🍖","must_try":True},{"name":"Akki Rotti","type":"Breakfast","description":"Rice flour flatbread with coconut — Kodava breakfast staple","emoji":"🫓","must_try":True},{"name":"Coorg Coffee","type":"Drink","description":"Filter coffee from estate-fresh beans — world's finest","emoji":"☕","must_try":True}], "restaurants": [{"name":"Old Courtyard","cuisine":"Kodava","price_range":"₹₹₹","specialty":"Pandi Curry and Coorg Thali in heritage home","area":"Madikeri","rating":4.5},{"name":"Coorg Green Hotel","cuisine":"South Indian","price_range":"₹₹","specialty":"Jackfruit curries and fresh coffee","area":"Virajpet","rating":4.2}], "accommodation": [{"name":"Amanvana Spa Resort","type":"Luxury","price_per_night":14000,"highlights":["River-facing villas","Spa","Organic garden","Coffee plantation"],"rating":4.8},{"name":"Honey Valley Estate","type":"Homestay","price_per_night":2800,"highlights":["Coffee plantation stay","Trekking trails","Home-cooked Kodava food"],"rating":4.6}], "itinerary": {"3_day": [{"day":1,"title":"Madikeri Town","morning":"Madikeri Fort → Abbey Falls (25m waterfall through coffee estate)","afternoon":"Raja's Seat viewpoint — sunset over valleys","evening":"Omkareshwar Temple"},{"day":2,"title":"Wildlife & Waterfalls","morning":"Nagarhole National Park safari (tigers, elephants, leopards)","afternoon":"Iruppu Falls near Brahmagiri Wildlife Sanctuary","evening":"Dubare Elephant Camp — elephant bathing"},{"day":3,"title":"Plantation Walk","morning":"Coffee plantation guided walk — learn processing from cherry to cup","afternoon":"Talakaveri (source of Kaveri River)","evening":"Departure"}]}, "tips": ["Monsoon (June-September): Coorg turns emerald green — most beautiful but roads can flood","Coffee and pepper estates welcome visitors — many offer plantation walks","Kodavas (locals) have rich warrior heritage — very hospitable but privacy-loving"], "nearby": ["Mysore (120km)","Wayanad (80km)","Mangalore (130km)"], "weather": [{"month":"Oct","temp_high":25,"temp_low":16,"description":"Post-monsoon — lush green","emoji":"🌿"},{"month":"Jan","temp_high":22,"temp_low":12,"description":"Ideal — cool and misty","emoji":"☀️"},{"month":"Jun","temp_high":22,"temp_low":17,"description":"Monsoon — dramatic waterfalls","emoji":"🌧️"}]},
  "Munnar": {"overview": {"tagline": "Sea of tea gardens rolling across misty mountain peaks", "best_for": ["Nature Lovers","Couples","Photographers"], "avg_trip_days": 3, "budget_per_day": {"budget":1000,"mid":3000,"luxury":8000}, "language":"Malayalam, Tamil, English", "currency":"INR", "timezone":"IST"}, "food": [{"name":"Appam & Kerala Stew","type":"Breakfast","description":"Lacy hoppers with creamy vegetable stew — the mountain morning classic","emoji":"🥞","must_try":True},{"name":"Tea-Smoked Duck","type":"Main","description":"Duck slow-cooked with Munnar tea leaves — unique to the hills","emoji":"🍗","must_try":True},{"name":"Fresh Cardamom Tea","type":"Drink","description":"Cardamom harvested here, infused in strong Munnar tea — unmatched aroma","emoji":"🫖","must_try":True}], "restaurants": [{"name":"Saravana Bhavan","cuisine":"South Indian Vegetarian","price_range":"₹","specialty":"Masala Dosa and Idli with gunpowder chutney","area":"Munnar Town","rating":4.3},{"name":"Rapsy Restaurant","cuisine":"Kerala","price_range":"₹₹","specialty":"Appam and tea-smoked chicken","area":"Munnar Town","rating":4.4}], "accommodation": [{"name":"Windermere Estate","type":"Boutique","price_per_night":8500,"highlights":["Working cardamom estate","Heritage bungalow","Walking trails"],"rating":4.7},{"name":"Zostel Munnar","type":"Hostel","price_per_night":500,"highlights":["Budget option","Trekking desk","Mountain views"],"rating":4.2}], "itinerary": {"3_day": [{"day":1,"title":"Tea Gardens","morning":"Eravikulam NP — Nilgiri Tahr sighting on rolling meadows","afternoon":"Tea Museum → Pothamedu Viewpoint","evening":"Tea plantation walk at dusk — golden light through green rows"},{"day":2,"title":"Waterfalls & Peaks","morning":"Lakkam Waterfalls → Attukal Waterfalls","afternoon":"Anamudi Peak base trek (2695m — South India's highest)","evening":"Night sky stargazing — minimal light pollution"},{"day":3,"title":"Spice & Departure","morning":"Marayoor Sandalwood Forest → Dolmens (prehistoric stone tombs)","afternoon":"Spice garden visit — cardamom, pepper, vanilla","evening":"Drive to Kochi"}]}, "tips": ["Neelakurinji blooms only every 12 years — next bloom 2030. Check before planning","Visit Rajamala (Eravikulam) early morning before clouds roll in","Top Station viewpoint (32km) — worth the drive for the most dramatic views of Kerala plains below"], "nearby": ["Thekkady (85km)","Kodaikanal (60km)","Kochi (130km)"], "weather": [{"month":"Sep","temp_high":22,"temp_low":14,"description":"Post-monsoon — mist on tea","emoji":"🌿"},{"month":"Jan","temp_high":20,"temp_low":10,"description":"Excellent — clear and cool","emoji":"☀️"},{"month":"Jun","temp_high":19,"temp_low":14,"description":"Monsoon — heavy rain","emoji":"🌧️"}]},
  "Kaziranga": {"overview": {"tagline": "Home to the great one-horned rhinoceros — wildlife at its rawest", "best_for": ["Wildlife Enthusiasts","Photographers","Nature Lovers"], "avg_trip_days": 3, "budget_per_day": {"budget":2000,"mid":5000,"luxury":12000}, "language":"Assamese, Hindi, English", "currency":"INR", "timezone":"IST"}, "food": [{"name":"Masor Tenga","type":"Main","description":"Assamese fish curry with tomatoes and elephant apple — light and tangy","emoji":"🐟","must_try":True},{"name":"Pitha","type":"Snack","description":"Sticky rice cakes steamed in banana leaves — Bihu festival delicacy","emoji":"🫘","must_try":True},{"name":"Assam Tea","type":"Drink","description":"World-famous strong black tea from Assam gardens — best drunk with jaggery","emoji":"☕","must_try":True}], "restaurants": [{"name":"Wild Grass Resort Restaurant","cuisine":"Assamese","price_range":"₹₹₹","specialty":"Authentic Assamese Thali with 12 dishes","area":"Kohora","rating":4.5},{"name":"Diphlu River Lodge Restaurant","cuisine":"Assamese/Indian","price_range":"₹₹₹₹","specialty":"Wild mushroom dishes and smoked fish","area":"Kohora","rating":4.6}], "accommodation": [{"name":"Iora The Retreat","type":"Resort","price_per_night":9000,"highlights":["Adjacent to park","Wildlife viewing deck","Elephant rides"],"rating":4.6},{"name":"Diphlu River Lodge","type":"Eco-lodge","price_per_night":14000,"highlights":["Riverside jungle setting","Exclusive safaris","Expert naturalist guides"],"rating":4.8}], "itinerary": {"3_day": [{"day":1,"title":"Elephant Safari","morning":"Elephant-back safari at dawn — get close to rhinos in tall grass","afternoon":"Kohora Range jeep safari","evening":"Wildlife evening lecture at resort"},{"day":2,"title":"Jeep Safaris","morning":"Bagori Range safari — best for tiger sightings","afternoon":"Agoratoli Range — water buffalo herds and swamp deer","evening":"Tea estate visit near park boundary"},{"day":3,"title":"Bird Walk & Departure","morning":"Kaziranga bird walk — 480 species including Greater Adjutant Stork","afternoon":"Orchid Park → departure","evening":""}]}, "tips": ["Book safaris ONLINE before arriving — elephant safaris especially sell out","October to April is best — park is closed June-October (monsoon floods)","Layer up for early morning safaris — very cold on the elephant","Carry binoculars — rhinos look small from the elephant distance"], "nearby": ["Majuli Island (100km)","Jorhat (97km)","Shillong (280km)"], "weather": [{"month":"Nov","temp_high":26,"temp_low":12,"description":"Best — park fully open","emoji":"☀️"},{"month":"Feb","temp_high":25,"temp_low":10,"description":"Excellent — dry and clear","emoji":"☀️"},{"month":"Jun","temp_high":29,"temp_low":23,"description":"Monsoon — park CLOSED","emoji":"🌧️"}]},
  "Spiti Valley": {"overview": {"tagline": "Middle land between India and Tibet — cold desert magic", "best_for": ["Adventure Seekers","Photographers","Motorcyclists"], "avg_trip_days": 6, "budget_per_day": {"budget":1500,"mid":3500,"luxury":7000}, "language":"Spitian, Hindi, English", "currency":"INR", "timezone":"IST"}, "food": [{"name":"Thukpa","type":"Main","description":"Tibetan noodle soup essential for cold nights at 4000m","emoji":"🍜","must_try":True},{"name":"Tsampa","type":"Breakfast","description":"Roasted barley with butter tea — nomad breakfast","emoji":"🌾","must_try":True},{"name":"Sea Buckthorn Juice","type":"Drink","description":"Bright orange superfruit juice native to Spiti — medicinal and delicious","emoji":"🧃","must_try":True}], "restaurants": [{"name":"Sakya Abode Café","cuisine":"Tibetan","price_range":"₹₹","specialty":"Butter tea and Thukpa","area":"Kaza","rating":4.3},{"name":"Himalayan Café","cuisine":"Indian/Continental","price_range":"₹₹","specialty":"Only wood-fire pizza in Spiti","area":"Kaza","rating":4.2}], "accommodation": [{"name":"Kaza Camp","type":"Luxury Camp","price_per_night":8000,"highlights":["Heated Swiss tents","Stargazing deck","Himalayan views"],"rating":4.6},{"name":"Spiti Ecosphere Homestay","type":"Homestay","price_per_night":1200,"highlights":["Local family","Traditional Spitian food","Community tourism"],"rating":4.5}], "itinerary": {"3_day": [{"day":1,"title":"Kaza Base","morning":"Key Monastery sunrise — 1000-year-old clifftop monastery","afternoon":"Kibber (4205m) — world's highest village with motorable road","evening":"Stargazing — Milky Way visible"},{"day":2,"title":"Fossil Hunting","morning":"Langza village — Tibetan Buddhist carvings and marine fossils at 4400m","afternoon":"Hikkim — world's highest post office (send a postcard!)","evening":"Komic village — world's highest motorable village"},{"day":3,"title":"Chandratal","morning":"Chandratal Lake (4300m) — half-moon shaped glacial lake","afternoon":"Trekking around Chandratal shores","evening":"Camp at Chandratal for unforgettable sunset"}]}, "tips": ["Inner Line Permit required for Sangla and Chitkul (₹100, get at Karcham)","No ATMs beyond Kaza — carry sufficient cash from Shimla","Spiti is only accessible May-October. All other months it is completely cut off","Acclimatise at Kaza (3800m) for a full day before going higher"], "nearby": ["Lahaul (via Kunzum Pass)","Pin Valley NP","Manali (7hrs)"], "weather": [{"month":"Jun","temp_high":22,"temp_low":5,"description":"Season opens — snow still on peaks","emoji":"🌤️"},{"month":"Aug","temp_high":25,"temp_low":8,"description":"Best — all roads open, wildflowers","emoji":"☀️"},{"month":"Oct","temp_high":12,"temp_low":-2,"description":"Season closing — first winter snow","emoji":"🌨️"}]},
  "Andaman Islands": {"overview": {"tagline": "India's tropical island paradise with Asia's best beaches", "best_for": ["Divers","Couples","Beach Lovers"], "avg_trip_days": 6, "budget_per_day": {"budget":2500,"mid":6000,"luxury":15000}, "language":"Hindi, Bengali, Tamil, English", "currency":"INR", "timezone":"IST+30min (IST+5:30)"}, "food": [{"name":"Grilled Barracuda","type":"Main","description":"Fresh barracuda from Andaman waters, grilled with lemon and herbs — astonishingly fresh","emoji":"🐟","must_try":True},{"name":"Coconut Prawn Curry","type":"Main","description":"Island prawns in coconut and red chili gravy — fresh from morning catch","emoji":"🦐","must_try":True},{"name":"Fresh Tender Coconut","type":"Drink","description":"The most refreshing drink on earth after snorkelling on coral reefs","emoji":"🥥","must_try":True}], "restaurants": [{"name":"Full Moon Café","cuisine":"Seafood","price_range":"₹₹₹","specialty":"Grilled fish platter with 5 island fish varieties","area":"Havelock","rating":4.5},{"name":"Anju Coco Restaurant","cuisine":"Indian/Seafood","price_range":"₹₹","specialty":"Lobster and prawn tawa fry","area":"Port Blair","rating":4.3}], "accommodation": [{"name":"Barefoot at Havelock","type":"Eco-Resort","price_per_night":12000,"highlights":["Jungle cottages 100m from Radhanagar","Private beach","Diving center"],"rating":4.7},{"name":"Symphony Palms Beach Resort","type":"Resort","price_per_night":8000,"highlights":["Beachfront","Pool","Water sports"],"rating":4.5}], "itinerary": {"3_day": [{"day":1,"title":"Port Blair & Cellular Jail","morning":"Cellular Jail — India's dark Andaman prison, emotional light & sound show","afternoon":"Ross Island (British ruins) → Viper Island ferry","evening":"Aberdeen Bazaar seafood dinner"},{"day":2,"title":"Havelock — Best Beach","morning":"Ferry to Havelock (90 mins). Radhanagar Beach — Asia's best beach","afternoon":"Elephant Beach snorkelling (coral reefs)","evening":"Night bioluminescence kayaking (seasonal)"},{"day":3,"title":"Neil Island","morning":"Neil Island ferry. Bharatpur Beach snorkel","afternoon":"Natural Bridge formation (rock arch in sea)","evening":"Ferry back to Port Blair. Departure"}]}, "tips": ["Book ferries and inter-island transport WELL in advance — they fill up","Radhanagar Beach (Beach No. 7, Havelock): go at sunset — genuinely one of Asia's most beautiful beaches","Scuba diving: PADI open water course in Havelock (₹25,000) — visibility is 30m+","Inner Line Permit required — issued free at Port Blair airport"], "nearby": ["Neil Island (35km)","Havelock (57km)","Baratang (100km)"], "weather": [{"month":"Jan","temp_high":30,"temp_low":23,"description":"Best — calm seas, clear visibility","emoji":"☀️"},{"month":"Mar","temp_high":31,"temp_low":24,"description":"Excellent — dive season peak","emoji":"☀️"},{"month":"Jun","temp_high":29,"temp_low":24,"description":"SW Monsoon — seas rough, avoid","emoji":"⛈️"}]},
  "Kovalam Beach": {"overview": {"tagline": "Kerala's crescent beaches framed by red laterite cliffs", "best_for": ["Couples","Wellness Seekers","Solo Travellers"], "avg_trip_days": 4, "budget_per_day": {"budget":1500,"mid":4000,"luxury":12000}, "language":"Malayalam, English", "currency":"INR", "timezone":"IST"}, "food": [{"name":"Seer Fish Masala","type":"Main","description":"King of Kerala fish — neymeen in spiced red coconut masala. Unforgettable","emoji":"🐟","must_try":True},{"name":"Prawn Moilee","type":"Main","description":"Delicate white coconut milk prawn curry — Kovalam's signature","emoji":"🦐","must_try":True},{"name":"Fresh Coconut Toddy","type":"Drink","description":"Fermented coconut flower sap — natural, slightly effervescent (legal in Kerala!)","emoji":"🥥","must_try":False}], "restaurants": [{"name":"Rockholm Restaurant","cuisine":"Kerala Seafood","price_range":"₹₹₹","specialty":"Rooftop dining over Lighthouse Beach with fresh catch","area":"Lighthouse Beach","rating":4.5},{"name":"Malabar Café","cuisine":"Kerala","price_range":"₹₹","specialty":"Kerala Sadya and seafood on beach","area":"Hawah Beach","rating":4.3}], "accommodation": [{"name":"Niraamaya Surya Samudra","type":"Luxury","price_per_night":22000,"highlights":["Cliffside infinity pool","Traditional Kerala cottages","Ayurvedic center"],"rating":4.8},{"name":"Wilson's Tourist Home","type":"Budget","price_per_night":800,"highlights":["Walking distance to beach","Clean rooms","Helpful owners"],"rating":4.0}], "itinerary": {"3_day": [{"day":1,"title":"Beaches & Lighthouse","morning":"Lighthouse Beach walk → climb the 30m red lighthouse for panoramic view","afternoon":"Hawah Beach → Samudra Beach (quieter, more local)","evening":"Seafood dinner at Rockholm with sea view"},{"day":2,"title":"Ayurveda & Temple","morning":"Ayurvedic Panchakarma treatment — 2-3 hours full body therapy","afternoon":"Padmanabhapuram Palace (1hr, 55km) — Kerala's finest wooden palace","evening":"Kanyakumari sunset (India's southernmost tip — 90 mins)"},{"day":3,"title":"Water Activities","morning":"Snorkelling at Vizhinjam harbour reef","afternoon":"Poovar backwaters boat tour through mangroves","evening":"Farewell seafood feast"}]}, "tips": ["Lighthouse Beach gets crowded — walk 10 mins south for peaceful Samudra Beach","Monsoon (June-September): sea is rough, swimming not allowed — red flags are serious","Ayurvedic centres are cheaper and more authentic here than in Kochi or Munnar","Vizhinjam fishing harbour (2km walk) at 5am — watch fishermen bring the night's catch"], "nearby": ["Trivandrum (14km)","Kanyakumari (75km)","Varkala (51km)"], "weather": [{"month":"Jan","temp_high":31,"temp_low":22,"description":"Perfect — peak season","emoji":"☀️"},{"month":"Mar","temp_high":33,"temp_low":25,"description":"Warm — good beach weather","emoji":"☀️"},{"month":"Jun","temp_high":28,"temp_low":23,"description":"Monsoon — stay away","emoji":"🌧️"}]},
  "Radhanagar Beach": {"overview": {"tagline": "Ranked Asia's best beach — raw, pristine and magical", "best_for": ["Beach Lovers","Couples","Divers"], "avg_trip_days": 3, "budget_per_day": {"budget":2500,"mid":6000,"luxury":14000}, "language":"Hindi, Bengali, English", "currency":"INR", "timezone":"IST"}, "food": [{"name":"Seafood Barbecue","type":"Main","description":"Fresh catch from morning — grilled on beach shacks at Havelock","emoji":"🍢","must_try":True},{"name":"Coconut Rice & Fish Curry","type":"Main","description":"Andaman island comfort food — simple and fresh","emoji":"🍚","must_try":True}], "restaurants": [{"name":"Emerald Gecko","cuisine":"International","price_range":"₹₹₹","specialty":"Pasta, pizza and fresh seafood — consistently excellent","area":"Havelock","rating":4.5},{"name":"Red Snapper","cuisine":"Seafood","price_range":"₹₹₹","specialty":"Grilled red snapper and lobster thermidor","area":"Havelock","rating":4.4}], "accommodation": [{"name":"Barefoot at Havelock","type":"Eco-Resort","price_per_night":13000,"highlights":["Steps from Radhanagar","Jungle setting","Dive centre"],"rating":4.8},{"name":"Havelock Island Beach Resort","type":"Resort","price_per_night":7000,"highlights":["Beach access","Watersports","Restaurant"],"rating":4.4}], "itinerary": {"3_day": [{"day":1,"title":"Radhanagar Arrival","morning":"Arrive Havelock by ferry from Port Blair (90 mins)","afternoon":"Radhanagar Beach (Beach 7) — 3km white sand, sunset is otherworldly","evening":"Bioluminescent plankton kayaking (if available)"},{"day":2,"title":"Snorkel & Dive","morning":"Elephant Beach snorkel (30-min boat) — massive coral gardens and fish","afternoon":"PADI Discover Scuba Diving (₹3500 for first-timers)","evening":"Beach bonfire and seafood BBQ"},{"day":3,"title":"Neil Island","morning":"Ferry to Neil Island. Bharatpur coral snorkel","afternoon":"Natural Bridge arch rock formation","evening":"Ferry back. Night ferry to Port Blair"}]}, "tips": ["Radhanagar Beach: no food/drink vendors on the beach — carry water","Take the 5:30pm ferry from Port Blair to watch sunset from the ship","Glass-bottom boat for non-swimmers — see coral without diving","Book Barefoot Resort 3+ months in advance for peak season"], "nearby": ["Neil Island (35km ferry)","Port Blair (90 min ferry)","Elephant Beach (20 min boat)"], "weather": [{"month":"Jan","temp_high":30,"temp_low":23,"description":"Peak season — calm, clear seas","emoji":"☀️"},{"month":"Apr","temp_high":31,"temp_low":24,"description":"Last good month before monsoon","emoji":"☀️"},{"month":"Jul","temp_high":29,"temp_low":24,"description":"Monsoon — avoid (rough seas)","emoji":"⛈️"}]},
  "Varanasi": {"overview": {"tagline": "The oldest living city — where life and death dance on the Ganges", "best_for": ["Spiritual Travellers","Photographers","Solo Travellers","Philosophers"], "avg_trip_days": 3, "budget_per_day": {"budget":800,"mid":2500,"luxury":7000}, "language":"Hindi, Bhojpuri, English", "currency":"INR", "timezone":"IST"}, "food": [{"name":"Banarasi Paan","type":"Experience","description":"Sweet betel leaf stuffed with rose petals, fennel, gulkand — the Varanasi goodbye ritual","emoji":"🌿","must_try":True},{"name":"Tamatar Chaat","type":"Street Food","description":"Varanasi's unique tomato-based chaat — spicy, tangy and utterly addictive","emoji":"🍅","must_try":True},{"name":"Malaiyo","type":"Dessert","description":"Winter-only airy milk mousse whipped with dew water — vanishes on the tongue. Winter only (Oct-Feb)","emoji":"🍮","must_try":True},{"name":"Lassi (Blue Lassi)","type":"Drink","description":"Famous by-the-Ganges lassi shop — topped with seasonal fruit. Queue for it","emoji":"🥛","must_try":True},{"name":"Kachori Sabzi","type":"Breakfast","description":"Deep-fried kachoris with potato curry — the Varanasi street breakfast","emoji":"🥐","must_try":True}], "restaurants": [{"name":"Assi Ghat Restaurants","cuisine":"Indian Vegetarian","price_range":"₹₹","specialty":"Ganga-view thali and lassi at sunset","area":"Assi Ghat","rating":4.3},{"name":"Harmony Restaurant","cuisine":"Indian/Continental","price_range":"₹₹","specialty":"German Bakery meets Indian — backpacker paradise","area":"Godaulia","rating":4.2},{"name":"Varuna Restaurant","cuisine":"North Indian","price_range":"₹₹₹","specialty":"Banarasi cuisine — mungodi, chena dalna and tamatar chaat","area":"Cantonment","rating":4.4}], "accommodation": [{"name":"Brijrama Palace","type":"Heritage Palace","price_per_night":18000,"highlights":["250-year-old Ghat-facing palace","Balcony over Ganges","Boat included"],"rating":4.8},{"name":"Hotel Ganges View","type":"Heritage","price_per_night":4500,"highlights":["Ghat-front location","Terrace view","Home-cooked meals"],"rating":4.5},{"name":"Stops Hostel","type":"Hostel","price_per_night":500,"highlights":["Best backpacker hostel","Walking tours","Rooftop Ganges view"],"rating":4.4}], "itinerary": {"3_day": [{"day":1,"title":"The Ghats — Dawn to Dusk","morning":"Boat ride at DAWN (5am) — Ganga Aarti at Dashashwamedh ends at 6am. Watch from water","afternoon":"Manikarnika Ghat (cremation ghat) — life, death and fire. Silent observation only","evening":"Dashashwamedh Ghat evening Ganga Aarti — 7 priests, fire lamps, incense — overwhelming"},{"day":2,"title":"Sarnath — Buddha's First Sermon","morning":"Sarnath (12km) — where Buddha gave his first sermon after Enlightenment. Dhamek Stupa","afternoon":"Sarnath Museum — finest Buddhist sculptures in India","evening":"Old city walk — silk weaving workshops, Kashi Vishwanath Temple area"},{"day":3,"title":"Morning Rituals & Departure","morning":"Pre-dawn boat ride again — different every time. Sunrise is life-changing","afternoon":"Sankat Mochan Temple → Tulsi Manas Temple","evening":"Blue Lassi. Banarasi Paan ritual. Departure"}]}, "tips": ["ALWAYS take the pre-dawn boat (4:30-6am) — the Aarti, the mist, the life — it'll change you","Do NOT photograph at Manikarnika cremation ghat — deeply disrespectful","Hire a local guide for old city — the lanes are a labyrinth and stories are extraordinary","Avoid loud, insensitive behaviour at ghats — people are bathing, praying, and grieving"], "nearby": ["Sarnath (12km)","Allahabad/Prayagraj (120km)","Bodh Gaya (250km)"], "weather": [{"month":"Jan","temp_high":20,"temp_low":7,"description":"Excellent — Kumbh Mela (periodical). Very cold nights","emoji":"🌤️"},{"month":"Oct","temp_high":30,"temp_low":19,"description":"Best — Diwali on Ganga is spectacular","emoji":"🪔"},{"month":"Jul","temp_high":31,"temp_low":24,"description":"Monsoon — Ganga floods beautifully","emoji":"🌧️"}]},
  "Mysore": {"overview": {"tagline": "City of palaces, incense, and royal Dasara grandeur", "best_for": ["Families","History Buffs","Shoppers","Culture Lovers"], "avg_trip_days": 2, "budget_per_day": {"budget":1000,"mid":2800,"luxury":7000}, "language":"Kannada, English", "currency":"INR", "timezone":"IST"}, "food": [{"name":"Mysore Pak","type":"Sweet","description":"Gram flour, ghee, and sugar cooked to create crumbly melt-in-mouth blocks — invented in Mysore Palace","emoji":"🍬","must_try":True},{"name":"Mysore Masala Dosa","type":"Breakfast","description":"The original — crispy dosa with red chutney inside, potato filling, served at MTR or Hotel Dasaprakash","emoji":"🥞","must_try":True},{"name":"Obbattu/Holige","type":"Sweet","description":"Sweet flatbread stuffed with jaggery and coconut — Karnataka's Diwali sweet","emoji":"🫓","must_try":True}], "restaurants": [{"name":"Hotel Mylari","cuisine":"South Indian","price_range":"₹","specialty":"Mysore Masala Dosa — the original. Queue at 7am or miss out","area":"Nazarbad","rating":4.7},{"name":"Lalitha Mahal Palace Hotel","cuisine":"Fine Dining","price_range":"₹₹₹₹","specialty":"Royal Karnataka Thali in a stunning palace","area":"Lalitha Mahal","rating":4.7}], "accommodation": [{"name":"Mysore Royal Heritage","type":"Heritage","price_per_night":6000,"highlights":["Heritage home","Palace-style architecture","Garden"],"rating":4.5},{"name":"Radisson Blu Mysore","type":"Hotel","price_per_night":5500,"highlights":["Pool","City views","Modern amenities"],"rating":4.4}], "itinerary": {"3_day": [{"day":1,"title":"Mysore Palace","morning":"Mysore Palace interior (10 darbar halls) — arrive at 10am before crowds","afternoon":"Chamundeshwari Temple on Chamundi Hill (1000 steps or drive up)","evening":"Palace sound & light show at 7pm — 97,000 bulbs illuminate the palace"},{"day":2,"title":"Gardens & Zoo","morning":"Brindavan Gardens (16km) — evening visit for musical fountain show — go at 6:30pm","afternoon":"Mysore Zoo — one of India's finest. White tigers!","evening":"Devaraja Market — Mysore jasmine garlands, sandalwood and silk"},{"day":3,"title":"Ranganathittu & Somnathpur","morning":"Ranganathittu Bird Sanctuary boat ride — 200+ species, crocodiles","afternoon":"Somnathpur Hoysala Temple (35km) — intricate 13th century sculpture","evening":"Mysore Pak and silk shopping at Cauvery Emporium"}]}, "tips": ["Dasara festival (October) — Mysore is the Dasara capital of India. Elephant procession, palace lit with 1 lakh bulbs — book hotels 6 months ahead","Mysore silk: buy at government Cauvery Emporium for fixed prices and authenticity","Hotel Mylari dosas (Nazarbad) — queue starts at 7am, runs out by 10am"], "nearby": ["Ooty (140km)","Coorg (120km)","Bandipur NP (80km)"], "weather": [{"month":"Oct","temp_high":29,"temp_low":19,"description":"Dasara season — best month","emoji":"🎭"},{"month":"Jan","temp_high":27,"temp_low":14,"description":"Excellent — clear and cool","emoji":"☀️"},{"month":"Aug","temp_high":26,"temp_low":19,"description":"Moderate monsoon","emoji":"🌧️"}]},
  "Kolkata": {"overview": {"tagline": "India's cultural soul — poetry, food, football and revolution", "best_for": ["Food Lovers","Culture Seekers","Solo Travellers","Art Lovers"], "avg_trip_days": 3, "budget_per_day": {"budget":800,"mid":2500,"luxury":7000}, "language":"Bengali, Hindi, English", "currency":"INR", "timezone":"IST"}, "food": [{"name":"Kathi Roll","type":"Street Food","description":"Kolkata's invention — paratha rolled around egg and meat filling with onions and chutney. Life-changing street food","emoji":"🌯","must_try":True},{"name":"Mishti Doi","type":"Dessert","description":"Sweetened yogurt set in earthen pots — a Bengal obsession. Try at KC Das or Balaram Mullick","emoji":"🍮","must_try":True},{"name":"Kosha Mangsho","type":"Main","description":"Slow-cooked spiced mutton — deeply caramelised. Sunday ritual in every Bengali household","emoji":"🍖","must_try":True},{"name":"Phuchka","type":"Street Food","description":"Kolkata's version of Pani Puri — with tamarind water and spiced mashed potato. Better than anywhere else","emoji":"🫙","must_try":True},{"name":"Rosogolla","type":"Sweet","description":"The great sweet — spongy paneer balls in sugar syrup. Invented here in 1868 at Nobin Chandra Das","emoji":"🍡","must_try":True}], "restaurants": [{"name":"Peter Cat","cuisine":"Continental/Indian","price_range":"₹₹₹","specialty":"Chelo Kebab — Kolkata's iconic dish since 1975","area":"Park Street","rating":4.5},{"name":"6 Ballygunge Place","cuisine":"Bengali Fine Dining","price_range":"₹₹₹","specialty":"Authentic Bengali Thali — Maacher Jhol, Kosha Mangsho","area":"Ballygunge","rating":4.6},{"name":"Flurys","cuisine":"Continental/Bakery","price_range":"₹₹₹","specialty":"Iconic 1927 tearoom on Park Street — patisseries and English breakfast","area":"Park Street","rating":4.4}], "accommodation": [{"name":"Zostel Kolkata","type":"Hostel","price_per_night":500,"highlights":["Central location","Heritage building","Social events"],"rating":4.3},{"name":"The Oberoi Grand","type":"Luxury","price_per_night":18000,"highlights":["Heritage 1880s grand hotel","Pool","Landmark on Chowringhee"],"rating":4.8}], "itinerary": {"3_day": [{"day":1,"title":"Colonial Grandeur","morning":"Victoria Memorial at 9am → Princep Ghat walk along Hooghly","afternoon":"Howrah Bridge walk → Mullick Ghat flower market (5am best)","evening":"Park Street — Flurys tea → Peter Cat dinner"},{"day":2,"title":"Cultural Deep Dive","morning":"Kumartuli — watch artisans sculpt Durga idols from clay","afternoon":"College Street book market → Indian Coffee House (legendary adda since 1942)","evening":"Kalighat Kali Temple → Dakshineswar across river by ferry"},{"day":3,"title":"Food Trail & Departure","morning":"Phuchka at Vivekananda Park → Kathi Roll at Nizam's (original since 1932)","afternoon":"New Market for handicrafts → Sweets at KC Das (Rosogolla inventors)","evening":"Farewell mustard fish curry at 6 Ballygunge Place"}]}, "tips": ["Durga Puja (October) — 4-day festival transforms entire city into open-air art gallery. THE time to visit","Try tram rides — Kolkata is the only city with functional trams. ₹7 for full city view","Eat where Bengalis eat — follow locals to find the real food","Yellow Ambassador taxis are iconic — take at least one ride"], "nearby": ["Sundarbans (100km)","Bishnupur (150km)","Darjeeling (650km overnight)"], "weather": [{"month":"Oct","temp_high":30,"temp_low":22,"description":"Durga Puja — best month to visit","emoji":"🎭"},{"month":"Jan","temp_high":24,"temp_low":13,"description":"Excellent — cool and dry","emoji":"☀️"},{"month":"Jul","temp_high":32,"temp_low":26,"description":"Monsoon — humidity extreme","emoji":"🌧️"}]}
}

# Merge all
ALL_INTELLIGENCE = {**INTELLIGENCE, **REMAINING}

# Save to JSON
with open(OUT / "destination_intelligence.json", "w", encoding="utf-8") as f:
    json.dump(ALL_INTELLIGENCE, f, indent=2, ensure_ascii=False)

print(f"✅ Destination intelligence created for {len(ALL_INTELLIGENCE)} destinations")
for name in ALL_INTELLIGENCE:
    d = ALL_INTELLIGENCE[name]
    print(f"   {name}: {len(d.get('food',[]))} foods, {len(d.get('restaurants',[]))} restaurants, "
          f"{len(d.get('accommodation',[]))} stay options, {len(d.get('weather',[]))} months, "
          f"{len(d.get('itinerary',{}).get('3_day',[]))}+{len(d.get('itinerary',{}).get('5_day',[]))} day plans")
