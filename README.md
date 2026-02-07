# Stock Price Prediction System (Statistical Approach)

## 📌 Overview

This project is a **stock price prediction system** that applies **statistical theory at the level of the Japan Statistical Certification Grade 2** together with **Python and SQL**.

Rather than aiming to perfectly predict stock prices, the primary goal is to **quantitatively analyze market trends and risks using statistically derived features**.

The system is developed as a **web application**, separating:

* Backend (data processing, statistical modeling, API)
* Frontend (visualization and user interface)

This project is collaboratively developed, with clear role separation between data analysis and frontend/backend implementation.

---

## 🎯 Objectives

* Apply statistical knowledge from the Statistical Certification Grade 2 to real-world financial data
* Build a practical data analysis pipeline using Python and SQL
* Understand the statistical structure of stock price movements
* Create a portfolio-ready project suitable for job applications and internships

---

## 🧠 Statistical Methods Used

The following statistical concepts are actively used in this project:

* Expectation, variance, and standard deviation
* Covariance and correlation coefficients
* Standardization and logarithmic transformation
* Regression analysis (simple and multiple regression)
* Residual analysis and coefficient of determination (R²)
* Consideration of multicollinearity

All implementations are based on **interpretable statistical models**, not black-box predictions.

---

## 🛠 Technologies

### Backend / Data Analysis

* Python

  * pandas
  * numpy
  * scikit-learn
  * matplotlib
* SQL

  * PostgreSQL (planned)
* Market data acquisition

  * yfinance

### Frontend (Collaborative Development)

* JavaScript
* React or Vue (planned)
* REST API communication

### Infrastructure & Tools

* FastAPI (API server)
* Git / GitHub

---

## 🧩 System Architecture

```
[ Market Data Acquisition ]
            ↓
[ Data Preprocessing & Statistical Feature Calculation ]
            ↓
[ Feature Engineering ]
            ↓
[ Prediction Model Training ]
            ↓
[ Model Evaluation ]
            ↓
[ API Layer ] → [ Frontend Visualization ]
```

---

## 📊 Data Description

### Raw Data

* Open
* High
* Low
* Close
* Volume

### Derived Variables

* Log returns
* Moving averages
* Volatility (standard deviation)

---

## 📈 Feature Examples

* Mean return over the past *n* days
* Volatility over the past *n* days
* Moving average deviation rate
* Volume change rate

These statistically derived features are used as explanatory variables in the models.

---

## 🤖 Prediction Models

The project prioritizes **model interpretability** and therefore starts with classical statistical models:

* Linear regression
* Multiple regression
* Ridge regression / Lasso regression (planned)

The objective is to clearly explain **why** a prediction is made, not only **what** is predicted.

---

## 📏 Evaluation Metrics

* RMSE (Root Mean Squared Error)
* MAE (Mean Absolute Error)
* Visualization of actual vs. predicted values

---

## 🌐 Planned Web Application Features

* Stock symbol selection
* Date range selection
* Price and prediction charts
* Statistical indicator visualization

---

## ⚠ Disclaimer

* This system is **not intended to provide investment advice**
* Short-term stock prices cannot be predicted perfectly
* The purpose is **statistical trend analysis and risk quantification**

---

## 🚀 Future Work

* Expansion of feature sets
* Time-series models (ARIMA, state space models)
* Comparison with machine learning and deep learning models (e.g., LSTM)
* Backtesting functionality

---

## 👥 Development Roles

* Data analysis, statistical modeling, API development: Project owner
* Frontend development and UI design: Collaborator

---

## 📄 License

This project is licensed under the MIT License.
