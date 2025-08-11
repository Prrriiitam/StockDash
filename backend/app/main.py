# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import pandas as pd
import joblib
import os

from stock_utils import fetch_and_cache_stock,  predict_next_day
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Stock Dashboard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for testing, allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# simple in-memory/company list - you can expand
COMPANIES = [
    {"symbol": "RELIANCE.NS", "name": "Reliance Industries"},
    {"symbol": "TCS.NS", "name": "Tata Consultancy Services"},
    {"symbol": "INFY.NS", "name": "Infosys"},
    {"symbol": "HDFCBANK.NS", "name": "HDFC Bank"},
    {"symbol": "ICICIBANK.NS", "name": "ICICI Bank"},
    {"symbol": "HINDUNILVR.NS", "name": "Hindustan Unilever"},
    {"symbol": "SBIN.NS", "name": "State Bank of India"},
    {"symbol": "BHARTIARTL.NS", "name": "Bharti Airtel"},
    {"symbol": "LT.NS", "name": "Larsen & Toubro"},
    {"symbol": "AXISBANK.NS", "name": "Axis Bank"}
]

@app.get("/companies")
async def companies():
    return COMPANIES

@app.get("/historical/{symbol}")
async def historical(symbol: str, period: str = "6mo", interval: str = "1d"):
    # fetch and cache (stock_utils handles caching)
    df = fetch_and_cache_stock(symbol, period=period, interval=interval)
    if df is None or df.empty:
        raise HTTPException(status_code=404, detail="No data found")
    # return basic fields to frontend
    result = df.reset_index().to_dict(orient="records") #converts rows of df to list of dicts suitable for JSON. 
    return {"symbol": symbol, "data": result}

class PredictRequest(BaseModel):
    symbol: str

@app.post("/predict")
async def predict(req: PredictRequest):
    symbol = req.symbol
    # fetch data first
    df = fetch_and_cache_stock(symbol, period="1y", interval="1d")
    if df is None or df.empty:
        raise HTTPException(status_code=404, detail="No data for symbol")
    # returns dict: {"prediction": float, "last_date": "...", "model_info": {...}}
    res = predict_next_day(df, symbol)
    return res
