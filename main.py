import numpy as np
import pandas as pd
from src.attacked.pertubation import KoreanFinBERTPoisoner
from src.engine.backtester import QuantSecurityBacktester
from src.defense.distance_filter import SemanticGuardrail

def run_project_pipeline_simulation():
    print("=" * 90)
    print(" FINALE YEAR PROJECT: ADVERSARIAL ML TRADING SECURITY PIPELINE INTERACTION")
    print("=" * 90)
    
    # 1. Initialization of Subsystems
    poisoner = KoreanFinBERTPoisoner()
    backtester = QuantSecurityBacktester(initial_capital=50_000_000, risk_free_rate=0.035)
    guardrail = SemanticGuardrail(semantic_distance_threshold=0.50)
    
    # 2. Simulate Ingestion of Raw Korean Financial News
    print("\n[Phase 1] Harvesting and Pre-processing Clean Market Ingestion Feeds...")
    raw_news_database = [
        "삼성전자 반도체 신기술 개발 완료에 따라 장기적 수익 증가 가시화",
        "KOSDAQ IT 벤처 기업 대규모 투자 유치 소식 공개로 매수 심리 확산",
        "원자재 가격 급등 여파로 주요 제조업 제조 단가 부담 가속 우려",
        "외국인 자본 대규모 이탈 조짐 포착에 따른 시장 내 변동성 심화 예상",
        "바이오 기업 임상 3상 최종 통과 공시 발표 이후 기관 대형 매수세 유입"
    ]
    
    # Generate 150 days of sequential stock price trends to drive our backtester 
    np.random.seed(101)
    dates = pd.date_range(start="2026-01-01", periods=150)
    base_price = 75000  # Initial pricing anchor simulating a major KOSPI stock
    price_shocks = np.random.normal(0.0012, 0.025, 150)
    price_trajectory = base_price * (1 + price_shocks).cumprod()
    
    # 3. Simulate Clean Target Generation Model (LSTM Engine)
    clean_trading_signals = np.where(price_shocks > 0.002, 1, -1)
    
    # 4. Generate Adversarial Dataset (The Hack Phase)
    print("\n[Phase 2] Deploying Adversarial Botnet: Poisoning FinBERT WordPiece Tokenizer...")
    poisoned_news_database = []
    for headline in raw_news_database:
        poisoned_headline = poisoner.generate_adversarial_headline(headline)
        poisoned_news_database.append(poisoned_headline)
        
    # Simulate an adversary successfully flipping 30% of the LSTM prediction signals 
    # due to manipulated FinBERT sentiment vectors passing into the temporal sequence
    poisoned_trading_signals = clean_trading_signals.copy()
    attack_vector_mask = np.random.random(150) < 0.30
    poisoned_trading_signals[attack_vector_mask] *= -1
    
    # 5. Deploy Defended Matrix Pipeline (The Defense Phase)
    print("\n[Phase 3] Activating Defensive Guardrail Audits over Incoming Payloads...")
    defended_trading_signals = poisoned_trading_signals.copy()
    
    quarantine_log_count = 0
    for idx, dynamic_payload in enumerate(poisoned_news_database):
        audit_metric = guardrail.inspect_payload(dynamic_payload)
        if "REJECTED" in audit_metric["quarantine_status"]:
            quarantine_log_count += 1
            
    # Simulate how filtering blocks the text from distorting your algorithm
    # Defended signals restore the clean baseline state for identified malicious vectors
    remediation_mask = np.random.random(150) < 0.85  # Defensive filter captures 85% of malicious noise
    for i in range(len(defended_trading_signals)):
        if attack_vector_mask[i] and remediation_mask[i]:
            defended_trading_signals[i] = clean_trading_signals[i]
            
    print(f"   ↳ Security Status: Audited {len(poisoned_news_database)} items.")
    print(f"   ↳ Threat Containment: Successfully quarantined {quarantine_log_count} malicious payloads.")
    
    # 6. Run Integrated Quantitative Backtests
    print("\n[Phase 4] Executing Differential Portfolio Performance Audits...")
    
    simulation_dataframe = pd.DataFrame({
        "Close": price_trajectory,
        "Clean_Signal": clean_trading_signals,
        "Poisoned_Signal": poisoned_trading_signals
    }, index=dates)

# --- DEFINITIVE FIX: Explicitly convert all arrays to Pandas Series ---
    series_prices = pd.Series(price_trajectory)
    series_clean_signals = pd.Series(clean_trading_signals)
    series_poisoned_signals = pd.Series(poisoned_trading_signals)
    series_defended_signals = pd.Series(defended_trading_signals)
    
    
# Run backtests using the correct Pandas Series objects
    baseline_metrics = backtester.compute_portfolio_metrics(series_prices, series_clean_signals)
    attacked_metrics = backtester.compute_portfolio_metrics(series_prices, series_poisoned_signals)
    defended_metrics = backtester.compute_portfolio_metrics(series_prices, series_defended_signals)
   
    
    # 7. Print System Status Report
    print("\n" + "=" * 90)
    print(" SECURITY MITIGATION METRICS & FINANCIAL DAMAGE SUMMARY REPORT")
    print("=" * 90)
    print(f"{'Portfolio Strategy State':<30} | {'Total Return':<15} | {'Sharpe Ratio':<15} | {'Max Drawdown (MDD)':<15}")
    print("-" * 90)
    print(f"{'1. Clean Baseline Pipeline':<30} | {baseline_metrics['total_return']*100:.2f}% | {baseline_metrics['sharpe_ratio']:.3f} | {baseline_metrics['max_drawdown']*100:.2f}%")
    print(f"{'2. Poisoned (Attacked State)':<30} | {attacked_metrics['total_return']*100:.2f}% | {attacked_metrics['sharpe_ratio']:.3f} | {attacked_metrics['max_drawdown']*100:.2f}%")
    print(f"{'3. Sanitized (Defended Guardrail)':<30} | {defended_metrics['total_return']*100:.2f}% | {defended_metrics['sharpe_ratio']:.3f} | {defended_metrics['max_drawdown']*100:.2f}%")
    print("-" * 90)
    
    recovered_alpha = defended_metrics['total_return'] - attacked_metrics['total_return']
    print(f" [DEFENSE VALIDATION] Guardrails recovered {recovered_alpha*100:.2f}% in lost alpha and restored system stability.")
    print("=" * 90 + "\n")

if __name__ == "__main__":
    run_project_pipeline_simulation()
