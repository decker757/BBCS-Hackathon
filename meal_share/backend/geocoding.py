import requests
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Replace with your Google Maps API key
GOOGLE_MAPS_API_KEY = "AIzaSyB33V6scRrJ6yK36qt-XD_DgshA_CHPZ6U"

# Path to the business.txt file
BUSINESS_FILE_PATH = "users/business.txt"

def geocode_address(address):
    """Geocode the address using Google Maps Geocoding API."""
    url = f"https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": address, "key": GOOGLE_MAPS_API_KEY}
    response = requests.get(url, params=params)
    geocode_data = response.json()

    if geocode_data["status"] == "OK":
        location = geocode_data["results"][0]["geometry"]["location"]
        return {"lat": location["lat"], "lng": location["lng"]}
    return None


@app.route('/api/locations', methods=['GET'])
def get_locations():
    """Read business.txt, extract addresses, and geocode them."""
    locations = []
    try:
        # Read and parse the business.txt file
        with open(BUSINESS_FILE_PATH, "r") as file:
            business_data = json.load(file)
        
        # Extract the address and geocode it
        address = business_data.get("address")
        if not address:
            return jsonify({"error": "No address found in the file"}), 400

        coords = geocode_address(address)
        if coords:
            locations.append({
                "title": f"{business_data.get('firstname', '')} {business_data.get('lastname', '')}",
                "address1": address,
                "address2": f"Postal Code: {business_data.get('postal', '')}",
                "coords": coords,
            })

        return jsonify(locations)

    except FileNotFoundError:
        return jsonify({"error": "business.txt not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Error decoding business.txt"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/geocode', methods=['POST'])
def geocode_address_api():
    """Geocode an address provided in the request."""
    data = request.json
    address = data.get("address")

    if not address:
        return jsonify({"error": "Address is required"}), 400

    coords = geocode_address(address)
    if coords:
        return jsonify(coords)
    else:
        return jsonify({"error": "Unable to fetch coordinates"}), 400


if __name__ == '__main__':
    app.run(debug=True)
