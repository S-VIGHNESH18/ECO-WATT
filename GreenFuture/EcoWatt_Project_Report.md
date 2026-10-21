# A PROJECT REPORT ON
# ECOWATT: ENERGY CONSUMPTION PREDICTION AND CARBON EMISSION ESTIMATION USING MACHINE LEARNING

**Submitted in partial fulfilment of the requirements for the course**  
**24ESQ2119(B)-A/B/C ARTIFICIAL INTELLIGENCE and MACHINE LEARNING/DEEP LEARNING/ DATA SCIENCE/ PROJECT**  
*(Introductory Level Artificial Intelligence for Engineers – Project)*  
of the degree of  
**BACHELOR OF TECHNOLOGY in MECHANICAL ENGINEERING**

---

### Submitted by:
1. **Aaliya Fathima Arif** ([Register No.])
2. **Afrah Zulfi** ([Register No.])
3. **Muhammed Aasif** ([Register No.])
4. **Sanju Philip Saji** ([Register No.])
5. **S. Vighnesh (Team Leader)** ([Register No.])

**Under the guidance of:**  
**Er. Philip Jacob Perakathu**  
Assistant Professor (Senior)

**DEPARTMENT OF MECHANICAL ENGINEERING**  
**SAINTGITS COLLEGE OF ENGINEERING (AUTONOMOUS)**  
Kottukulam Hills, Pathamuttom P.O., Kottayam – 686 532, Kerala  
**OCTOBER 2026**

---

## CERTIFICATE

This is to certify that the project report entitled **“EcoWatt: Energy Consumption Prediction and Carbon Emission Estimation Using Machine Learning”** submitted by **Aaliya Fathima Arif** ([Reg. No.]), **Afrah Zulfi** ([Reg. No.]), **Muhammed Aasif** ([Reg. No.]), **Sanju Philip Saji** ([Reg. No.]) and **S. Vighnesh** ([Reg. No.]) in partial fulfilment of the requirements for the course **24ESQ2119(B)-A/B/C Artificial Intelligence and Machine Learning/Deep Learning/ Data Science Project** of the degree of **Bachelor of Technology in Mechanical Engineering**, Saintgits College of Engineering (Autonomous), is a bonafide record of the project work carried out by them under our guidance and supervision during the academic year 2025–2026.

| Project Supervisor | Project Coordinator | Head of the Department |
| :--- | :--- | :--- |
| **Er. Philip Jacob Perakathu**<br>Assistant Professor (Senior) | **[Name, Designation]** | **Dr. Chacko Peno**<br>Head of Department |

**Place:** Pathamuttom  
**Date:** 18 October 2026  
*(Department Seal)*

---

## DECLARATION

We hereby declare that the project report entitled **“EcoWatt: Energy Consumption Prediction and Carbon Emission Estimation Using Machine Learning”**, submitted in partial fulfilment of the requirements for the course **24ESQ2119(B)-A/B/C Artificial Intelligence and Machine Learning/Deep Learning/ Data Science Project** of the degree of **Bachelor of Technology in Mechanical Engineering** of Saintgits College of Engineering (Autonomous), is a bonafide record of the work carried out by us under the supervision of **Er. Philip Jacob Perakathu**. This report has not been submitted, either in part or in full, for the award of any other degree or course. All sources of information, data and code used in this work have been duly acknowledged.

| Sl. | Name of the Student | Register No. | Signature |
| :---: | :--- | :---: | :---: |
| 1 | Aaliya Fathima Arif | [Register No.] | |
| 2 | Afrah Zulfi | [Register No.] | |
| 3 | Muhammed Aasif | [Register No.] | |
| 4 | Sanju Philip Saji | [Register No.] | |
| 5 | S. Vighnesh (Team Leader) | [Register No.] | |

**Place:** Pathamuttom  
**Date:** 18 October 2026

---

## ACKNOWLEDGEMENT

We express our sincere gratitude to **Dr. Sudha T.**, Principal, Saintgits College of Engineering (Autonomous), for providing the facilities required for this project. We are thankful to **Dr. Chacko Peno**, Head of the Department of Mechanical Engineering, for the constant support and encouragement.

We are deeply indebted to our project supervisor, **Er. Philip Jacob Perakathu**, for the valuable guidance, suggestions and supervision throughout the course of this work. We also thank **[Name]**, Project Coordinator, and the members of the project evaluation committee for their constructive feedback during the reviews.

Finally, we thank our parents, friends and all those who helped us directly or indirectly in the successful completion of this project.

*— Aaliya Fathima Arif, Afrah Zulfi, Muhammed Aasif, Sanju Philip Saji and S. Vighnesh*

---

## ABSTRACT

Rising household electricity consumption increases both domestic electricity bills and the greenhouse gas emissions associated with fossil-fuel power generation, yet most households lack accessible tools to anticipate their electricity consumption or assess its environmental footprint prior to the arrival of billing statements. This project, **EcoWatt** (implemented as part of the modern **GreenFuture** web platform), addresses this challenge by formulating residential energy prediction as a physics-informed regression problem: estimating household electricity consumption (kWh) from seven key parameters—ambient temperature, time of day, relative humidity, appliance rated power, usage duration, number of operating devices, and residence occupancy—and translating the predicted consumption into estimated electricity cost (INR), carbon footprint ($CO_2$ in kg), and actionable energy-saving opportunities.

Two complementary machine learning paradigms were implemented and evaluated on a physically grounded 6,000-record dataset (`EcoWatt_6000_v7.csv`): a physics-informed SGD Logarithmic Regression pipeline (incorporating a `log1p` feature transformation, `StandardScaler`, and `SGDRegressor`) predicting the environmental residual over physical appliance base load, and a 10-step lagged Random Forest Regressor for non-linear feature interaction and multi-step recursive forecasting. The Random Forest achieved superior performance ($R^2 = 0.6342$, $\text{MAE} = 1.1228\text{ kWh}$, $\text{RMSE} = 1.4752\text{ kWh}$) over the Logarithmic Regression pipeline ($R^2 = 0.5631$, $\text{MAE} = 1.2262\text{ kWh}$, $\text{RMSE} = 1.6122\text{ kWh}$).

To provide a robust, responsive end-user experience, the system has been developed and deployed as a modern single-page web application using **React 18, TypeScript, Vite, and Tailwind CSS**, featuring an in-browser physics-informed ML engine, live weather integration via the **OpenWeatherMap REST API**, real-time tariff calculation ($\text{₹}8.40/\text{kWh}$ based on KSEB slabs), carbon footprint audit ($0.716\text{ kg }CO_2/\text{kWh}$ based on CEA India baseline), and interactive analytics, directly advancing UN Sustainable Development Goals 7 (Affordable and Clean Energy) and 13 (Climate Action).

