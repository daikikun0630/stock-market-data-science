# 自分が買っている株(レザーテック銘柄)の株価を予測するコード
# ボラティリティが非常に高く、短期的な価格変動が激しいくテクニカル分析が有効な銘柄であるため、過去の価格データを基に将来の株価を予測するモデルを構築 

import yfinance as yf # Yahoo Financeから株価データを取得
import pandas as pd # データ操作用ライブラリ 
import numpy as np # 数値計算用ライブラリ
from sklearn.linear_model import LinearRegression # 線形回帰モデル

# 1. データ取得
# 作成日時が2026年2月8日（日曜日）なので2月6日までのデータを取得
df = yf.download(
    "6920.T", # レザーテック銘柄(東証プライム市場)
    start="2025-02-01",
    end="2026-02-06",
    auto_adjust=True,
    progress=False
)# レザーテック社の株価データを取得

# 2. 特徴量作成
df["return"] = df["Close"].pct_change() #日次リターン

df["ma_5"] = df["Close"].rolling(5).mean() #5日移動平均(5営業日=約1週間)

df["ma_20"] = df["Close"].rolling(20).mean() #20日移動平均(20営業日=約1ヶ月)
df["volatility"] = df["return"].rolling(20).std() #標準偏差により20日間のボラティリティを算出

df = df.dropna() # 欠損値を含む行を削除

# 3. 学習データ作成
df["z_score_20"] = (
    (df["Close"] - df["Close"].rolling(20).mean()) /
    df["Close"].rolling(20).std()
) # 20日間のZスコア

df["var_20"] = df["log_return"].rolling(20).var() # 20日間の分散
df["return_lag1"] = df["log_return"].shift(1) # 1日遅れの対数リターン

df = df.dropna() # 欠損値を含む行を削除

x = df[["z_score_20", "var_20", "return_lag1"]] # 説明変数

# 最初X = df[["ma_5", "ma_20", "volatility"]]を説明変数にしていたが、予測精度が低かったため上記の特徴量に変更
# 価格予測モデルではなく、確率予測モデルに近い形に変更

df["log_return"] = np.log(df["Close"] / df["Close"].shift(1)) # 対数リターンを計算
df["target"] = df["log_return"].shift(-1) # 次の日の対数リターンを目的変数に設定

df = df.dropna() # 欠損値を含む行を削除

y = df["target"] # 目的変数

#最初y = df["Close"]を目的変数にしていたが、予測精度が低かったため上記の特徴量に変更
# 価格予測モデルではなく、確率予測モデルに近い形に変更

model = LinearRegression() # 線形回帰モデルのインスタンス化
model.fit(x, y) # モデルの学習

# 4. 2026年3月以降を予測

last_date = df.index[-1] # 最終日付
future_days = 22  # 約1ヶ月分（営業日）

future_prices = [] # 予測価格を格納するリスト
current_df = df.copy() # 予測用にデータフレームをコピー

model = LinearRegression() # 線形回帰モデルのインスタンス化
model.fit(x, y) # モデルの学習

mu_hat = model.predict(x) # 学習データに対する予測値
residuals = y - mu_hat # 残差を計算
sigma_hat = residuals.std() # 残差の標準偏差を計算

from scipy.stats import norm # 正規分布を扱うためのライブラリ

latest_x = x.iloc[-1].values.reshape(1, -1) # 最新の特徴量データ
mu_next = model.predict(latest_x)[0]    # 次の日の対数リターンの予測値

current_price = df["Close"].iloc[-1] # 最新の株価

# リターン分布
r_dist = norm(loc=mu_next, scale=sigma_hat)

# 価格分布（モンテカルロ）
price_samples = current_price * np.exp(r_dist.rvs(size=10000))

# 5. 結果表示

future_index = pd.date_range(
    start=last_date + pd.Timedelta(days=1),
    periods=future_days,
    freq="B"
) # 営業日ベースの日付インデックスを作成

forecast_df = pd.DataFrame(
    {"Predicted_Close": future_prices},
    index=future_index
) # 予測結果のデータフレームを作成

print(forecast_df) # 予測結果を表示

print("期待価格:", price_samples.mean()) # 期待価格を表示
print("中央値:", np.median(price_samples)) # 中央値を表示
print("95%信頼区間:",
      np.percentile(price_samples, [2.5, 97.5])) # 95%信頼区間を表示

