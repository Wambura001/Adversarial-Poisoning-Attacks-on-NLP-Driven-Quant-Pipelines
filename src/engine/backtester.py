import numpy as np
import pandas as pd

class QuantSecurityBacktester:
    """
    Event-driven simulation backtester to quantify portfolio alpha loss 
    caused by Adversarial ML Data Poisoning attacks on FinBERT + LSTM models.
    """
    def __init__(self, initial_capital: float = 10_000_000.0, risk_free_rate: float = 0.035):
        """
        Initializes portfolio parameters. 
        Default risk-free rate mapped to Bank of Korea (BOK) base rates.
        """
        self.initial_capital = initial_capital
        self.risk_free_rate = risk_free_rate

    def compute_portfolio_metrics(self, price_series: pd.Series, signals: pd.Series) -> dict:
        """
        Calculates performance and variance tracking data from long/short execution triggers.
        """
        # Calculate base daily market percentage returns
        market_returns = price_series.pct_change().fillna(0)
        
        # Shift signals by 1 day to prevent forward-looking lookahead bias during execution
        strategy_signals = signals.shift(1).fillna(0)
        
        # Calculate daily execution returns
        strategy_returns = market_returns * strategy_signals
        
        # Build capital growth trajectory chart vector
        cumulative_returns = (1 + strategy_returns).cumprod()
        portfolio_value = self.initial_capital * cumulative_returns
        
        # Total Realized Return Calculation
        final_return = cumulative_returns.iloc[-1] - 1
        
        # Calculate Sharpe Ratio (Annualized)
        daily_rf = self.risk_free_rate / 252
        excess_returns = strategy_returns - daily_rf
        if excess_returns.std() != 0:
            sharpe_ratio = (excess_returns.mean() / excess_returns.std()) * np.sqrt(252)
        else:
            sharpe_ratio = 0.0
            
        # Calculate Maximum Drawdown (MDD)
        rolling_max = portfolio_value.cummax()
        drawdowns = (portfolio_value - rolling_max) / rolling_max
        max_drawdown = drawdowns.min()
        
        return {
            "total_return": final_return,
            "sharpe_ratio": sharpe_ratio,
            "max_drawdown": max_drawdown,
            "final_value": portfolio_value.iloc[-1]
        }

    def run_differential_analysis(self, mock_market_data: pd.DataFrame) -> None:
        """
        Runs parallel processing simulations comparing Baseline vs. Attacked states.
        """
        print("\n" + "=" * 80)
        print("QUANTITATIVE BACKTESTING ANALYSIS: CLEAN BASELINE VS POISONED LSTM SIGNALS")
        print("=" * 80)
        
        prices = mock_market_data["Close"]
        clean_signals = mock_market_data["Clean_Signal"]
        poisoned_signals = mock_market_data["Poisoned_Signal"]
        
        # Run Backtests
        baseline_metrics = self.compute_portfolio_metrics(prices, clean_signals)
        attacked_metrics = self.compute_portfolio_metrics(prices, poisoned_signals)
        
        # Calculate Degradation Margins
        lost_alpha = baseline_metrics["total_return"] - attacked_metrics["total_return"]
        mdd_expansion = attacked_metrics["max_drawdown"] - baseline_metrics["max_drawdown"]
        
        # Print Tabular Summary Layout
        print(f"{'Performance Metric':<25} | {'Clean Baseline':<18} | {'Poisoned Execution':<18}")
        print("-" * 80)
        print(f"{'Final Account Value':<25} | ₩{baseline_metrics['final_value']:,.0f} | ₩{attacked_metrics['final_value']:,.0f}")
        print(f"{'Total Strategy Return':<25} | {baseline_metrics['total_return']*100:.2f}% | {attacked_metrics['total_return']*100:.2f}%")
        print(f"{'Annualized Sharpe Ratio':<25} | {baseline_metrics['sharpe_ratio']:.3f} | {attacked_metrics['sharpe_ratio']:.3f}")
        print(f"{'Maximum Drawdown (MDD)':<25} | {baseline_metrics['max_drawdown']*100:.2f}% | {attacked_metrics['max_drawdown']*100:.2f}%")
        print("-" * 80)
        
        print(f"[ATTACK IMPACT SUMMARY]")
        print(f"   ↳ Total Strategy Profit Destruction (Lost Alpha): {lost_alpha*100:.2f}%")
        print(f"   ↳ Risk Exposure Amplification (MDD Delta)     : {abs(mdd_expansion)*100:.2f}% increase in losses")
        print("=" * 80)

# --- Verification & Simulation Initialization ---
if __name__ == "__main__":
    # Generate 100 days of random walk market price charts mirroring a volatile KOSPI stock
    np.random.seed(42)
    dates = pd.date_range(start="2026-01-01", periods=100)
    
    initial_price = 50000 # ~Average price configuration for standard Korean mid-caps
    price_shocks = np.random.normal(0.001, 0.02, 100)
    price_path = initial_price * (1 + price_shocks).cumprod()
    
    # Simulate Model Predictions
    # Clean model executes highly profitable long(1)/short(-1) transitions
    clean_predictions = np.where(price_shocks > 0, 1, -1)
    
    # Poisoned model gets inverse tokens injected via our FinBERT text perturbation engine
    # We simulate an attacker successfully manipulating 35% of prediction triggers
    poisoned_predictions = clean_predictions.copy()
    poison_mask = np.random.random(100) < 0.35
    poisoned_predictions[poison_mask] *= -1 # Flips the directional sentiment forecast
    
    mock_data = pd.DataFrame({
        "Close": price_path,
        "Clean_Signal": clean_predictions,
        "Poisoned_Signal": poisoned_predictions
    }, index=dates)
    
    # Execute Quantitative Engine
    engine = QuantSecurityBacktester(initial_capital=50_000_000) # 50 Million KRW Baseline
    engine.run_differential_analysis(mock_data)
