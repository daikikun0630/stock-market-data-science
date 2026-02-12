import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


def fetch_stock_data(ticker: str, start: str, end: str) -> pd.DataFrame:
    """yfinanceで株価データを取得し、特徴量を作成して返す"""
    df = yf.download(
        ticker,
        start=start,
        end=end,
        auto_adjust=True,
        progress=False,
    )

    if df.empty:
        raise ValueError(f"No data found for ticker: {ticker}")

    # MultiIndex対策（yfinance が ticker列を含む場合）
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # 特徴量作成
    df["log_return"] = np.log(df["Close"] / df["Close"].shift(1))
    df["z_score_20"] = (
        (df["Close"] - df["Close"].rolling(20).mean())
        / df["Close"].rolling(20).std()
    )
    df["var_20"] = df["log_return"].rolling(20).var()
    df["return_lag1"] = df["log_return"].shift(1)
    df["target"] = df["log_return"].shift(-1)
    df = df.dropna()

    return df


def run_prediction(
    ticker: str,
    start: str,
    end: str,
    n_sim: int = 10000,
    future_days: int = 22,
) -> dict:
    """線形回帰 + モンテカルロシミュレーションで株価を予測する"""
    df = fetch_stock_data(ticker, start, end)

    X = df[["z_score_20", "var_20", "return_lag1"]]
    y = df["target"]

    model = LinearRegression()
    model.fit(X, y)

    mu_hat = model.predict(X)
    residuals = y.values - mu_hat
    sigma_hat = float(residuals.std())

    current_price = float(df["Close"].iloc[-1])
    latest_X = X.iloc[-1].values.reshape(1, -1)
    mu_next = float(model.predict(latest_X)[0])

    # モンテカルロシミュレーション
    rng = np.random.default_rng()
    random_returns = rng.normal(mu_next, sigma_hat, size=(n_sim, future_days))
    cumulative_log_returns = np.cumsum(random_returns, axis=1)
    simulated_paths = current_price * np.exp(cumulative_log_returns)

    final_prices = simulated_paths[:, -1]
    ci_lower, ci_upper = np.percentile(final_prices, [2.5, 97.5])

    # 株価履歴（JSON用）
    history = [
        {"date": d.strftime("%Y-%m-%d"), "close": float(c)}
        for d, c in zip(df.index, df["Close"])
    ]

    # シミュレーションパス（表示用に間引く: 最大20本）
    sample_indices = rng.choice(n_sim, size=min(20, n_sim), replace=False)
    sample_paths = []
    for idx in sample_indices:
        path = [{"day": int(d + 1), "price": float(p)} for d, p in enumerate(simulated_paths[idx])]
        sample_paths.append(path)

    return {
        "ticker": ticker,
        "current_price": current_price,
        "future_days": future_days,
        "n_simulations": n_sim,
        "expected_price": float(final_prices.mean()),
        "median_price": float(np.median(final_prices)),
        "ci_95_lower": float(ci_lower),
        "ci_95_upper": float(ci_upper),
        "sigma": sigma_hat,
        "history": history,
        "sample_paths": sample_paths,
    }
