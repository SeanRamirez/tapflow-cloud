from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from storage import GoldLayerReader
import pandas as pd
import uvicorn
import os

app = FastAPI(title="TapFlow Cloud API")

# Enable CORS so your future React dashboard can talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL here
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize our storage reader
try:
    storage = GoldLayerReader()
    print("✅ Successfully connected to Azure Storage")
except Exception as e:
    print(f"❌ Failed to connect to Azure Storage: {e}")
    storage = None

@app.get("/")
def root():
    return {"message": "TapFlow API is running", "status": "active"}

# Endpoint 1: Real-time Sales Summary
@app.get("/api/sales/summary")
def get_sales_summary():
    if not storage:
        raise HTTPException(status_code=500, detail="Storage connection failed")
        
    df = storage.read_table("daily_sales")
    
    if df.empty:
        return {"error": "No data found"}

    # Calculate summary metrics
    return {
        "total_transactions": int(df["transaction_count"].sum()),
        "total_pints": int(df["total_pints_sold"].sum()),
        "total_revenue": float(df["total_revenue"].sum()),
        "avg_price": float(df["avg_price"].mean())
    }

# Endpoint 2: Top Beers
@app.get("/api/beers/top")
def get_top_beers(limit: int = 5):
    if not storage:
        raise HTTPException(status_code=500, detail="Storage connection failed")

    df = storage.read_table("beer_metrics")
    
    if df.empty:
        return []

    # Sort by revenue and take the top N
    top_beers = df.sort_values(by="total_revenue", ascending=False).head(limit)
    
    return top_beers.to_dict(orient="records")

# Endpoint 3: Brewery Performance
@app.get("/api/breweries/performance")
def get_brewery_performance():
    if not storage:
        raise HTTPException(status_code=500, detail="Storage connection failed")

    df = storage.read_table("brewery_metrics")
    
    if df.empty:
        return []
        
    # Sort by revenue for better display
    df_sorted = df.sort_values(by="total_revenue", ascending=False)
    
    return df_sorted.to_dict(orient="records")

# Endpoint 4: Daily Trends
@app.get("/api/sales/daily")
def get_daily_trends():
    if not storage:
        raise HTTPException(status_code=500, detail="Storage connection failed")

    df = storage.read_table("daily_sales")
    
    if df.empty:
        return []

    # Aggregate by date in case there are multiple entries per day
    daily = df.groupby("date").agg({
        "total_revenue": "sum",
        "total_pints_sold": "sum",
        "transaction_count": "sum"
    }).reset_index()
    
    # Sort by date
    daily = daily.sort_values("date")
    
    # Convert date to string for JSON serialization
    daily["date"] = daily["date"].astype(str)
    
    return daily.to_dict(orient="records")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)