from flask import Flask, jsonify
from flask_cors import CORS  # Ensure you have flask_cors installed
import pandas as pd

# Load data
hydro = pd.read_csv("hydro_power_data_cleaned.csv")
customer = pd.read_csv("customer_data_modified.csv")

# Calculate total hydro power produced
def Total_power(hydro):
    total = hydro["CurrentCapacity(MW)"].sum()
    return total # Return instead of printing

# Group by "Region" and sum the "Current_Power_Used"
def subHydro(customer):
    region_power_usage = customer.groupby("Region")["Current_Power_Used(kWh)"].sum()/1000
    return region_power_usage.to_dict()  # Convert to dict for JSON compatibility

# Calculate required power by subtracting used power from total capacity
def required_power(hydro, customer):
    total_capacity = Total_power(hydro)
    total_used_power = sum(subHydro(customer).values())  # Convert kWh to MW
    return total_capacity - total_used_power

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all origins

# List of states (provinces)
states = ['Bagmati', 'Bheri', 'Bhojpur', 'Dhawalagiri', 'Gandaki', 'Janakpur', 
          'Karnali', 'Lumbini', 'Mahakali', 'Mechi', 'Narayani', 'Rapti', 'Sagarmatha', 'Seti']

# Function to generate power data for the provinces
def generate_power_data():
    current_usage = subHydro(customer)  # Dictionary of region-wise power usage
    total_allocated_power = Total_power(hydro)  # Total power produced
    allocated_power = total_allocated_power / len(states)  # Evenly distribute power

    # Construct response data
    power_data = {state: {
        'current': int(current_usage.get(state, 0)),  # Get value or default 0
        'allocated': int(allocated_power)  # Evenly allocated power
    } for state in states}

    return power_data

# API endpoint to fetch power data
@app.route('/power-data')
def power_data():
    return jsonify(generate_power_data())

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
