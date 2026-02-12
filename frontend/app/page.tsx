"use client";

import { useState } from "react";
import StockChart from "@/components/StockChart";
import PredictionResult from "@/components/PredictionResult";

const API_BASE = "http://localhost:8000";

type HistoryPoint = { date: string; close: number };

type PredictionData = {
  ticker: string;
  current_price: number;
  future_days: number;
  n_simulations: number;
  expected_price: number;
  median_price: number;
  ci_95_lower: number;
  ci_95_upper: number;
  sigma: number;
  history: HistoryPoint[];
  sample_paths: { day: number; price: number }[][];
};

export default function Home() {
  const [history, setHistory] = useState<HistoryPoint[]>([]);
  const [prediction, setPrediction] = useState<PredictionData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const ticker = "6920.T";

  async function fetchData() {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/api/stock/${ticker}?start=2025-02-01&end=2026-02-06`);
      if (!res.ok) throw new Error("株価データの取得に失敗しました");
      const data = await res.json();
      setHistory(data.history);

      const predRes = await fetch(`${API_BASE}/api/stock/${ticker}/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          start: "2025-02-01",
          end: "2026-02-06",
          n_sim: 10000,
          future_days: 22,
        }),
      });
      if (!predRes.ok) throw new Error("予測の実行に失敗しました");
      const predData: PredictionData = await predRes.json();
      setPrediction(predData);
    } catch (e) {
      setError(e instanceof Error ? e.message : "エラーが発生しました");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="max-w-5xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-2">Stock Market Prediction</h1>
      <p className="text-gray-600 mb-6">
        レザーテック (6920.T) - モンテカルロシミュレーションによる株価予測
      </p>

      <button
        onClick={fetchData}
        disabled={loading}
        className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed mb-8"
      >
        {loading ? "読み込み中..." : "データ取得 & 予測実行"}
      </button>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
          {error}
        </div>
      )}

      {history.length > 0 && (
        <section className="mb-8">
          <h2 className="text-xl font-semibold mb-4">株価チャート (終値)</h2>
          <StockChart data={history} />
        </section>
      )}

      {prediction && (
        <section>
          <h2 className="text-xl font-semibold mb-4">予測結果 (1ヶ月後)</h2>
          <PredictionResult prediction={prediction} />
        </section>
      )}
    </main>
  );
}
