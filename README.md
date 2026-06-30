# ⚡ Vattenfall Wind Operations: SCADA Power Curve & Anomaly Monitor

An enterprise-grade, physics-informed Machine Learning pipeline and interactive control-room dashboard designed to optimize renewable energy assets. This platform ingests high-frequency wind turbine SCADA (Supervisory Control and Data Acquisition) logs, applies engineering physics baseline constraints, and runs unsupervised anomaly detection to catch structural degradation, mechanical faults, and aerodynamic inefficiencies early.

---

## 🚀 The Core Engineering Problem

Wind turbines are complex mechanical structures operating in harsh environments. Standard static threshold alerts (e.g., *“Alert if temperature > 80°C”*) fail to catch silent killers like slow bearing degradation or aerodynamic blade misalignments because sensor outputs look "normal" when viewed in isolation. 

This project solves that by bridging **Industrial Domain Physics** with **Multivariate Machine Learning**. It flags anomalous performance by assessing how variables move *together*—specifically mapping wind velocity, actual active power yield, and internal component temperatures simultaneously.

---

## 🏗️ System Architecture & Workflow

The codebase strictly adheres to a clean, production-ready modular layout, separating ingestion layers from feature analytics and modeling components:

```text
wind-turbine-scada-analytics/
├── requirements.txt         # Project runtime dependencies
├── config.py                 # Structural parameters & physics baselines
├── data_simulator.py         # Multi-variable SCADA telemetry stream simulator
├── app.py                    # Streamlit Operator Dashboard (UI)
└── pipeline/
    ├── ingestion.py          # Data validation, cleansing & sequencing
    └── features.py           # Physics-informed power curve calculations
└── models/
    └── anomaly_detector.py   # Multivariate Isolation Forest core engine
```

---

### 🧠 The Pipeline Under the Hood:
- Data Ingestion (**pipeline/ingestion.py**): Ingests raw telemetry logs, enforces chronological sequencing, handles missing sensor data, and strips out corrupted entries.
- Feature Engineering (**pipeline/features.py**): Calculates the Theoretical Power Curve based on aerodynamic cubic principles (Cut-in, Rated, and Cut-out wind limits). It extracts critical indicators like power_deviation and rolling high-frequency structural variance.
- Multivariate ML Inference (**models/anomaly_detector.py**): Uses an Isolation Forest ensemble model to evaluate multi-dimensional spaces. It scores data based on how far a point drifts from healthy structural baselines.
- Actionable Operations (**app.py**): Exposes a clean, high-visibility control dashboard for grid operators, translating technical data arrays into priority-ranked maintenance dispatches.

---

### Tech Stack & Competencies
- Language: Python 3.10+
- Data Science & ML: Pandas, NumPy, Scikit-learn (Isolation Forest), Statsmodels
- Visualization & UI: Streamlit, Plotly Express, Plotly Graph Objects
- Infrastructure Patterns: Modular pipeline architecture, configuration decoupling, data validation workflows.

---

### 🏃 Quickstart: Run the Control Room Locally

Follow these quick steps to stand up the pipeline and explore the interactive control center:
1. Clone the repository and navigate into it:
```bash

git clone https://github.com/HopeyCodeDS/wind-turbine-scada-analytics
cd wind-turbine-scada-analytics
```

2. Set up your environment and install requirements:
```bash

# Create a virtual environment

python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

3. Spin up the live Streamlit dashboard:
```bash

streamlit run app.py
```

Your browser will automatically open a tab showing the dashboard running live on http://localhost:8501.

---

### 💼 Business Impact & Core Focus
- 🎯 Predictive Over Reactive: Shifting workflows from reactive repairs to predictive dispatching, minimizing asset downtime.
- 📈 Target Alignment: Built with scalability in mind to support the optimization of high-capacity wind, solar, and battery energy storage assets.
- 🤝 Domain Integration: Developed to bridge the gap between heavy operational sensor telemetry and strategic executive-level decision making.