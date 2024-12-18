import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Replace with your Google Maps API key
GOOGLE_MAPS_API_KEY = "AIzaSyB33V6scRrJ6yK36qt-XD_DgshA_CHPZ6U"

@app.route('/api/geocode', methods=['POST'])
def geocode_address():
    data = request.json
    address = data.get('address')

    if not address:
        return jsonify({"error": "Address is required"}), 400

    # Make a request to the Geocoding API
    url = f"https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": GOOGLE_MAPS_API_KEY
    }
    response = requests.get(url, params=params)
    geocode_data = response.json()

    if geocode_data['status'] == 'OK':
        # Extract the first result
        location = geocode_data['results'][0]['geometry']['location']
        return jsonify({
            "lat": location['lat'],
            "lng": location['lng']
        })
    else:
        return jsonify({"error": geocode_data['status']}), 400

if __name__ == '__main__':
    app.run(debug=True)
