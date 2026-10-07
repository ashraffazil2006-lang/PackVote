import urllib.request, json

payload = json.dumps({
    'travelers': [
        {'preferences': ['Beach', 'Historical']},
        {'preferences': ['Nature', 'Adventure']},
        {'preferences': ['City', 'Historical']},
        {'preferences': ['Nature', 'Adventure']}
    ],
    'budget_per_person': 5000,
    'accommodation_type': 'Hotel',
    'top_n': 5
}).encode()

req = urllib.request.Request(
    'http://localhost:8000/api/recommend',
    data=payload,
    headers={'Content-Type': 'application/json'},
    method='POST'
)

with urllib.request.urlopen(req) as r:
    resp = json.loads(r.read())

travelers = resp['total_travelers']
budget    = resp['budget_per_person']
accom     = resp['accommodation_type']
print(f"PACKVOTE RESULTS — {travelers} Travelers | Budget Rs.{budget}/night | {accom}")
print("=" * 65)
for rec in resp['recommendations']:
    cost = rec['predicted_accommodation_cost']
    cost_str = "Rs.{:,.0f}".format(cost) if cost else "N/A"
    rank   = rec['rank']
    dest   = rec['destination']
    state  = rec['state']
    dtype  = rec['destination_type']
    compat = rec['group_compatibility']
    pmatch = rec['group_preference_match']
    suit   = rec['suitability']
    exp    = rec['predicted_experience']
    rating = rec['average_rating']
    bstatus = rec['budget_status']
    btime  = rec['best_time']
    spots  = [s['name'] for s in rec['tourist_spots'][:3]]
    print(f"#{rank}  {dest} ({state}) [{dtype}]")
    print(f"    Compatibility   : {compat:.1f}/100")
    print(f"    Pref Match      : {pmatch:.1f}% | Suitability: {suit:.1f}%")
    print(f"    Experience      : {exp:.2f}/5 | Rating: {rating:.2f}/5")
    print(f"    Budget          : {bstatus} ({cost_str})")
    print(f"    Best Time       : {btime}")
    if spots:
        print(f"    Attractions     : {spots}")
    print()

print("ALL SYSTEMS OPERATIONAL")
