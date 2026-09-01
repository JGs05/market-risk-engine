import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, Any

class RiskEngine:
    @staticmethod
    def calculate_var_es(returns: pd.DataFrame, weights: np.ndarray, nav: float, alpha: float = 0.99, horizon: int = 10, mc_sims: int = 50_000) -> Dict[str, Any]:
        w = np.array(weights)
        port_returns = returns.dot(w).values

        # 1. Parametric VaR / ES
        mu = np.mean(port_returns)
        sigma = np.std(port_returns, ddof=1)
        z = stats.norm.ppf(alpha)
        
        param_var = (z * sigma - mu) * nav * np.sqrt(horizon)
        param_es = (stats.norm.pdf(z) / (1 - alpha) * sigma - mu) * nav * np.sqrt(horizon)

        # 2. Historical Simulation VaR / ES
        hist_cutoff = np.percentile(port_returns, (1 - alpha) * 100)
        hist_var = -hist_cutoff * nav * np.sqrt(horizon)
        tail_returns = port_returns[port_returns <= hist_cutoff]
        hist_es = -np.mean(tail_returns) * nav * np.sqrt(horizon) if len(tail_returns) > 0 else hist_var

        # 3. Monte Carlo Simulation
        cov_mat = returns.cov().values
        mean_vec = returns.mean().values
        L = np.linalg.cholesky(cov_mat)
        sim_draws = mean_vec + (L @ np.random.normal(size=(len(w), mc_sims))).T
        sim_port = sim_draws.dot(w)
        
        mc_cutoff = np.percentile(sim_port, (1 - alpha) * 100)
        mc_var = -mc_cutoff * nav * np.sqrt(horizon)
        mc_tail = sim_port[sim_port <= mc_cutoff]
        mc_es = -np.mean(mc_tail) * nav * np.sqrt(horizon) if len(mc_tail) > 0 else mc_var

        return {
            "parametric": {"VaR": float(param_var), "ES": float(param_es)},
            "historical": {"VaR": float(hist_var), "ES": float(hist_es)},
            "monte_carlo": {"VaR": float(mc_var), "ES": float(mc_es)},
            "portfolio_daily_vol": float(sigma),
            "portfolio_annual_vol": float(sigma * np.sqrt(252))
        }