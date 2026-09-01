from fastapi import FastAPI, HTTPException
from api.schemas import RiskQuery, RiskResponse
from src.database import DataManager
from src.engine import RiskEngine
from src.stress_testing import StressTester
import numpy as np

app = FastAPI(title="Market Risk & Stress Testing Engine", version="1.0.0")
db = DataManager()

@app.post("/api/v1/risk/evaluate", response_model=RiskResponse)
def evaluate_risk(payload: RiskQuery):
    if len(payload.tickers) != len(payload.weights):
        raise HTTPException(status_code=400, detail="Tickers and weights must be equal in length.")
    if not np.isclose(sum(payload.weights), 1.0, atol=1e-3):
        raise HTTPException(status_code=400, detail="Portfolio weights must sum to 1.0.")

    returns = db.fetch_return_matrix(payload.tickers)
    if returns.empty:
        raise HTTPException(status_code=404, detail="No price history found. Ingest tickers first.")

    # Calculate VaR and ES
    metrics = RiskEngine.calculate_var_es(
        returns=returns,
        weights=np.array(payload.weights),
        nav=payload.nav,
        alpha=payload.confidence_level,
        horizon=payload.horizon_days
    )
    
    # Run Stress Tests
    stress_results = StressTester.run_historical_stress(
        nav=payload.nav,
        tickers=payload.tickers,
        weights=payload.weights
    )

    return RiskResponse(
        nav=payload.nav,
        confidence_level=payload.confidence_level,
        horizon_days=payload.horizon_days,
        metrics=metrics,
        stress_tests=stress_results
    )