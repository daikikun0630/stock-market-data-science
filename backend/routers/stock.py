from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.services.stock_service import fetch_stock_data, run_prediction

router = APIRouter(prefix="/api/stock", tags=["stock"])


class PredictRequest(BaseModel):
    start: str = "2025-02-01"
    end: str = "2026-02-06"
    n_sim: int = 10000
    future_days: int = 22


@router.get("/{ticker}")
def get_stock_data(ticker: str, start: str = "2025-02-01", end: str = "2026-02-06"):
    """株価履歴データを取得する"""
    try:
        df = fetch_stock_data(ticker, start, end)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    history = [
        {"date": d.strftime("%Y-%m-%d"), "close": float(c)}
        for d, c in zip(df.index, df["Close"])
    ]
    return {"ticker": ticker, "history": history}


@router.post("/{ticker}/predict")
def predict_stock(ticker: str, req: PredictRequest):
    """モンテカルロシミュレーションで株価予測を実行する"""
    try:
        result = run_prediction(
            ticker=ticker,
            start=req.start,
            end=req.end,
            n_sim=req.n_sim,
            future_days=req.future_days,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return result
