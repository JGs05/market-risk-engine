import numpy as np
from scipy import stats
from typing import Dict, Any

class RegulatoryBacktest:
    @staticmethod
    def kupiec_test(realized_losses: np.ndarray, var_series: np.ndarray, alpha: float = 0.99) -> Dict[str, Any]:
        N = len(realized_losses)
        exceptions = int(np.sum(realized_losses > var_series))
        p = 1 - alpha
        p_hat = exceptions / N if N > 0 else 0

        if exceptions == 0:
            lr = -2 * np.log((1 - p) ** N)
        else:
            lr = -2 * ((N - exceptions) * np.log(1 - p) + exceptions * np.log(p) -
                       (N - exceptions) * np.log(1 - p_hat) - exceptions * np.log(p_hat))

        p_value = 1 - stats.chi2.cdf(lr, df=1)

        if exceptions <= 4:
            zone = "GREEN"
        elif exceptions <= 9:
            zone = "YELLOW"
        else:
            zone = "RED"

        return {
            "observations": N,
            "exceptions": exceptions,
            "expected_exceptions": round(N * p, 2),
            "lr_statistic": float(lr),
            "p_value": float(p_value),
            "basel_zone": zone
        }