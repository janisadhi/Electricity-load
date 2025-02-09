from flask import Flask, jsonify
from flask_cors import CORS  # Ensure you have flask_cors installed
import numpy as np

app = Flask(__name__)

# Enable CORS for all origins (this allows requests from any domain)
CORS(app)

# Provinces from the JSON file
states = ['Bagmati', 'Bheri', 'Bhojpur', 'Dhawalagiri', 'Gandaki', 'Janakpur', 
          'Karnali', 'Lumbini', 'Mahakali', 'Mechi', 'Narayani', 'Rapti', 'Sagarmatha', 'Seti']

# Function to generate power data for the provinces
def generate_power_data():
    current_usage = np.random.randint(50, 150, size=len(states))  # Random current usage (50-150 MW)
    allocated_power = np.random.randint(60, 120, size=len(states))  # Random allocated power (60-120 MW)

    # Convert NumPy arrays to Python types for JSON serialization
    power_data = {state: {'current': int(current_usage[i]), 'allocated': int(allocated_power[i])} 
                  for i, state in enumerate(states)}
    
    return power_data

@app.route('/power-data')
def power_data():
    """API endpoint to fetch power data"""
    return jsonify(generate_power_data())

if __name__ == '__main__':
    app.run(debug=True)
