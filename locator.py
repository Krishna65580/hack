"""
Nearby healthcare resource locator.

For the hackathon demo this uses a small static dataset so the feature
works reliably offline/on stage. In a production build, replace
`search_facilities()` with a real Google Places / OpenStreetMap Overpass
API call keyed on the user's live coordinates - the function signature
is already designed to be a drop-in swap.
"""

FACILITIES = [
    {"name": "Government Primary Health Center, Tekkali", "type": "PHC",
     "distance_km": 1.2, "phone": "08947-232244",
     "services": "General OPD, Maternal care, Immunization"},
    {"name": "AITAM Community Health Camp", "type": "Camp/Clinic",
     "distance_km": 0.5, "phone": "08947-232345",
     "services": "General checkups, First aid"},
    {"name": "Srikakulam Government General Hospital", "type": "Hospital",
     "distance_km": 28.0, "phone": "08942-240333",
     "services": "Emergency, Surgery, Specialist care, Maternity"},
    {"name": "Area Hospital, Palasa", "type": "Hospital",
     "distance_km": 22.0, "phone": "08945-244233",
     "services": "General medicine, Pediatrics, Emergency"},
    {"name": "Rural Health Sub-Center, Naupada", "type": "Sub-Center",
     "distance_km": 6.4, "phone": "08947-235100",
     "services": "Immunization, Basic maternal care"},
]


def search_facilities(query: str = "", max_results: int = 5):
    """
    Return facilities sorted by distance. `query` can filter by
    type/service keyword (case-insensitive substring match); empty
    query returns all, nearest first.
    """
    results = FACILITIES
    if query.strip():
        q = query.lower()
        results = [
            f for f in FACILITIES
            if q in f["name"].lower() or q in f["type"].lower() or q in f["services"].lower()
        ]
        if not results:
            results = FACILITIES  # graceful fallback: show everything nearby
    return sorted(results, key=lambda f: f["distance_km"])[:max_results]
