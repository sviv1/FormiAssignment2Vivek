# app.py
from flask import Flask, request, jsonify
from utils import get_corrected_location, geocode_location, get_nearby_properties

app = Flask(__name__)

@app.route('/nearest-properties', methods=['GET'])
def nearest_properties():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Query parameter is required."}), 400

    # STEP 1: Try direct geocoding
    coords = geocode_location(query)

    # STEP 2: If geocoding fails, try fuzzy matching
    corrected = None
    if not coords:
        corrected = get_corrected_location(query)
        if corrected:
            coords = geocode_location(corrected)

    if not coords:
        return jsonify({"error": "Could not geocode the location."}), 404

    lat, lon = coords
    nearby_props = get_nearby_properties(lat, lon)

    return jsonify({
        "query": query,
        "corrected_location": corrected or query,
        "coordinates": {"latitude": lat, "longitude": lon},
        "nearby_properties": nearby_props
    })


if __name__ == '__main__':
    app.run(debug=True)
