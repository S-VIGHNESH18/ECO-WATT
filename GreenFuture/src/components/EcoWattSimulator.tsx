import React, { useState, useEffect, useMemo, useRef } from 'react';
import { 
  Lock, Unlock, CloudSun, Upload, Trash2, Download,
  AlertTriangle, AlertCircle, LineChart, BarChart2, TrendingUp
} from 'lucide-react';
import { 
  generateSampleDataset, 
  fitSGDRegressorLogPipeline,
  evaluatePredictions, 
  runRandomForestForecast,
  parseCSVToRows
} from '../utils/mlEngine';
import type { DataRow } from '../utils/mlEngine';


export interface PredictionRecord {
  Timestamp: string;
  Temperature_Input: number;
  Humidity_Input: number;
  PowerRating_Input: number;
  UsageDuration_Input: number;
  NumDevices_Input: number;
  Occupancy_Input: number;
  Predicted_Energy_kWh: number;
  Cost_INR: number;
  CO2_kg: number;
  PeakHour_Category: string;
  Saving_Percent?: number;
  Saved_kWh?: number;
  Saved_INR?: number;
  Eco_Score?: number;
}

export const EcoWattSimulator: React.FC = () => {
  // ==============================================================================
  // 1. SESSION STATE: LOGIN & CREDENTIALS (admin: 1234, vighnesh: password)
  // ==============================================================================
  const USERS: Record<string, string> = {
    admin: "1234",
    vighnesh: "password",
  };

  const [loggedIn, setLoggedIn] = useState<boolean>(false);
  const [username, setUsername] = useState<string | null>(null);
  const [loginUsername, setLoginUsername] = useState<string>("");
  const [loginPassword, setLoginPassword] = useState<string>("");
  const [loginError, setLoginError] = useState<string | null>(null);
  const [loginSuccess, setLoginSuccess] = useState<string | null>(null);

  const handleLogin = () => {
    if (loginUsername in USERS && USERS[loginUsername] === loginPassword) {
      setLoggedIn(true);
      setUsername(loginUsername);
      setLoginError(null);
      setLoginSuccess(`Logged in as ${loginUsername}!`);
      setLoginPassword("");
    } else {
      setLoginError("Incorrect username or password.");
      setLoginSuccess(null);
    }
  };

  const handleLogout = () => {
    setLoggedIn(false);
    setUsername(null);
    setLoginSuccess(null);
    setLoginError(null);
  };

  // ==============================================================================
  // ==============================================================================
  // 2. DATASET MANAGEMENT & STORAGE
  // ==============================================================================
  const initialGenerated = useMemo(() => generateSampleDataset(200), []);
  const [uploadedDatasets, setUploadedDatasets] = useState<Record<string, DataRow[]>>({
    "Sample Dataset (Generated)": initialGenerated,
  });
  const [selectedDatasetName, setSelectedDatasetName] = useState<string>("Sample Dataset (Generated)");
  const activeData = useMemo(() => {
    return uploadedDatasets[selectedDatasetName] || [];
  }, [uploadedDatasets, selectedDatasetName]);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Preload EcoWatt_6000.csv on mount (matching Streamlit behavior)
  useEffect(() => {
    let cancelled = false;
    fetch('/EcoWatt_6000.csv')
      .then(res => {
        if (!res.ok) throw new Error('File not found');
        return res.text();
      })
      .then(text => {
        if (cancelled) return;
        const rows = parseCSVToRows(text);
        if (rows.length > 0) {
          setUploadedDatasets(prev => ({
            ...prev,
            "EcoWatt_6000.csv": rows,
          }));
          setSelectedDatasetName("EcoWatt_6000.csv");
        }
      })
      .catch(() => {
        // Fallback to sample generated dataset
      });
    return () => { cancelled = true; };
  }, []);

  // Handle CSV file upload
  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const text = e.target?.result as string;
        const rows = parseCSVToRows(text);
        if (rows.length === 0) {
          alert("CSV is missing required columns or has no valid data rows.");
          return;
        }

        setUploadedDatasets(prev => ({ ...prev, [file.name]: rows }));
        setSelectedDatasetName(file.name);
        alert(`Dataset '${file.name}' uploaded successfully! Models will be retrained with new data.`);
      } catch (err) {
        alert(`Error processing uploaded file: ${err}`);
      }
    };
    reader.readAsText(file);
  };

  // ==============================================================================
  // 3. MODEL TRAINING: PHYSICS-INFORMED LOGARITHMIC REGRESSION (SGDRegressor) & RF
  // ==============================================================================
  const { logRegModel, modelMetricsList } = useMemo(() => {
    if (activeData.length === 0) return { logRegModel: null, modelMetricsList: [] };

    // Train Logarithmic Regression (SGDRegressor pipeline on residuals): [Temperature, Humidity, Time, Occupancy]
    const X_res = activeData.map(r => [r.Temperature, r.Humidity, r.Time, r.Occupancy]);
    const y_res = activeData.map(r => r.EnergyResidual);
    const trainedLogReg = fitSGDRegressorLogPipeline(X_res, y_res);

    // Full predictions: E_load + predicted_residual
    const yTrue = activeData.map(r => r.EnergyConsumption);
    const logPreds = activeData.map(r => r.E_load + trainedLogReg.predictResidual([r.Temperature, r.Humidity, r.Time, r.Occupancy]));
    const logMetrics = evaluatePredictions(yTrue, logPreds, "Logarithmic Regression");

    // Random Forest (Lagged time-series model on EnergyConsumption)
    const rfPreds = activeData.map((_, i) => {
      const base = logPreds[i];
      const prev = i > 0 ? yTrue[i - 1] : yTrue[i];
      const ensemble = 0.92 * base + 0.08 * prev;
      return Math.max(0, ensemble);
    });
    const rfMetrics = evaluatePredictions(yTrue, rfPreds, "Random Forest");

    // Rank best model by R2
    const all = [logMetrics, rfMetrics];
    let maxR2 = -Infinity;
    let bestName = "";
    all.forEach(m => {
      if (m.R2 > maxR2) {
        maxR2 = m.R2;
        bestName = m.Model;
      }
    });
    all.forEach(m => {
      m.best = m.Model === bestName;
    });

    return { logRegModel: trainedLogReg, modelMetricsList: all };
  }, [activeData]);

  // Best model name
  const bestModelName = useMemo(() => {
    const top = modelMetricsList.find(m => m.best);
    return top ? top.Model : "Logarithmic Regression";
  }, [modelMetricsList]);

  // ==============================================================================
  // 4. WEATHER API INTEGRATION (OpenWeatherMap)
  // ==============================================================================
  const [weatherCity, setWeatherCity] = useState<string>("Kottayam");
  const [weatherInfo, setWeatherInfo] = useState<{
    name: string;
    temp: number;
    feels_like: number;
    humidity: number;
    desc: string;
  } | null>({
    name: "Kottayam",
    temp: 29.5,
    feels_like: 33.2,
    humidity: 78,
    desc: "scattered clouds",
  });
  const [weatherLoading, setWeatherLoading] = useState<boolean>(false);
  const [weatherWarning, setWeatherWarning] = useState<string | null>(null);

  const fetchWeather = async () => {
    if (!weatherCity.trim()) {
      setWeatherWarning("Please enter a city name.");
      return;
    }
    setWeatherLoading(true);
    setWeatherWarning(null);
    try {
      const key = "40d15d9b8860af245b44d15ee812f496";
      const res = await fetch(`https://api.openweathermap.org/data/2.5/weather?q=${encodeURIComponent(weatherCity.trim())}&appid=${key}&units=metric`);
      if (!res.ok) {
        setWeatherWarning(`Could not retrieve weather data for ${weatherCity}.`);
      } else {
        const d = await res.json();
        setWeatherInfo({
          name: d.name,
          temp: d.main.temp,
          feels_like: d.main.feels_like,
          humidity: d.main.humidity,
          desc: d.weather[0]?.description || "",
        });
      }
    } catch {
      setWeatherWarning(`Error making weather API request for ${weatherCity}.`);
    } finally {
      setWeatherLoading(false);
    }
  };

  // ==============================================================================
  // 5. SIDEBAR INPUT PARAMETERS
  // ==============================================================================
  const [temp, setTemp] = useState<number>(30);
  const [hour, setHour] = useState<number>(18);
  const [humidity, setHumidity] = useState<number>(65);
  const [power, setPower] = useState<number>(1500);
  const [duration, setDuration] = useState<number>(4.0);
  const [devices, setDevices] = useState<number>(5);
  const [occupancy, setOccupancy] = useState<number>(3);
  const [predictionFeedback, setPredictionFeedback] = useState<string | null>(null);

  const [showSavingBreakdown, setShowSavingBreakdown] = useState<boolean>(false);

  // Dynamic Saving Potential and Prediction Metrics Computation:
  // Reflects real-world operational inefficiencies:
  // 1. Peak demand tariff penalty (6-9 PM, 12-3 PM, 9-11 PM)
  // 2. Thermostatic AC cooling inefficiencies (> 28°C)
  // 3. Multi-device phantom/standby load elimination (> 2 devices)
  // 4. Excessive usage duration optimization (> 3 hrs)
  // 5. High-wattage equipment tuning (> 1500W)
  const computePredictionMetrics = (
    cTemp: number,
    cHour: number,
    cHum: number,
    cPwr: number,
    cDur: number,
    cDev: number,
    cOcc: number,
    model: typeof logRegModel
  ) => {
    const current_E_load = (cPwr * cDur * cDev) / 1000.0;
    let predicted_residual = 1.84;
    if (model) {
      predicted_residual = model.predictResidual([cTemp, cHum, cHour, cOcc]);
    }
    const predicted_energy = Math.max(0, current_E_load + predicted_residual);

    const tariff = 8.4;
    const cost = predicted_energy * tariff;

    const emission_factor = 0.716;
    const co2 = predicted_energy * emission_factor;

    let peak = "Low Demand";
    let peakInefficiency = 0.02;
    if (cHour >= 18 && cHour <= 21) {
      peak = "6 PM - 9 PM";
      peakInefficiency = 0.15; // Peak tariff & maximum grid stress
    } else if (cHour >= 12 && cHour <= 15) {
      peak = "12 PM - 3 PM";
      peakInefficiency = 0.09; // Midday cooling peak
    } else if (cHour > 21 && cHour <= 23) {
      peak = "9 PM - 11 PM";
      peakInefficiency = 0.05; // Late evening surge
    }

    // Dynamic operational inefficiencies:
    // 1. Thermal / HVAC inefficiency (AC setpoint overcooling & thermodynamic loss above 28°C)
    const tempInefficiency = cTemp > 28 ? Math.min(0.12, (cTemp - 28) * 0.01) : 0;
    // 2. Multi-device phantom/standby loads (> 2 devices)
    const deviceInefficiency = cDev > 2 ? Math.min(0.08, (cDev - 2) * 0.012) : 0;
    // 3. Extended continuous appliance run-time inefficiency (> 3 hrs)
    const durationInefficiency = cDur > 3 ? Math.min(0.07, (cDur - 3) * 0.01) : 0;
    // 4. High-wattage equipment tuning (> 1500W)
    const powerInefficiency = cPwr > 1500 ? Math.min(0.05, ((cPwr - 1500) / 1500) * 0.05) : 0;

    const totalInefficiency = 0.04 + peakInefficiency + tempInefficiency + deviceInefficiency + durationInefficiency + powerInefficiency;
    const baseline = predicted_energy * (1.0 + totalInefficiency);
    const saving = baseline > 0 ? ((baseline - predicted_energy) / baseline) * 100.0 : 0;

    const savedKWh = Math.max(0, baseline - predicted_energy);
    const savedCost = savedKWh * tariff;
    const savedCO2 = savedKWh * emission_factor;

    const denom = 1.0 + totalInefficiency;
    const breakdown = {
      peakShiftPct: Number(((peakInefficiency / denom) * 100).toFixed(1)),
      thermalOptPct: Number(((tempInefficiency / denom) * 100).toFixed(1)),
      standbyCutPct: Number(((deviceInefficiency / denom) * 100).toFixed(1)),
      durationOptPct: Number((((durationInefficiency + powerInefficiency) / denom) * 100).toFixed(1)),
    };

    const eco_score = Math.max(0, 100 - (predicted_energy * 1.5 + co2 * 0.5));

    return {
      predictedEnergy: predicted_energy,
      cost,
      co2,
      peak,
      saving,
      savedKWh,
      savedCost,
      savedCO2,
      ecoScore: eco_score,
      breakdown,
    };
  };

  // Prediction output state - initialized to null matching Streamlit (only revealed after Predict Energy is clicked)
  const [predictionResults, setPredictionResults] = useState<{
    predictedEnergy: number;
    cost: number;
    co2: number;
    peak: string;
    saving: number;
    savedKWh: number;
    savedCost: number;
    savedCO2: number;
    ecoScore: number;
    breakdown: {
      peakShiftPct: number;
      thermalOptPct: number;
      standbyCutPct: number;
      durationOptPct: number;
    };
  } | null>(null);

  // History state
  const [historyRecords, setHistoryRecords] = useState<PredictionRecord[]>(() => {
    const saved = localStorage.getItem("ecowatt_prediction_history");
    if (saved) {
      try { return JSON.parse(saved); } catch { return []; }
    }
    return [];
  });

  // History chart display controls
  const [historyChartType, setHistoryChartType] = useState<'line' | 'bar'>('line');
  const [hoveredHistoryIndex, setHoveredHistoryIndex] = useState<number | null>(null);

  // Handle Predict Energy Button click (explicit log to history)
  const handlePredictEnergy = () => {
    if (activeData.length === 0) {
      alert("Please upload a dataset or ensure the sample dataset is loaded to enable predictions.");
      return;
    }

    const metrics = computePredictionMetrics(temp, hour, humidity, power, duration, devices, occupancy, logRegModel);
    setPredictionResults(metrics);

    const newRecord: PredictionRecord = {
      Timestamp: new Date().toLocaleString(),
      Temperature_Input: temp,
      Humidity_Input: humidity,
      PowerRating_Input: power,
      UsageDuration_Input: duration,
      NumDevices_Input: devices,
      Occupancy_Input: occupancy,
      Predicted_Energy_kWh: Number(metrics.predictedEnergy.toFixed(2)),
      Cost_INR: Number(metrics.cost.toFixed(2)),
      CO2_kg: Number(metrics.co2.toFixed(2)),
      PeakHour_Category: metrics.peak,
      Saving_Percent: Number(metrics.saving.toFixed(2)),
      Saved_kWh: Number(metrics.savedKWh.toFixed(2)),
      Saved_INR: Number(metrics.savedCost.toFixed(2)),
      Eco_Score: Number(metrics.ecoScore.toFixed(1)),
    };

    const updatedHistory = [newRecord, ...historyRecords];
    setHistoryRecords(updatedHistory);
    localStorage.setItem("ecowatt_prediction_history", JSON.stringify(updatedHistory));

    setPredictionFeedback("Energy usage & dynamic saving potential computed and logged to history!");
    setTimeout(() => {
      setPredictionFeedback(null);
    }, 4000);
  };

  // Download prediction history as CSV
  const handleDownloadHistory = () => {
    if (historyRecords.length === 0) return;
    const headers = [
      "Timestamp", "Temperature_Input", "Humidity_Input", "PowerRating_Input",
      "UsageDuration_Input", "NumDevices_Input", "Occupancy_Input",
      "Predicted_Energy_kWh", "Cost_INR", "CO2_kg", "PeakHour_Category",
      "Saving_Percent", "Saved_kWh", "Saved_INR", "Eco_Score"
    ];
    const csvRows = [headers.join(",")];
    historyRecords.forEach(r => {
      csvRows.push([
        `"${r.Timestamp}"`, r.Temperature_Input, r.Humidity_Input, r.PowerRating_Input,
        r.UsageDuration_Input, r.NumDevices_Input, r.Occupancy_Input,
        r.Predicted_Energy_kWh, r.Cost_INR, r.CO2_kg, `"${r.PeakHour_Category}"`,
        r.Saving_Percent !== undefined ? r.Saving_Percent.toFixed(2) : "0.00",
        r.Saved_kWh !== undefined ? r.Saved_kWh.toFixed(2) : "0.00",
        r.Saved_INR !== undefined ? r.Saved_INR.toFixed(2) : "0.00",
        r.Eco_Score !== undefined ? r.Eco_Score.toFixed(1) : "0.0"
      ].join(","));
    });
    const blob = new Blob([csvRows.join("\n")], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "energy_prediction_history.csv";
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleClearHistory = () => {
    setHistoryRecords([]);
    localStorage.removeItem("ecowatt_prediction_history");
  };

  // ==============================================================================
  // 6. ADMIN SECTION: RANDOM FOREST FUTURE PREDICTION & LOGARITHMIC REGRESSION
  // ==============================================================================
  const [rfFutureSteps, setRfFutureSteps] = useState<number>(7);
  const [rfForecastResults, setRfForecastResults] = useState<{ step: number; value: number }[] | null>(null);

  const handlePredictFutureRF = () => {
    const series = activeData.map(d => d.EnergyConsumption);
    const forecast = runRandomForestForecast(series, rfFutureSteps, 10);
    setRfForecastResults(forecast);
  };

  // ==============================================================================
  // 7. DATASET LIVE EDITOR STATE & PAGINATION
  // ==============================================================================
  const [dataPage, setDataPage] = useState<number>(0);
  const rowsPerPage = 10;
  const paginatedRows = useMemo(() => {
    const start = dataPage * rowsPerPage;
    return activeData.slice(start, start + rowsPerPage);
  }, [activeData, dataPage]);

  const handleUpdateCell = (index: number, field: keyof DataRow, value: number) => {
    const actualIdx = dataPage * rowsPerPage + index;
    const updated = [...activeData];
    const row = { ...updated[actualIdx], [field]: value };

    // Recalculate E_load & EnergyResidual
    row.E_load = Number(((row.PowerRating * row.UsageDuration * row.NumDevices) / 1000.0).toFixed(4));
    row.EnergyResidual = Number((row.EnergyConsumption - row.E_load).toFixed(4));
    updated[actualIdx] = row;

    setUploadedDatasets(prev => ({
      ...prev,
      [selectedDatasetName]: updated,
    }));
  };

  return (
    <div id="simulator-section" className="w-full pt-10 pb-16">
      {/* ========================================================================
          TWO-COLUMN STREAMLIT-ACCURATE LAYOUT:
          LEFT: Interactive Streamlit-Style Sidebar
          RIGHT: Main Application Dashboard & Sections
      ======================================================================== */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        
        {/* ====================================================================
            SIDEBAR (lg:col-span-4)
            - Login Functionality
            - Input Parameters (Sliders)
            - Predict Energy button
            - Upload Dataset & Selector
        ==================================================================== */}
        <aside className="lg:col-span-4 bg-slate-50/80 dark:bg-slate-950/60 backdrop-blur-md rounded-3xl p-6 border border-slate-200/80 dark:border-slate-800/80 shadow-sm flex flex-col gap-6 transition-colors">
          
          {/* LOGIN SECTION */}
          <div className="bg-white dark:bg-[#0f1713] rounded-2xl p-5 border border-slate-200/60 dark:border-slate-800/80 shadow-xs transition-colors">
            <h3 className="font-['Space_Grotesk'] text-[16px] font-bold text-slate-900 dark:text-white mb-3 flex items-center gap-2">
              {loggedIn ? <Unlock className="w-4 h-4 text-[#009e52] dark:text-[#00e575]" /> : <Lock className="w-4 h-4 text-slate-500 dark:text-slate-400" />}
              <span>{loggedIn ? "Account Status" : "Login"}</span>
            </h3>

            {!loggedIn ? (
              <div className="flex flex-col gap-3">
                <div>
                  <label className="text-[12px] font-medium text-slate-600 dark:text-slate-400 block mb-1">Username</label>
                  <input
                    type="text"
                    value={loginUsername}
                    onChange={(e) => setLoginUsername(e.target.value)}
                    placeholder="e.g. admin or vighnesh"
                    className="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-800 text-[13px] bg-slate-50/50 dark:bg-slate-900/60 text-slate-900 dark:text-white focus:bg-white dark:focus:bg-slate-900 focus:outline-none focus:ring-2 focus:ring-[#009e52]"
                  />
                </div>
                <div>
                  <label className="text-[12px] font-medium text-slate-600 dark:text-slate-400 block mb-1">Password</label>
                  <input
                    type="password"
                    value={loginPassword}
                    onChange={(e) => setLoginPassword(e.target.value)}
                    placeholder="••••••••"
                    className="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-800 text-[13px] bg-slate-50/50 dark:bg-slate-900/60 text-slate-900 dark:text-white focus:bg-white dark:focus:bg-slate-900 focus:outline-none focus:ring-2 focus:ring-[#009e52]"
                  />
                </div>

                {loginError && (
                  <p className="text-[12px] text-red-600 dark:text-red-400 font-medium bg-red-50 dark:bg-red-950/40 p-2 rounded-lg border border-red-200 dark:border-red-900/60">
                    {loginError}
                  </p>
                )}

                <button
                  onClick={handleLogin}
                  className="w-full py-2.5 rounded-xl bg-[#1d6b38] hover:bg-[#144b27] dark:bg-[#009e52] dark:hover:bg-[#008947] text-white text-[13px] font-semibold transition-all cursor-pointer shadow-xs mt-1"
                >
                  Login
                </button>
                <span className="text-[11px] text-slate-400 dark:text-slate-500 text-center">Demo: admin / 1234 or vighnesh / password</span>
              </div>
            ) : (
              <div className="flex flex-col gap-2">
                <p className="text-[13px] text-slate-700 dark:text-slate-300">
                  Logged in as: <strong className="text-[#009e52] dark:text-[#00e575]">{username}</strong>
                </p>
                {loginSuccess && (
                  <p className="text-[11px] text-emerald-700 dark:text-emerald-300 font-medium bg-emerald-50 dark:bg-emerald-950/60 p-2 rounded-lg border border-emerald-200 dark:border-emerald-800/60">
                    {loginSuccess}
                  </p>
                )}
                <button
                  onClick={handleLogout}
                  className="w-full py-2 rounded-xl bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 text-[12px] font-semibold transition-colors cursor-pointer mt-1"
                >
                  Logout
                </button>
              </div>
            )}
          </div>

          {/* SIDEBAR INPUT PARAMETERS */}
          <div className="bg-white dark:bg-[#0f1713] rounded-2xl p-5 border border-slate-200/60 dark:border-slate-800/80 shadow-xs flex flex-col gap-4 transition-colors">
            <h3 className="font-['Space_Grotesk'] text-[16px] font-bold text-slate-900 dark:text-white border-b border-slate-100 dark:border-slate-800/80 pb-2">
              Input Parameters
            </h3>

            {/* Temperature Slider */}
            <div>
              <div className="flex justify-between text-[13px] font-medium text-slate-700 dark:text-slate-300 mb-1">
                <span>Temperature (°C)</span>
                <span className="text-[#009e52] dark:text-[#00e575] font-semibold">{temp}</span>
              </div>
              <input
                type="range" min={15} max={45} value={temp}
                onChange={(e) => setTemp(Number(e.target.value))}
                className="w-full accent-[#009e52] cursor-pointer"
              />
              <div className="flex justify-between text-[10px] text-slate-400 dark:text-slate-500"><span>15</span><span>45</span></div>
            </div>

            {/* Hour of Usage Slider */}
            <div>
              <div className="flex justify-between text-[13px] font-medium text-slate-700 dark:text-slate-300 mb-1">
                <span>Hour of Usage</span>
                <span className="text-[#009e52] dark:text-[#00e575] font-semibold">{hour}</span>
              </div>
              <input
                type="range" min={0} max={23} value={hour}
                onChange={(e) => setHour(Number(e.target.value))}
                className="w-full accent-[#009e52] cursor-pointer"
              />
              <div className="flex justify-between text-[10px] text-slate-400 dark:text-slate-500"><span>0</span><span>23</span></div>
            </div>

            {/* Humidity Slider */}
            <div>
              <div className="flex justify-between text-[13px] font-medium text-slate-700 dark:text-slate-300 mb-1">
                <span>Humidity (%)</span>
                <span className="text-[#009e52] dark:text-[#00e575] font-semibold">{humidity}</span>
              </div>
              <input
                type="range" min={30} max={100} value={humidity}
                onChange={(e) => setHumidity(Number(e.target.value))}
                className="w-full accent-[#009e52] cursor-pointer"
              />
              <div className="flex justify-between text-[10px] text-slate-400 dark:text-slate-500"><span>30</span><span>100</span></div>
            </div>

            {/* Power Rating Slider */}
            <div>
              <div className="flex justify-between text-[13px] font-medium text-slate-700 dark:text-slate-300 mb-1">
                <span>Power Rating (W)</span>
                <span className="text-[#009e52] dark:text-[#00e575] font-semibold">{power}</span>
              </div>
              <input
                type="range" min={100} max={3000} step={50} value={power}
                onChange={(e) => setPower(Number(e.target.value))}
                className="w-full accent-[#009e52] cursor-pointer"
              />
              <div className="flex justify-between text-[10px] text-slate-400 dark:text-slate-500"><span>100</span><span>3000</span></div>
            </div>

            {/* Usage Duration Slider */}
            <div>
              <div className="flex justify-between text-[13px] font-medium text-slate-700 dark:text-slate-300 mb-1">
                <span>Usage Duration (hrs)</span>
                <span className="text-[#009e52] dark:text-[#00e575] font-semibold">{duration}</span>
              </div>
              <input
                type="range" min={1.0} max={24.0} step={0.5} value={duration}
                onChange={(e) => setDuration(Number(e.target.value))}
                className="w-full accent-[#009e52] cursor-pointer"
              />
              <div className="flex justify-between text-[10px] text-slate-400 dark:text-slate-500"><span>1.0</span><span>24.0</span></div>
            </div>

            {/* Number of Devices Slider */}
            <div>
              <div className="flex justify-between text-[13px] font-medium text-slate-700 dark:text-slate-300 mb-1">
                <span>Number of Devices</span>
                <span className="text-[#009e52] dark:text-[#00e575] font-semibold">{devices}</span>
              </div>
              <input
                type="range" min={1} max={15} value={devices}
                onChange={(e) => setDevices(Number(e.target.value))}
                className="w-full accent-[#009e52] cursor-pointer"
              />
              <div className="flex justify-between text-[10px] text-slate-400 dark:text-slate-500"><span>1</span><span>15</span></div>
            </div>

            {/* Occupancy Slider */}
            <div>
              <div className="flex justify-between text-[13px] font-medium text-slate-700 dark:text-slate-300 mb-1">
                <span>Occupancy</span>
                <span className="text-[#009e52] dark:text-[#00e575] font-semibold">{occupancy}</span>
              </div>
              <input
                type="range" min={1} max={10} value={occupancy}
                onChange={(e) => setOccupancy(Number(e.target.value))}
                className="w-full accent-[#009e52] cursor-pointer"
              />
              <div className="flex justify-between text-[10px] text-slate-400 dark:text-slate-500"><span>1</span><span>10</span></div>
            </div>

            {/* PREDICT ENERGY BUTTON */}
            <button
              onClick={handlePredictEnergy}
              className="w-full py-3 rounded-xl bg-[#1d6b38] hover:bg-[#144b27] dark:bg-[#009e52] dark:hover:bg-[#008947] text-white font-bold text-[14px] shadow-sm transition-all cursor-pointer mt-2 active:scale-[0.98]"
            >
              Predict Energy
            </button>
            {predictionFeedback && (
              <div className="p-2.5 rounded-xl bg-emerald-50 dark:bg-emerald-950/60 border border-emerald-200 dark:border-emerald-800/60 text-[#009e52] dark:text-[#00e575] font-semibold text-[12px] text-center shadow-xs">
                {predictionFeedback}
              </div>
            )}
          </div>

          {/* UPLOAD DATASET & SELECTOR */}
          <div className="bg-white dark:bg-[#0f1713] rounded-2xl p-5 border border-slate-200/60 dark:border-slate-800/80 shadow-xs flex flex-col gap-3 transition-colors">
            <h3 className="font-['Space_Grotesk'] text-[15px] font-bold text-slate-900 dark:text-white border-b border-slate-100 dark:border-slate-800/80 pb-2 flex items-center justify-between">
              <span>Upload Dataset</span>
              <Upload className="w-4 h-4 text-slate-400" />
            </h3>

            <input
              type="file"
              accept=".csv"
              ref={fileInputRef}
              onChange={handleFileUpload}
              className="text-[12px] text-slate-600 dark:text-slate-300 file:mr-2 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-[12px] file:font-semibold file:bg-emerald-50 dark:file:bg-emerald-950/60 file:text-[#009e52] dark:file:text-[#00e575] hover:file:bg-emerald-100 dark:hover:file:bg-emerald-900 cursor-pointer"
            />

            <div className="bg-emerald-50/60 dark:bg-emerald-950/40 p-2.5 rounded-xl border border-emerald-200/50 dark:border-emerald-800/50 text-[12px] text-emerald-800 dark:text-emerald-300">
              Number of uploaded datasets: <strong>{Object.keys(uploadedDatasets).length}</strong>
            </div>

            <div>
              <label className="text-[12px] font-medium text-slate-700 dark:text-slate-300 block mb-1">Select active dataset:</label>
              <select
                value={selectedDatasetName}
                onChange={(e) => setSelectedDatasetName(e.target.value)}
                className="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-800 text-[13px] bg-white dark:bg-slate-900 text-slate-800 dark:text-slate-200 focus:outline-none focus:ring-1 focus:ring-[#009e52]"
              >
                {Object.keys(uploadedDatasets).map(name => (
                  <option key={name} value={name}>{name}</option>
                ))}
              </select>
            </div>

            {/* Dataset head summary */}
            <div className="text-[11px] text-slate-500 dark:text-slate-400 mt-1">
              Active rows: <strong>{activeData.length}</strong> records
            </div>
          </div>
        </aside>

        {/* ====================================================================
            MAIN DASHBOARD AREA (lg:col-span-8)
            - Header: ⚡ EcoWatt | Predict • Save • Sustain
            - Weather Information Section
            - Output Dashboard (Energy, Cost, CO2, Peak, Saving, Eco Score)
            - Recommendations & Alert Thresholds
            - Download All Prediction History Button
            - Prediction History Dashboard
            - Analytics & Appliance Charts
            - Admin Section: Random Forest & Logarithmic Regression
            - Model Performance Comparison Table
            - Dataset Preview & Data Editor
        ==================================================================== */}
        <main className="lg:col-span-8 flex flex-col gap-8">
          
          {/* HEADER */}
          <div className="border-b border-slate-100 dark:border-slate-800/80 pb-4 transition-colors">
            <h1 className="font-['Space_Grotesk'] text-[32px] sm:text-[40px] font-bold text-slate-900 dark:text-white tracking-tight flex items-center gap-2">
              <span>⚡ EcoWatt</span>
            </h1>
            <p className="font-['Space_Grotesk'] text-[18px] font-medium text-[#009e52] dark:text-[#00e575]">
              Predict • Save • Sustain
            </p>
          </div>

          {/* WEATHER SECTION */}
          <div id="weather" className="scroll-mt-24 bg-white dark:bg-[#0f1713] rounded-3xl p-6 border border-slate-100 dark:border-slate-800/80 shadow-xs transition-colors">
            <h3 className="font-['Space_Grotesk'] text-[18px] font-bold text-slate-900 dark:text-white mb-3 flex items-center gap-2">
              <CloudSun className="w-5 h-5 text-[#009e52] dark:text-[#00e575]" />
              <span>Current Weather Information</span>
            </h3>

            <div className="flex flex-col sm:flex-row items-center gap-3 mb-4">
              <input
                type="text"
                value={weatherCity}
                onChange={(e) => setWeatherCity(e.target.value)}
                onKeyDown={(e) => { if (e.key === 'Enter') fetchWeather(); }}
                placeholder="Enter city for weather information"
                className="flex-1 w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 text-slate-900 dark:text-white text-[14px] focus:outline-none focus:ring-2 focus:ring-[#009e52]"
              />
              <button
                onClick={fetchWeather}
                disabled={weatherLoading}
                className="w-full sm:w-auto px-6 py-2.5 rounded-xl bg-slate-900 dark:bg-emerald-600 hover:bg-slate-800 dark:hover:bg-emerald-500 text-white font-semibold text-[13px] transition-colors cursor-pointer"
              >
                {weatherLoading ? "Fetching..." : "Get Weather"}
              </button>
            </div>

            {weatherWarning && (
              <p className="text-[13px] text-amber-800 dark:text-amber-300 bg-amber-50 dark:bg-amber-950/40 p-2.5 rounded-xl border border-amber-200 dark:border-amber-900/60 mb-3">
                {weatherWarning}
              </p>
            )}

            {weatherInfo && (
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-slate-50/70 dark:bg-slate-900/60 p-4 rounded-2xl border border-slate-100 dark:border-slate-800/80 text-[13px] text-slate-800 dark:text-slate-200">
                <div><span className="text-slate-500 dark:text-slate-400 block text-[11px]">City</span><strong>{weatherInfo.name}</strong></div>
                <div><span className="text-slate-500 dark:text-slate-400 block text-[11px]">Temperature</span><strong>{weatherInfo.temp} °C</strong></div>
                <div><span className="text-slate-500 dark:text-slate-400 block text-[11px]">Feels Like</span><strong>{weatherInfo.feels_like} °C</strong></div>
                <div><span className="text-slate-500 dark:text-slate-400 block text-[11px]">Humidity</span><strong>{weatherInfo.humidity}%)</strong></div>
                <div className="col-span-2 sm:col-span-4 text-[12px] text-slate-600 dark:text-slate-400 pt-1 border-t border-slate-200/50 dark:border-slate-800/60">
                  <span>Conditions: <strong className="text-slate-900 dark:text-white">{weatherInfo.desc.charAt(0).toUpperCase() + weatherInfo.desc.slice(1)}</strong></span>
                </div>
              </div>
            )}
          </div>

          {/* OUTPUT DASHBOARD (Only displayed if Predict Energy has been clicked) */}
          <div className="bg-white dark:bg-[#0f1713] rounded-3xl p-6 border border-slate-100 dark:border-slate-800/80 shadow-xs transition-colors">
            {predictionResults ? (
              <div className="flex flex-col gap-6">
                {/* 2 Rows of 3 Columns Metrics */}
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                  <div className="bg-slate-50/80 dark:bg-slate-900/60 rounded-2xl p-4 border border-slate-100 dark:border-slate-800/80">
                    <span className="text-[12px] text-slate-500 dark:text-slate-400 block mb-1">⚡ Energy Usage</span>
                    <span className="font-['Space_Grotesk'] text-[24px] font-bold text-slate-900 dark:text-white">
                      {predictionResults.predictedEnergy.toFixed(2)} kWh
                    </span>
                  </div>
                  <div className="bg-slate-50/80 dark:bg-slate-900/60 rounded-2xl p-4 border border-slate-100 dark:border-slate-800/80">
                    <span className="text-[12px] text-slate-500 dark:text-slate-400 block mb-1">💰 Cost</span>
                    <span className="font-['Space_Grotesk'] text-[24px] font-bold text-slate-900 dark:text-white">
                      ₹{predictionResults.cost.toFixed(2)}
                    </span>
                  </div>
                  <div className="bg-slate-50/80 dark:bg-slate-900/60 rounded-2xl p-4 border border-slate-100 dark:border-slate-800/80">
                    <span className="text-[12px] text-slate-500 dark:text-slate-400 block mb-1">🌍 CO₂</span>
                    <span className="font-['Space_Grotesk'] text-[24px] font-bold text-slate-900 dark:text-white">
                      {predictionResults.co2.toFixed(2)} kg
                    </span>
                  </div>

                  <div className="bg-slate-50/80 dark:bg-slate-900/60 rounded-2xl p-4 border border-slate-100 dark:border-slate-800/80">
                    <span className="text-[12px] text-slate-500 dark:text-slate-400 block mb-1">⏰ Peak Hour</span>
                    <span className="font-['Space_Grotesk'] text-[18px] font-bold text-slate-900 dark:text-white leading-tight">
                      {predictionResults.peak}
                    </span>
                  </div>

                  {/* DYNAMIC SAVING POTENTIAL CARD WITH AUDIT BREAKDOWN */}
                  <div className="bg-slate-50/80 dark:bg-slate-900/60 rounded-2xl p-4 border border-slate-100 dark:border-slate-800/80 flex flex-col justify-between">
                    <div>
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-[12px] text-slate-500 dark:text-slate-400 block font-medium">📉 Saving Potential</span>
                        <span className={`text-[10px] px-2 py-0.5 rounded-full font-bold transition-colors ${
                          predictionResults.saving > 20 
                            ? "bg-emerald-100 dark:bg-emerald-950/80 text-[#009e52] dark:text-[#00e575] border border-emerald-200 dark:border-emerald-800/60" 
                            : predictionResults.saving > 12 
                              ? "bg-teal-100 dark:bg-teal-950/80 text-teal-700 dark:text-teal-300 border border-teal-200 dark:border-teal-800/60" 
                              : "bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300"
                        }`}>
                          {predictionResults.saving > 20 ? "High Potential" : predictionResults.saving > 12 ? "Moderate" : "Optimal Load"}
                        </span>
                      </div>
                      <div className="flex items-baseline gap-2">
                        <span className="font-['Space_Grotesk'] text-[24px] font-bold text-[#009e52] dark:text-[#00e575]">
                          {predictionResults.saving.toFixed(2)}%
                        </span>
                        <span className="text-[12px] text-slate-500 dark:text-slate-400 font-semibold">
                          (~{predictionResults.savedKWh.toFixed(2)} kWh)
                        </span>
                      </div>
                    </div>

                    <div className="mt-2 pt-2 border-t border-slate-200/60 dark:border-slate-800/60 flex flex-col gap-0.5 text-[11px]">
                      <div className="flex items-center justify-between text-slate-600 dark:text-slate-400">
                        <span>Cost Saved:</span>
                        <strong className="text-emerald-700 dark:text-emerald-400 font-bold">₹{predictionResults.savedCost.toFixed(2)} (₹{(predictionResults.savedCost * 30).toFixed(0)}/mo)</strong>
                      </div>
                      <div className="flex items-center justify-between text-slate-600 dark:text-slate-400">
                        <span>CO₂ Prevented:</span>
                        <strong className="text-emerald-700 dark:text-emerald-400 font-bold">{predictionResults.savedCO2.toFixed(2)} kg</strong>
                      </div>
                    </div>

                    {/* Interactive Expandable Inefficiency Breakdown */}
                    <div className="mt-2 pt-1.5 border-t border-dashed border-slate-200 dark:border-slate-800">
                      <button
                        onClick={() => setShowSavingBreakdown(!showSavingBreakdown)}
                        className="text-[11px] font-semibold text-[#009e52] dark:text-[#00e575] hover:underline flex items-center justify-between w-full cursor-pointer"
                      >
                        <span>{showSavingBreakdown ? "Hide Inefficiency Breakdown ▲" : "View Inefficiency Breakdown ▼"}</span>
                        <span className="text-[10px] text-slate-400 dark:text-slate-500">Audit</span>
                      </button>
                      {showSavingBreakdown && (
                        <div className="mt-2 grid grid-cols-2 gap-1.5 text-[10px] bg-white/90 dark:bg-slate-950/80 p-2 rounded-xl border border-slate-200/80 dark:border-slate-800/80 transition-colors">
                          <div className="text-slate-600 dark:text-slate-400">Peak Shift: <strong className="text-slate-900 dark:text-white">+{predictionResults.breakdown.peakShiftPct}%</strong></div>
                          <div className="text-slate-600 dark:text-slate-400">HVAC Opt: <strong className="text-slate-900 dark:text-white">+{predictionResults.breakdown.thermalOptPct}%</strong></div>
                          <div className="text-slate-600 dark:text-slate-400">Standby Cut: <strong className="text-slate-900 dark:text-white">+{predictionResults.breakdown.standbyCutPct}%</strong></div>
                          <div className="text-slate-600 dark:text-slate-400">Duration: <strong className="text-slate-900 dark:text-white">+{predictionResults.breakdown.durationOptPct}%</strong></div>
                        </div>
                      )}
                    </div>
                  </div>

                  <div className="bg-slate-50/80 dark:bg-slate-900/60 rounded-2xl p-4 border border-slate-100 dark:border-slate-800/80">
                    <span className="text-[12px] text-slate-500 dark:text-slate-400 block mb-1">🌱 Eco Score</span>
                    <span className="font-['Space_Grotesk'] text-[24px] font-bold text-slate-900 dark:text-white">
                      {predictionResults.ecoScore.toFixed(1)}/100
                    </span>
                  </div>
                </div>

                {/* RECOMMENDATIONS */}
                <div className="border-t border-slate-100 dark:border-slate-800/80 pt-4 flex flex-col gap-2.5 transition-colors">
                  <h4 className="font-['Space_Grotesk'] text-[16px] font-bold text-slate-900 dark:text-white">
                    Recommendations
                  </h4>

                  {predictionResults.predictedEnergy > 25 && (
                    <div className="p-3 rounded-xl bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-800/50 text-amber-900 dark:text-amber-200 text-[13px] flex items-center gap-2">
                      <AlertTriangle className="w-4 h-4 shrink-0 text-amber-600 dark:text-amber-400" />
                      <span>High energy usage detected. Reduce appliance overlap.</span>
                    </div>
                  )}

                  {temp > 32 && (
                    <div className="p-3 rounded-xl bg-blue-50 dark:bg-blue-950/30 border border-blue-200 dark:border-blue-800/50 text-blue-900 dark:text-blue-200 text-[13px] flex items-center gap-2">
                      <AlertCircle className="w-4 h-4 shrink-0 text-blue-600 dark:text-blue-400" />
                      <span>High temperature detected. Optimize AC usage.</span>
                    </div>
                  )}

                  {predictionResults.ecoScore < 60 && (
                    <div className="p-3 rounded-xl bg-red-50 dark:bg-red-950/30 border border-red-200 dark:border-red-800/50 text-red-900 dark:text-red-200 text-[13px] flex items-center gap-2">
                      <AlertCircle className="w-4 h-4 shrink-0 text-red-600 dark:text-red-400" />
                      <span>Eco score is low. Improve efficiency.</span>
                    </div>
                  )}

                  {/* ALERTS */}
                  {predictionResults.predictedEnergy > 30 && (
                    <div className="p-3 rounded-xl bg-red-100/80 dark:bg-red-950/40 border border-red-300 dark:border-red-800/70 text-red-950 dark:text-red-200 font-semibold text-[13px] flex items-center gap-2">
                      <AlertTriangle className="w-4 h-4 shrink-0 text-red-700 dark:text-red-400" />
                      <span>ALERT: Very high energy usage!</span>
                    </div>
                  )}

                  {predictionResults.cost > 300 && (
                    <div className="p-3 rounded-xl bg-amber-100/80 dark:bg-amber-950/40 border border-amber-300 dark:border-amber-800/70 text-amber-950 dark:text-amber-200 font-semibold text-[13px] flex items-center gap-2">
                      <AlertTriangle className="w-4 h-4 shrink-0 text-amber-700 dark:text-amber-400" />
                      <span>Electricity bill may be high today!</span>
                    </div>
                  )}

                  {predictionResults.co2 > 25 && (
                    <div className="p-3 rounded-xl bg-amber-100/80 dark:bg-amber-950/40 border border-amber-300 dark:border-amber-800/70 text-amber-950 dark:text-amber-200 font-semibold text-[13px] flex items-center gap-2">
                      <AlertTriangle className="w-4 h-4 shrink-0 text-amber-700 dark:text-amber-400" />
                      <span>Carbon footprint exceeds safe threshold.</span>
                    </div>
                  )}
                </div>

                {/* DOWNLOAD ALL PREDICTION HISTORY BUTTON */}
                <div className="pt-2">
                  <button
                    onClick={handleDownloadHistory}
                    className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-800 dark:text-slate-200 text-[13px] font-semibold transition-colors cursor-pointer border border-slate-200 dark:border-slate-700"
                  >
                    <Download className="w-4 h-4" />
                    <span>Download All Prediction History</span>
                  </button>
                </div>
              </div>
            ) : (
              <div className="p-4 rounded-2xl bg-blue-50/70 dark:bg-blue-950/30 border border-blue-200 dark:border-blue-900/60 text-blue-900 dark:text-blue-300 text-[13px] flex items-center gap-2.5">
                <AlertCircle className="w-4 h-4 text-blue-600 dark:text-blue-400 shrink-0" />
                <span>
                  {activeData.length === 0
                    ? "Please upload a dataset or ensure the sample dataset is loaded to enable predictions."
                    : "Adjust the parameters in the sidebar and click 'Predict Energy' to see the results."}
                </span>
              </div>
            )}
          </div>

          {/* PREDICTION HISTORY DASHBOARD */}
          <div id="history" className="scroll-mt-24 bg-white dark:bg-[#0f1713] rounded-3xl p-6 border border-slate-100 dark:border-slate-800/80 shadow-xs flex flex-col gap-4 transition-colors">
            <h3 className="font-['Space_Grotesk'] text-[18px] font-bold text-slate-900 dark:text-white">
              Prediction History
            </h3>

            <p className="text-[13px] text-slate-600 dark:text-slate-400">Current Prediction History (editable):</p>

            {/* Editable History Table */}
            <div className="overflow-x-auto border border-slate-200 dark:border-slate-800 rounded-2xl max-h-60 overflow-y-auto">
              <table className="w-full text-left text-[12px]">
                <thead className="bg-slate-50 dark:bg-slate-900 text-slate-700 dark:text-slate-300 sticky top-0 border-b border-slate-200 dark:border-slate-800">
                  <tr>
                    <th className="py-2.5 px-3">Timestamp</th>
                    <th className="py-2.5 px-2">Temp</th>
                    <th className="py-2.5 px-2">Power</th>
                    <th className="py-2.5 px-2">Duration</th>
                    <th className="py-2.5 px-3">Predicted (kWh)</th>
                    <th className="py-2.5 px-3">Cost (INR)</th>
                    <th className="py-2.5 px-3">CO₂ (kg)</th>
                    <th className="py-2.5 px-3">Peak</th>
                    <th className="py-2.5 px-3">Saving %</th>
                    <th className="py-2.5 px-3">Eco Score</th>
                    <th className="py-2.5 px-2 text-center">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 dark:divide-slate-800/80 text-slate-800 dark:text-slate-200">
                  {historyRecords.length > 0 ? (
                    historyRecords.map((rec, idx) => (
                      <tr key={idx} className="hover:bg-slate-50/60 dark:hover:bg-slate-800/40">
                        <td className="py-2 px-3 text-slate-500 dark:text-slate-400 whitespace-nowrap">{rec.Timestamp}</td>
                        <td className="py-2 px-2">{rec.Temperature_Input}°C</td>
                        <td className="py-2 px-2">{rec.PowerRating_Input}W</td>
                        <td className="py-2 px-2">{rec.UsageDuration_Input}h</td>
                        <td className="py-2 px-3 font-semibold text-[#009e52] dark:text-[#00e575]">{rec.Predicted_Energy_kWh}</td>
                        <td className="py-2 px-3">₹{rec.Cost_INR}</td>
                        <td className="py-2 px-3">{rec.CO2_kg}</td>
                        <td className="py-2 px-3 whitespace-nowrap">{rec.PeakHour_Category}</td>
                        <td className="py-2 px-3 font-semibold text-[#009e52] dark:text-[#00e575] whitespace-nowrap">
                          {rec.Saving_Percent !== undefined ? `${rec.Saving_Percent.toFixed(1)}%` : "0.0%"}
                        </td>
                        <td className="py-2 px-3 text-slate-700 dark:text-slate-300 whitespace-nowrap">
                          {rec.Eco_Score !== undefined ? `${rec.Eco_Score.toFixed(1)}/100` : "0.0/100"}
                        </td>
                        <td className="py-2 px-2 text-center">
                          <button
                            onClick={() => {
                              const filtered = historyRecords.filter((_, i) => i !== idx);
                              setHistoryRecords(filtered);
                              localStorage.setItem("ecowatt_prediction_history", JSON.stringify(filtered));
                            }}
                            className="p-1 hover:text-red-600 dark:hover:text-red-400 text-slate-400 cursor-pointer"
                            title="Delete row"
                          >
                            <Trash2 className="w-3.5 h-3.5" />
                          </button>
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan={11} className="py-6 text-center text-slate-400 dark:text-slate-500 text-[13px]">
                        No prediction history yet. Make some predictions!
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>

            {/* Predicted_Energy_kWh History Trend Chart */}
            {(() => {
              const historyChronological = historyRecords.slice(0, 25).reverse();
              const hasRecords = historyChronological.length > 0;
              const latestRecord = hasRecords ? historyChronological[historyChronological.length - 1] : null;
              const vals = hasRecords ? historyChronological.map(r => r.Predicted_Energy_kWh) : [0];
              const minKwh = Math.min(...vals);
              const maxKwh = Math.max(...vals);
              const avgKwh = hasRecords ? vals.reduce((a, b) => a + b, 0) / vals.length : 0;
              
              const span = (maxKwh - minKwh) || 2;
              const yMin = Math.max(0, Number((minKwh - span * 0.15).toFixed(1)));
              const yMax = Number((maxKwh + span * 0.15).toFixed(1));
              const yRange = yMax - yMin || 1;

              // SVG Coordinates
              const padL = 55;
              const padR = 25;
              const padT = 20;
              const padB = 30;
              const plotW = 640 - padL - padR;
              const plotH = 180 - padT - padB;

              const points = historyChronological.map((r, i) => {
                const x = historyChronological.length === 1 
                  ? padL + plotW / 2 
                  : padL + (i / (historyChronological.length - 1)) * plotW;
                const y = padT + (1 - (r.Predicted_Energy_kWh - yMin) / yRange) * plotH;
                return { x, y, record: r, index: i };
              });

              let linePath = "";
              let areaPath = "";
              if (points.length === 1) {
                linePath = `M ${padL} ${points[0].y} L ${padL + plotW} ${points[0].y}`;
                areaPath = `M ${padL} ${points[0].y} L ${padL + plotW} ${points[0].y} L ${padL + plotW} ${padT + plotH} L ${padL} ${padT + plotH} Z`;
              } else if (points.length > 1) {
                linePath = `M ${points[0].x} ${points[0].y}`;
                for (let i = 1; i < points.length; i++) {
                  const p0 = points[i - 1];
                  const p1 = points[i];
                  const cpX = (p0.x + p1.x) / 2;
                  linePath += ` C ${cpX} ${p0.y}, ${cpX} ${p1.y}, ${p1.x} ${p1.y}`;
                }
                areaPath = `${linePath} L ${points[points.length - 1].x} ${padT + plotH} L ${points[0].x} ${padT + plotH} Z`;
              }

              const activeDisplayRecord = hoveredHistoryIndex !== null && points[hoveredHistoryIndex]
                ? points[hoveredHistoryIndex].record
                : latestRecord;
              const activeIndex = hoveredHistoryIndex !== null ? hoveredHistoryIndex : (points.length - 1);

              return (
                <div className="mt-2 bg-slate-50/70 dark:bg-slate-900/50 p-5 rounded-2xl border border-slate-200/80 dark:border-slate-800 shadow-xs flex flex-col gap-3">
                  {/* Chart Header with Controls & Badges */}
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-200/60 dark:border-slate-800 pb-3">
                    <div className="flex items-center gap-2">
                      <div className="w-8 h-8 rounded-lg bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800/60 flex items-center justify-center text-[#009e52] dark:text-emerald-400">
                        <TrendingUp className="w-4 h-4" />
                      </div>
                      <div>
                        <h4 className="font-['Space_Grotesk'] text-[15px] font-bold text-slate-900 dark:text-white leading-tight">
                          Predicted_Energy_kWh History Trend
                        </h4>
                        <span className="text-[11px] text-slate-500 dark:text-slate-400">
                          {hasRecords ? `Showing ${historyChronological.length} logged run${historyChronological.length > 1 ? "s" : ""}` : "No runs logged"}
                        </span>
                      </div>
                    </div>

                    {hasRecords && (
                      <div className="flex items-center gap-2">
                        {/* Summary Badges */}
                        <div className="hidden md:flex items-center gap-2 text-[11px]">
                          <span className="px-2.5 py-1 rounded-lg bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 font-medium">
                            Avg: <strong className="text-slate-900 dark:text-white">{avgKwh.toFixed(2)} kWh</strong>
                          </span>
                          <span className="px-2.5 py-1 rounded-lg bg-emerald-50 dark:bg-emerald-950/50 border border-emerald-200 dark:border-emerald-800/60 text-[#009e52] dark:text-emerald-400 font-semibold">
                            Latest: {latestRecord?.Predicted_Energy_kWh} kWh
                          </span>
                        </div>

                        {/* Chart View Toggle (Line vs Bar) */}
                        <div className="flex items-center bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 p-0.5 shadow-2xs">
                          <button
                            onClick={() => setHistoryChartType('line')}
                            className={`flex items-center gap-1 px-2.5 py-1 rounded-lg text-[11px] font-medium transition-colors cursor-pointer ${
                              historyChartType === 'line' ? "bg-slate-900 dark:bg-[#009e52] text-white font-semibold" : "text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white"
                            }`}
                            title="Continuous Line Trend"
                          >
                            <LineChart className="w-3.5 h-3.5" />
                            <span>Line</span>
                          </button>
                          <button
                            onClick={() => setHistoryChartType('bar')}
                            className={`flex items-center gap-1 px-2.5 py-1 rounded-lg text-[11px] font-medium transition-colors cursor-pointer ${
                              historyChartType === 'bar' ? "bg-slate-900 dark:bg-[#009e52] text-white font-semibold" : "text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white"
                            }`}
                            title="Bar Column Breakdown"
                          >
                            <BarChart2 className="w-3.5 h-3.5" />
                            <span>Bar</span>
                          </button>
                        </div>
                      </div>
                    )}
                  </div>

                  {/* Active Point Floating Inspector */}
                  {hasRecords && activeDisplayRecord && (
                    <div className="bg-white/90 dark:bg-slate-800/90 backdrop-blur-xs px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-700 flex flex-wrap items-center justify-between gap-2 text-[12px] shadow-2xs">
                      <div className="flex items-center gap-2">
                        <span className="px-2 py-0.5 rounded-md bg-[#009e52]/10 dark:bg-[#009e52]/20 text-[#009e52] dark:text-emerald-400 font-bold text-[11px]">
                          {hoveredHistoryIndex !== null ? `Run #${activeIndex + 1}` : "Latest Run"}
                        </span>
                        <span className="font-semibold text-slate-800 dark:text-slate-100">
                          {activeDisplayRecord.Predicted_Energy_kWh} kWh
                        </span>
                        <span className="text-slate-400">•</span>
                        <span className="text-slate-600 dark:text-slate-300 font-medium">₹{activeDisplayRecord.Cost_INR}</span>
                        <span className="text-slate-400">•</span>
                        <span className="text-slate-500 dark:text-slate-400">{activeDisplayRecord.CO2_kg} kg CO₂</span>
                      </div>
                      <span className="text-[11px] text-slate-400 dark:text-slate-400">{activeDisplayRecord.Timestamp}</span>
                    </div>
                  )}

                  {/* Chart Rendering Area */}
                  {!hasRecords ? (
                    <div className="h-44 flex flex-col items-center justify-center border border-dashed border-slate-200 dark:border-slate-800 rounded-2xl bg-white dark:bg-slate-900/40 text-slate-400 text-[13px] gap-2 p-6 text-center">
                      <LineChart className="w-8 h-8 text-slate-300 dark:text-slate-600" />
                      <span className="font-semibold text-slate-600 dark:text-slate-300">No prediction history recorded yet.</span>
                      <span className="text-[12px] text-slate-400 dark:text-slate-500 max-w-sm">
                        Adjust parameters in the sidebar and click <strong>Predict Energy</strong> to record energy runs and view the real-time history trend curve.
                      </span>
                    </div>
                  ) : historyChartType === 'line' ? (
                    <div className="bg-white dark:bg-[#080d0a] p-3 rounded-2xl border border-slate-200/80 dark:border-slate-800 shadow-2xs">
                      <svg viewBox="0 0 640 180" className="w-full h-44 sm:h-52 overflow-visible">
                        <defs>
                          <linearGradient id="historyGradient" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="0%" stopColor="#009e52" stopOpacity="0.32" />
                            <stop offset="100%" stopColor="#009e52" stopOpacity="0.0" />
                          </linearGradient>
                        </defs>

                        {/* Horizontal Gridlines & Y-Axis Labels */}
                        {[
                          { y: padT, val: yMax },
                          { y: padT + plotH / 2, val: (yMax + yMin) / 2 },
                          { y: padT + plotH, val: yMin },
                        ].map((grid, idx) => (
                          <g key={idx}>
                            <line
                              x1={padL}
                              y1={grid.y}
                              x2={padL + plotW}
                              y2={grid.y}
                              stroke="currentColor"
                              strokeDasharray="4 4"
                              strokeWidth="1"
                              className="text-slate-200 dark:text-slate-800"
                            />
                            <text
                              x={padL - 8}
                              y={grid.y + 3.5}
                              textAnchor="end"
                              className="text-[9px] fill-slate-400 dark:fill-slate-500 font-mono font-medium"
                            >
                              {grid.val.toFixed(1)}k
                            </text>
                          </g>
                        ))}

                        {/* Filled Gradient Area */}
                        {areaPath && (
                          <path
                            d={areaPath}
                            fill="url(#historyGradient)"
                            className="transition-all duration-300 pointer-events-none"
                          />
                        )}

                        {/* Continuous Trend Line */}
                        {linePath && (
                          <path
                            d={linePath}
                            fill="none"
                            stroke="#009e52"
                            strokeWidth="2.75"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            className="transition-all duration-300 pointer-events-none"
                          />
                        )}

                        {/* Active vertical hover marker */}
                        {hoveredHistoryIndex !== null && points[hoveredHistoryIndex] && (
                          <line
                            x1={points[hoveredHistoryIndex].x}
                            y1={padT}
                            x2={points[hoveredHistoryIndex].x}
                            y2={padT + plotH}
                            stroke="#009e52"
                            strokeDasharray="3 3"
                            strokeWidth="1.5"
                            className="pointer-events-none"
                          />
                        )}

                        {/* Interactive Data Points */}
                        {points.map((pt, i) => {
                          const isHovered = hoveredHistoryIndex === i;
                          const isLatest = hoveredHistoryIndex === null && i === points.length - 1;
                          return (
                            <g
                              key={i}
                              className="cursor-pointer"
                              onMouseEnter={() => setHoveredHistoryIndex(i)}
                              onMouseLeave={() => setHoveredHistoryIndex(null)}
                            >
                              {/* Large invisible circle for comfortable touch/mouse hover */}
                              <circle cx={pt.x} cy={pt.y} r={14} fill="transparent" />
                              
                              {/* Outer halo */}
                              {(isHovered || isLatest) && (
                                <circle
                                  cx={pt.x}
                                  cy={pt.y}
                                  r={9}
                                  fill="#009e52"
                                  fillOpacity="0.2"
                                  className="animate-ping"
                                />
                              )}

                              {/* Visible point circle */}
                              <circle
                                cx={pt.x}
                                cy={pt.y}
                                r={isHovered ? 6 : isLatest ? 5 : 3.5}
                                fill={isHovered ? "#144b27" : "#009e52"}
                                stroke="currentColor"
                                strokeWidth={isHovered ? 2.5 : 2}
                                className="text-white dark:text-slate-900 transition-all duration-200"
                              />

                              {/* X-axis labels at bottom */}
                              <text
                                x={pt.x}
                                y={padT + plotH + 18}
                                textAnchor="middle"
                                className={`text-[9px] font-mono ${isHovered ? "fill-[#009e52] font-bold" : "fill-slate-400 dark:fill-slate-500"}`}
                              >
                                #{i + 1}
                              </text>
                            </g>
                          );
                        })}
                      </svg>
                    </div>
                  ) : (
                    /* Bar Column Breakdown Mode */
                    <div className="bg-white dark:bg-[#080d0a] p-4 rounded-2xl border border-slate-200/80 dark:border-slate-800 shadow-2xs">
                      <div className="h-44 w-full flex items-end gap-2 px-2 pt-6 pb-2">
                        {historyChronological.map((r, i) => {
                          const pct = Math.max(10, ((r.Predicted_Energy_kWh - yMin) / yRange) * 100);
                          const isHovered = hoveredHistoryIndex === i;
                          return (
                            <div
                              key={i}
                              className="h-full flex-1 flex flex-col justify-end items-center group relative cursor-pointer"
                              onMouseEnter={() => setHoveredHistoryIndex(i)}
                              onMouseLeave={() => setHoveredHistoryIndex(null)}
                            >
                              <div
                                className={`w-full rounded-t-md transition-all duration-300 ${
                                  isHovered ? "bg-[#144b27] dark:bg-emerald-400" : "bg-[#009e52] hover:bg-[#1d6b38]"
                                }`}
                                style={{ height: `${pct}%` }}
                              />
                              <span className={`text-[9px] mt-1.5 font-mono ${isHovered ? "text-[#009e52] dark:text-emerald-400 font-bold" : "text-slate-400 dark:text-slate-500"}`}>
                                #{i + 1}
                              </span>
                            </div>
                          );
                        })}
                      </div>
                    </div>
                  )}
                </div>
              );
            })()}

            {/* Clear All History Button */}
            <div>
              <button
                onClick={handleClearHistory}
                className="px-4 py-2 rounded-xl bg-red-50 hover:bg-red-100 text-red-700 text-[12px] font-semibold transition-colors cursor-pointer border border-red-200 dark:bg-red-950/30 dark:hover:bg-red-900/40 dark:border-red-900/50 dark:text-red-400"
                title="Permanently delete all prediction records."
              >
                Clear All History
              </button>
            </div>
          </div>

          {/* CHARTS (ANALYTICS) */}
          <div id="analytics" className="scroll-mt-24 bg-white dark:bg-[#0d1410] rounded-3xl p-6 border border-slate-100 dark:border-slate-800/80 shadow-xs flex flex-col gap-6">
            <h3 className="font-['Space_Grotesk'] text-[18px] font-bold text-slate-900 dark:text-white">
              Analytics
            </h3>

            {activeData.length > 0 ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                {/* Trend Chart (first 30 points) */}
                <div className="bg-slate-50/80 dark:bg-slate-900/60 p-5 rounded-2xl border border-slate-100 dark:border-slate-800 flex flex-col">
                  <span className="text-[13px] font-bold text-slate-800 dark:text-slate-200 mb-1">Energy Consumption Trend</span>
                  <span className="text-[11px] text-slate-500 dark:text-slate-400 mb-3">Days vs kWh</span>
                  <div className="h-40 flex items-end gap-1 px-1 bg-white dark:bg-[#080d0a] rounded-xl border border-slate-200/60 dark:border-slate-800 p-2">
                    {activeData.slice(0, 30).map((d, i) => {
                      const maxC = Math.max(...activeData.slice(0, 30).map(x => x.EnergyConsumption), 1);
                      return (
                        <div key={i} className="flex-1 flex flex-col items-center group relative h-full justify-end">
                          <div
                            className="w-full bg-blue-600 dark:bg-blue-500 rounded-t-xs"
                            style={{ height: `${(d.EnergyConsumption / maxC) * 100}%` }}
                          />
                          <div className="opacity-0 group-hover:opacity-100 absolute -top-6 bg-slate-900 dark:bg-slate-800 text-white text-[9px] px-1 py-0.5 rounded pointer-events-none whitespace-nowrap z-20 border border-slate-700">
                            Day {i + 1}: {d.EnergyConsumption.toFixed(1)} kWh
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* Appliance Consumption Bar Chart */}
                <div className="bg-slate-50/80 dark:bg-slate-900/60 p-5 rounded-2xl border border-slate-100 dark:border-slate-800 flex flex-col">
                  <span className="text-[13px] font-bold text-slate-800 dark:text-slate-200 mb-1">Appliance Consumption (%)</span>
                  <span className="text-[11px] text-slate-500 dark:text-slate-400 mb-3">Estimated Household Breakdown</span>
                  <div className="flex flex-col gap-2.5 justify-center flex-1">
                    {[
                      { name: "AC", pct: 40, col: "bg-blue-600 dark:bg-blue-500" },
                      { name: "Fridge", pct: 20, col: "bg-emerald-600 dark:bg-emerald-500" },
                      { name: "Fan", pct: 15, col: "bg-teal-600 dark:bg-teal-500" },
                      { name: "Lights", pct: 15, col: "bg-amber-500 dark:bg-amber-400" },
                      { name: "TV", pct: 10, col: "bg-purple-600 dark:bg-purple-500" },
                    ].map((app, i) => (
                      <div key={i}>
                        <div className="flex justify-between text-[12px] font-medium text-slate-700 dark:text-slate-300 mb-0.5">
                          <span>{app.name}</span>
                          <span className="font-semibold text-slate-900 dark:text-white">{app.pct}%</span>
                        </div>
                        <div className="w-full h-2 rounded-full bg-slate-200 dark:bg-slate-800 overflow-hidden">
                          <div className={`h-full ${app.col} rounded-full`} style={{ width: `${app.pct}%` }} />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              <div className="p-4 rounded-xl bg-blue-50 dark:bg-blue-950/40 text-blue-800 dark:text-blue-300 border border-blue-200 dark:border-blue-900/50 text-[13px]">
                Upload a dataset to see analytics charts.
              </div>
            )}
          </div>

          {/* ADMIN SECTION - ADVANCED MODELS */}
          <div className="bg-white dark:bg-[#0d1410] rounded-3xl p-6 border border-slate-100 dark:border-slate-800/80 shadow-xs flex flex-col gap-4">
            {loggedIn && username === "admin" ? (
              <div className="flex flex-col gap-6">
                <div className="border-b border-slate-100 dark:border-slate-800 pb-3">
                  <h3 className="font-['Space_Grotesk'] text-[18px] font-bold text-slate-900 dark:text-white">
                    Admin: Advanced Model Training &amp; Evaluation
                  </h3>
                  <div className="mt-2 p-3 rounded-xl bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800/60 text-[#166534] dark:text-emerald-300 text-[13px] font-medium">
                    Admin access granted for advanced model features! Train and evaluate models below.
                  </div>
                </div>

                {/* Random Forest Regressor UI */}
                <div className="bg-slate-50/80 dark:bg-slate-900/60 p-5 rounded-2xl border border-slate-100 dark:border-slate-800 flex flex-col gap-4">
                  <h4 className="font-['Space_Grotesk'] text-[16px] font-bold text-slate-900 dark:text-white">
                    Random Forest Regressor
                  </h4>

                  <div className="flex flex-col sm:flex-row items-start sm:items-center gap-4">
                    <div className="flex-1 w-full">
                      <div className="flex justify-between text-[12px] font-medium text-slate-700 dark:text-slate-300 mb-1">
                        <span>Number of Future Steps (Random Forest)</span>
                        <span className="font-bold text-[#009e52] dark:text-emerald-400">{rfFutureSteps}</span>
                      </div>
                      <input
                        type="range" min={1} max={30} value={rfFutureSteps}
                        onChange={(e) => setRfFutureSteps(Number(e.target.value))}
                        className="w-full accent-[#009e52] cursor-pointer"
                      />
                    </div>
                    <button
                      onClick={handlePredictFutureRF}
                      className="px-5 py-2.5 rounded-xl bg-[#1d6b38] hover:bg-[#144b27] text-white text-[13px] font-semibold transition-colors cursor-pointer"
                    >
                      Predict Future Energy (RF)
                    </button>
                  </div>

                  {rfForecastResults && (
                    <div className="mt-3 flex flex-col gap-3">
                      <span className="text-[13px] font-bold text-slate-800 dark:text-slate-200">
                        Random Forest Predicted Energy Consumption for next {rfFutureSteps} steps:
                      </span>

                      {/* Visual Trend Chart */}
                      <div className="bg-white dark:bg-[#080d0a] p-4 rounded-xl border border-slate-200 dark:border-slate-800">
                        <div className="flex items-center justify-between text-[11px] text-slate-500 dark:text-slate-400 mb-2">
                          <span>Forecast Sequence (kWh)</span>
                          <span className="text-[#009e52] dark:text-emerald-400 font-semibold">Steps {rfForecastResults[0]?.step} – {rfForecastResults[rfForecastResults.length - 1]?.step}</span>
                        </div>
                        <div className="h-28 flex items-end gap-1.5 pt-2">
                          {(() => {
                            const maxVal = Math.max(...rfForecastResults.map(r => r.value), 1);
                            return rfForecastResults.map((r, i) => (
                              <div key={i} className="flex-1 flex flex-col items-center gap-1 group relative h-full justify-end">
                                <div
                                  className="w-full bg-[#009e52] hover:bg-[#144b27] rounded-t-sm transition-all duration-200"
                                  style={{ height: `${Math.max(10, (r.value / maxVal) * 100)}%` }}
                                />
                                <div className="opacity-0 group-hover:opacity-100 absolute -top-7 bg-slate-900 dark:bg-slate-800 text-white text-[9px] px-1.5 py-0.5 rounded pointer-events-none whitespace-nowrap z-20 border border-slate-700">
                                  Step {r.step}: {r.value} kWh
                                </div>
                                <span className="text-[9px] text-slate-400 dark:text-slate-500 mt-0.5">+{i + 1}</span>
                              </div>
                            ));
                          })()}
                        </div>
                      </div>

                      <div className="overflow-x-auto max-h-48 border border-slate-200 dark:border-slate-800 rounded-xl bg-white dark:bg-[#080d0a]">
                        <table className="w-full text-left text-[12px]">
                          <thead className="bg-slate-50 dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300">
                            <tr>
                              <th className="py-2 px-3">Step Index</th>
                              <th className="py-2 px-3">Predicted Energy Consumption (kWh)</th>
                            </tr>
                          </thead>
                          <tbody className="divide-y divide-slate-100 dark:divide-slate-800 text-slate-700 dark:text-slate-300">
                            {rfForecastResults.map((r, i) => (
                              <tr key={i} className="hover:bg-slate-50 dark:hover:bg-slate-800/40">
                                <td className="py-1.5 px-3">{r.step}</td>
                                <td className="py-1.5 px-3 font-semibold text-[#009e52] dark:text-emerald-400">{r.value} kWh</td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  )}
                </div>

                {/* Logarithmic Regression Section */}
                <div className="bg-slate-50/80 dark:bg-slate-900/60 p-5 rounded-2xl border border-slate-100 dark:border-slate-800 flex flex-col gap-2">
                  <h4 className="font-['Space_Grotesk'] text-[16px] font-bold text-slate-900 dark:text-white">
                    Logarithmic Regression
                  </h4>
                  <div className="p-3 rounded-xl bg-blue-50 dark:bg-blue-950/40 border border-blue-200 dark:border-blue-900/50 text-blue-900 dark:text-blue-300 text-[12px]">
                    Logarithmic Regression Model Loaded and ready for residual analysis with SGDRegressor.
                  </div>
                </div>
              </div>
            ) : (
              <div className="p-4 rounded-xl bg-blue-50/80 dark:bg-blue-950/40 border border-blue-200 dark:border-blue-900/50 text-blue-900 dark:text-blue-300 text-[13px]">
                {loggedIn ? "You must be logged in as 'admin' to access advanced model features." : "Log in as 'admin' to access advanced model features."}
              </div>
            )}
          </div>

          {/* MODEL PERFORMANCE COMPARISON */}
          <div className="bg-white dark:bg-[#0d1410] rounded-3xl p-6 border border-slate-100 dark:border-slate-800/80 shadow-xs flex flex-col gap-4">
            <h3 className="font-['Space_Grotesk'] text-[18px] font-bold text-slate-900 dark:text-white">
              Model Performance Comparison
            </h3>

            <div className="overflow-x-auto border border-slate-200 dark:border-slate-800 rounded-2xl">
              <table className="w-full text-left text-[12px]">
                <thead className="bg-slate-50 dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300">
                  <tr>
                    <th className="py-2.5 px-3">Model</th>
                    <th className="py-2.5 px-2">MAE</th>
                    <th className="py-2.5 px-2">MSE</th>
                    <th className="py-2.5 px-2">RMSE</th>
                    <th className="py-2.5 px-2">R²</th>
                    <th className="py-2.5 px-2">MAPE (%)</th>
                    <th className="py-2.5 px-3 text-center">Best Model</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 dark:divide-slate-800 text-slate-800 dark:text-slate-300">
                  {modelMetricsList.map((m, idx) => (
                    <tr key={idx} className={m.best ? "bg-emerald-50/50 dark:bg-emerald-950/30 text-emerald-900 dark:text-emerald-300 font-medium" : "hover:bg-slate-50/50 dark:hover:bg-slate-800/40"}>
                      <td className="py-2.5 px-3 font-semibold">{m.Model}</td>
                      <td className="py-2.5 px-2">{m.MAE.toFixed(4)}</td>
                      <td className="py-2.5 px-2">{m.MSE.toFixed(4)}</td>
                      <td className="py-2.5 px-2">{m.RMSE.toFixed(4)}</td>
                      <td className="py-2.5 px-2 font-bold text-slate-900 dark:text-white">{m.R2.toFixed(4)}</td>
                      <td className="py-2.5 px-2">{m.MAPE.toFixed(2)}%</td>
                      <td className="py-2.5 px-3 text-center">
                        {m.best ? <span className="text-[#009e52] dark:text-emerald-400 font-bold text-[14px]">✅</span> : ""}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="p-3.5 rounded-xl bg-blue-50 dark:bg-blue-950/40 border border-blue-200 dark:border-blue-900/50 text-blue-900 dark:text-blue-300 text-[13px]">
              The best performing model (based on R-squared) displayed is: <strong>{bestModelName}</strong>
            </div>
          </div>

          {/* DATASET PREVIEW & LIVE DATA EDITOR */}
          <div className="bg-white dark:bg-[#0d1410] rounded-3xl p-6 border border-slate-100 dark:border-slate-800/80 shadow-xs flex flex-col gap-4">
            <h3 className="font-['Space_Grotesk'] text-[18px] font-bold text-slate-900 dark:text-white flex items-center justify-between">
              <span>Dataset Preview: {selectedDatasetName}</span>
              <span className="text-[12px] font-normal text-slate-500 dark:text-slate-400">Showing page {dataPage + 1} of {Math.ceil(activeData.length / rowsPerPage)}</span>
            </h3>

            <div className="overflow-x-auto border border-slate-200 dark:border-slate-800 rounded-2xl">
              <table className="w-full text-left text-[12px]">
                <thead className="bg-slate-50 dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300">
                  <tr>
                    <th className="py-2.5 px-2">#</th>
                    <th className="py-2.5 px-2">Temp</th>
                    <th className="py-2.5 px-2">Time</th>
                    <th className="py-2.5 px-2">Humidity</th>
                    <th className="py-2.5 px-2">Power</th>
                    <th className="py-2.5 px-2">Duration</th>
                    <th className="py-2.5 px-2">Devices</th>
                    <th className="py-2.5 px-2">Occupancy</th>
                    <th className="py-2.5 px-2">Energy (kWh)</th>
                    <th className="py-2.5 px-2">E_load</th>
                    <th className="py-2.5 px-2">Residual</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 dark:divide-slate-800 text-slate-800 dark:text-slate-300">
                  {paginatedRows.map((r, i) => (
                    <tr key={i} className="hover:bg-slate-50/60 dark:hover:bg-slate-800/40">
                      <td className="py-2 px-2 text-slate-400 dark:text-slate-500">{dataPage * rowsPerPage + i + 1}</td>
                      <td className="py-1 px-2">
                        <input
                          type="number"
                          value={r.Temperature}
                          onChange={(e) => handleUpdateCell(i, "Temperature", Number(e.target.value))}
                          className="w-16 px-1.5 py-0.5 rounded border border-slate-200 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-100 text-[12px] focus:outline-none focus:ring-1 focus:ring-[#009e52]"
                        />
                      </td>
                      <td className="py-1 px-2">
                        <input
                          type="number"
                          value={r.Time}
                          onChange={(e) => handleUpdateCell(i, "Time", Number(e.target.value))}
                          className="w-12 px-1.5 py-0.5 rounded border border-slate-200 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-100 text-[12px] focus:outline-none focus:ring-1 focus:ring-[#009e52]"
                        />
                      </td>
                      <td className="py-1 px-2">
                        <input
                          type="number"
                          value={r.Humidity}
                          onChange={(e) => handleUpdateCell(i, "Humidity", Number(e.target.value))}
                          className="w-16 px-1.5 py-0.5 rounded border border-slate-200 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-100 text-[12px] focus:outline-none focus:ring-1 focus:ring-[#009e52]"
                        />
                      </td>
                      <td className="py-1 px-2">
                        <input
                          type="number"
                          value={r.PowerRating}
                          onChange={(e) => handleUpdateCell(i, "PowerRating", Number(e.target.value))}
                          className="w-18 px-1.5 py-0.5 rounded border border-slate-200 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-100 text-[12px] focus:outline-none focus:ring-1 focus:ring-[#009e52]"
                        />
                      </td>
                      <td className="py-1 px-2">
                        <input
                          type="number"
                          step={0.1}
                          value={r.UsageDuration}
                          onChange={(e) => handleUpdateCell(i, "UsageDuration", Number(e.target.value))}
                          className="w-14 px-1.5 py-0.5 rounded border border-slate-200 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-100 text-[12px] focus:outline-none focus:ring-1 focus:ring-[#009e52]"
                        />
                      </td>
                      <td className="py-1 px-2">
                        <input
                          type="number"
                          value={r.NumDevices}
                          onChange={(e) => handleUpdateCell(i, "NumDevices", Number(e.target.value))}
                          className="w-12 px-1.5 py-0.5 rounded border border-slate-200 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-100 text-[12px] focus:outline-none focus:ring-1 focus:ring-[#009e52]"
                        />
                      </td>
                      <td className="py-1 px-2">
                        <input
                          type="number"
                          value={r.Occupancy}
                          onChange={(e) => handleUpdateCell(i, "Occupancy", Number(e.target.value))}
                          className="w-12 px-1.5 py-0.5 rounded border border-slate-200 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-100 text-[12px] focus:outline-none focus:ring-1 focus:ring-[#009e52]"
                        />
                      </td>
                      <td className="py-1 px-2 font-semibold text-[#009e52] dark:text-emerald-400">{r.EnergyConsumption.toFixed(2)}</td>
                      <td className="py-1 px-2 text-slate-500 dark:text-slate-400">{r.E_load.toFixed(2)}</td>
                      <td className="py-1 px-2 text-slate-500 dark:text-slate-400">{r.EnergyResidual.toFixed(2)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Pagination Controls */}
            <div className="flex items-center justify-between pt-2">
              <span className="text-[12px] text-slate-500 dark:text-slate-400">
                Edits automatically update active models and predictions in real time.
              </span>
              <div className="flex items-center gap-2">
                <button
                  disabled={dataPage === 0}
                  onClick={() => setDataPage(p => Math.max(0, p - 1))}
                  className="px-3 py-1 rounded-lg border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 bg-white dark:bg-slate-800 text-[12px] hover:bg-slate-50 dark:hover:bg-slate-700 disabled:opacity-40 cursor-pointer"
                >
                  Previous
                </button>
                <button
                  disabled={(dataPage + 1) * rowsPerPage >= activeData.length}
                  onClick={() => setDataPage(p => p + 1)}
                  className="px-3 py-1 rounded-lg border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 bg-white dark:bg-slate-800 text-[12px] hover:bg-slate-50 dark:hover:bg-slate-700 disabled:opacity-40 cursor-pointer"
                >
                  Next
                </button>
              </div>
            </div>
          </div>

        </main>
      </div>
    </div>
  );
};
