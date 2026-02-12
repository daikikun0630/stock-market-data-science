"use client";

type Props = {
  prediction: {
    current_price: number;
    expected_price: number;
    median_price: number;
    ci_95_lower: number;
    ci_95_upper: number;
    future_days: number;
    n_simulations: number;
  };
};

function fmt(n: number): string {
  return `¥${Math.round(n).toLocaleString()}`;
}

export default function PredictionResult({ prediction }: Props) {
  const {
    current_price,
    expected_price,
    median_price,
    ci_95_lower,
    ci_95_upper,
    future_days,
    n_simulations,
  } = prediction;

  const change = ((expected_price - current_price) / current_price) * 100;

  const cards = [
    { label: "現在価格", value: fmt(current_price), color: "bg-gray-100" },
    {
      label: "期待価格",
      value: fmt(expected_price),
      sub: `${change >= 0 ? "+" : ""}${change.toFixed(2)}%`,
      color: change >= 0 ? "bg-green-50" : "bg-red-50",
    },
    { label: "中央値", value: fmt(median_price), color: "bg-blue-50" },
    {
      label: "95% 信頼区間",
      value: `${fmt(ci_95_lower)} ~ ${fmt(ci_95_upper)}`,
      color: "bg-purple-50",
    },
  ];

  return (
    <div>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {cards.map((c) => (
          <div
            key={c.label}
            className={`${c.color} rounded-xl shadow p-4`}
          >
            <p className="text-sm text-gray-500">{c.label}</p>
            <p className="text-xl font-bold mt-1">{c.value}</p>
            {c.sub && <p className="text-sm mt-1 text-gray-600">{c.sub}</p>}
          </div>
        ))}
      </div>
      <p className="text-xs text-gray-400 mt-4">
        {future_days}営業日先 / {n_simulations.toLocaleString()}回シミュレーション
      </p>
    </div>
  );
}