**Keywords:** Machine Learning, Physics-Informed ML, Logarithmic Regression, Random Forest Regressor, Energy Consumption Prediction, Carbon Emission Estimation, React, TypeScript, OpenWeatherMap API.

---

## CONTENTS

- **CERTIFICATE** .................................................... i
- **DECLARATION** .................................................... ii
- **ACKNOWLEDGEMENT** ................................................ iii
- **ABSTRACT** ....................................................... iv
- **LIST OF FIGURES** ................................................ vii
- **LIST OF TABLES** ................................................. viii
- **LIST OF ABBREVIATIONS** .......................................... ix
- **CHAPTER 1: INTRODUCTION** ........................................ 1
  - 1.1 Background ................................................... 1
  - 1.2 Problem Statement ............................................. 1
  - 1.3 Objectives .................................................... 1
  - 1.4 Social and Technical Relevance ............................... 2
  - 1.5 Scope and Limitations ........................................ 2
  - 1.6 Organisation of the Report ................................... 3
- **CHAPTER 2: LITERATURE REVIEW** ................................... 4
  - 2.1 Review of Existing Works ..................................... 4
  - 2.2 Summary of Literature Review ................................. 4
  - 2.3 Limitations of Existing Systems and Research Gap ............. 5
  - 2.4 Feasibility Study ............................................ 6
- **CHAPTER 3: SYSTEM REQUIREMENTS AND SPECIFICATION** ............... 7
  - 3.1 Software and Hardware Requirements ........................... 7
  - 3.2 Dataset Description .......................................... 7
- **CHAPTER 4: METHODOLOGY AND SYSTEM DESIGN** ....................... 9
  - 4.1 Proposed System Overview ..................................... 9
  - 4.2 System Architecture .......................................... 9
  - 4.3 Data Pre-processing .......................................... 10
  - 4.4 Model Selection and Justification ............................ 11
  - 4.5 Algorithm .................................................... 12
  - 4.6 Design Diagrams .............................................. 12
  - 4.7 Evaluation Metrics ........................................... 14
- **CHAPTER 5: IMPLEMENTATION** ...................................... 15
  - 5.1 Development Environment ...................................... 15
  - 5.2 Module Description ........................................... 15
  - 5.3 Sample Code .................................................. 16
  - 5.4 GitHub Repository ............................................ 17
  - 5.5 Real-time Implementation / Deployment ........................ 17
- **CHAPTER 6: RESULTS AND DISCUSSION** .............................. 19
  - 6.1 Experimental Setup ........................................... 19
  - 6.2 Performance Evaluation ....................................... 19
  - 6.3 Graphical Analysis ........................................... 20
  - 6.4 Comparison with Existing Works ............................... 21
  - 6.5 Observations, Failures and Inferences ........................ 21
  - 6.6 Objectives vs. Outcomes ...................................... 22
- **CHAPTER 7: CONCLUSION AND FUTURE SCOPE** ......................... 23
  - 7.1 Conclusion ................................................... 23
  - 7.2 Future Scope ................................................. 23
- **REFERENCES** ..................................................... 24
- **APPENDIX A: SOURCE CODE** ........................................ 25
- **APPENDIX B: SCREENSHOTS** ........................................ 28
- **APPENDIX C: MAPPING WITH SUSTAINABLE DEVELOPMENT GOALS** ......... 30
- **APPENDIX D: INDIVIDUAL CONTRIBUTION OF TEAM MEMBERS** ............. 31

---

## LIST OF FIGURES

| Figure No. | Title | Page No. |
| :---: | :--- | :---: |
| 4.1 | System architecture of the proposed EcoWatt web platform | 10 |
| 4.2 | Activity (workflow) diagram of the EcoWatt web application | 13 |
| 4.3 | Use-case diagram of the EcoWatt web application | 13 |
| 5.1 | Landing page of the EcoWatt web application | 17 |
| 5.2 | Prediction dashboard for a sample session | 18 |
| 6.1 | Model performance comparison reported by the application | 20 |
| 6.2 | Random Forest multi-step forecast (admin panel) | 20 |
| 6.3 | Analytics: energy-consumption trend and appliance share | 21 |
| B.1 | Landing hero section and responsive theme toggle | 28 |
| B.2 | Live weather telemetry, parameter inputs, and prediction dashboard | 28 |
| B.3 | Prediction history trend chart (bar/line views) and CSV export | 29 |

---

## LIST OF TABLES

| Table No. | Title | Page No. |
| :---: | :--- | :---: |
| 2.1 | Summary of literature review | 4 |
| 3.1 | Software and hardware requirements | 7 |
| 3.2 | Description of dataset attributes | 8 |
| 5.1 | Modules of the EcoWatt application | 15 |
| 6.1 | Performance comparison of machine learning regression models | 19 |
| 6.2 | Summary of observed issues, causes and solutions | 21 |
| C.1 | Mapping with Sustainable Development Goals (SDGs) | 30 |
| D.1 | Individual contribution of team members | 31 |

---

## LIST OF ABBREVIATIONS

| Abbreviation | Expansion |
| :--- | :--- |
| **AI** | Artificial Intelligence |
| **API** | Application Programming Interface |
| **CEA** | Central Electricity Authority (Government of India) |
| **CO₂** | Carbon Dioxide |
| **CSV** | Comma-Separated Values |
| **INR** | Indian Rupee (₹) |
| **KSEB** | Kerala State Electricity Board |
| **kWh** | Kilowatt-hour |
| **MAE** | Mean Absolute Error |
| **MAPE** | Mean Absolute Percentage Error |
| **ML** | Machine Learning |
| **MSE** | Mean Squared Error |
| **R²** | Coefficient of Determination |
| **RF** | Random Forest |
| **RMSE** | Root Mean Squared Error |
| **SDG** | Sustainable Development Goal |
| **SGD** | Stochastic Gradient Descent |

---

## CHAPTER 1: INTRODUCTION

### 1.1 Background
Rising household electricity consumption is a growing concern for both domestic budgets and national carbon-reduction targets. Residential electricity use is shaped by a complex interplay of environmental factors—such as ambient temperature, relative humidity, and time of day—and consumer behavior, including appliance rated power, usage duration, operating device count, and household occupancy levels. Despite this direct correlation, most households have no simple or intuitive way to see how everyday appliance choices translate into monetary billing cost and carbon emissions before the monthly utility statement arrives.

Artificial Intelligence and Machine Learning (AI/ML) offer a practical, accessible way to bridge this gap. Regression-based models can capture the underlying relationship between everyday household parameters and actual electrical energy consumption. This allows instantaneous, scenario-based energy predictions to be generated from intuitive user inputs, entirely eliminating the requirement for costly smart-meter hardware or specialized sub-metering installations. This project, **EcoWatt** (integrated within the modern **GreenFuture** web platform), applies these machine learning principles to construct an interactive, physics-informed decision-support application that predicts residential energy demand and translates it into electricity tariffs and carbon dioxide ($CO_2$) emissions.

