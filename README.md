# 🚀 MLOps Signal Pipeline

![Python](https://img.shields.io/badge/Python-3.9-blue)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![MLOps](https://img.shields.io/badge/MLOps-Pipeline-green)
![Status](https://img.shields.io/badge/Status-Production--Ready-brightgreen)

## 📌 Overview
This project implements a **production-style MLOps batch pipeline** for generating trading signals from financial time-series (OHLCV) data.

The system computes a rolling mean on the closing price and produces binary signals based on price trends. It emphasizes **reproducibility, observability, and deployment readiness**, simulating real-world ML engineering workflows.

---

## ⚙️ Key Features

- ✅ Config-driven execution using YAML
- ✅ Deterministic runs via random seed
- ✅ Rolling mean-based signal generation
- ✅ Structured metrics output (JSON)
- ✅ Detailed logging for observability
- ✅ Robust error handling
- ✅ Fully Dockerized (one-command execution)

---

## 📊 Signal Logic

- Compute rolling mean on `close` prices
- Generate signal:
-signal = 1 if close > rolling_mean else 0

- Output metric:
- `signal_rate` = average of generated signals

---

## 🏗️ Tech Stack

- Python 3.9
- Pandas, NumPy
- YAML (config management)
- Logging module
- Docker

---

## 🚀 How to Run

### 🔹 Local Run

```bash
python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log

```

### 🐳 Docker Run
```bash
docker build -t mlops-task .
docker run --rm mlops-task

```
---
## 📁 Project Structure
```bash
├──  run.py
├──  config.yaml
├──  data.csv
├──  requirements.txt
├──  Dockerfile
├──  README.md
├──  metrics.json
└──  run.log
```
---
## Example Output (metrics.json)
```bash
{
  "version": "v1",
  "rows_processed": 10000,
  "metric": "signal_rate",
  "value": 0.4990,
  "latency_ms": 127,
  "seed": 42,
  "status": "success"
}
```
---
## 🎯 Learning Outcomes
- Applied MLOps principles to a real-world-style pipeline
- Built a reproducible and observable system
- Practiced Docker-based deployment
- Implemented robust validation and error handling


---
## 📌 Domain
This project lies at the intersection of:

  - Quantitative Finance (Trading Signals)
  - Machine Learning Engineering (MLOps)

---

## 🤝 Contribution
Feel free to fork, improve, and extend the pipeline with advanced indicators or ML models

---