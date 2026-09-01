import numpy as np
from typing import Dict, List

class StressTester:
    # Standard historical shock scenarios mapping to tickers
    SCENARIOS = {
        "2008_Lehman_Crisis": {"SPY": -0.0903, "QQQ": -0.0895, "TLT": 0.0245, "HYG": -0.0520},
        "2020_COVID_Shock": {"SPY": -0.1198, "QQQ": -0.1232, "TLT": -0.0150, "HYG": -0.0710},
        "1987_Black_Monday": {"SPY": -0.2040, "QQQ": -0.2040, "TLT": 0.0400, "HYG": -0.1200},
        "Stagflation_Rates_Up": {"SPY": -0.0450, "QQQ": -0.0650, "TLT": -0.0820, "HYG": -0.0410}
    }

    @classmethod
    def run_historical_stress(cls, nav: float, tickers: List[str], weights: List[float]) -> Dict[str, float]:
        results = {}
        for scenario_name, shocks in cls.SCENARIOS.items():
            pnl = 0.0
            for ticker, weight in zip(tickers, weights):
                # Default to -5% shock if ticker is missing from scenario mapping
                shock = shocks.get(ticker, -0.05)
                pnl += weight * shock * nav
            results[scenario_name] = float(pnl)
        return results