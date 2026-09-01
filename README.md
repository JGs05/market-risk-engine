# Market Risk & Stress Testing Engine

An institutional-grade Quantitative Risk Engine designed to calculate portfolio exposure under extreme market distress. This engine computes Value-at-Risk (VaR) and Expected Shortfall (ES) using historical, parametric, and Monte Carlo methodologies, aligning with Basel III / FRTB risk frameworks. 

The backend is powered by a localized DuckDB columnar database for high-performance vectorised querying, and exposed via a robust FastAPI REST service.

## 🚀 Key Features
* **Automated Data Ingestion:** Pulls multi-asset daily market data (Equities, Treasuries, Bonds) via Yahoo Finance directly into an embedded DuckDB SQL database.
* **Core Risk Metrics:** Calculates Parametric, Historical Simulation, and Monte Carlo VaR & CVaR (Expected Shortfall) at 95% and 99% confidence intervals over scalable T-day horizons.
* **Historical Stress Testing:** Simulates portfolio drawdowns against historical macroeconomic shocks (e.g., 2008 Lehman Crisis, 2020 COVID Shock, 1987 Black Monday).
* **Regulatory Backtesting:** Implements the Kupiec Proportion of Failures (POF) test to validate VaR models against the Basel Traffic Light framework.
* **Interactive API:** Fully documented REST API via FastAPI and Swagger UI.
* **Tail-Risk Visualization:** Generates publication-grade P&L density distribution charts highlighting VaR thresholds and Expected Shortfall tail regions.

## 🛠️ Tech Stack
* **Language:** Python 3.11+
* **Framework:** FastAPI, Uvicorn, Pydantic
* **Database:** DuckDB
* **Quant & Data Science:** NumPy, SciPy, Pandas, yfinance
* **Visualization:** Matplotlib, Seaborn
* **Testing:** Pytest

---

## ⚙️ Local Setup & Installation

**1. Clone the repository and navigate to the project directory:**
```bash
git clone [https://github.com/YOUR-USERNAME/market-risk-engine.git](https://github.com/YOUR-USERNAME/market-risk-engine.git)
cd market-risk-engine
2. Create and activate a virtual environment:

Mac/Linux: python3 -m venv .venv && source .venv/bin/activate

Windows: python -m venv .venv and then .\.venv\Scripts\Activate.ps1

3. Install dependencies:

Bash
pip install -r requirements.txt

🏃‍♂️ Usage Guide
1. Ingest Market Data
Before calculating risk, populate the DuckDB database with historical asset prices:

Bash
python -c "from src.database import DataManager; db = DataManager(); db.ingest_tickers(['SPY', 'QQQ', 'TLT', 'HYG'])"

2. Start the API Server
Launch the FastAPI application with live-reload:
Bash
uvicorn api.main:app --reload
Navigate to http://127.0.0.1:8000/docs in your browser to access the interactive Swagger UI and run risk evaluations.

3. Generate Tail-Risk Visualizations
To generate a P&L distribution plot for your portfolio (saved as var_plot.png in the root directory):

Bash
python -c "from src.database import DataManager; from src.visualizer import RiskVisualizer; import numpy as np; db = DataManager(); returns = db.fetch_return_matrix(['SPY', 'QQQ', 'TLT']); RiskVisualizer.plot_return_distribution(returns, np.array([0.5, 0.3, 0.2]), 250000, 10000000)"

4. Run the Test Suite
Validate the quantitative math and engine logic using Pytest:
Bash
pytest tests/ -v

📂 Project Architecture
Plaintext
market-risk-engine/
├── api/
│   ├── main.py              # FastAPI application and routing
│   └── schemas.py           # Pydantic data validation models
├── data/
│   └── market_data.duckdb   # Local DuckDB database (Generated)
├── src/
│   ├── backtesting.py       # Kupiec POF and Basel Traffic Light logic
│   ├── database.py          # DuckDB ingestion and query manager
│   ├── engine.py            # VaR and Expected Shortfall math engine
│   ├── stress_testing.py    # Historical crisis factor shocks
│   └── visualizer.py        # Matplotlib/Seaborn charting tools
├── tests/
│   └── test_risk_engine.py  # Automated unit and integration tests
├── .gitignore
├── Dockerfile               # Containerization config
├── README.md                # Project documentation
└── requirements.txt         # Python dependencies
