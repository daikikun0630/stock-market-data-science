import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Stock Market Prediction",
  description: "レザーテック(6920.T)の株価予測ダッシュボード",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ja">
      <body className="bg-gray-50 text-gray-900 min-h-screen">{children}</body>
    </html>
  );
}
