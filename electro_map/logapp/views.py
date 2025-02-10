from django.shortcuts import render
from django.http import JsonResponse
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from django.contrib.auth.decorators import login_required


@login_required
def power_allocation(request):
    zones = [
        "Mechi", "Koshi", "Sagarmatha", "Janakpur", "Bagmati", "Narayani", "Gandaki",
        "Lumbini", "Dhaulagiri", "Rapti", "Bheri", "Karnali", "Seti", "Mahakali"
    ]
    days = 30  # Keeping 30 days of data

    # Generate synthetic data
    np.random.seed(42)
    data = []
    for day in range(days):
        for zone in zones:
            temperature = np.random.uniform(10, 40)
            time_of_day = np.random.choice([0, 6, 12, 18])
            weekday = day % 7
            base_consumption = np.random.uniform(80, 200)
            noise = np.random.uniform(-20, 20)
            if time_of_day in [18, 0]:
                base_consumption *= 1.2
            if weekday >= 5:  # Weekend adjustment
                base_consumption *= 0.8
            consumption = base_consumption + noise - (temperature * 0.4)
            data.append([day, zone, temperature, time_of_day, weekday, base_consumption, consumption])

    df = pd.DataFrame(data, columns=["Day", "Zone", "Temperature", "TimeOfDay", "Weekday", "Base_Consumption", "Consumption"])
    
    # One-hot encode the Zone column
    df = pd.get_dummies(df, columns=["Zone"], drop_first=True)

    # Prepare training data
    X = df.drop(columns=["Consumption"])
    y = df["Consumption"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)

    # Predict on test set and calculate error
    predicted_consumption = rf.predict(X_test)
    mae = mean_absolute_error(y_test, predicted_consumption)

    # Predict for the latest 14 zones (most recent data)
    latest_data = df[df['Day'] == df['Day'].max()].drop(columns=["Consumption"])  # Latest day's data
    latest_data = latest_data[:14]  # Only take 14 zones
    predicted_consumption = rf.predict(latest_data[X_train.columns])

    # Power Allocation
    available_power = 2000
    allocated_power = available_power / len(zones)

    allocation_df = pd.DataFrame({
        "Zone": zones[:14],  # Assigning only the first 14 zones
        "Predicted_Consumption": predicted_consumption,
        "Allocated_Power": allocated_power
    })
    allocation_df["Surplus/Deficit"] = allocation_df["Allocated_Power"] - allocation_df["Predicted_Consumption"]

    # Rename "Surplus/Deficit" to "Surplus_Deficit" to make it a valid key in the template
    allocation_df.rename(columns={"Surplus/Deficit": "Surplus_Deficit"}, inplace=True)

    # Power Redistribution Logic
    def redistribute_power(df):
        surplus_zones = df[df["Surplus_Deficit"] > 0].sort_values("Surplus_Deficit", ascending=False)
        deficit_zones = df[df["Surplus_Deficit"] < 0].sort_values("Surplus_Deficit")

        transactions = []
        for idx, deficit_row in deficit_zones.iterrows():
            deficit = -deficit_row["Surplus_Deficit"]
            for s_idx, surplus_row in surplus_zones.iterrows():
                surplus = surplus_row["Surplus_Deficit"]
                if surplus <= 0:
                    continue
                transfer = min(surplus, deficit)
                df.at[idx, "Allocated_Power"] += transfer
                df.at[s_idx, "Allocated_Power"] -= transfer
                df.at[idx, "Surplus_Deficit"] += transfer
                df.at[s_idx, "Surplus_Deficit"] -= transfer
                transactions.append(f"Transferred {transfer:.2f} from {surplus_row['Zone']} to {deficit_row['Zone']}")
                if df.at[idx, "Surplus_Deficit"] >= 0:
                    break

        df["Allocated_Power"] = df["Allocated_Power"].clip(lower=0)
        return df, transactions

    final_allocation, logs = redistribute_power(allocation_df)

    # Convert to dictionary for the template
    context = {
        "mean_absolute_error": mae,
        "final_allocation": final_allocation.to_dict(orient="records"),
        "redistribution_log": logs
    }

    return render(request, "power_allocation.html", context)
