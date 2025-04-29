# filename: dashboard.py

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib

# Page configuration
st.set_page_config(
    page_title="NAIJAWATT MONITOR",
    page_icon="⚡",
    layout="wide"
)

# Load your trained model
model = joblib.load('model.joblib')

# Create feature columns in the same order as used during training
expected_features = model.feature_names_in_

# Maps for encoding categorical variables
time_mapping = {'Morning': 0, 'Afternoon': 1, 'Evening': 2, 'Night': 3}
day_mapping = {'Weekday': 0, 'Weekend': 1}
weather_mapping = {'Clear': 0, 'Cloudy': 1, 'Rainy': 2, 'Windy': 3}

# Custom CSS for styling
st.markdown("""
    <style>
        .main-title {
            color: #1E90FF;
            text-align: center;
            font-size: 2.5em;
            margin-bottom: 20px;
        }
        .sidebar .sidebar-content {
            background-color: #f0f2f6;
        }
        .stButton>button {
            background-color: #1E90FF;
            color: white;
            border-radius: 5px;
            padding: 10px 24px;
            width: 100%;
        }
        .stNumberInput, .stSelectbox {
            margin-bottom: 15px;
        }
        .success-box {
            text-align: center;
            padding: 15px;
            border-radius: 5px;
            background-color: #e6f7e6;
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# Main title
st.markdown('<h1 class="main-title">⚡ NAIJAWATT MONITOR</h1>', unsafe_allow_html=True)
st.markdown("---")

# Create two columns for layout
col1, col2 = st.columns([1, 1])

with col1:
    st.header("Power System Parameters")
    voltage = st.number_input('Voltage (V)', min_value=0.0, max_value=500.0, value=220.0, step=1.0)
    current = st.number_input('Current (A)', min_value=0.0, max_value=10.0, value=5.0, step=0.1)
    power = st.number_input('Power (W)', min_value=0.0, max_value=10000.0, value=1000.0, step=100.0)
    power_factor = st.number_input('Power Factor', min_value=0.0, max_value=1.0, value=0.8, step=0.05)
    temperature = st.number_input('Temperature (°C)', min_value=-20.0, max_value=50.0, value=25.0, step=1.0)

with col2:
    st.header("Environmental Factors")
    light_intensity = st.number_input('Light Intensity (%)', min_value=0.0, max_value=100.0, value=75.0, step=5.0)
    time_of_day = st.selectbox('Time of Day', ['Morning', 'Afternoon', 'Evening', 'Night'])
    day_type = st.selectbox('Day Type', ['Weekday', 'Weekend'])
    system_load = st.number_input('System Load (%)', min_value=0.0, max_value=100.0, value=50.0, step=5.0)
    weather = st.selectbox('Weather Condition', ['Clear', 'Cloudy', 'Rainy', 'Windy'])
    past_faults = st.number_input('Past Faults Count', min_value=0, max_value=10, value=0)

# Process the input data
input_data = pd.DataFrame({
    'Voltage (V)': [voltage],
    'Current (A)': [current],
    'Power (kW)': [power / 1000],  # Convert to kW
    'Power Factor': [power_factor],
    'Temperature (°C)': [temperature],
    'Light Intensity (%)': [light_intensity / 10],  # Scale to 0-10
    'Time of Day': [time_mapping[time_of_day]],  # Map string to number
    'Day Type Encoded': [day_mapping[day_type]],  # Map string to number
    'System Load (%)': [system_load],
    'Weather Encoded': [weather_mapping[weather]],  # Map string to number
    'Past faults': [past_faults]
})

# Align the input data with expected features used during model training
for col in expected_features:
    if col not in input_data.columns:
        input_data[col] = 0  # Add missing columns with default value 0

# Ensure the columns are in the correct order as expected by the model
input_data = input_data[expected_features]

# Prediction button centered
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if st.button('ANALYZE SYSTEM STATUS'):
        prediction = model.predict(input_data)
        st.markdown(f"""
            <div class="success-box">
                <h3>System Status Prediction</h3>
                <p style="font-size: 24px; font-weight: bold;">{prediction[0]}</p>
            </div>
        """, unsafe_allow_html=True)