### 1.2 Problem Statement
Increasing residential power demand drives higher electricity utility bills and expands greenhouse gas emissions from fossil-fuel-dominated electrical grids. However, domestic energy consumers rarely possess accessible tools to anticipate their electricity usage, identify peak-demand periods, or gauge the carbon impact of their appliances before billing cycles close. EcoWatt addresses this problem by formulating residential energy prediction as a physics-informed machine learning regression task: given seven household and environmental parameters—temperature, hour of day, humidity, appliance power rating, usage duration, device count, and residence occupancy—the system predicts continuous electricity consumption (kWh). It then dynamically derives the financial electricity cost (INR), associated $CO_2$ emissions (kg), peak usage classification, and tailored efficiency recommendations.

### 1.3 Objectives
The main objectives of this project are:
1. To generate, preprocess, and benchmark a physically grounded household energy-consumption dataset, identifying ambient temperature, occupancy, and appliance load as core predictive features consistent with building energy literature.
2. To formulate and compare two machine learning paradigms: a physics-informed SGD Logarithmic Regression residual pipeline and a 10-step lagged Random Forest Regressor for non-linear energy forecasting.
3. To systematically evaluate both models across established regression metrics: Mean Absolute Error (MAE), Mean Squared Error (MSE), Root Mean Squared Error (RMSE), Coefficient of Determination ($R^2$), and Mean Absolute Percentage Error (MAPE).
4. To translate raw energy predictions into actionable socio-economic and environmental outputs: electricity tariff cost (INR), carbon emissions (kg $CO_2$), peak-demand classifications, and an Energy Efficiency Score (Eco Score).
5. To engineer a modern, responsive, client-side web application using React 18, TypeScript, Tailwind CSS, and Vite, integrating live weather telemetry via the OpenWeatherMap REST API and client-side machine learning inference.

### 1.4 Social and Technical Relevance
EcoWatt directly benefits domestic energy consumers by replacing opaque end-of-month electricity bills with transparent, real-time feedback that empowers proactive conservation. Globally, residential and commercial buildings account for roughly 36% of total final energy consumption and approximately 40% of direct and indirect carbon emissions [1]. By equipping households with immediate insights into energy waste, EcoWatt directly supports United Nations Sustainable Development Goals: SDG 7 (Affordable and Clean Energy), SDG 13 (Climate Action), and SDG 11 (Sustainable Cities and Communities) (Appendix C).

Technically, residential electricity modeling presents both linear physical relationships ($\text{wattage} \times \text{hours} \times \text{devices}$) and non-linear environmental and behavioral dynamics (thermostat adjustments under high heat and humidity). This justifies a hybrid physics-informed approach: decomposing energy into an explicit appliance base load and a learned environmental residual, comparing gradient-descent linear pipelines against multi-tree ensemble methods.

### 1.5 Scope and Limitations
The project scope encompasses household-level energy consumption prediction using seven accessible user inputs, with real-time derivation of costs, emissions, and efficiency metrics. Exclusions include physical smart-meter hardware development and invasive circuit-level appliance sub-metering. Key limitations include: the dataset utilized for benchmarking (`EcoWatt_6000_v7.csv`) is synthesised using physics-grounded mathematical relationships rather than intrusive multi-year hardware logging; the electricity tariff rate ($\text{₹}8.40/\text{kWh}$) and grid emission factor ($0.716\text{ kg }CO_2/\text{kWh}$) represent standard benchmark averages for Kerala/India (Section 4.4); and model metrics reflect controlled test-split evaluations.

### 1.6 Organisation of the Report
The rest of this report is organised as follows: Chapter 2 reviews the existing literature and identifies the research gap; Chapter 3 presents system requirements and describes the dataset; Chapter 4 explains the methodology and system design; Chapter 5 describes the implementation; Chapter 6 discusses the results obtained; and Chapter 7 concludes the report with the scope for future work.

---

## CHAPTER 2: LITERATURE REVIEW

### 2.1 Review of Existing Works
A rigorous review of academic and practical energy prediction literature was conducted. Khalil et al. [1] performed a comprehensive systematic review of machine learning, deep learning, and statistical methods across building energy forecasting, noting that residential buildings account for over 36% of global energy demand and 40% of carbon emissions. Their findings established that machine learning models consistently yield 15–28% energy conservation improvements when integrated into user-facing decision feedback loops, strongly motivating EcoWatt's carbon-emission derivation module.

A meta-survey covering 431 studies on machine learning for building energy prediction published in the Journal of Building Engineering [4] identified ambient temperature, residence occupancy, and appliance operating schedules as the three most statistically influential predictive features. This informed EcoWatt's feature selection and its architectural decision to separate deterministic appliance base load from environmental residuals. In smart energy forecasting studies [5], the incorporation of real-time contextual weather data demonstrated significant forecast enhancements, highlighting the necessity of live weather API telemetry.

Empirical household data surveys from Kerala, notably the Cherukunnu Gramapanchayath Socio-Economic Survey [6] covering 3,785 households, provided realistic domestic consumption benchmarks, typical device ownership numbers, and regional electricity expenditure ranges. Furthermore, international open benchmarks—including the UCI Appliances Energy Prediction dataset [7] and the UCI Individual Household Electric Power Consumption dataset [8]—established reference frameworks for regression evaluation.

### 2.2 Summary of Literature Review

**Table 2.1: Summary of literature review**

| Ref. | Author(s) & Year | Method / Technique | Dataset | Key Findings & Limitations |
| :---: | :--- | :--- | :--- | :--- |
| **[1]** | Khalil et al. (2022) | Systematic Review of ML/DL Forecasting | Global building studies | Buildings consume 36% of global energy; ML reduces waste; lacks end-user apps. |
| **[4]** | Building Energy Survey (2021) | Meta-analysis of 431 ML studies | Literature corpus | Temp, occupancy & appliance wattage dominate; models rarely deployed to web. |
| **[5]** | AI Smart Energy Study (2023) | Context-Aware Energy Forecasting | Industrial & domestic sites | Real-time weather integration improves accuracy; peak hours enable demand shift. |
| **[6]** | DES Kerala (2024) | Socio-Economic Survey Analysis | 3,785 Kerala households | Provided realistic ranges for Kerala household appliances, bills and load profiles. |
| **[7]** | UCI ML Repository (2017) | Appliance Energy Prediction | Measured house sensor logs | Benchmark for environmental regressors; lacks cost and CO2 impact translations. |
| **[8]** | UCI ML Repository (2012) | Electric Power Consumption | Single-household 4-yr records | Demonstrated high variance and lag correlation; lacks real-time interactive UI. |

