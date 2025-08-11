# stock_utils.py
import yfinance as yf
import pandas as pd
import os
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import numpy as np
from datetime import datetime, timedelta

CACHE_DIR = "cache"
MODEL_DIR = "models"
os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

def fetch_and_cache_stock(symbol, period="6mo", interval="1d"):
    # simple file cache by symbol+period+interval
    fname = f"{CACHE_DIR}/{symbol.replace('/','_')}_{period}_{interval}.csv"
    if os.path.exists(fname):
        df = pd.read_csv(fname, index_col=0, parse_dates=True)
        return df
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period, interval=interval)
        if df is None or df.empty:
            return pd.DataFrame()
        df.to_csv(fname)
        return df
    except Exception as e:
        print("yfinance fetch err:", e)
        return pd.DataFrame()

def create_lag_features(df, lags=[1,2,3,5,10]): # prev closing price 1 day ago, 2 day ago , ....
    # assumes df has 'Close' column
    #Rolling mean: 5-day moving average of closing prices. Gives a trend indicator.
    out = df.copy().sort_index() #(oldest → newest).
    for lag in lags:
        out[f"lag_{lag}"] = out["Close"].shift(lag)
    out["rolling_mean_5"] = out["Close"].rolling(window=5).mean().shift(1) #5-day rolling mean shifted by 1. so it does not include the current day (avoid leakage).
    out["target"] = out["Close"].shift(-1)   # next-day price
    out = out.dropna() #.dropna() removes rows that lack any lag/rolling value (early rows).
    return out

def train_model_from_df(df, symbol):
    data = create_lag_features(df)
    features = [c for c in data.columns if c.startswith("lag_") or c.startswith("rolling_")]
    X = data[features].values
    y = data["target"].values
    # small train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, shuffle=False)
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X_train, y_train)
    # save model
    model_path = f"{MODEL_DIR}/{symbol.replace('/','_')}_rf.joblib"
    joblib.dump({"model": model, "features": features}, model_path)
    # compute a simple score
    score = model.score(X_test, y_test)
    return model_path, score

def predict_next_day(df, symbol):
    model_path = f"{MODEL_DIR}/{symbol.replace('/','_')}_rf.joblib"
    # train if model missing
    if not os.path.exists(model_path):
        model_path, score = train_model_from_df(df, symbol)
    obj = joblib.load(model_path)
    model = obj["model"]
    features = obj["features"]
    data = create_lag_features(df)
    last_row = data.iloc[-1]
    X_last = last_row[features].values.reshape(1, -1)
    pred = model.predict(X_last)[0] #.predict() returns a NumPy array — [0] gets the single value out of it.
    last_date = last_row.name.strftime("%Y-%m-%d")
    return {"symbol": symbol, "prediction": float(pred), "last_date": last_date, "model_score": float(np.round(model.score(data[features].values, data["target"].values),4))}
