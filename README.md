# Adversarial Poisoning Attacks on NLP-Driven Quant Pipelines: Vulnerability Analysis and Defenses within the Korean Equity Market

This repository contains the source code, attack frameworks, and defensive machine learning pipelines for my Final Year Project on Ethical Hacking and Quantitative Finance.

## 🎯 Project Overview
This project evaluates the security vulnerabilities of Natural Language Processing (NLP) models used in algorithmic trading. Specifically, we simulate a **Data Poisoning Attack** where an adversary deploys a semantic botnet on South Korean retail trading forums (e.g., Naver Financial, Paxnet) to manipulate the sentiment metrics feeding a quantitative trading engine. 

The project demonstrates how minor text perturbations can trigger catastrophic financial miscalculations in trading algorithms, and proposes an enterprise-ready defense matrix to neutralize semantic malware.

---

## 🔬 Research Core

### 1. The Target Pipeline
* **NLP Sentiment Aggregator:** A transformer model (**KoBERT/KoELECTRA**) fine-tuned on Korean financial slang, tracking macro signals and retail forum sentiment.
* **Math Execution Engine:** A sequential Deep Learning (**LSTM**) model that processes historical market data alongside lagging news sentiment to forecast asset directional movements.

### 2. The Offensive Vector (The Attack)
* **Adversarial Perturbations:** Using rule-based NLP modifiers to subtly alter text syntax (e.g., replacing common Korean financial terms like "급등" with slang variants like "떡상", or embedding hidden Unicode characters). This misleads the transformer tokenization without raising human suspicion.
* **Botnet Injection Simulation:** Flooding the input stream with adversarial data right before market open to artificially distort trading signals.

### 3. The Defensive Matrix (The Patch)
* **Semantic Distance Filtering:** A pre-processing autoencoder layer that maps incoming string embeddings. If a post's syntax distance deviates from historically verified Korean financial journalism patterns, it is quarantined.
* **Algorithmic Circuit Breakers:** A risk management feature built into the execution engine that halts automated trading on an asset if its 5-minute rolling sentiment variance spikes beyond a 3-standard-deviation threshold.

---

## 🛠 Directory Layout
* `src/attack/` - Scripts generating adversarial text and simulating botnet injections.
* `src/engine/` - The core KoBERT sentiment tokenizer, LSTM model, and backtesting suite.
* `src/defense/` - Semantic embedding filters and portfolio circuit breakers.
* `main.py` - The execution gate to compare: (1) Clean Baseline Performance, (2) Poisoned Attack Performance, and (3) Defended Performance.

---

## ⚡ Quick Start (Local Setup)

```bash
# 1. Clone your repo after pushing
git clone https://github.com
cd YOUR-NEW-REPO-NAME

# 2. Setup environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install requirements
pip install -r requirements.txt
```

## ⚖️ Academic Disclaimer
This project is built strictly for educational validation and security research under ethical hacking frameworks. It does not constitute financial advice, nor does it encourage live market manipulation.
