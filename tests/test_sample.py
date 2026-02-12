# 自分が買っている株(レザーテック銘柄)の株価を予測するコード
# ボラティリティが非常に高く、短期的な価格変動が激しいくテクニカル分析が有効な銘柄であるため、過去の価格データを基に将来の株価を予測するモデルを構築 

import yfinance as yf # Yahoo Financeからデータ取得
import pandas as pd # データ操作
import numpy as np # 数値計算
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
# 対数リターン
df["log_return"] = np.log(df["Close"] / df["Close"].shift(1))

# Zスコア
df["z_score_20"] = (
    (df["Close"] - df["Close"].rolling(20).mean()) /
    df["Close"].rolling(20).std()
)

# 20日分散（リターン）
df["var_20"] = df["log_return"].rolling(20).var()

# 1日ラグ
df["return_lag1"] = df["log_return"].shift(1)

# 目的変数（1日先リターン）
df["target"] = df["log_return"].shift(-1)

# 最後に1回だけ欠損削除
df = df.dropna()

# 説明変数・目的変数
X = df[["z_score_20", "var_20", "return_lag1"]]
y = df["target"]

print("X shape:", X.shape)
print("y shape:", y.shape)

# 3. モデル学習
model = LinearRegression() # 線形回帰モデル
model.fit(X, y) # モデル学習

mu_hat = model.predict(X) # 予測リターン

# 残差
residuals = y.values - mu_hat # 実測値 - 予測値
sigma_hat = residuals.std() # 残差の標準偏差

print("残差標準偏差:", sigma_hat)

# 4. 未来22営業日モンテカルロ予測
future_days = 22 # 1ヶ月(22営業日)先まで予測
n_sim = 10000 # シミュレーション数

current_price = df["Close"].iloc[-1] # 最新の株価
latest_X = X.iloc[-1].values.reshape(1, -1) # 最新の説明変数

# 次期リターンの期待値
mu_next = model.predict(latest_X)[0]

# モンテカルロパス生成
simulated_paths = []

for _ in range(n_sim):
    price = current_price # シミュレーションごとに初期価格を設定
    for _ in range(future_days):
        r = np.random.normal(mu_next, sigma_hat) # 正規分布からリターンをサンプリング
        price *= np.exp(r) # 株価更新
    simulated_paths.append(price) # 1ヶ月後の価格を保存

simulated_paths = np.array(simulated_paths) # シミュレーション結果を配列に変換

# 5. 結果表示
print("---- 1ヶ月後予測分布 ----")
print("期待価格:", simulated_paths.mean())
print("中央値:", np.median(simulated_paths))
print("95%信頼区間:",
      np.percentile(simulated_paths, [2.5, 97.5]))
