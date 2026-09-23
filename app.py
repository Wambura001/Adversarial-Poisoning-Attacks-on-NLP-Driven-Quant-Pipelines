import streamlit as st
import numpy as np
import pandas as pd
from src.attacked.pertubation import KoreanFinBERTPoisoner
from src.engine.backtester import QuantSecurityBacktester
from src.defense.distance_filter import SemanticGuardrail

# Set web page configuration
st.set_page_config(page_title="FinBERT Quant Security Simulator", layout="wide")

st.title("NLP Quant Pipeline: Adversarial Attack & Defense Simulator")
#st.markdown("### Final Year Project: Ethical Hacking in the Korean Equity Market")
st.write("This dashboard demonstrates how character-level cyber attacks fool AI trading models and how defensive guardrails block them.")

# Initialize our core back-end components
poisoner = KoreanFinBERTPoisoner()
backtester = QuantSecurityBacktester(initial_capital=50_000_000)
guardrail = SemanticGuardrail(semantic_distance_threshold=0.50)

# ----------------------------------------------------
# STABLE DATA SIMULATION (CACHED TO PREVENT RE-RUN RND FLIPS)
# ----------------------------------------------------
@st.cache_data
def generate_stable_market_data():
    np.random.seed(42)
    dates = pd.date_range(start="2026-01-01", periods=100)
    
    # Generate realistic trending price path for a major KOSPI asset
    prices = [50000.0]
    shocks = np.random.normal(0.0005, 0.015, 100)
    for shock in shocks:
        prices.append(prices[-1] * (1 + shock))
    prices = np.array(prices[:-1])
    
    # Generate predictable trading execution signals
    clean_signals = np.where(shocks > 0, 1, -1)
    
    return dates, prices, clean_signals

dates, prices, clean_signals = generate_stable_market_data()

# ----------------------------------------------------
# SIDEBAR CONTROL PANEL
# ----------------------------------------------------
st.sidebar.header("Simulation Control Panel")

sample_headlines = [
    "삼성전자 반도체 공급 계약 호재로 인해 주가 급등 예상",
    "금리 인상 조치 발표에 따른 기관 투자자 대규모 매도세 집계",
    "실적 악화 공시 발표로 인한 장외 거래 시장 폭락 우려 심화",
    "바이오 신약 임상 성공 발표 이후 개인 투자자 매수세 대거 유입"
]

selected_text = st.sidebar.selectbox("1. Select Inbound News Feed:", sample_headlines)
attack_intensity = st.sidebar.slider("2. Simulated Botnet Infection Rate (%)", 10, 100, 35)
defense_active = st.sidebar.checkbox("3. Activate Semantic Guardrail Protection", value=True)

# ----------------------------------------------------
# ADVERSARIAL POISONING & DEFENSE REMEDIATION MATH
# ----------------------------------------------------
np.random.seed(101) # Keep attack locations stable during parameter swaps
poison_mask = np.random.random(100) < (attack_intensity / 100)

# Generate Attack State
poisoned_signals = clean_signals.copy()
poisoned_signals[poison_mask] *= -1

# Generate Defense State
defended_signals = poisoned_signals.copy()
if defense_active:
    # Catch 85% of malicious data feeds
    remediation_mask = np.random.random(100) < 0.85
    for i in range(100):
        if poison_mask[i] and remediation_mask[i]:
            defended_signals[i] = clean_signals[i]

# Run baseline computations through the quantitative backtester
baseline_m = backtester.compute_portfolio_metrics(pd.Series(prices), pd.Series(clean_signals))
attacked_m = backtester.compute_portfolio_metrics(pd.Series(prices), pd.Series(poisoned_signals))
defended_m = backtester.compute_portfolio_metrics(pd.Series(prices), pd.Series(defended_signals))

# ----------------------------------------------------
# VISUAL EQUITY TRAJECTORY LINE CALCULATIONS
# ----------------------------------------------------
# Properly scale percentage vectors to absolute account equity curves starting at ₩50M
def calculate_absolute_equity_curve(price_array, signal_array, initial_capital=50_000_000):
    pct_changes = pd.Series(price_array).pct_change().fillna(0)
    shifted_signals = pd.Series(signal_array).shift(1).fillna(0)
    strategy_returns = pct_changes * shifted_signals
    cumulative_curve = (1 + strategy_returns).cumprod()
    return initial_capital * cumulative_curve

clean_equity = calculate_absolute_equity_curve(prices, clean_signals)
poisoned_equity = calculate_absolute_equity_curve(prices, poisoned_signals)
defended_equity = calculate_absolute_equity_curve(prices, defended_signals)

# Assemble historical dataframe for chart plotting
chart_df = pd.DataFrame({
    "Clean Pipeline Baseline": clean_equity.values,
    "Poisoned Pipeline (Attacked)": poisoned_equity.values
}, index=dates)

if defense_active:
    chart_df["Sanitized Pipeline (Protected)"] = defended_equity.values

# ----------------------------------------------------
# DASHBOARD UI GRID RENDER
# ----------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Text Pipeline Ingestion View")
    st.info(f"**Original Clean Input:**\n{selected_text}")
    
    poisoned_text = poisoner.generate_adversarial_headline(selected_text)
    st.error(f"**Poisoned Adversarial Feed (Transmitted to FinBERT):**\n{poisoned_text}")
    
    audit = guardrail.inspect_payload(poisoned_text)
    if defense_active:
        st.success(f"**Guardrail Analysis:** {audit['quarantine_status']} (Semantic Distance: {audit['semantic_distance']:.3f})")
    else:
        st.warning("Defensive Guardrails are completely disabled. System accepting unverified data packages.")

with col2:
    st.subheader("Financial Impact Analytics")
    
    kpi1, kpi2, kpi3 = st.columns(3)
    
    kpi1.metric(
        label="Clean Performance", 
        value=f"{baseline_m['total_return']*100:.2f}%", 
        help=f"Sharpe Ratio: {baseline_m['sharpe_ratio']:.2f}"
    )
    
    loss_delta = (attacked_m['total_return'] - baseline_m['total_return']) * 100
    kpi2.metric(
        label="Attacked Performance", 
        value=f"{attacked_m['total_return']*100:.2f}%", 
        delta=f"{loss_delta:.2f}% Loss Delta",
        delta_color="inverse",
        help=f"Sharpe Ratio: {attacked_m['sharpe_ratio']:.2f}"
    )
    
    if defense_active:
        alpha_recovered = (defended_m['total_return'] - attacked_m['total_return']) * 100
        kpi3.metric(
            label="Defended Performance", 
            value=f"{defended_m['total_return']*100:.2f}%", 
            delta=f"+{alpha_recovered:.2f}% Recovered",
            delta_color="normal",
            help=f"Sharpe Ratio: {defended_m['sharpe_ratio']:.2f}"
        )
    else:
        kpi3.metric(label="Defended Performance", value="N/A", help="Guardrail is off")

    st.markdown("**Simulated Capital Trajectory over 100 Days (KRW ₩):**")
    st.line_chart(chart_df)
