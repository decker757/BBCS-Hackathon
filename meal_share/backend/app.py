# backend/app.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json
import requests
import json
import os
from flask import Flask, jsonify, request

app = Flask(__name__)
CORS(app)

GOOGLE_MAPS_API_KEY = "AIzaSyB33V6scRrJ6yK36qt-XD_DgshA_CHPZ6U"
BUSINESS_FILE_PATH = "users/business.txt"
DRIVER_FILE_PATH = 'users/drivers.txt'
DATA_DIR = 'meals'

# Utility functions for file-based user and meal management
def read_file(filepath):
    """Read contents of a text file."""
    try:
        with open(filepath, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def write_file(filepath, content):
    """Write content to a text file."""
    with open(filepath, 'w') as f:
        f.write(content)

def append_file(filepath, content):
    """Append content to a text file."""
    with open(filepath, 'a') as f:
        f.write(content + '\n')


def is_username_taken(username, file_path):
    """Check if the username already exists in the file."""
    if not os.path.exists(file_path):
        return False  # File doesn't exist, so no duplicates yet

    with open(file_path, 'r') as file:
        for line in file:
            user = json.loads(line.strip())
            if user.get('username') == username:
                return True  # Username found
    return False

def is_email_taken(email, file_path):
    """Check if the email already exists in the file."""
    if not os.path.exists(file_path):
        return False  # File doesn't exist, so no duplicates yet

    with open(file_path, 'r') as file:
        for line in file:
            user = json.loads(line.strip())
            if user.get('email') == email:
                return True  # email found
    return False


def is_businessemail_taken(businessemail, file_path):
    """Check if the username already exists in the file."""
    if not os.path.exists(file_path):
        return False  # File doesn't exist, so no duplicates yet

    with open(file_path, 'r') as file:
        for line in file:
            user = json.loads(line.strip())
            if user.get('businessemail') == businessemail:
                return True  # Username found
    return False

def create_user_meals_file(username):
    file_path = os.path.join(DATA_DIR, f'{username}_meals.txt')
    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            file.write("")
    return file_path


def find_business_user_in_file(username):
    """Find a user by username in the .txt file."""
    if not os.path.exists(BUSINESS_FILE_PATH):
        return None  # File does not exist yet

    with open(BUSINESS_FILE_PATH, "r") as file:
        for line in file:
            user = json.loads(line.strip())
            if user.get("username") == username:
                return user  # Return the user data
    return None

def find_driver_user_in_file(username):
    """Find a user by username in the .txt file."""
    if not os.path.exists(DRIVER_FILE_PATH):
        return None  # File does not exist yet

    with open(DRIVER_FILE_PATH, "r") as file:
        for line in file:
            user = json.loads(line.strip())
            if user.get("username") == username:
                return user  # Return the user data
    return None

def get_user_file(username):
    return os.path.join(DATA_DIR, f"{username}_meals.txt")

def read_meals(username):
    user_file = get_user_file(username)
    if not os.path.exists(user_file):
        return []
    with open(user_file, 'r') as file:
        return [json.loads(line.strip()) for line in file]
    
def write_meals(username, data):
    user_file = get_user_file(username)
    with open(user_file, 'a') as file:
        file.write(json.dumps(data) + "\n")

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


# User Authentication Routes
@app.route('/api/driver/login', methods=['POST'])
def driver_login():
    """Handle driver login."""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    # Super basic authentication (plaintext as requested)
    drivers_file = 'users/drivers.txt'
    if not os.path.exists(drivers_file):
        return jsonify({"error": "No drivers registered"}), 404
    
    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    # Find user in file
    user = find_driver_user_in_file(username)
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Validate password
    if check_password_hash(user["password"], password):
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid password"}), 401

@app.route('/api/business/login', methods=['POST'])
def business_login():
    """Handle business login."""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    # Super basic authentication (plaintext as requested)
    business_file = 'users/business.txt'
    if not os.path.exists(business_file):
        return jsonify({"error": "No business registered"}), 404
    
    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    # Find user in file
    user = find_business_user_in_file(username)
    if not user:
        return jsonify({"message": "User not found"}), 401

    # Validate password
    if check_password_hash(user["password"], password):
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid password"}), 401

# Meal Management Routes
@app.route('/meals/available/<username>', methods=['POST'])
def add_meal(username):
    data = request.json
    if not username or not all(key in data for key in ["dishName", "mealType", "quantity"]):
        return jsonify({"message": "Invalid input or missing username"}), 400

    # Write to user-specific file
    write_meals(username, {
        "dishName": data["dishName"],
        "mealType": data["mealType"],
        "quantity": data["quantity"]
    })

    return jsonify({"message": f"Meal added successfully for {username}"}), 201

@app.route('/business/updatemeals/<username>', methods=['GET'])
def get_meals(username):
    if not username:
        return jsonify({"message": "Username is required"}), 400

    meals = read_meals(username)
    return jsonify(meals), 200

@app.route('/business/updatemeals/<username>', methods=['PUT'])
def update_meal(username):
    data = request.json
    dish_name = data.get("dishName")
    new_quantity = data.get("newQuantity")

    if not dish_name or not new_quantity:
        return jsonify({"message": "Dish name and new quantity are required"}), 400

    user_file = os.path.join(DATA_DIR, f"{username}_meals.txt")
    if not os.path.exists(user_file):
        return jsonify({"message": "User file not found"}), 404

    updated_meals = []
    meal_updated = False

    # Update the specific meal's quantity
    with open(user_file, "r") as file:
        for line in file:
            meal = json.loads(line.strip())
            if meal["dishName"] == dish_name:
                meal["quantity"] = new_quantity
                meal_updated = True
            updated_meals.append(meal)

    # Write updated meals back to the file
    with open(user_file, "w") as file:
        for meal in updated_meals:
            file.write(json.dumps(meal) + "\n")

    if meal_updated:
        return jsonify({"message": "Meal updated successfully"}), 200
    else:
        return jsonify({"message": "Dish not found"}), 404
    
# Registration Routes
@app.route('/api/driver/register', methods=['POST'])
def register_driver():
    """Register a new driver."""
    data = request.get_json()

    if not data:
        return jsonify({"message": "No data received"}), 400
    drivers_file = 'users/drivers.txt'


    # Validate required fields
    required_fields = ["firstname", "lastname", "username", "password", "email", "deliverycompany"]
    errors = []
    for field in required_fields:
        if field not in data or not data[field]:
            errors.append(f"Missing field: {field}")
        
    if is_username_taken(data['username'], drivers_file):
        errors.append("Username already exists") 
    
    if is_email_taken(data['email'], drivers_file):
        errors.append("Email is already used")

    if errors:
        print("Validation Errors:", errors)  # Log errors
        return jsonify({"errors": errors}), 400
    
    hashed_password = generate_password_hash(data['password'])

    driver_data = {
        "firstname": data['firstname'],
        "lastname": data['lastname'],
        "username": data['username'],
        "password": hashed_password,  # Note: Hash this in production
        "email": data['email'],
        "deliverycompany": data['deliverycompany']
    }
    
    # Basic registration (plaintext storage)
    with open(drivers_file, 'a') as f:
        f.write(json.dumps(driver_data) + "\n")
    
    return jsonify({"message": "Driver registered successfully"}), 201

@app.route('/api/business/register', methods=['POST'])
def register_business():
    """Register a new food business."""
    data = request.json
    business_file = 'users/business.txt'

    required_fields = ["firstname", "lastname", "role", "businessname","businessemail", "address", "postal", "username", "password"]
    errors = []

    for field in required_fields:
        if field not in data or not data[field]:
            errors.append(f"Missing field: {field}")
        
    if is_username_taken(data['username'], business_file):
        errors.append("Username already exists")  
    
    if is_businessemail_taken(data['businessemail'], business_file):
        errors.append("Email is already used") 

    if errors:
        print("Validation Errors:", errors)  # Log errors
        return jsonify({"errors": errors}), 400
    
    hashed_password = generate_password_hash(data['password'])

    business_data = {
        "firstname": data['firstname'],
        "lastname": data['lastname'],
        "role": data['role'],
        "businessname": data['businessname'],
        "businessemail": data['businessemail'],
        "address": data['address'],
        "postal": data['postal'],
        "username": data['username'],
        "password": hashed_password,
    }
    
    # Basic registration (plaintext storage)
    with open(business_file, 'a') as f:
        f.write(json.dumps(business_data) + "\n")
    
    create_user_meals_file(data['username'])

    return jsonify({"message": "Business registered successfully"}), 201

@app.route('/api/locations', methods=['GET'])
def get_locations():
    """Read business.txt, geocode addresses, and return a list of locations."""
    print('here')
    try:
        # Check if the file exists
        if not os.path.exists(BUSINESS_FILE_PATH):
            return jsonify({"error": "business.txt not found"}), 404
        # Read the business.txt file
        with open(BUSINESS_FILE_PATH, "r") as file:
            # business_data = json.load(file)
            all_business_data = [json.loads(line) for line in file] # list of dictionaries
            print(all_business_data)

        all_correct_business_data = []
        for business_data in all_business_data:
            # Extract address and postal code
            address = business_data.get("address", "")
            postal_code = business_data.get("postal", "")
            username = business_data.get("username", "")

            if not address or not postal_code:
                return jsonify({"error": "Address or postal code missing"}), 400

            # Combine address and postal code
            full_address = f"{address}, {postal_code}"

            # Geocode the address
            coords = geocode_address(full_address)

            # Get meals availble for the business
            MEALS_PATH = f"meals/{username}_meals.txt"
            with open(MEALS_PATH, "a+") as file:
                file.seek(0)
                meals = [json.loads(line) for line in file]
                print(meals)
            print('here')
            if coords:
                all_correct_business_data.append({
                    "title": f"{business_data.get('firstname', '')} {business_data.get('lastname', '')}",
                    "address1": address,
                    "address2": f"Postal Code: {postal_code}",
                    "coords": coords,
                    "meals": meals
                })
            else:
                return jsonify({"error": "Error geocoding address}"}), 500
        if all_correct_business_data:
            print(all_correct_business_data)
            return jsonify(all_correct_business_data), 200
        else:
            return jsonify({"error": "No locations found"}), 404

    except json.JSONDecodeError:
        return jsonify({"error": "Error parsing business.txt"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Ensure necessary directories exist
    os.makedirs('users', exist_ok=True)
    os.makedirs('meals', exist_ok=True)
    
    # Run the Flask app
    # app.run(debug=True, port=5000)
    app.run(debug=True)