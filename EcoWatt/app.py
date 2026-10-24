import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import SGDRegressor
import matplotlib.pyplot as plt
import requests # For OpenWeatherMap API
import os # Added for file operations
from sklearn.ensemble import RandomForestRegressor # NEW: For Random Forest
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score # For model evaluation
from sklearn.preprocessing import FunctionTransformer, StandardScaler # For Logarithmic Regression
from sklearn.pipeline import make_pipeline # For Logarithmic Regression Pipeline

# --- SECRETS: do NOT hard-code keys. Add them in Colab (key icon -> Secrets) as
# OPENWEATHER_API_KEY and NGROK_AUTHTOKEN, or set them as environment variables.
def _get_secret(name):
    try:
        from google.colab import userdata
        value = userdata.get(name)
        if value:
            return value
    except Exception:
        pass
    return os.environ.get(name, "")

OPENWEATHER_API_KEY_VALUE = _get_secret("OPENWEATHER_API_KEY")
NGROK_AUTHTOKEN_VALUE = _get_secret("NGROK_AUTHTOKEN") or "3FXkJDsAj9osZANxjN0KtlK0Qkc_3PSiqjKHNzPu3idjY39Pb"

# Set the environment variable for the API key with safe fallback
if not OPENWEATHER_API_KEY_VALUE:
    OPENWEATHER_API_KEY_VALUE = os.environ.get("OPENWEATHER_API_KEY", "40d15d9b8860af245b44d15ee812f496")
os.environ["OPENWEATHER_API_KEY"] = OPENWEATHER_API_KEY_VALUE

# Initialize session state for login and username
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = None

# Initialize session state for uploaded datasets
if "uploaded_datasets" not in st.session_state:
    st.session_state["uploaded_datasets"] = {} # Stores {'filename': dataframe}
if "selected_dataset_name" not in st.session_state:
    st.session_state["selected_dataset_name"] = None # Name of the currently active dataset

# =========================
# LOGIN FUNCTIONALITY
# =========================
# Define user credentials
USERS = {
    "admin": "1234",
    "vighnesh": "password"
}

if not st.session_state["logged_in"]:
    st.sidebar.subheader("Login")
    username_input = st.sidebar.text_input("Username", key="login_username")
    password_input = st.sidebar.text_input("Password", type="password", key="login_password")

    if st.sidebar.button("Login", key="login_button"):
        if username_input in USERS and USERS[username_input] == password_input:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username_input
            st.sidebar.success(f"Logged in as {username_input}!")
        else:
            st.sidebar.error("Incorrect username or password.")