### 2.3 Limitations of Existing Systems and Research Gap
Existing research overwhelmingly emphasizes model accuracy metrics (such as MSE and $R^2$) in isolated Jupyter notebooks or server-heavy environments, rarely packaging models into responsive, user-friendly digital tools that ordinary households can operate. Furthermore, prior solutions rarely translate raw kilowatt-hour (kWh) values into direct financial billing metrics (INR) or localized greenhouse gas equivalents (kg $CO_2$). EcoWatt resolves this gap by combining a physics-informed ML pipeline with a production-ready, client-side web application that instantly converts predictions into costs, emissions, and actionable conservation recommendations.

### 2.4 Feasibility Study
- **Technical Feasibility:** Highly viable. Modern client-side web architectures (React 18, TypeScript, Vite) execute mathematical matrix operations and ML regression in-browser without server dependencies.
- **Operational Feasibility:** Outstanding. Users access the system via standard web browsers with zero installation requirements, adjusting simple intuitive sliders.
- **Economic Feasibility:** Optimal. Developed completely with open-source software, requiring zero server hosting fees or expensive smart-meter hardware.

---

## CHAPTER 3: SYSTEM REQUIREMENTS AND SPECIFICATION

### 3.1 Software and Hardware Requirements

**Table 3.1: Software and hardware requirements**

| Category | Item | Specification |
| :--- | :--- | :--- |
| **Web Platform** | Frontend Framework | React 18, TypeScript 5, Vite Build Tool, Tailwind CSS |
| **Web UI & Styling** | Icons & Styling | Lucide React, Space Grotesk & Inter typography, Dark/Light Themes |
| **ML & Data** | Machine Learning Stack | TypeScript client ML Engine (`mlEngine.ts`) & Python scikit-learn |
| **External Telemetry** | Weather REST API | OpenWeatherMap API (live temperature, feels-like, humidity, condition) |
| **Development IDE** | Code & Version Control | Antigravity IDE / VS Code, Git, GitHub repository |
| **Client Hardware** | End-User Device | Modern Web Browser (Chrome, Edge, Firefox, Safari); 2 GB RAM minimum |
| **Data Formats** | Storage & Export | CSV (`EcoWatt_6000.csv`, `prediction_history.csv`), JSON, Web Storage |

### 3.2 Dataset Description
The EcoWatt system operates on two physically grounded dataset representations: a real-time 200-sample generator with seed 42, and a comprehensive 6,000-record benchmark dataset (`EcoWatt_6000.csv`). The target energy consumption $E$ (kWh) is synthesised according to physical energy laws with thermal non-linearities and Gaussian disturbance:

$$E = \left(\frac{P \times t \times N}{1000}\right) \times \left[1 + 0.023 \times \max(T - 24, 0)\right] + 0.13 \times O \times t + \varepsilon \quad (3.1)$$

where $P$ is the appliance rated power in Watts, $t$ is usage duration in hours, $N$ is the count of operating devices, $T$ is ambient temperature in °C, $O$ is residence occupancy, and $\varepsilon \sim \mathcal{N}(0, 2)$ represents unobserved random stochastic load. The model isolates deterministic appliance base load and environmental residual:

$$E_{load} = \frac{P \times t \times N}{1000} \quad (\text{kWh}) \quad (3.2)$$
$$E_{residual} = E - E_{load} \quad (\text{kWh}) \quad (3.3)$$

**Table 3.2: Description of dataset attributes**

| Sl. | Attribute Name | Type & Unit | Physical Description & Valid Range |
| :---: | :--- | :--- | :--- |
| 1 | Temperature | Float (°C) | Ambient indoor/outdoor temperature (20.0 to 40.0 °C) |
| 2 | Time | Integer (h) | Hour of day (0 to 23 h) governing diurnal occupancy cycles |
| 3 | Humidity | Integer (%) | Relative atmospheric humidity (40 to 90 %) influencing HVAC loads |
| 4 | PowerRating | Integer (W) | Mean electrical power rating of active appliances (100 to 2500 W) |
| 5 | UsageDuration | Float (h) | Continuous operational appliance duration (0.5 to 10.0 hours) |
| 6 | NumDevices | Integer | Total count of simultaneously active appliances (1 to 10 units) |
| 7 | Occupancy | Integer | Count of active human occupants in the dwelling (1 to 6 persons) |
| 8 | EnergyConsumption | Float (kWh) | Target variable: Total electrical energy consumed (0.0 to 180.0+ kWh) |

---

## CHAPTER 4: METHODOLOGY AND SYSTEM DESIGN

### 4.1 Proposed System Overview
The proposed system bridges machine learning theory and practical consumer utility through a decoupled, client-centric architecture. Users provide household appliance and occupancy parameters through an intuitive user interface, augmented by live atmospheric data retrieved via the OpenWeatherMap REST API. The core ML pipeline separates deterministic physical appliance load from learned environmental residuals, ensuring that predictions adhere to physical conservation laws while capturing subtle non-linear dependencies. The predicted kilowatt-hours are immediately converted into billing costs (INR), grid carbon emissions (kg $CO_2$), peak demand classifications, and efficiency scores.

### 4.2 System Architecture
The application architecture comprises four decoupled tiers:
1. **Presentation & UI Tier:** Parameter control sliders, weather telemetry display, simulation triggers, role-based login modal, and analytics dashboards.
2. **Client Machine Learning Engine (`mlEngine.ts`):** In-browser matrix operations performing `log1p` feature transformation, `StandardScaler` normalization, L2-regularized SGD regression for residual estimation, and lag-10 recursive Random Forest autoregression.
3. **External Telemetry Tier:** Asynchronous REST HTTP requests to the OpenWeatherMap API for live ambient city weather.
4. **Persistence & Export Tier:** Session storage, CSV dataset parsing/upload, and historical prediction logging with downloadable CSV reports.

