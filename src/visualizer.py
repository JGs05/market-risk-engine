import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

class RiskVisualizer:
    @staticmethod
    def plot_return_distribution(returns: pd.DataFrame, weights: np.ndarray, var_99: float, nav: float, save_path: str = "var_plot.png"):
        """Plots the portfolio return distribution and highlights the VaR tail."""
        port_returns = returns.dot(weights).values * nav  # Convert to dollar P&L
        
        plt.figure(figsize=(10, 6))
        sns.histplot(port_returns, bins=50, kde=True, color='blue', alpha=0.6)
        
        # Highlight VaR Threshold
        plt.axvline(x=-var_99, color='red', linestyle='--', linewidth=2, label=f'99% VaR: -${var_99:,.2f}')
        
        # Highlight Tail Risk (Expected Shortfall area)
        kdeline = plt.gca().lines[0]
        x = kdeline.get_xdata()
        y = kdeline.get_ydata()
        plt.fill_between(x, 0, y, where=(x < -var_99), color='red', alpha=0.3, label='Expected Shortfall Region')
        
        plt.title("Portfolio P&L Distribution with Tail Risk")
        plt.xlabel("Daily P&L ($)")
        plt.ylabel("Frequency")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(save_path)
        plt.close()