# utils.py
import json
from geopy.geocoders import Nominatim
from rapidfuzz import process, fuzz
from math import radians, sin, cos, sqrt, atan2

# Load property data from file (replace with your actual file if needed)
with open('data.json') as f:
    PROPERTIES = json.load(f)

# Extract locations for fuzzy match (e.g., city or area names)
ALL_LOCATIONS = list(set([prop["name"].split()[-1] for prop in PROPERTIES]))



def get_corrected_location(query):
    match, score, _ = process.extractOne(query, ALL_LOCATIONS, scorer=fuzz.token_sort_ratio)
    return match



def geocode_location(location):
    geolocator = Nominatim(user_agent="moustache-api")
    try:
        location = geolocator.geocode(location, timeout=5)
        if location:
            return (location.latitude, location.longitude)
    except Exception as e:
        print("Geocoding failed:", e)
    return None


def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth radius in kilometers
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


def get_nearby_properties(query_lat, query_lon, radius_km=50):
    results = []
    for prop in PROPERTIES:
        dist = haversine(query_lat, query_lon, prop["latitude"], prop["longitude"])
        if dist <= radius_km or dist == 0:
            results.append({
                "property": prop["name"],
                "latitude": prop["latitude"],
                "longitude": prop["longitude"],
                "distance_km": round(dist, 2)
            })
    return sorted(results, key=lambda x: x["distance_km"])