```
+-----------------------------------------------------------------------------------+
|                        CLIENT BROWSER (React 18 + Vite)                           |
|                                                                                   |
|  [Header & Nav]   [Hero Presentation]   [Theme: Dark/Light]   [Role Auth: Admin]  |
|                                                                                   |
|  +---------------------------+       +-----------------------------------------+  |
|  |  User Parameter Controls  |       |     OpenWeatherMap API Telemetry        |  |
|  |  (Temp, Time, Hum, Power, | <---> |     (City search -> Temp, Humidity,     |  |
|  |   Duration, Devices, Occ) |       |      Conditions auto-populate sliders)  |  |
|  +---------------------------+       +-----------------------------------------+  |
|               |                                           |                       |
|               v                                           v                       |
|  +-----------------------------------------------------------------------------+  |
|  |                  In-Browser Physics-Informed ML Engine                      |  |
|  |                                                                             |  |
|  |  1. Physics Base Load:   E_load = (Power * Duration * Devices) / 1000       |  |
|  |  2. Residual Regressor:  log1p -> StandardScaler -> SGD Regression weights  |  |
|  |  3. Reconstructed kWh:   E = max(0, E_load + E_residual)                    |  |
|  |  4. Admin Forecaster:    10-step Lag Random Forest Recursive Forecaster     |  |
|  +-----------------------------------------------------------------------------+  |
|               |                                           |                       |
|               v                                           v                       |
|  +------------------------------------+  +-------------------------------------+  |
|  |        Simulation Dashboard        |  |     Analytics & Historical Audit    |  |
|  |  - Energy (kWh) & Cost (Rs 8.40)   |  |  - 20-Step Historical Sequence Trend|  |
|  |  - Carbon Footprint (0.716 kg CO2) |  |  - Typical Appliance Share (AC 40%) |  |
|  |  - Eco Score & Peak Categorization |  |  - Interactive Bar/Line Charts      |  |
|  |  - Actionable Savings Breakdown    |  |  - 1-Click CSV Export / Download    |  |
|  +------------------------------------+  +-------------------------------------+  |
+-----------------------------------------------------------------------------------+
```
*Figure 4.1: System architecture of the proposed EcoWatt web platform.*

### 4.3 Data Pre-processing
- **Range Verification:** Validating input slider values and uploaded CSV columns against physical constraints.
- **Physical Load Decomposition:** Separating base load $E_{load}$ (Equation 3.2) from target consumption to generate the target training residual $E_{residual}$.
- **Feature Transformation:** Applying natural logarithmic $\log(1 + x)$ scaling to skewed environmental regressors (Temperature, Humidity, Time, Occupancy).
- **Standard Normalization:** Computing column-wise means and sample standard deviations to z-score normalize the transformed features: $z = \frac{\log(1+x) - \mu}{\sigma}$.

### 4.4 Model Selection and Justification
Two regression paradigms were selected and comparatively evaluated:
1. **Physics-Informed SGD Logarithmic Regression Pipeline:** Deterministic electrical wattage represents the bulk of power consumption. Thus, machine learning is tasked only with estimating the residual environmental variance:
   $$\hat{y}_{res} = w^T z + b, \quad z = \text{StandardScaler}(\log(1 + x_{env})) \quad (4.1)$$
   The overall prediction is reconstructed and strictly constrained against negative values:
   $$\hat{E} = \max(0, E_{load} + \hat{y}_{res}) \quad (\text{kWh}) \quad (4.2)$$
2. **Random Forest Regressor:** An ensemble of $B = 100$ decision trees ($\hat{y} = \frac{1}{B} \sum T_b(x)$) capable of capturing non-linear feature interactions without manual interaction term engineering. Operating over a 10-step lagged historical sequence, it recursively forecasts multi-step forward trajectories.
3. **Domain-Specific Derivations:**
   $$\text{Cost (₹)} = \hat{E} \times R \quad (4.4) \quad [R = \text{₹}8.40/\text{kWh}, \text{ KSEB standard higher slab}]$$
   $$\text{CO}_2\text{ (kg)} = \hat{E} \times EF \quad (4.5) \quad [EF = 0.716\text{ kg }CO_2/\text{kWh}, \text{ CEA India Grid Baseline}]$$
   $$\text{EcoScore} = 100 \times \left[1 - \min\left(1, \frac{\hat{E}}{E_{ref}}\right)\right] \quad (4.6) \quad [E_{ref} = \text{95th percentile benchmark}]$$

### 4.5 Algorithm
```
Algorithm 1: EcoWatt Real-Time Energy Prediction and Carbon Audit
Input  : Temp, Time, Humidity, Power, Duration, Devices, Occupancy; City name
Output : Energy (kWh), Cost (Rs), CO2 (kg), Peak Category, Eco Score, Savings Potential, Multi-step Forecast
--------------------------------------------------------------------------------------------------
 1: Initialize application state: theme context, authentication, and preloaded benchmark CSV dataset
 2: IF user requests weather: fetch OpenWeatherMap REST API, extract Temp & Humidity, auto-populate sliders
 3: Parse active dataset; compute E_load = (P * t * N) / 1000 and E_residual = EnergyConsumption - E_load
 4: Fit Logarithmic Pipeline: log1p transform -> StandardScaler -> regularized SGD regression weights
 5: ON "Predict Energy" / parameter change:
      a. Compute current base load: current_E_load = (Power * Duration * Devices) / 1000
      b. Predict residual: ŷ_res = Pipeline.predict([Temp, Humidity, Time, Occupancy])
      c. Total Predicted Energy: Ê = max(0, current_E_load + ŷ_res)
      d. Electricity Cost: Cost = Ê * 8.40;  Carbon Footprint: CO2 = Ê * 0.716
      e. Compute Eco Score = 100 * (1 - min(1, Ê / E_ref))
      f. Evaluate saving opportunities (peak shift, HVAC setpoint, standby cut, duration optimization)
      g. Classify peak demand slot: 18-21 -> "Peak (6-9 PM)"; 12-15 -> "Afternoon (12-3 PM)"; etc.
      h. Append record to prediction history; update interactive trend charts & CSV export buffer
 6: IF authenticated as Admin:
      a. Construct 10-step lag autoregressive matrices from historical sequence
      b. Execute recursive multi-step forecasting across 1 to 30 forward steps
      c. Render comparative model metrics table: MAE, MSE, RMSE, R², MAPE
 7: END
```

### 4.6 Design Diagrams
- **Figure 4.2:** Activity workflow diagram detailing the execution pipeline from weather telemetry retrieval to prediction logging.
- **Figure 4.3:** Use-case diagram detailing the user interactions for regular domestic consumers versus system administrators.

### 4.7 Evaluation Metrics
- **Mean Absolute Error (MAE):** $\text{MAE} = \frac{1}{n} \sum |y_i - \hat{y}_i| \quad (4.7)$
- **Root Mean Squared Error (RMSE):** $\text{RMSE} = \sqrt{\frac{1}{n} \sum (y_i - \hat{y}_i)^2} \quad (4.8)$
- **Coefficient of Determination ($R^2$):** $R^2 = 1 - \frac{\sum (y_i - \hat{y}_i)^2}{\sum (y_i - \bar{y})^2} \quad (4.9)$
- **Mean Absolute Percentage Error (MAPE):** $\text{MAPE} = \frac{100}{n} \sum \frac{|y_i - \hat{y}_i|}{y_i} \quad (4.10)$
- **Mean Squared Error (MSE):** $\text{MSE} = \frac{1}{n} \sum (y_i - \hat{y}_i)^2$

---

## CHAPTER 5: IMPLEMENTATION

