from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers import stock

app = FastAPI(title="Stock Market Prediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stock.router)


@app.get("/")
def root():
    return {"message": "Stock Market Prediction API"}
