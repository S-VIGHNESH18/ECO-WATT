# projects info

---------------------------------------------------------------------------------------------------------------------------

## Energy Consumption Predictor - Summary

This Jupyter notebook is a Streamlit web application that predicts household energy consumption and provides sustainability insights. Here's what it does:

### Core Features

**Energy Prediction**
- Uses Linear Regression to predict energy consumption based on inputs like temperature, humidity, power rating, device count, and occupancy
- Generates predictions and calculates associated metrics

### Key Metrics Displayed

- ⚡ Energy usage (kWh)
- 💰 Cost in INR (₹)
- 🌍 CO₂ emissions (kg)
- ⏰ Peak hour category
- 📉 Saving potential (%)
- 🌱 Eco Score (0-100)

### User Features

- Login system with credentials (admin/vighnesh)
- Weather integration via OpenWeatherMap API to fetch current weather data
- Prediction history stored in CSV with editable/deletable records
- Dataset upload capability to use custom CSV data
- Interactive visualizations including energy trends and appliance consumption charts

### Admin-Only Features

- Random Forest model for time-series forecasting
- Future energy consumption predictions (up to 30 steps ahead)
- Model evaluation metrics (MAE, MSE, RMSE, R² Score)

### Data Management

- Editable sample dataset (200 synthetic records)
- Automatic model retraining when data is modified
- CSV report download for predictions

### Deployment

The notebook deploys the app to Google Colab using Streamlit + ngrok, creating a public URL to access the web interface.