### 5.1 Development Environment
The project was initially prototyped in Python 3.10+ using scikit-learn, Pandas, NumPy, and Streamlit. To overcome server-side execution bottlenecks, tunnel latency, and process instability, the platform was re-architected into a modern, production-grade web application (**GreenFuture**). The frontend is engineered in **React 18 with TypeScript 5, Vite build orchestration, and Tailwind CSS**. Client-side linear algebra and machine learning routines are implemented in TypeScript (`mlEngine.ts`), executing directly inside the user's browser runtime with sub-millisecond latency. Atmospheric weather telemetry is integrated through asynchronous Fetch API calls to OpenWeatherMap.

### 5.2 Module Description

**Table 5.1: Modules of the EcoWatt application**

| Module Name | Source Component / File | Functional Responsibilities |
| :--- | :--- | :--- |
| **Header & Theme Module** | `Header.tsx`, `ThemeContext.tsx` | Global navigation, brand identity, dark/light theme switching, and smooth anchor scrolling. |
| **Hero Experience** | `HeroLeft.tsx`, `HeroRight.tsx` | Modern visual introduction, interactive feature highlights, and ambient clean-energy design motifs. |
| **Energy Simulator Core** | `EcoWattSimulator.tsx` | Input parameter sliders, weather auto-fill, prediction trigger, cost/carbon displays, and smart alerts. |
| **Client ML Engine** | `mlEngine.ts` | Synthetic dataset generator, CSV parsing, log1p + StandardScaler pipeline, SGD regression, and RF lag forecasting. |
| **Analytics & Benchmarks** | `EcoWattAnalytics.tsx` | Historical consumption sequence trends, typical household appliance shares (AC 40%, Fridge 20%, etc.), model metric cards. |
| **Weather Telemetry** | `fetchWeather` REST API | Live temperature, humidity, feels-like, and condition retrieval for any entered city name. |

### 5.3 Sample Code
```typescript
// TypeScript Physics-Informed ML Residual Estimator (from mlEngine.ts)
export function fitSGDRegressorLogPipeline(X: number[][], y: number[]) {
  const N = X.length, p = X[0].length;
  // 1. Natural logarithmic feature transformation: log(1 + x)
  const logX = X.map(row => row.map(v => Math.log1p(Math.max(0, v))));
  // 2. StandardScaler z-score normalization
  const means = Array(p).fill(0), stds = Array(p).fill(0);
  for (let j = 0; j < p; j++) {
    let sum = 0; for (let i = 0; i < N; i++) sum += logX[i][j];
    means[j] = sum / N;
    let sq = 0; for (let i = 0; i < N; i++) sq += (logX[i][j] - means[j]) ** 2;
    stds[j] = Math.sqrt(sq / N) || 1.0;
  }
  const normX = logX.map(r => r.map((val, j) => (val - means[j]) / stds[j]));
  // 3. Regularized Least Squares / SGD normal equations with L2 shrinkage
  const meanY = y.reduce((a, b) => a + b, 0) / N;
  // Solve (X^T * X + lambda * I) * w = X^T * (y - meanY)
  // Returns residual predictor: Ê = max(0, E_load + predictResidual(features))
}
```

### 5.4 GitHub Repository
- **Repository URL:** `https://github.com/S-VIGHNESH18/projects` (branch: `project`)
- **Project Directory:** `d:/GreenFuture` (Web Platform) & `d:/EcoWatt` (Python Prototype)
- **Tech Stack:** React 18, TypeScript 5, Vite, Tailwind CSS, Python 3.10+, scikit-learn
- **Contents:** Full source code, trained model logic, `EcoWatt_6000.csv`, `run_web.bat`, project documentation

### 5.5 Real-time Implementation / Deployment
The application is compiled and served using Vite's optimized local development and production pipeline (`npm run dev -- --port 5173`). Upon launching, users are presented with a clean hero section (Figure 5.1). Users configure appliance parameters using responsive sliders or auto-populate them via live weather telemetry. Clicking 'Simulate Energy Usage' immediately updates the prediction metrics card (Figure 5.2), displaying 46.82 kWh predicted energy, ₹393.26 electricity cost, 33.52 kg $CO_2$ emissions, an Eco Score of 13.0/100, and a 12.74% potential saving breakdown (₹57.42/day), logged automatically to the historical audit table.

---

## CHAPTER 6: RESULTS AND DISCUSSION

### 6.1 Experimental Setup
Model evaluation experiments were conducted on the 6,000-record benchmark dataset (`EcoWatt_6000_v7.csv`). An 80:20 train-test partition was applied with random seed 42 to ensure deterministic reproducibility. The Logarithmic Regression pipeline was trained on environmental residuals using SGD optimization, while the Random Forest Regressor was configured with $B = 100$ decision trees operating over 10-step lagged historical sequences. Predictions were evaluated using scikit-learn and the client-side evaluation engine.

### 6.2 Performance Evaluation

**Table 6.1: Performance comparison of machine learning regression models**

| Model Architecture | MAE (kWh) | MSE | RMSE (kWh) | R² Score | MAPE (%) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Logarithmic Regression (SGD Pipeline)** | 1.2262 | 2.5992 | 1.6122 | 0.5631 | 31.82% |
| **Random Forest Regressor (Ensemble Best)** | **1.1228** | **2.1763** | **1.4752** | **0.6342** | **29.19%** |

The Random Forest Regressor outperforms the Logarithmic Regression pipeline across all evaluation metrics. The ensemble model achieves an $R^2$ of 0.6342 (a 7.1 percentage-point improvement), while reducing MAE to 1.1228 kWh and RMSE to 1.4752 kWh (an 8.5% error reduction). The superior performance of Random Forest stems from its ability to model complex, multi-variate interactions—such as the compounding non-linear effect of high ambient temperature coupled with maximum household occupancy—which simple linear combinations cannot fully capture.

### 6.3 Graphical Analysis
- **Figure 6.1:** Bar chart comparison of regression metrics between Logarithmic Regression and Random Forest.
- **Figure 6.2:** Random Forest 9-step recursive autoregressive forecast generated in the admin panel, showing bounded trajectories between 2.51 kWh and 3.64 kWh.
- **Figure 6.3:** Domestic energy consumption sequence alongside typical residential appliance shares: Air Conditioning 40%, Refrigeration 20%, Ceiling Fans 15%, Lighting 15%, and Television 10%.

### 6.4 Comparison with Existing Works
While direct numeric benchmarking against published building studies is constrained by varying physical datasets, qualitative alignment is strong. In agreement with Khalil et al. [1] and survey literature [4], occupancy and thermal parameters exert strong secondary modulation over baseline appliance load. Furthermore, by packaging the model into a responsive web application that couples energy prediction with tariff costs and carbon footprints, EcoWatt advances beyond purely theoretical literature models into practical consumer decision support.

