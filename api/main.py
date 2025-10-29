from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from random import randint
import joblib
import time
import pandas as pd
from datetime import datetime
import os
import json

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
LOG_DIR = "../logs"
LOG_FILE = os.path.join(LOG_DIR, "prediction_logs.json")

# Ensure /logs directory exists (Docker volume will mount here)
os.makedirs(LOG_DIR, exist_ok=True)

def log_prediction(request_text: str, predicted_sentiment: str, true_sentiment: str):
    """Append a log entry as a JSON line to /logs/prediction_logs.json"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "request_text": request_text,
        "predicted_sentiment": predicted_sentiment,
        "true_sentiment": true_sentiment
    }

    # Append as a new JSON line
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")


# ========================
# REQUEST MODEL
# ========================
class Review(BaseModel):
    text: str
    true_sentiment: str = None  # optional, but needed for logging


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

    # If true_sentiment was provided, log it
    true_sentiment = input.true_sentiment if input.true_sentiment else "unknown"
    log_prediction(input.text, predicted, true_sentiment)

    return {"sentiment": predicted}