"""Meal Share API. Existing JSON-lines records remain the storage format."""
from datetime import timedelta
from functools import wraps
from pathlib import Path
from threading import RLock
import json
import os
import re
import tempfile

from flask import Flask, request, jsonify, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import requests

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.getenv('FLASK_SECRET_KEY'),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=os.getenv('SESSION_COOKIE_SECURE', 'true').lower() != 'false',
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=timedelta(hours=8),
    SESSION_REFRESH_EACH_REQUEST=False,
    MAX_CONTENT_LENGTH=64 * 1024,
)
allowed_origins = [origin.strip().rstrip('/') for origin in os.getenv(
    'FRONTEND_ORIGINS', 'http://localhost:3000,http://127.0.0.1:3000'
).split(',') if origin.strip()]
CORS(app, origins=allowed_origins, supports_credentials=True,
     allow_headers=['Content-Type', 'X-Meal-Share-Request'])

BASE_DIR = Path(os.getenv('MEAL_SHARE_DATA_DIR', str(Path(__file__).resolve().parent)))
BUSINESS_FILE_PATH = str(BASE_DIR / 'users/business.txt')
DRIVER_FILE_PATH = str(BASE_DIR / 'users/drivers.txt')
DATA_DIR = str(BASE_DIR / 'meals')
MEAL_LOCK = RLock()


@app.before_request
def protect_mutations():
    if request.method not in ('POST', 'PUT', 'PATCH', 'DELETE'):
        return None
    # Forms cannot set this header. Cross-origin JavaScript requires a CORS
    # preflight, and the server also checks its explicit origin allowlist.
    origin = request.headers.get('Origin')
    same_origin = request.host_url.rstrip('/')
    if request.headers.get('X-Meal-Share-Request') != '1' or (
        origin is not None and origin not in [same_origin, *allowed_origins]
    ):
        return jsonify({'message': 'Request origin is not allowed'}), 403
    return None


@app.after_request
def private_responses(response):
    if request.path != '/api/locations':
        response.headers['Cache-Control'] = 'no-store'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response


def valid_username(value) -> bool:
    return isinstance(value, str) and 0 < len(value) <= 100 and bool(
        re.fullmatch(r'[\w .@+-]+', value)
    ) and value == value.strip() and value not in ('.', '..')


def json_object():
    data = request.get_json(silent=True)
    return data if isinstance(data, dict) else {}


def quantity_value(value):
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        number = value
    elif isinstance(value, str) and re.fullmatch(r'[0-9]{1,10}', value):
        number = int(value)
    else:
        return None
    return number if 0 <= number <= 2147483647 else None


def require_business_owner(function):
    @wraps(function)
    def checked(username):
        if not session.get('username'):
            return jsonify({'message': 'Sign in to manage meals'}), 401
        if session.get('role') != 'business' or session['username'] != username:
            return jsonify({'message': 'You can only manage your own meals'}), 403
        if not valid_username(username):
            return jsonify({'message': 'Invalid username'}), 400
        return function(username)
    return checked


@app.get('/api/session')
def current_session():
    if not session.get('username'):
        return jsonify({'username': None, 'role': None})
    return jsonify({'username': session['username'], 'role': session.get('role')})


@app.post('/api/logout')
def logout():
    if not app.secret_key:
        return jsonify({'message': 'Sign-out is temporarily unavailable'}), 503
    session.clear()
    return jsonify({'message': 'Signed out'})


def get_google_maps_api_key():
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_MAPS_API_KEY environment variable is not configured")
    return api_key

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
            if str(user.get('username', '')).casefold() == username.casefold():
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
    os.makedirs(DATA_DIR, exist_ok=True)
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
        return [json.loads(line.strip()) for line in file if line.strip()]
    
def write_meals(username, data):
    user_file = get_user_file(username)
    os.makedirs(DATA_DIR, exist_ok=True)
    with MEAL_LOCK, open(user_file, 'a') as file:
        file.write(json.dumps(data) + "\n")

def geocode_address(address):
    """Geocode the address using Google Maps Geocoding API."""
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": address, "key": get_google_maps_api_key()}
    response = requests.get(url, params=params, timeout=(3, 5))
    response.raise_for_status()
    geocode_data = response.json()

    if geocode_data["status"] == "OK":
        location = geocode_data["results"][0]["geometry"]["location"]
        return {"lat": location["lat"], "lng": location["lng"]}
    return None        


# User Authentication Routes
def login_user(role):
    data = json_object()
    username, password = data.get('username'), data.get('password')
    if not valid_username(username) or not isinstance(password, str) or not password:
        return jsonify({'message': 'Username and password are required'}), 400
    if not app.secret_key:
        return jsonify({'message': 'Sign-in is temporarily unavailable'}), 503
    user = (find_business_user_in_file if role == 'business' else find_driver_user_in_file)(username)
    if not user or not check_password_hash(user['password'], password):
        return jsonify({'message': 'Invalid username or password'}), 401
    session.clear()
    session['username'] = user['username']
    session['role'] = role
    session.permanent = True
    return jsonify({'message': 'Login successful', 'username': user['username'], 'role': role}), 200


@app.post('/api/driver/login')
def driver_login():
    return login_user('driver')


@app.post('/api/business/login')
def business_login():
    return login_user('business')

