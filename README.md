<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-0.110-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/PyCaret-3.3-orange?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/WebSocket-Real--Time-blueviolet?style=for-the-badge&logo=websocket&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />
</p>

<h1 align="center">🛡️ Secure180</h1>
<h3 align="center">Real-Time Credit Card Fraud Detection System with AutoML</h3>

<p align="center">
  <i>An end-to-end AI-powered fraud detection pipeline that generates synthetic transactions, trains models using AutoML (PyCaret), detects fraud in real-time via WebSockets, and visualizes everything on a live cyberpunk dashboard.</i>
</p>

---

## 📌 Table of Contents

- [Overview](#-overview)
- [System Architecture](#-system-architecture)
- [Data Pipeline](#-data-pipeline)
- [ML Pipeline](#-ml-pipeline)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [API Reference](#-api-reference)
- [Dashboard](#-dashboard)
- [How It Works](#-how-it-works)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

**Secure180** is a complete real-time fraud detection system that simulates a production environment for credit card transaction monitoring. It combines **AutoML model training**, **real-time transaction simulation**, **instant fraud scoring**, and a **live cyberpunk-themed dashboard** — all in a single, self-contained application.

### Key Highlights

| Feature | Description |
|---------|-------------|
| 🤖 **AutoML Training** | PyCaret compares 8+ ML algorithms and selects the best one automatically |
| 📡 **Real-Time Streaming** | WebSocket-based live data feed — transactions every 2 seconds |
| 🚨 **Instant Alerts** | Color-coded terminal alerts + dashboard toast notifications |
| 🌐 **Interactive Globe** | 3D globe visualization showing fraud origin locations |
| 📊 **6 Live Charts** | Doughnut, line, radar, bar, hourly, and geospatial visualizations |
| ⚡ **Sub-100ms Detection** | Millisecond-level fraud scoring per transaction |
| 🗄️ **Persistent Storage** | SQLite database for transaction history and model metrics |

---

## 🏗️ System Architecture

```mermaid
graph TB
    subgraph "Data Layer"
        A[("🗃️ Synthetic Data<br/>Generator")] -->|50K transactions| B[("📁 creditcard_sample.csv")]
        B --> C["⚖️ SMOTE<br/>Balancing"]
    end

    subgraph "ML Layer"
        C --> D["🔧 PyCaret Setup<br/>normalize + fix_imbalance"]
        D --> E["🏆 compare_models()<br/>8 algorithms"]
        E --> F["🎯 tune_model()<br/>Hyperparameter Tuning"]
        F --> G[("💾 best_fraud_model.pkl")]
    end

    subgraph "Application Layer"
        H["🎲 Transaction<br/>Simulator"] -->|every 2s| I["🛡️ Fraud<br/>Detector"]
        G --> I
        I --> J["🗄️ SQLite<br/>Database"]
        I --> K["🚨 Alert<br/>System"]
        I --> L["📡 WebSocket<br/>Broadcast"]
    end

    subgraph "API Layer (FastAPI)"
        L --> M["🌐 REST Endpoints"]
        L --> N["🔌 WebSocket /ws"]
        M --> O["📊 Dashboard"]
        N --> O
    end

    style A fill:#1a1a2e,stroke:#00d4ff,color:#fff
    style G fill:#1a1a2e,stroke:#00ff9d,color:#fff
    style I fill:#1a1a2e,stroke:#ff2d55,color:#fff
    style O fill:#1a1a2e,stroke:#a855f7,color:#fff
```

---

## 🔄 Data Pipeline

```mermaid
flowchart LR
    A["make_classification()<br/>10K samples, 29 features"] --> B["Feature Engineering<br/>V1-V28 + Amount + Time"]
    B --> C["Class Imbalance<br/>99% legit, 1% fraud"]
    C --> D["SMOTE Oversampling<br/>Balance to ~50/50"]
    D --> E["Export CSV<br/>creditcard_sample.csv"]

    style A fill:#0d1b2a,stroke:#00d4ff,color:#e0e0e0
    style B fill:#0d1b2a,stroke:#00d4ff,color:#e0e0e0
    style C fill:#0d1b2a,stroke:#ffb800,color:#e0e0e0
    style D fill:#0d1b2a,stroke:#00ff9d,color:#e0e0e0
    style E fill:#0d1b2a,stroke:#a855f7,color:#e0e0e0
```

---

## 🧠 ML Pipeline

```mermaid
flowchart TD
    A["📥 Load Dataset"] --> B["⚙️ PyCaret Setup<br/>normalize=True<br/>fix_imbalance=True<br/>session_id=42"]
    B --> C["🏁 compare_models()"]
    
    C --> D1["Random Forest"]
    C --> D2["Extra Trees"]
    C --> D3["Gradient Boosting"]
    C --> D4["Logistic Regression"]
    C --> D5["Decision Tree"]
    C --> D6["KNN"]
    C --> D7["Naive Bayes"]
    C --> D8["AdaBoost"]
    
    D1 & D2 & D3 & D4 & D5 & D6 & D7 & D8 --> E["🏆 Best Model<br/>Selected by F1 Score"]
    E --> F["🔧 tune_model()<br/>Hyperparameter Optimization"]
    F --> G["💾 Save Model<br/>best_fraud_model.pkl"]
    F --> H["📊 Save Metrics<br/>model_comparison.json"]

    style E fill:#1a1a2e,stroke:#00ff9d,color:#fff
    style F fill:#1a1a2e,stroke:#ffb800,color:#fff
    style G fill:#1a1a2e,stroke:#00d4ff,color:#fff
```

### Model Comparison Metrics

| Metric | Description |
|--------|-------------|
| **F1 Score** | Primary selection criterion — harmonic mean of precision and recall |
| **AUC** | Area Under ROC Curve — overall discriminative ability |
| **Precision** | Ratio of true positives to predicted positives |
| **Recall** | Ratio of true positives to actual positives |
| **Accuracy** | Overall correct predictions |

---

## ✨ Features

### 🔬 Detection Engine
- **AutoML model selection** across 8 classification algorithms
- **Hyperparameter tuning** with F1 optimization
- **Three-tier risk classification**: LOW / MEDIUM / HIGH
- **Configurable thresholds** (fraud: 0.5, high-risk: 0.7)

### 📡 Real-Time Processing
- **WebSocket streaming** — live transaction feed to all connected clients
- **2-second intervals** — simulated transaction generation
- **Broadcast architecture** — multiple dashboard instances supported
- **Automatic stats refresh** — KPIs update every 5 transactions

### 📊 Dashboard Visualizations
- **Doughnut Chart** — Legit vs. fraud transaction ratio
- **Live Line Chart** — Streaming transaction amounts (last 60)
- **Radar Chart** — Fraud distribution by merchant category
- **Bar Chart** — Fraud rate per store category
- **3D Globe** — Geographic fraud origin visualization
- **Hourly Chart** — Fraud activity by hour of day

### 🚨 Alert System
- **Terminal alerts** with color-coded severity (🚨 RED / 🟡 YELLOW / ✅ GREEN)
- **Dashboard toast notifications** for fraud events
- **Persistent fraud log** file for audit trail
- **Risk-level badges** on all transaction records

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend** | FastAPI + Uvicorn | REST API + WebSocket server |
| **ML Engine** | PyCaret 3.3 | AutoML training and prediction |
| **Database** | SQLite + SQLAlchemy | Transaction & model storage |
| **Frontend** | Vanilla HTML/CSS/JS | Single-file cyberpunk dashboard |
| **Charts** | Chart.js 4.4 | Interactive data visualizations |
| **Globe** | Globe.gl | 3D geospatial fraud mapping |
| **Data Gen** | scikit-learn + imbalanced-learn | Synthetic dataset + SMOTE |
| **Streaming** | WebSockets | Real-time bi-directional communication |

---

## 📁 Project Structure

```
Secure360/
└── fraud_detection_system/
    ├── run_system.py              # 🚀 Main entry point — orchestrates everything
    ├── config.py                  # ⚙️ Global configuration (thresholds, paths)
    ├── requirements.txt           # 📦 Python dependencies
    │
    ├── api/
    │   ├── __init__.py
    │   └── main_api.py            # 🌐 FastAPI app — REST + WebSocket endpoints
    │
    ├── models/
    │   ├── __init__.py
    │   ├── automl_trainer.py      # 🤖 PyCaret AutoML training pipeline
    │   └── saved_model/
    │       └── best_fraud_model.pkl  # 💾 Trained model (generated)
    │
    ├── realtime/
    │   ├── __init__.py
    │   ├── fraud_detector.py      # 🛡️ Real-time prediction engine
    │   └── transaction_simulator.py # 🎲 Synthetic transaction generator
    │
    ├── database/
    │   ├── __init__.py
    │   ├── db_handler.py          # 🗄️ SQLite operations & queries
    │   └── fraud_detection.db     # 📀 Database file (generated)
    │
    ├── alerts/
    │   ├── __init__.py
    │   ├── alert_system.py        # 🚨 Terminal alerts & fraud logging
    │   └── fraud_alerts.log       # 📝 Fraud audit log (generated)
    │
    ├── data/
    │   ├── __init__.py
    │   ├── generate_dataset.py    # 📊 Synthetic data + SMOTE pipeline
    │   ├── creditcard_sample.csv  # 📁 Generated dataset (50K rows)
    │   └── model_comparison.json  # 📈 AutoML comparison results
    │
    └── dashboard/
        ├── __init__.py
        └── index.html             # 🎨 Cyberpunk dashboard (single file)
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+** (required for PyCaret 3.x compatibility)
- **pip** package manager

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/Secure360.git
cd Secure360/fraud_detection_system

# 2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch the system
python run_system.py
```

### What Happens on Launch

```mermaid
sequenceDiagram
    participant User
    participant System as run_system.py
    participant Data as generate_dataset.py
    participant ML as automl_trainer.py
    participant DB as db_handler.py
    participant API as FastAPI Server

    User->>System: python run_system.py
    System->>Data: Check/Generate dataset
    Data-->>System: ✅ 50K transactions ready
    System->>ML: Check/Train model
    ML-->>System: ✅ Best model saved (.pkl)
    System->>DB: Initialize tables
    DB-->>System: ✅ SQLite ready
    System->>API: Start Uvicorn server
    API-->>User: 🌐 http://localhost:8000
    
    loop Every 2 seconds
        API->>API: Generate transaction
        API->>API: Predict fraud
        API->>API: Store + Alert + Broadcast
    end
```

### Access Points

| Service | URL |
|---------|-----|
| 🌐 **Dashboard** | [http://localhost:8000](http://localhost:8000) |
| 📡 **WebSocket** | `ws://localhost:8000/ws` |
| 📖 **API Docs** | [http://localhost:8000/docs](http://localhost:8000/docs) |

---

## 📡 API Reference

### REST Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Serve the dashboard HTML |
| `GET` | `/health` | Health check — model status |
| `GET` | `/stats` | Fraud statistics + model info |
| `GET` | `/transactions?limit=100` | Recent transactions |
| `GET` | `/transactions/fraud?limit=50` | Fraud-only transactions |
| `GET` | `/model-comparison` | AutoML model comparison results |
| `GET` | `/hourly-stats` | Fraud count by hour |
| `GET` | `/category-stats` | Fraud rate by merchant category |

### WebSocket

| Endpoint | Message Types |
|----------|---------------|
| `ws://localhost:8000/ws` | `transaction` — new transaction data |
| | `stats_update` — refreshed KPI metrics |

**Example WebSocket message:**
```json
{
  "type": "transaction",
  "data": {
    "transaction_id": "a1b2c3d4-...",
    "timestamp": "2026-02-20T11:30:00",
    "amount": 2450.00,
    "merchant_category": "electronics",
    "location": "Lagos/Nigeria",
    "fraud_probability": 0.9234,
    "prediction": 1,
    "risk_level": "HIGH",
    "processing_time_ms": 45.23,
    "model_used": "AutoML"
  }
}
```

---

## 🎨 Dashboard

The dashboard features a **cyberpunk-inspired UI** with real-time data streaming:

### Dashboard Layout

```
┌──────────────────────────────────────────────────────┐
│  🛡️ FRAUDSHIELD AI            🔴 LIVE    ● CONNECTED │
├──────────────────────────────────────────────────────┤
│ [Total] [Fraud] [Rate%] [Saved$] [Speed] [Model]    │  ← KPI Cards
├──────────┬─────────────────┬─────────────────────────┤
│ 🍩 Donut │  📈 Live Line   │  📡 Radar              │  ← Charts Row 1
├──────────┴─────────────────┤─────────────────────────┤
│ 🛒 Category│ 🌍 Globe       │  🕐 Hourly             │  ← Charts Row 2
├─────────────────────────────┬────────────────────────┤
│ 📋 Transaction Feed         │  🚨 Fraud Alerts       │  ← Bottom Row
└─────────────────────────────┴────────────────────────┘
```

### Visual Features
- **Dark cyberpunk theme** with grid background and neon accents
- **Real-time animations** — slide-in rows, pulsing indicators, toast alerts
- **6 KPI cards** with color-coded borders (cyan, red, yellow, green, purple)
- **Interactive 3D globe** showing fraud origin hotspots
- **Fully responsive** — works on desktop, tablet, and mobile

> 📸 **Add your own screenshots below after running the system!**
> 
> Place screenshots in a `screenshots/` folder and update the paths:
> 
> ```markdown
> ![Dashboard Overview](screenshots/dashboard_overview.png)
> ![Fraud Alert Toast](screenshots/fraud_alert.png)
> ![3D Globe](screenshots/globe_view.png)
> ```

---

## ⚙️ How It Works

### 1. Data Generation (`data/generate_dataset.py`)
- Uses `sklearn.make_classification()` to create **10,000 synthetic transactions** with 29 features (V1–V28 + Amount)
- Applies **SMOTE** (Synthetic Minority Oversampling) to balance fraud/legit classes
- Saves balanced dataset to `creditcard_sample.csv`

### 2. Model Training (`models/automl_trainer.py`)
- **PyCaret AutoML** compares 8 classification models:
  - Random Forest, Extra Trees, Gradient Boosting, Logistic Regression, Decision Tree, KNN, Naive Bayes, AdaBoost
- Best model selected by **F1 Score**
- Winner is **hyperparameter-tuned** and saved as `.pkl`

### 3. Real-Time Detection (`realtime/`)
- **Transaction Simulator** generates realistic transactions every 2 seconds
  - ~2% fraud rate with high-amount, suspicious-location patterns
- **Fraud Detector** loads the trained model and scores each transaction
  - Returns probability, prediction, risk level, and processing time

### 4. Alert System (`alerts/alert_system.py`)
- Color-coded terminal output: 🚨 Fraud / 🟡 Suspicious / ✅ Legitimate
- Persistent `fraud_alerts.log` for audit compliance

### 5. API & Dashboard (`api/` + `dashboard/`)
- **FastAPI** serves REST endpoints and WebSocket connections
- **Single HTML dashboard** connects via WebSocket for live updates
- **Chart.js** renders 6 interactive visualizations
- **Globe.gl** provides 3D geographic fraud mapping

### Risk Classification

```
┌─────────────────────────────────────────────┐
│  Fraud Probability    →    Risk Level       │
├─────────────────────────────────────────────┤
│     0.0 - 0.4         →    🟢 LOW          │
│     0.4 - 0.7         →    🟡 MEDIUM       │
│     0.7 - 1.0         →    🔴 HIGH         │
└─────────────────────────────────────────────┘
```

---

## 🔧 Configuration

All settings are in `config.py`:

```python
DATABASE_PATH = "database/fraud_detection.db"
MODEL_SAVE_PATH = "models/saved_model/best_fraud_model"
FRAUD_THRESHOLD = 0.5          # Minimum probability to flag as fraud
HIGH_RISK_THRESHOLD = 0.7      # Threshold for HIGH risk level
TRANSACTION_INTERVAL_SECONDS = 2  # Seconds between simulated transactions
HOST = "0.0.0.0"
PORT = 8000
```

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👩‍💻 Author

**Gagandeep Kaur** (E11625)

---

<p align="center">
  <i>Built with ❤️ using Python, FastAPI, PyCaret, and Chart.js</i>
</p>
