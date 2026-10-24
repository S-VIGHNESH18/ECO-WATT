# 🌱 EcoWatt (GreenFuture) — Smart Energy Intelligence & Sustainability Platform

[![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Vite](https://img.shields.io/badge/Vite-6.x-646CFF?logo=vite&logoColor=white)](https://vitejs.dev/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-v4-06B6D4?logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)


An intelligent, next-generation energy analytics dashboard and machine-learning driven forecasting platform designed to optimize household and commercial power consumption, reduce peak-hour strain, calculate actionable carbon emissions ($CO_2$), and improve consumer eco-scores.

---

## ✨ Key Features

- **⚡ Real-Time ML Consumption Forecaster**:
  - Predicts energy usage ($\text{kWh}$) based on live multi-variable parameters: ambient temperature, humidity, power ratings, device count, room occupancy, and appliance load.
  - Implements trained linear regression & multi-factor ML inference models (`mlEngine.ts`).

- **🌿 Eco-Score & Sustainability Metrics**:
  - Dynamically calculates consumer **Eco-Score (0–100)**.
  - Computes carbon emissions ($kg\text{ }CO_2$), estimated cost in INR ($\text{₹}$), and potential energy savings ($\%$) with personalized eco-tips.

- **📊 Comprehensive Interactive Analytics**:
  - Real-time time-series trends and peak-demand classification.
  - Appliance-level energy distribution breakdowns (HVAC, refrigeration, lighting, electronics).
  - Multi-scenario simulation tools for peak load shifting.

- **📑 Automated Comprehensive Report Generator**:
  - Built-in Python generator (`build_complete_report.py`) capable of compiling complete academic and industrial documentation with high-resolution vector architecture & flow diagrams.
  - Generates ready-to-publish `.docx`, `.pdf`, and `.md` reports.

- **🎨 Modern Responsive UI / UX**:
  - Dark & Light mode system with fluid transitions.
  - Glassmorphic interface styled with Tailwind CSS v4 and smooth Framer Motion micro-interactions.

---

## 🛠️ Tech Stack

### Frontend & Dashboard
- **Framework**: [React 19](https://react.dev/)
- **Language**: [TypeScript](https://www.typescriptlang.org/)
- **Build Tool**: [Vite](https://vitejs.dev/)
- **Styling**: [Tailwind CSS v4](https://tailwindcss.com/) + Custom Glassmorphism
- **Animations**: [Motion](https://motion.dev/)
- **Icons**: [Lucide React](https://lucide.dev/)

### Machine Learning & Data Pipeline
- **Client ML Engine**: Multi-variable Linear Regression & Forecast Algorithms (`src/utils/mlEngine.ts`)
- **Dataset**: `EcoWatt_6000.csv` (Synthetic & real-world continuous load records)
- **Report Generation**: Python (`python-docx`, `matplotlib`, `seaborn`)

---

## 📂 Project Structure

```text
GreenFuture/
├── public/                     # Static assets & dataset (EcoWatt_6000.csv, favicons)
├── report_figures/             # High-res diagrams (Architecture, Workflow, Use Case, ML Comparison)
├── src/
│   ├── assets/                 # Icons and branding illustrations
│   ├── components/             # React modular components
│   │   ├── EcoWattSimulator.tsx    # Interactive simulation & control dashboard
│   │   ├── EcoWattAnalytics.tsx    # Visual analytics, charts, & metrics
│   │   ├── Header.tsx              # Navigation & theme controls
│   │   ├── HeroLeft.tsx            # Hero value proposition
│   │   └── HeroRight.tsx           # Live preview & metric summary cards
│   ├── context/
│   │   └── ThemeContext.tsx        # Dark / Light theme provider
│   ├── utils/
│   │   └── mlEngine.ts             # Energy calculation & ML inference utilities
│   ├── App.tsx                 # Root layout & composition
│   ├── main.tsx                # Application entrypoint
│   └── index.css               # Global theme & typography styles
├── EcoWatt_Project_Report.pdf  # Compiled full research & technical project report
├── EcoWatt_Project_Report.docx # Formatted DOCX report
├── EcoWatt_Project_Report.md   # Markdown version of comprehensive report
├── build_complete_report.py    # Python script for generating the report & figures
├── package.json                # Project dependencies and npm scripts
└── vite.config.ts              # Vite build configuration
```

---

## 🚀 Getting Started

### Prerequisites
- [Node.js](https://nodejs.org/) (v18.0.0 or higher recommended)
- `npm` or `yarn` / `pnpm`

### Installation & Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/S-VIGHNESH18/projects.git
   cd projects/GreenFuture
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the local development server**:
   ```bash
   npm run dev
   ```
   Open [http://localhost:5173](http://localhost:5173) in your browser to view the app.

4. **Build for production**:
   ```bash
   npm run build
   ```

---

## 📄 Automated Report Generation

To regenerate the project documentation, figures, and research paper:

```bash
# Ensure Python 3.9+ is installed with necessary libraries
pip install python-docx matplotlib seaborn pandas

# Run the complete report builder
python build_complete_report.py
```

Outputs will be saved in `EcoWatt_Project_Report.docx` and `report_figures/`.

---

## 👨‍💻 Author

**S Vighnesh **  
- GitHub: [@S-VIGHNESH18](https://github.com/S-VIGHNESH18)