### 6.5 Observations, Failures and Inferences

**Table 6.2: Summary of observed issues, causes and solutions**

| Sl. | Issue / Challenge Observed | Root Cause | Solution Applied & Architecture Evolution |
| :---: | :--- | :--- | :--- |
| 1 | Colab/ngrok tunnel dropouts and port conflicts | Fragile external tunnelling and ephemeral cloud runtime | Re-engineered platform into client-side Vite/React app with in-browser ML execution. |
| 2 | Potential negative predicted energy | Linear residual model can mathematically produce negative offsets | Enforced non-negative clipping: $\hat{E} = \max(0, E_{load} + \hat{y}_{res})$. |
| 3 | Unmodelled variance (MAPE ~29-31%) | Synthetic Gaussian noise and physical stochastic load | Formulated ensemble Random Forest model; planned future smart-meter sensor logging. |
| 4 | Eco Score baseline dependency | Score relied on arbitrary local sample max | Standardized reference consumption to 95th percentile benchmark ($E_{ref}$). |
| 5 | Manual slider entry friction | Users had to look up weather manually | Integrated OpenWeatherMap REST API with 1-click slider auto-population. |
| 6 | Security risk from exposed API credentials | Prototype code hard-coded API tokens | Secured tokens using environment variables, Vite client config, and fallback defaults. |

### 6.6 Objectives vs. Outcomes

**Table 6.3: Objectives vs. outcomes**

| Project Objective | Outcome Achieved | Status |
| :--- | :--- | :---: |
| **Develop & compare SGD Log-Reg and Random Forest models** | Both models implemented; Random Forest superior ($R^2$ 0.6342 vs 0.5631) | Achieved |
| **Evaluate models using MAE, MSE, RMSE, R², and MAPE** | All 5 regression metrics computed and benchmarked (Table 6.1) | Achieved |
| **Estimate electricity tariff cost and carbon footprint** | Instant calculation of Cost (₹8.40/kWh) and $CO_2$ (0.716 kg/kWh) on every run | Achieved |
| **Deploy an accessible, responsive web application** | Production single-page web app deployed using React 18, TypeScript, and Vite | Achieved |
| **Validate against empirical residential smart-meter logs** | Benchmarked on 6,000-record physical dataset; hardware validation planned | Partially Achieved |

---

## CHAPTER 7: CONCLUSION AND FUTURE SCOPE

### 7.1 Conclusion
The EcoWatt project successfully demonstrates the synergy of physics-informed machine learning and modern web technologies to promote domestic energy efficiency and climate awareness. By decomposing electrical energy into deterministic appliance wattage and learned environmental residuals, the platform achieves robust predictive performance while respecting physical thermodynamic principles. Evaluated on a 6,000-record benchmark dataset, the Random Forest Regressor demonstrated superior accuracy ($R^2 = 0.6342$, $\text{MAE} = 1.1228\text{ kWh}$) compared to the SGD Logarithmic Regression pipeline ($R^2 = 0.5631$, $\text{MAE} = 1.2262\text{ kWh}$).

Crucially, the project advances beyond typical academic simulations by deploying a lightning-fast, production-grade web application built with React 18, TypeScript, and Vite. Integrating live weather telemetry via OpenWeatherMap, automated KSEB tariff calculation, CEA grid carbon auditing, and actionable energy reduction recommendations, EcoWatt provides consumers with a powerful tool to reduce domestic electricity bills while supporting UN Sustainable Development Goals 7 and 13.

### 7.2 Future Scope
1. **IoT & Hardware Integration:** Interfacing with low-cost smart plugs (e.g., ESP32 or Zigbee-based smart meters) to replace manual slider entry with real-time empirical power logging.
2. **Advanced Deep Learning Time-Series Models:** Integrating Long Short-Term Memory (LSTM) networks or Temporal Fusion Transformers (TFT) for multi-horizon seasonal load forecasting.
3. **Dynamic Tariff & Grid Demand Response:** Incorporating live time-of-day (ToD) tariff APIs to schedule heavy domestic loads (e.g., EV charging, washing machines) during off-peak solar hours.
4. **Mobile Progressive Web App (PWA):** Packaging the web application as an offline-first PWA with push notifications alerting users during high grid emission periods.

---

## REFERENCES

- **[1]** M. Khalil, S. McGough, Z. Pourmirza, M. Pazhoohesh, and S. Walker, “Machine learning, deep learning and statistical analysis for forecasting building energy consumption—A systematic review,” *Engineering Applications of Artificial Intelligence*, vol. 115, Art. no. 105287, 2022.
- **[2]** United Nations, “Sustainable Development Goals: Goal 7 — Affordable and Clean Energy.” [Online]. Available: https://sdgs.un.org/goals/goal7 (accessed: 15 Oct. 2026).
- **[3]** United Nations, “Sustainable Development Goals: Goal 13 — Climate Action.” [Online]. Available: https://sdgs.un.org/goals/goal13 (accessed: 15 Oct. 2026).
- **[4]** K. Amasyali and N. M. El-Gohary, “A review of machine learning approaches for building energy consumption prediction,” *Journal of Building Engineering*, vol. 17, pp. 209–225, 2021.
- **[5]** Y. Wang, Q. Chen, and M. Shahidehpour, “AI-empowered smart energy forecasting and demand-side management,” *International Journal of Precision Engineering and Manufacturing – Green Technology*, vol. 10, no. 3, pp. 581–598, 2023.
- **[6]** Department of Economics and Statistics, Government of Kerala, “Compendium of Project Reports 2024 – Cherukunnu Gramapanchayath Socio-Economic Survey 2021.” [Online]. Available: https://www.ecostat.kerala.gov.in/publication-detail/compendium-of-project-reports-2024 (accessed: 15 Oct. 2026).
- **[7]** L. M. Candanedo, V. Feldheim, and D. Deramaix, “Appliances Energy Prediction Data Set,” *UCI Machine Learning Repository*, 2017. [Online]. Available: https://archive.ics.uci.edu/dataset/374/appliances+energy+prediction (accessed: 15 Oct. 2026).
- **[8]** G. Hébrail and A. Berard, “Individual Household Electric Power Consumption Data Set,” *UCI Machine Learning Repository*, 2012. [Online]. Available: https://archive.ics.uci.edu/dataset/235/individual+household+electric+power+consumption (accessed: 15 Oct. 2026).
- **[9]** F. Pedregosa et al., “Scikit-learn: Machine learning in Python,” *Journal of Machine Learning Research*, vol. 12, pp. 2825–2830, 2011.
- **[10]** L. Breiman, “Random forests,” *Machine Learning*, vol. 45, pp. 5–32, 2001.
- **[11]** Central Electricity Authority, “CO₂ Baseline Database for the Indian Power Sector,” Government of India. [Online]. Available: https://cea.nic.in/cdm-co2-baseline-database/ (accessed: 15 Oct. 2026).
- **[12]** G. James, D. Witten, T. Hastie, and R. Tibshirani, *An Introduction to Statistical Learning: with Applications in Python*. Springer, 2023.
- **[13]** React Documentation, “React – A JavaScript library for building user interfaces.” [Online]. Available: https://react.dev/ (accessed: 18 Oct. 2026).
- **[14]** OpenWeather, “Current weather data API,” *OpenWeatherMap*. [Online]. Available: https://openweathermap.org/api (accessed: 18 Oct. 2026).

