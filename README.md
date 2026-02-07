# Stock Price Prediction System (Statistical Approach)

## Overview

A web application that implements **statistical theory (Japan Statistical Certification Grade 2 level)** with **Python + SQL** to quantitatively analyze stock market trends and risks. The goal is **market analysis through statistically derived features**, not perfect price prediction.

## Technologies

| Layer | Stack |
|-------|-------|
| Data / ML | Python (pandas, numpy, scikit-learn, matplotlib), yfinance |
| API | FastAPI |
| DB | PostgreSQL (planned) |
| Frontend | React or Vue (planned) |

## Architecture

```
Market Data → Preprocessing → Feature Engineering → Model Training → Evaluation → API → Frontend
```

## Statistical Methods

- Expectation, variance, standard deviation / Covariance, correlation coefficients
- Standardization, logarithmic transformation
- Regression analysis (simple, multiple, Ridge/Lasso)
- Residual analysis, R² / Multicollinearity consideration

## Features & Models

**Features**: Log returns, moving averages, volatility, moving average deviation rate, volume change rate

**Models**: Linear regression → Multiple regression → Ridge/Lasso (planned)
Prioritizing interpretability over black-box predictions.

**Evaluation**: RMSE, MAE, actual vs. predicted visualization

## Future Work

- Time-series models (ARIMA, state space models)
- Comparison with deep learning (LSTM, etc.)
- Backtesting functionality

## Disclaimer

This system is not intended to provide investment advice. Its purpose is statistical trend analysis and risk quantification.

## License

MIT License