# Meal Management Routes
@app.route('/meals/available/<username>', methods=['POST'])
@require_business_owner
def add_meal(username):
    data = json_object()
    quantity = quantity_value(data.get('quantity'))
    if quantity is None or not all(isinstance(data.get(key), str) and data[key].strip() for key in ['dishName', 'mealType']):
        return jsonify({"message": "Invalid input or missing username"}), 400

    # Write to user-specific file
    write_meals(username, {
        "dishName": data["dishName"],
        "mealType": data["mealType"],
        "quantity": quantity
    })

    return jsonify({"message": f"Meal added successfully for {username}"}), 201

@app.route('/business/updatemeals/<username>', methods=['GET'])
@require_business_owner
def get_meals(username):
    if not username:
        return jsonify({"message": "Username is required"}), 400

    meals = read_meals(username)
    return jsonify(meals), 200

@app.route('/business/updatemeals/<username>', methods=['PUT'])
@require_business_owner
def update_meal(username):
    data = json_object()
    dish_name = data.get("dishName")
    new_quantity = quantity_value(data.get("newQuantity"))

    if not isinstance(dish_name, str) or not dish_name.strip() or new_quantity is None:
        return jsonify({"message": "Dish name and new quantity are required"}), 400

    with MEAL_LOCK:
        user_file = get_user_file(username)
        if not os.path.exists(user_file):
            return jsonify({'message': 'User file not found'}), 404
        meals = read_meals(username)
        if not any(meal.get('dishName') == dish_name for meal in meals):
            return jsonify({'message': 'Dish not found'}), 404
        for meal in meals:
            if meal.get('dishName') == dish_name:
                meal['quantity'] = new_quantity
        # Replace only after a complete write; never truncate the existing file
        # before its replacement is ready. The in-process lock also covers adds.
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(mode='w', dir=DATA_DIR, prefix='.meals-', delete=False) as file:
                temporary = file.name
                for meal in meals:
                    file.write(json.dumps(meal) + '\n')
                file.flush()
                os.fsync(file.fileno())
            os.replace(temporary, user_file)
        finally:
            if temporary and os.path.exists(temporary):
                os.unlink(temporary)
    return jsonify({'message': 'Meal updated successfully'}), 200

# Registration Routes
@app.route('/api/driver/register', methods=['POST'])
def register_driver():
    """Register a new driver."""
    data = json_object()

    if not data:
        return jsonify({"message": "No data received"}), 400
    drivers_file = DRIVER_FILE_PATH


    # Validate required fields
    required_fields = ["firstname", "lastname", "username", "password", "email", "deliverycompany"]
    errors = []
    for field in required_fields:
        if not isinstance(data.get(field), str) or not data[field].strip():
            errors.append(f"Missing field: {field}")
        
    if not valid_username(data.get('username')):
        errors.append('Invalid username')
    if errors:
        return jsonify({'errors': errors}), 400

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
    
    # Retain the existing JSON-lines format with a password hash
    os.makedirs(Path(drivers_file).parent, exist_ok=True)
    with open(drivers_file, 'a') as f:
        f.write(json.dumps(driver_data) + "\n")
    
    return jsonify({"message": "Driver registered successfully"}), 201

@app.route('/api/business/register', methods=['POST'])
def register_business():
    """Register a new food business."""
    data = json_object()
    business_file = BUSINESS_FILE_PATH

    required_fields = ["firstname", "lastname", "role", "businessname","businessemail", "address", "postal", "username", "password"]
    errors = []

    for field in required_fields:
        if not isinstance(data.get(field), str) or not data[field].strip():
            errors.append(f"Missing field: {field}")
        
    if not valid_username(data.get('username')):
        errors.append('Invalid username')
    if errors:
        return jsonify({'errors': errors}), 400

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
    
    # Retain the existing JSON-lines format with a password hash
    os.makedirs(Path(business_file).parent, exist_ok=True)
    with open(business_file, 'a') as f:
        f.write(json.dumps(business_data) + "\n")
    
    create_user_meals_file(data['username'])

    return jsonify({"message": "Business registered successfully"}), 201

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
            username = business_data.get("username", "")

            if not address or not postal_code:
                return jsonify({"error": "Address or postal code missing"}), 400

            # Combine address and postal code
            full_address = f"{address}, {postal_code}"

            # Geocode the address
            coords = geocode_address(full_address)

            # Get meals availble for the business
            meals = read_meals(username) if valid_username(username) else []
            if coords:
                all_correct_business_data.append({
                    "title": f"{business_data.get('businessname', '')}",
                    "address1": address,
                    "address2": f"Postal Code: {postal_code}",
                    "coords": coords,
                    "meals": meals
                })
            else:
                return jsonify({"error": "Error geocoding address}"}), 500
        if all_correct_business_data:
            return jsonify(all_correct_business_data), 200
        else:
            return jsonify({"error": "No locations found"}), 404

    except json.JSONDecodeError:
        return jsonify({"error": "Error parsing business.txt"}), 400
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 503
    except requests.RequestException:
        return jsonify({"error": "Location provider is temporarily unavailable"}), 502
    except Exception:
        return jsonify({"error": "Unable to load locations"}), 500

if __name__ == '__main__':
    os.makedirs(Path(BUSINESS_FILE_PATH).parent, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)
    app.run(debug=False)
