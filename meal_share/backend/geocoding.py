import requests
import json
import os
from flask import Flask, jsonify

app = Flask(__name__)

# Google Maps API Key
GOOGLE_MAPS_API_KEY = "AIzaSyB33V6scRrJ6yK36qt-XD_DgshA_CHPZ6U"

# Path to business.txt
BUSINESS_FILE_PATH = "users/business.txt"


def geocode_address(address):
    """Geocode the address using Google Maps Geocoding API."""
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": address, "key": GOOGLE_MAPS_API_KEY}
    response = requests.get(url, params=params)
    geocode_data = response.json()

    if geocode_data["status"] == "OK":
        location = geocode_data["results"][0]["geometry"]["location"]
        return {"lat": location["lat"], "lng": location["lng"]}
    return None


@app.route('/api/locations', methods=['GET'])
def get_locations():
    """Read business.txt, geocode addresses, and return a list of locations."""
    try:
        # Check if the file exists
        if not os.path.exists(BUSINESS_FILE_PATH):
            return jsonify({"error": "business.txt not found"}), 404
        # Read the business.txt file
        with open(BUSINESS_FILE_PATH, "r") as file:
            # business_data = json.load(file)
            all_business_data = [json.loads(line) for line in file] # list of dictionaries

        all_correct_business_data = []
        for business_data in all_business_data:
            # Extract address and postal code
            address = business_data.get("address", "")
            postal_code = business_data.get("postal", "")

            if not address or not postal_code:
                return jsonify({"error": "Address or postal code missing"}), 400

            # Combine address and postal code
            full_address = f"{address}, {postal_code}"

            # Geocode the address
            coords = geocode_address(full_address)
            if coords:
                all_correct_business_data.append({
                    "title": f"{business_data.get('firstname', '')} {business_data.get('lastname', '')}",
                    "address1": address,
                    "address2": f"Postal Code: {postal_code}",
                    "coords": coords,
                })
            else:
                return jsonify({"error": "Error geocoding address}"}), 500
        if all_correct_business_data:
            return jsonify(all_correct_business_data)
        else:
            return jsonify({"error": "No locations found"}), 404
        

    except json.JSONDecodeError:
        return jsonify({"error": "Error parsing business.txt"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

# AHHHH