else:
    st.sidebar.write(f"Logged in as: {st.session_state['username']}")
    if st.sidebar.button("Logout", key="logout_button"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = None
        st.sidebar.info("Logged out successfully.")

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="EcoWatt",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ EcoWatt")
st.subheader("Predict • Save • Sustain")

# Blended Video Hero Banner (Background Theme Only)
st.markdown("""
<div style="position: relative; border-radius: 24px; overflow: hidden; margin: 15px 0 25px 0; box-shadow: 0 16px 35px rgba(20, 75, 39, 0.08); background: linear-gradient(135deg, rgba(0, 158, 82, 0.08), rgba(59, 130, 246, 0.08)); border: 1px solid rgba(0, 158, 82, 0.15);">
    <video autoplay loop muted playsinline style="width: 100%; height: 260px; object-fit: cover; mix-blend-mode: multiply; filter: contrast(1.06) brightness(1.03);">
        <source src="https://strvid.nyc3.cdn.digitaloceanspaces.com/motionsite/hero_green_energy.mp4" type="video/mp4">
    </video>
    <div style="position: absolute; bottom: 18px; left: 20px; background: rgba(255,255,255,0.88); backdrop-filter: blur(10px); padding: 8px 18px; border-radius: 14px; font-weight: 700; color: #144b27; font-size: 13px; border: 1px solid rgba(255,255,255,0.6); display: flex; align-items: center; gap: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
        <span>⚡ EcoWatt Intelligence Engine</span>
        <span style="color: #009e52; font-weight: 500;">• Physics Load + SGD Logarithmic Regression</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Define history file globally within the app code
history_file = "prediction_history.csv"

# =========================
# WEATHER API INTEGRATION
# =========================
WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "40d15d9b8860af245b44d15ee812f496")
WEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

if not WEATHER_API_KEY:
    st.error("OpenWeatherMap API key not found. Please set the OPENWEATHER_API_KEY environment variable.")
    st.stop() # Stop the app if API key is missing

def get_weather_data(city_name):
    params = {
        "q": city_name,
        "appid": WEATHER_API_KEY,
        "units": "metric"
    }
    try:
        response = requests.get(WEATHER_BASE_URL, params=params, timeout=8)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.HTTPError as e:
        st.error(f"Error fetching weather: {e.response.status_code} - {e.response.text}")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error making weather API request: {e}")
        return None

# Add UI for weather display
st.subheader("Current Weather Information")
weather_city = st.text_input("Enter city for weather information", "Kottayam")

if st.button("Get Weather"):
    if weather_city:
        weather_data = get_weather_data(weather_city)
        if weather_data:
            st.write(f"**City:** {weather_data['name']}")
            st.write(f"**Temperature:** {weather_data['main']['temp']} °C")
            st.write(f"**Feels Like:** {weather_data['main']['feels_like']} °C")
            st.write(f"**Humidity:** {weather_data['main']['humidity']}%) ")
            st.write(f"**Conditions:** {weather_data['weather'][0]['description'].capitalize()}")
        else:
            st.warning(f"Could not retrieve weather data for {weather_city}.")
    else:
        st.warning("Please enter a city name.")

# =========================
# SAMPLE DATASET GENERATION / PRELOAD
# =========================
# Generate a sample dataset only if no datasets are loaded yet
if not st.session_state["uploaded_datasets"] and not st.session_state["selected_dataset_name"]:
    local_dataset_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "EcoWatt_6000.csv")
    loaded_local = False

    if os.path.exists(local_dataset_path):
        try:
            local_df = pd.read_csv(local_dataset_path)
            local_df['E_load'] = (local_df['PowerRating'] * local_df['UsageDuration'] * local_df['NumDevices']) / 1000
            local_df['EnergyResidual'] = local_df['EnergyConsumption'] - local_df['E_load']
            st.session_state.uploaded_datasets["EcoWatt_6000.csv"] = local_df.copy()
            st.session_state.selected_dataset_name = "EcoWatt_6000.csv"
            loaded_local = True
        except Exception:
            pass

    if not loaded_local:
        np.random.seed(42)
        data_size = 200

        temperature = np.random.randint(20, 40, data_size)
        time_hour = np.random.randint(0, 24, data_size)
        humidity = np.random.randint(40, 90, data_size)
        power_rating = np.random.randint(100, 2500, data_size)
        usage_duration = np.random.uniform(0.5, 10, data_size)
        num_devices = np.random.randint(1, 10, data_size)
        occu_pancy = np.random.randint(1, 6, data_size)

        energy_consumption = (
            (power_rating * usage_duration * num_devices) / 1000
            + 0.3 * temperature
            + 0.1 * humidity
            + 0.5 * occu_pancy
            + np.random.normal(0, 2, data_size)
        )

        initial_df = pd.DataFrame({
            "Temperature": temperature,
            "Time": time_hour,
            "Humidity": humidity,
            "PowerRating": power_rating,
            "UsageDuration": usage_duration,
            "NumDevices": num_devices,
            "Occupancy": occu_pancy,
            "EnergyConsumption": energy_consumption
        })

        initial_df['E_load'] = (initial_df['PowerRating'] * initial_df['UsageDuration'] * initial_df['NumDevices']) / 1000
        initial_df['EnergyResidual'] = initial_df['EnergyConsumption'] - initial_df['E_load']

        st.session_state.uploaded_datasets["Sample Dataset (Generated)"] = initial_df.copy()
        st.session_state.selected_dataset_name = "Sample Dataset (Generated)"

# Ensure df and original_df always refer to the currently selected dataset
if st.session_state.selected_dataset_name and st.session_state.selected_dataset_name in st.session_state.uploaded_datasets:
    df = st.session_state.uploaded_datasets[st.session_state.selected_dataset_name]
    st.session_state.original_df = df.copy() # For the editable data editor
else:
    # Fallback if no dataset is selected (should not happen with initial generation logic)
    st.warning("No active dataset selected. Please upload a CSV or ensure the sample dataset is loaded.")
    df = pd.DataFrame() # Empty DataFrame to prevent errors
    st.session_state.original_df = pd.DataFrame() # Empty DataFrame
    # Prevent model training if df is empty
    if 'log_reg_model' in st.session_state: del st.session_state.log_reg_model
    if 'model_metrics' in st.session_state: del st.session_state.model_metrics

# =========================
# MODEL TRAINING AND EVALUATION FUNCTIONS
# =========================
def mean_absolute_percentage_error(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    # Avoid division by zero by replacing 0s in y_true with a small epsilon
    return np.mean(np.abs((y_true - y_pred) / np.maximum(y_true, 1e-8))) * 100

def evaluate_model(model_obj, X_eval, y_true, model_name, is_residual_model=False):
    if is_residual_model:
        # For residual models, X_eval should contain the original features + E_load for final prediction
        E_load = X_eval['E_load']
        X_residual_features = X_eval[['Temperature', 'Humidity', 'Time', 'Occupancy']]
        predicted_residual = model_obj.predict(X_residual_features)

        # NOTE: Logarithmic Regression applies log1p to the INPUT features inside the pipeline,
        # so the model output is already in kWh. No inverse transform (expm1) is needed here.

        predictions = E_load + predicted_residual
    else:
        # For other models, direct prediction
        predictions = model_obj.predict(X_eval)

    # Ensure predictions are non-negative for energy consumption
    predictions[predictions < 0] = 0

    mae = mean_absolute_error(y_true, predictions)
    mse = mean_squared_error(y_true, predictions)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, predictions)
    mape = mean_absolute_percentage_error(y_true, predictions)
    return {
        "Model": model_name,
        "MAE": mae,
        "MSE": mse,
        "RMSE": rmse,
        "R2": r2,
        "MAPE (%)": mape
    }

# Function to apply log1p transform (log(1+x)) - Moved to global scope
log_transform = FunctionTransformer(np.log1p, inverse_func=np.expm1, validate=True)

# Initial model training and evaluation (Logarithmic Regression) - only if df is not empty
if not df.empty:
    if 'log_reg_model' not in st.session_state or st.session_state.get('log_reg_model_df_hash') != hash(tuple(df.values.flatten())):
        # Create a pipeline: transform y, then SGDRegressor fit
        # For Physics-informed Logarithmic Regression, the pipeline predicts EnergyResidual
        # X_log_reg_train uses features for the residual model
        X_log_reg_train = df[['Temperature', 'Humidity', 'Time', 'Occupancy']]
        y_log_reg_train = df["EnergyResidual"] # Target is now EnergyResidual

        log_reg_model = make_pipeline(
            log_transform,
            StandardScaler(),
            SGDRegressor(loss='squared_error', penalty=None, eta0=0.01, max_iter=1000, random_state=42)
        )

        try:
            with st.spinner('Training Logarithmic Regression model...'):
                log_reg_model.fit(X_log_reg_train, y_log_reg_train) # Fit on residuals
            st.session_state.log_reg_model = log_reg_model
            st.session_state.log_reg_model_df_hash = hash(tuple(df.values.flatten()))
            st.success("Logarithmic Regression Model Trained and Ready!")
            # Evaluate and store metrics using the physics-informed evaluation
            # X_log_reg_eval needs E_load for the final prediction step in evaluate_model
            X_initial_eval = df[['Temperature', 'Humidity', 'Time', 'Occupancy', 'E_load']]
            # y_true for evaluate_model should be the original EnergyConsumption for calculating metrics
            if "model_metrics" not in st.session_state:
                st.session_state.model_metrics = {}
            st.session_state.model_metrics["Logarithmic Regression"] = evaluate_model(log_reg_model, X_initial_eval, df["EnergyConsumption"], "Logarithmic Regression", is_residual_model=True)
        except Exception as e:
            st.error(f"Error training Logarithmic Regression: {e}")
            st.session_state.log_reg_model = None # Ensure state is clean on failure
    else:
        log_reg_model = st.session_state.log_reg_model
else:
    log_reg_model = None # No model if df is empty


# =========================
# SIDEBAR INPUT
# =========================
st.sidebar.header("Input Parameters")

temp = st.sidebar.slider("Temperature (°C)", 15, 45, 30)
hour = st.sidebar.slider("Hour of Usage", 0, 23, 18)
humidity = st.sidebar.slider("Humidity (%)", 30, 100, 65)
power = st.sidebar.slider("Power Rating (W)", 100, 3000, 1500)
duration = st.sidebar.slider("Usage Duration (hrs)", 1.0, 24.0, 4.0)
devices = st.sidebar.slider("Number of Devices", 1, 15, 5)
occu_pancy = st.sidebar.slider("Occupancy", 1, 10, 3)

# Add a button to trigger prediction
predict_button = st.sidebar.button("Predict Energy")

# Initialize prediction variables outside the button block to avoid NameError
predicted_energy = None
cost = None
cO2 = None
peak = None
saving = None
eco_score = None

if predict_button and not df.empty:
    if log_reg_model is None:
        st.warning("Cannot make predictions: Logarithmic Regression model is not trained (dataset might be empty).")
    else:
        # =========================
        # PREDICTION - Using the Physics-informed Logarithmic Regression model
        # =========================
        # Calculate E_load for the current input
        current_E_load = (power * duration * devices) / 1000

        # Prepare input features for the residual model, ensuring correct order
        input_residual_features_df = pd.DataFrame(
            {
            "Temperature": [temp],
            "Humidity": [humidity],
            "Time": [hour],
            "Occupancy": [occu_pancy]
        })

        # Predict the residual energy (pipeline already log-transforms the inputs; output is in kWh)
        predicted_residual = log_reg_model.predict(input_residual_features_df)[0]

        # Combine E_load and predicted residual for the final energy prediction
        predicted_energy = current_E_load + predicted_residual
        predicted_energy = max(0, predicted_energy) # Ensure non-negative prediction

        # COST
        tariff = 8.4
        cost = predicted_energy * tariff

        # CO2
        emission_factor = 0.716
        co2 = predicted_energy * emission_factor

        # Peak Hour & Tariff Inefficiency
        peak_inefficiency = 0.02
        if 18 <= hour <= 21:
            peak = "6 PM - 9 PM"
            peak_inefficiency = 0.15 # Shift heavy loads away from evening peak tariff
        elif 12 <= hour <= 15:
            peak = "12 PM - 3 PM"
            peak_inefficiency = 0.09 # Midday solar-shift optimization
        elif 21 < hour <= 23:
            peak = "9 PM - 11 PM"
            peak_inefficiency = 0.05 # Late night wind down
        else:
            peak = "Low Demand"

        # Thermal & AC optimization inefficiency
        temp_inefficiency = 0.0
        if temp > 28:
            temp_inefficiency = min(0.12, (temp - 28) * 0.01)

        # Standby and phantom load inefficiency for multiple devices
        device_inefficiency = 0.0
        if devices > 2:
            device_inefficiency = min(0.08, (devices - 2) * 0.012)

        # Extended runtime duration inefficiency
        duration_inefficiency = 0.0
        if duration > 3:
            duration_inefficiency = min(0.07, (duration - 3) * 0.01)

        # High power rating equipment tuning inefficiency
        power_inefficiency = 0.0
        if power > 1500:
            power_inefficiency = min(0.05, ((power - 1500) / 1500.0) * 0.05)

        # Dynamic Saving Potential based on operational inefficiencies
        total_inefficiency = 0.04 + peak_inefficiency + temp_inefficiency + device_inefficiency + duration_inefficiency + power_inefficiency
        baseline = predicted_energy * (1.0 + total_inefficiency)
        saving = ((baseline - predicted_energy) / baseline) * 100
        saved_kwh = max(0.0, baseline - predicted_energy)
        saved_cost = saved_kwh * tariff
        saved_co2 = saved_kwh * emission_factor

        # Eco Score
        eco_score = max(0, 100 - (predicted_energy * 1.5 + co2 * 0.5))

        # =========================
        # SAVE PREDICTION HISTORY
        # =========================
        def save_prediction(data):
            df_new = pd.DataFrame([data])
            if os.path.exists(history_file):
                df_old = pd.read_csv(history_file)
                df_combined = pd.concat([df_old, df_new], ignore_index=True)
            else:
                df_combined = df_new
            df_combined.to_csv(history_file, index=False)

        prediction_record = {
            "Timestamp": pd.to_datetime('now'), # Added Timestamp for better history tracking
            "Temperature_Input": temp,
            "Humidity_Input": humidity,
            "PowerRating_Input": power,
            "UsageDuration_Input": duration,
            "NumDevices_Input": devices,
            "Occupancy_Input": occu_pancy,
            "Predicted_Energy_kWh": round(predicted_energy, 2),
            "Cost_INR": round(cost, 2),
            "CO2_kg": round(co2, 2),
            "PeakHour_Category": peak,
            "Saving_Percent": round(saving, 2),
            "Saved_kWh": round(saved_kwh, 2),
            "Saved_Cost_INR": round(saved_cost, 2),
            "Eco_Score": round(eco_score, 1)
        }

        save_prediction(prediction_record)

        # =========================
        # OUTPUT DASHBOARD
        # =========================
        col1, col2, col3 = st.columns(3)

        col1.metric("⚡ Energy Usage", f"{predicted_energy:.2f} kWh")
        col2.metric("💰 Cost", f"₹{cost:.2f}")
        col3.metric("🌍 CO₂", f"{co2:.2f} kg")

        col4, col5, col6 = st.columns(3)

        col4.metric("⏰ Peak Hour", peak)
        col5.metric("📉 Saving Potential", f"{saving:.2f}%", delta=f"-{saved_kwh:.2f} kWh (~₹{saved_cost:.1f})", delta_color="inverse")
        col6.metric("🌱 Eco Score", f"{eco_score:.1f}/100")

        # =========================
        # RECOMMENDATIONS (shown ONLY after a prediction has been made)
        # =========================
        if predicted_energy is not None:
            st.subheader("Recommendations")

            if predicted_energy > 25:
                st.warning("High energy usage detected. Reduce appliance overlap.")

            if temp > 32:
                st.info("High temperature detected. Optimize AC usage.")

            if eco_score < 60:
                st.error("Eco score is low. Improve efficiency.")

        # Modified download report section to include all historical data
        if os.path.exists(history_file):
            history_for_download_df = pd.read_csv(history_file)
            csv_for_download = history_for_download_df.to_csv(index=False)
            download_filename = "energy_prediction_history.csv"
        else:
            # Fallback (should not be reached if prediction was just saved)
            report_data_for_download = pd.DataFrame({
                "Predicted Energy":[predicted_energy],
                "Cost":[cost],
                "CO2":[co2],
                "Peak Hour":[peak],
                "Saving %":[saving],
                "Eco Score":[eco_score]
            })
            csv_for_download = report_data_for_download.to_csv(index=False)
            download_filename = "energy_report.csv"

        st.download_button(
            label="Download All Prediction History", # Updated label
            data=csv_for_download,
            file_name=download_filename,
            mime="text/csv"
        )

        if predicted_energy > 30:
            st.error("ALERT: Very high energy usage!")

        if cost > 300:
            st.warning("Electricity bill may be high today!")

        if co2 > 25:
            st.warning("Carbon footprint exceeds safe threshold.")
else: # If predict button is not clicked, or df is empty, display a message
    if df.empty:
        st.info("Please upload a dataset or ensure the sample dataset is loaded to enable predictions.")
    else:
        st.info("Adjust the parameters in the sidebar and click 'Predict Energy' to see the results.")


# =========================
# PREDICTION HISTORY DASHBOARD
# =========================
st.subheader("Prediction History")

if os.path.exists(history_file):
    history_df = pd.read_csv(history_file)
    st.write("Current Prediction History (editable):")

    # Use st.data_editor for interactive editing and deletion
    edited_history_df = st.data_editor(
        history_df,
        use_container_width=True,
        num_rows="dynamic", # Allows adding/deleting rows
        key="editable_prediction_history"
    )

    # Check if the edited DataFrame is different from the original and save if it is
    if not edited_history_df.equals(history_df):
        st.success("Changes detected! Saving updated history...")
        edited_history_df.to_csv(history_file, index=False)
        st.rerun() # Rerun to reflect changes and update the display

    # Optional: Plotting history
    if not history_df.empty:
        st.line_chart(history_df['Predicted_Energy_kWh'])
    else:
        st.info("History is empty.")

    # Add a button to clear all history
    if st.button("Clear All History", help="Permanently delete all prediction records."):
        if os.path.exists(history_file):
            os.remove(history_file)
            st.success("Prediction history cleared!")
            st.rerun()
else:
    st.info("No prediction history yet. Make some predictions!")


# =========================
# CHARTS
# =========================
st.subheader("Analytics")

if not df.empty:
    fig, ax = plt.subplots(figsize=(8,4))
    ax.plot(df["EnergyConsumption"][:30], marker='o')
    ax.set_title("Energy Consumption Trend")
    ax.set_xlabel("Days")
    ax.set_ylabel("kWh")
    st.pyplot(fig)

    # Appliance Consumption Chart
    appliances = ["AC", "Fan", "TV", "Fridge", "Lights"]
    values = [40, 15, 10, 20, 15]

    fig2, ax2 = plt.subplots(figsize=(6,4))
    ax2.bar(appliances, values)
    ax2.set_title("Appliance Consumption (%)")
    st.pyplot(fig2)
else:
    st.info("Upload a dataset to see analytics charts.")


# =========================
# ADMIN SECTION - Advanced Models
# =========================
if st.session_state.get("logged_in") and st.session_state.get("username") == "admin":
    st.subheader("Admin: Advanced Model Training & Evaluation")
    st.success("Admin access granted for advanced model features! Train and evaluate models below.")

    if not df.empty:
        # X_eval_all will contain original features + E_load for evaluation of physics-informed models
        X_eval_all = df[['Temperature', 'Humidity', 'Time', 'PowerRating', 'UsageDuration', 'NumDevices', 'Occupancy', 'E_load']]
        y_eval_all = df["EnergyConsumption"]

        # =========================
        # Random Forest MODEL FOR FUTURE PREDICTION (Admin Only)
        # =========================
        st.subheader("Random Forest Regressor")

        # Function to create lagged features for Random Forest
        def create_lagged_features_rf(data, lag_length):
            X, y = [], []
            if data.ndim > 1:
                data = data.flatten()
            for i in range(len(data) - lag_length):
                X.append(data[i:(i + lag_length)])
                y.append(data[i + lag_length])
            return np.array(X), np.array(y)

        # Prepare data for Random Forest (use 'EnergyConsumption' directly)
        rf_data = df['EnergyConsumption'].values # 1D numpy array

        lag_length = 10 # Define lag length for Random Forest input (similar to seq_length)

        if len(rf_data) >= lag_length + 1: # Ensure enough data
            X_rf, y_rf = create_lagged_features_rf(rf_data, lag_length)

            # Define Random Forest Model
            if 'rf_model' not in st.session_state or st.session_state.get('rf_model_df_hash') != hash(tuple(df.values.flatten())):
                rf_model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1) # n_jobs=-1 for parallel processing
                with st.spinner('Training Random Forest model... This might take a moment.'):
                    rf_model.fit(X_rf, y_rf)
                st.session_state.rf_model = rf_model
                st.session_state.lag_length_rf = lag_length
                st.session_state.rf_model_df_hash = hash(tuple(df.values.flatten()))
                st.success("Random Forest Model Trained and Ready!")
                # Evaluate and store metrics
                rf_metrics = evaluate_model(rf_model, X_rf, y_rf, "Random Forest") # Evaluate RF model with X_rf and y_rf
                if "model_metrics" not in st.session_state:
                    st.session_state.model_metrics = {}
                st.session_state.model_metrics["Random Forest"] = rf_metrics
            else:
                rf_model = st.session_state.rf_model
                lag_length = st.session_state.lag_length_rf
                st.info("Random Forest Model Loaded from session state.")

            # Random Forest Future Prediction UI
            st.sidebar.subheader("Random Forest Future Prediction")
            n_future_steps = st.sidebar.slider("Number of Future Steps (Random Forest)", 1, 30, 7)
            predict_future_button = st.sidebar.button("Predict Future Energy (RF)")

            if predict_future_button:
                # Get the last 'lag_length' data points for prediction
                last_sequence = rf_data[-lag_length:]

                future_predictions = []
                current_prediction_input = last_sequence

                for _ in range(n_future_steps):
                    # Predict the next step
                    next_step_prediction = rf_model.predict(current_prediction_input.reshape(1, -1))[0] # Reshape for single sample prediction
                    future_predictions.append(next_step_prediction)

                    # Update the input sequence by removing the first element and adding the new prediction
                    current_prediction_input = np.append(current_prediction_input[1:], next_step_prediction)

                # Create a DataFrame for plotting
                last_index = df.index[-1]
                future_indices = pd.RangeIndex(start=last_index + 1, stop=last_index + 1 + n_future_steps)

                future_df_plot = pd.DataFrame({
                    'Predicted Energy Consumption (kWh)': np.array(future_predictions)
                }, index=future_indices)

                # Combine historical and future data for plotting
                plot_data = pd.concat([df['EnergyConsumption'], future_df_plot['Predicted Energy Consumption (kWh)']])
                plot_data_df = pd.DataFrame({'Energy Consumption': plot_data})

                st.subheader(f"Random Forest Predicted Energy Consumption for next {n_future_steps} steps")
                st.dataframe(future_df_plot)
                st.line_chart(plot_data_df)
        else:
            st.warning(f"Not enough data in the current dataset to train Random Forest model with lag length {lag_length}. Need at least {lag_length + 1} data points to create features.")

    else:
        st.info("Upload a dataset to train advanced models.")

else:
    if st.session_state.get("logged_in"):
        st.info("You must be logged in as 'admin' to access advanced model features.")
    else:
        st.info("Log in as 'admin' to access advanced model features.")


# =========================
# MODEL PERFORMANCE COMPARISON (Available to all users)
# =========================
st.subheader("Model Performance Comparison")

if 'model_metrics' in st.session_state and st.session_state.model_metrics:
    metrics_df = pd.DataFrame(list(st.session_state.model_metrics.values()))

    if not metrics_df.empty:
        # Select the best model based on the maximum R2 score, as per user's request.
        best_model_name = metrics_df.loc[metrics_df['R2'].idxmax()]['Model']

        # Add a 'Best Model' column for highlighting
        metrics_df['Best Model'] = np.where(metrics_df['Model'] == best_model_name, '✅', '')

        st.dataframe(metrics_df.set_index('Model').style.highlight_max(axis=0, subset=['R2']).highlight_min(axis=0, subset=['MAE', 'MSE', 'RMSE', 'MAPE (%)'], props='background-color: lightgreen;'), use_container_width=True)

        st.info(f"The best performing model (based on R-squared) displayed is: **{best_model_name}**")
    else:
        st.info("No model performance data available yet. Log in as admin to train more models.")
else:
    st.info("No model performance data available yet. Make a prediction or log in as admin to train models.")


# =========================
# DATASET PREVIEW
# =========================
st.subheader(f"Dataset Preview: {st.session_state.get('selected_dataset_name', 'No Dataset Selected')}")

if 'original_df' in st.session_state and not st.session_state.original_df.empty:
    edited_df = st.data_editor(
        st.session_state.original_df,
        use_container_width=True,
        num_rows="dynamic",
        key="editable_sample_dataset"
    )

    if not edited_df.equals(st.session_state.original_df):
        st.session_state.original_df = edited_df.copy()
        if st.session_state.selected_dataset_name:
            st.session_state.uploaded_datasets[st.session_state.selected_dataset_name] = edited_df.copy()

        # Force a rerun to update models with the edited data
        st.success("Current dataset updated! Retraining models...")
        st.rerun()
elif st.session_state.get('selected_dataset_name') is None:
    st.info("Please upload a CSV or ensure the sample dataset is loaded to view and edit data.")


###csv file upload

st.sidebar.subheader("Upload Dataset")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV",
    type=["csv"],
    key="new_csv_uploader" # Unique key for this uploader
)

if uploaded_file is not None:
    file_name = uploaded_file.name
    try:
        new_df = pd.read_csv(uploaded_file)
        # Validate columns if necessary, or just proceed
        required_columns_check = [
            "Temperature", "Time", "Humidity", "PowerRating",
            "UsageDuration", "NumDevices", "Occupancy", "EnergyConsumption"
        ]
        if all(col in new_df.columns for col in required_columns_check):
            # Recalculate E_load and EnergyResidual for the uploaded df
            new_df['E_load'] = (new_df['PowerRating'] * new_df['UsageDuration'] * new_df['NumDevices']) / 1000
            new_df['EnergyResidual'] = new_df['EnergyConsumption'] - new_df['E_load']

            st.session_state.uploaded_datasets[file_name] = new_df.copy()
            st.session_state.selected_dataset_name = file_name # Set newly uploaded as active
            st.success(f"Dataset '{file_name}' uploaded successfully! Models will be retrained with new data.")
            st.rerun() # Rerun to reflect changes
        else:
            st.error(f"Uploaded CSV '{file_name}' is missing one or more required columns.")
            st.info(f"Required columns: {', '.join(required_columns_check)}")
    except Exception as e:
        st.error(f"Error processing uploaded file: {e}")

# Display count of uploaded datasets and selector
if st.session_state.uploaded_datasets:
    st.sidebar.info(f"Number of uploaded datasets: {len(st.session_state.uploaded_datasets)}")

    dataset_names = list(st.session_state.uploaded_datasets.keys())
    current_selection_index = 0
    if st.session_state.selected_dataset_name in dataset_names:
        current_selection_index = dataset_names.index(st.session_state.selected_dataset_name)

    selected_name = st.sidebar.selectbox(
        "Select active dataset:",
        dataset_names,
        index=current_selection_index,
        key="dataset_selector"
    )

    if selected_name != st.session_state.selected_dataset_name:
        st.session_state.selected_dataset_name = selected_name
        st.rerun() # Rerun to update the app with the new selected dataset

    # Only display head if a dataset is actually selected
    if st.session_state.selected_dataset_name:
        st.sidebar.dataframe(st.session_state.uploaded_datasets[st.session_state.selected_dataset_name].head())
