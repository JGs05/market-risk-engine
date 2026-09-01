import pytest
import numpy as np
import pandas as pd
from src.engine import RiskEngine
from src.backtesting import RegulatoryBacktest
from src.stress_testing import StressTester

@pytest.fixture
def mock_returns():
    np.random.seed(42)
    dates = pd.date_range("2023-01-01", periods=250)
    data = np.random.normal(0.0005, 0.012, size=(250, 3))
    return pd.DataFrame(data, index=dates, columns=["SPY", "QQQ", "TLT"])

def test_var_monotonicity(mock_returns):
    weights = [0.4, 0.4, 0.2]
    res_95 = RiskEngine.calculate_var_es(mock_returns, weights, 1_000_000, alpha=0.95, horizon=1)
    res_99 = RiskEngine.calculate_var_es(mock_returns, weights, 1_000_000, alpha=0.99, horizon=1)
    
    assert res_99["parametric"]["VaR"] > res_95["parametric"]["VaR"]
    assert res_99["historical"]["ES"] >= res_99["historical"]["VaR"]

def test_kupiec_green_zone():
    losses = np.array([100, 200, 50, 400, 10])
    var_series = np.array([500] * 5)
    res = RegulatoryBacktest.kupiec_test(losses, var_series, alpha=0.99)
    
    assert res["basel_zone"] == "GREEN"
    assert res["exceptions"] == 0

def test_stress_testing():
    res = StressTester.run_historical_stress(1_000_000, ["SPY"], [1.0])
    assert "2008_Lehman_Crisis" in res
    assert res["2008_Lehman_Crisis"] < 0  # Market shock should cause loss