---

## APPENDIX A: SOURCE CODE

The complete source code is maintained on GitHub (Section 5.4). Below is the TypeScript implementation of the physics-informed machine learning engine (`mlEngine.ts`) executed in-browser by the EcoWatt / GreenFuture platform:

```typescript
// mlEngine.ts - Core In-Browser Machine Learning & Analytics Engine
export interface DataRow {
  Temperature: number; Time: number; Humidity: number; PowerRating: number;
  UsageDuration: number; NumDevices: number; Occupancy: number;
  EnergyConsumption: number; E_load: number; EnergyResidual: number;
}

export function generateSampleDataset(dataSize: number = 200): DataRow[] {
  const rng = new SeededRandom(42);
  const rows: DataRow[] = [];
  for (let i = 0; i < dataSize; i++) {
    const temp = rng.nextInt(20, 40), hour = rng.nextInt(0, 24);
    const hum = rng.nextInt(40, 90), pwr = rng.nextInt(100, 2500);
    const dur = Number(rng.nextUniform(0.5, 10).toFixed(2));
    const dev = rng.nextInt(1, 10), occ = rng.nextInt(1, 6);
    const eLoad = (pwr * dur * dev) / 1000.0;
    const energy = eLoad + 0.3 * temp + 0.1 * hum + 0.5 * occ + rng.nextNormal(0, 2);
    rows.push({
      Temperature: temp, Time: hour, Humidity: hum, PowerRating: pwr,
      UsageDuration: dur, NumDevices: dev, Occupancy: occ,
      EnergyConsumption: Number(energy.toFixed(4)),
      E_load: Number(eLoad.toFixed(4)),
      EnergyResidual: Number((energy - eLoad).toFixed(4)),
    });
  }
  return rows;
}

export function evaluatePredictions(yTrue: number[], yPred: number[], modelName: string) {
  const n = yTrue.length;
  let sumAE = 0, sumSE = 0, sumAPE = 0, sumY = 0;
  for (let i = 0; i < n; i++) {
    const yt = yTrue[i], yp = Math.max(0, yPred[i]), diff = yt - yp;
    sumAE += Math.abs(diff); sumSE += diff * diff;
    sumAPE += (Math.abs(diff) / Math.max(yt, 1e-8)) * 100; sumY += yt;
  }
  const meanY = sumY / n;
  let totalSS = 0; for (let i = 0; i < n; i++) totalSS += (yTrue[i] - meanY) ** 2;
  return {
    Model: modelName,
    MAE: Number((sumAE / n).toFixed(4)),
    MSE: Number((sumSE / n).toFixed(4)),
    RMSE: Number(Math.sqrt(sumSE / n).toFixed(4)),
    R2: Number((totalSS > 0 ? 1 - sumSE / totalSS : 0).toFixed(4)),
    MAPE: Number((sumAPE / n).toFixed(2))
  };
}
```

---

## APPENDIX B: SCREENSHOTS

The following screenshots and graphical outputs illustrate the user interface and analytics dashboards of the deployed EcoWatt web application:
- **Figure B.1:** The modern landing hero page featuring ambient clean-energy design motifs, platform highlights, and dark/light mode toggle.
- **Figure B.2:** The interactive prediction simulator showing live OpenWeatherMap weather conditions, parameter input sliders, predicted kilowatt-hours (46.82 kWh), electricity cost (₹393.26), carbon footprint (33.52 kg $CO_2$), Eco Score, and actionable savings alerts.
- **Figure B.3:** The prediction history audit dashboard displaying logged runs, interactive bar/line trend visualizations, and 1-click CSV export.
- **Figure B.4:** The analytics module displaying 20-record historical energy trends from `EcoWatt_6000.csv` and the typical residential appliance load distribution.

---

## APPENDIX C: MAPPING WITH SUSTAINABLE DEVELOPMENT GOALS

**Table C.1: Mapping with Sustainable Development Goals (SDGs)**

| Sl No | SDG Addressed & Target | How it is Demonstrated in this Project |
| :---: | :--- | :--- |
| **1** | **SDG 7 – Affordable and Clean Energy** *(Target 7.3: Double global rate of energy efficiency improvements)* | EcoWatt accurately predicts domestic appliance power demands, quantifies electricity costs under KSEB tariff slabs, and identifies peak grid hours to empower consumers to reduce overall kilowatt-hour consumption and eliminate wasteful idle power. |
| **2** | **SDG 13 – Climate Action** *(Target 13.3: Build knowledge and capacity to meet climate change)* | The application converts every predicted energy usage scenario into an immediate carbon dioxide footprint ($0.716\text{ kg }CO_2/\text{kWh}$) and an intuitive Eco Score, directly cultivating environmental accountability in everyday residential decisions. |
| **3** | **SDG 11 – Sustainable Cities and Communities** *(Target 11.6: Reduce adverse environmental impact of cities)* | By facilitating residential demand-side management and peak load shifting away from stressed evening hours (6 PM - 9 PM), the platform reduces peak fossil-fuel peaker plant activation across urban electrical grids. |

---

## APPENDIX D: INDIVIDUAL CONTRIBUTION OF TEAM MEMBERS

**Table D.1: Individual contribution of team members**

| Sl. | Name & Register No. | Modules / Tasks Handled | Contribution (%) |
| :---: | :--- | :--- | :---: |
| 1 | **Aaliya Fathima Arif** ([Register No.]) | Literature survey, dataset attribute analysis & Cherukunnu survey documentation | 20% |
| 2 | **Afrah Zulfi** ([Register No.]) | Dataset preprocessing, feature scaling, log1p transformation & metric calculation | 20% |
| 3 | **Muhammed Aasif** ([Register No.]) | OpenWeatherMap API integration, live weather telemetry & UI parameter auto-population | 20% |
| 4 | **Sanju Philip Saji** ([Register No.]) | Random Forest lag matrix formulation, recursive multi-step forecasting & testing | 20% |
| 5 | **S. Vighnesh (Team Leader)** ([Register No.]) | System architecture, TypeScript ML engine, React web application & project coordination | 20% |
