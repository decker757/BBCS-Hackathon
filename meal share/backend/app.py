# backend/app.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)

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
    
    with open(drivers_file, 'r') as f:
        for line in f:
            stored_username, stored_password = line.strip().split(',')
            if username == stored_username and password == stored_password:
                return jsonify({"message": "Login successful"}), 200
    
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/api/provider/login', methods=['POST'])
def provider_login():
    """Handle provider login."""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    # Super basic authentication (plaintext as requested)
    providers_file = 'users/providers.txt'
    if not os.path.exists(providers_file):
        return jsonify({"error": "No providers registered"}), 404
    
    with open(providers_file, 'r') as f:
        for line in f:
            stored_username, stored_password = line.strip().split(',')
            if username == stored_username and password == stored_password:
                return jsonify({"message": "Login successful"}), 200
    
    return jsonify({"error": "Invalid credentials"}), 401

# Meal Management Routes
@app.route('/api/meals/available', methods=['GET'])
def get_available_meals():
    """Retrieve available meals."""
    meals_file = 'meals/available_meals.txt'
    if not os.path.exists(meals_file):
        return jsonify({"meals": []})
    
    with open(meals_file, 'r') as f:
        meals = [line.strip().split(',') for line in f]
    
    return jsonify({"meals": meals})

@app.route('/api/provider/update-meals', methods=['POST'])
def update_available_meals():
    """Update available meals for a provider."""
    data = request.json
    meals_file = 'meals/available_meals.txt'
    
    # Basic validation
    if not data.get('restaurant') or not data.get('meals'):
        return jsonify({"error": "Invalid input"}), 400
    
    # Append new meals to file
    with open(meals_file, 'a') as f:
        for meal in data['meals']:
            f.write(f"{data['restaurant']},{meal}\n")
    
    return jsonify({"message": "Meals updated successfully"}), 200

# Registration Routes
@app.route('/api/driver/register', methods=['POST'])
def register_driver():
    """Register a new driver."""
    data = request.json
    drivers_file = 'users/drivers.txt'
    
    # Basic registration (plaintext storage)
    with open(drivers_file, 'a') as f:
        f.write(f"{data['username']},{data['password']}\n")
    
    return jsonify({"message": "Driver registered successfully"}), 201

@app.route('/api/provider/register', methods=['POST'])
def register_provider():
    """Register a new food provider."""
    data = request.json
    providers_file = 'users/providers.txt'
    
    # Basic registration (plaintext storage)
    with open(providers_file, 'a') as f:
        f.write(f"{data['username']},{data['password']}\n")
    
    return jsonify({"message": "Provider registered successfully"}), 201

if __name__ == '__main__':
    # Ensure necessary directories exist
    os.makedirs('users', exist_ok=True)
    os.makedirs('meals', exist_ok=True)
    
    # Run the Flask app
    app.run(debug=True, port=5000)