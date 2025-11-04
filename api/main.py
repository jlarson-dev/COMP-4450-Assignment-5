from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from random import randint
import joblib
import time
import pandas as pd
from datetime import datetime
import os
import json
from pathlib import Path

# ========================
# API CONFIGURATION
# ========================
app = FastAPI(
    title="Movie Review Sentiment Analyzer"
)

# ========================
# MODEL & DATASET LOADING
# ========================
try:
    model = joblib.load('sentiment_model.pkl')
    print("Model 'sentiment_model' loaded successfully.")
except Exception as e:
    print(f"Failed to load model: {e}")
    model = None

# ========================
# LOGGING CONFIGURATION
# ========================
LOG_DIR = "/app/logs"
LOG_FILE = Path("/app/logs/prediction_logs.json")

# Ensure /logs directory exists (Docker volume will mount here)
os.makedirs(LOG_DIR, exist_ok=True)

def log_prediction(request_text: str, predicted_sentiment: str, true_sentiment: str):
    """Append a log entry as an element in a valid JSON array."""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "request_text": request_text,
        "predicted_sentiment": predicted_sentiment,
        "true_sentiment": true_sentiment,
        "length": len(request_text)
    }

    # Ensure the log file exists
    if LOG_FILE.exists():
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                logs = json.load(f)
                # Ensure it's a list
                if not isinstance(logs, list):
                    logs = []
        except json.JSONDecodeError:
            # If file is empty or invalid JSON, start fresh
            logs = []
    else:
        logs = []

    # Append the new entry
    logs.append(log_entry)

    # Write back as valid JSON array
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2)



# ========================
# REQUEST MODEL
# ========================
class Review(BaseModel):
    text: str
    true_sentiment: str = None


# ========================
# HELPER FUNCTIONS
# ========================
def model_state():
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded.")
    return model

def predict_sentiment(text: str):
    """Predict sentiment of input review"""
    model_state()
    return model.predict([text])[0]

# ========================
# MIDDLEWARE
# ========================
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# ========================
# ENDPOINTS
# ========================
@app.get("/health")
def health():
    return {"status": "ok", "message": "API is running"}

@app.post("/predict")
def post_pred(input: Review):
    """
    Performs a sentiment prediction on an input string
    and logs the result to /logs/prediction_logs.json
    """
    predicted = predict_sentiment(input.text)

    true_sentiment = input.true_sentiment if input.true_sentiment else "unknown"
    log_prediction(input.text, predicted, true_sentiment)

    return {"sentiment": predicted}