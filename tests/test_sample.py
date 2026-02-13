# 自分が買っている株(レザーテック銘柄)の株価を予測するコード
# ボラティリティが非常に高く、短期的な価格変動が激しいくテクニカル分析が有効な銘柄であるため、過去の価格データを基に将来の株価を予測するモデルを構築 

import yfinance as yf # Yahoo Financeからデータ取得
import pandas as pd # データ操作
import numpy as np # 数値計算
from arch import arch_model # GARCHモデル
#GARCHにより分散の予測をしている
from sklearn.linear_model import LinearRegression # 線形回帰モデル
from scipy.stats import norm # 正規分布

# 1. データ取得
df = yf.download(
    "6920.T",
    start="2025-02-01",
    end="2026-02-06",
    auto_adjust=True,
    progress=False
) # レザーテックの株価データ取得

# 2. 特徴量 & 目的変数作成
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.droplevel(-1)

if "Close" not in df.columns:
    raise ValueError("Close列が存在しません。df.columnsを確認してください。")

# 数値型へ強制変換
df["Close"] = pd.to_numeric(df["Close"], errors="coerce")

# --- 対数リターン ---
df["log_return"] = np.log(df["Close"] / df["Close"].shift(1))

# --- 20日移動平均・標準偏差 ---
rolling_mean_20 = df["Close"].rolling(window=20).mean()
rolling_std_20  = df["Close"].rolling(window=20).std()

df["z_score_20"] = (df["Close"] - rolling_mean_20) / rolling_std_20

# --- 20日分散（リターン） ---
df["var_20"] = df["log_return"].rolling(window=20).var()

# --- 出来高変化率 ---
df["volume_change"] = df["Volume"].pct_change()

# --- ボラ変化率 ---
df["vol_change"] = df["var_20"].pct_change()

df = df.dropna()

# --- 1日ラグ ---
df["return_lag1"] = df["log_return"].shift(1)

# --- 目的変数（1日先リターン） ---
df["target"] = df["log_return"].shift(-1)

# --- 無限値除去（重要） ---
df.replace([np.inf, -np.inf], np.nan, inplace=True)

# --- 最後にまとめて欠損削除 ---
df = df.dropna().copy()
df = df.replace([np.inf, -np.inf], np.nan)
df = df.dropna()

# --- 説明変数・目的変数 ---
X = df[["z_score_20", "var_20", "return_lag1", "volume_change", "vol_change",]]
y = df["target"]

print("X shape:", X.shape)
print("y shape:", y.shape)

# 3. 時系列分割（リーク防止）
split = int(len(X) * 0.8)

X_train, X_test = X.iloc[:split], X.iloc[split:]
y_train, y_test = y.iloc[:split], y.iloc[split:]

# 4. 平均モデル（線形回帰）
mean_model = LinearRegression()
mean_model.fit(X_train, y_train)

mu_test = mean_model.predict(X_test)

residuals = y_test.values - mu_test

print("Out-of-sample 残差標準偏差:", residuals.std())

# 5. 分散モデル（GARCH）
garch = arch_model(y_train * 100, vol="Garch", p=1, q=1,dist="t") #GARCHをt分布化
garch_fit = garch.fit(disp="off")

# 6. 未来22営業日 動的モンテカルロ

future_days = 22
n_sim = 5000

current_price = df["Close"].iloc[-1]
simulated_prices = []

for _ in range(n_sim):

    price = current_price
    history_returns = df["log_return"].values.copy()

    for day in range(future_days):

        # --- 特徴量再計算 ---
        temp_series = pd.Series(history_returns)
        var_20 = temp_series[-20:].var()
        return_lag1 = temp_series.iloc[-1]

        # 価格履歴からZスコア更新
        # 簡略化（本気なら価格履歴も保存）
        z_score = 0  # 実装簡略化（価格履歴使う場合は更新必要）

        X_new = pd.DataFrame(
        [[z_score, var_20, return_lag1, 0, 0]], # volume_change and vol_change are set to 0 for simplicity
        columns=["z_score_20", "var_20", "return_lag1", "volume_change", "vol_change"]
        )

        mu_next = mean_model.predict(X_new)[0]

        # --- GARCHで分散予測 ---
        garch_forecast = garch_fit.forecast(horizon=1)
        sigma_next = np.sqrt(
            garch_forecast.variance.values[-1, 0]
        ) / 100

        # --- リターンサンプリング ---
        r = np.random.normal(mu_next, sigma_next)

        # --- 価格更新 ---
        price *= np.exp(r)

        # --- 履歴更新 ---
        history_returns = np.append(history_returns, r)

    simulated_prices.append(price)

simulated_prices = np.array(simulated_prices)

# 7. 結果
print("----- 1ヶ月後予測分布 -----")
print("期待価格:", simulated_prices.mean())
print("中央値:", np.median(simulated_prices))
print("95%信頼区間:",
      np.percentile(simulated_prices, [2.5, 97.5]))
