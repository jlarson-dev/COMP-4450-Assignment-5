from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from random import randint
import joblib
import time
import pandas as pd

# API
app = FastAPI(
    title = "Movie Review Sentiment Analyzer"
)

# Load the model
try:
    model = joblib.load('sentiment_model.pkl')
    print("Model 'sentiment_model' loaded successfully.")
except Exception as e:
    print(f"Failed to load model: {e}")
    model = None
    
# Load the dataset
try:
    df = pd.read_csv('IMDB Dataset.csv')
    reviews = df['review'].tolist()
except:
    print("Error: dataset 'IMDB Dataset.csv' not found.")
    reviews = None
class Review(BaseModel):
    text: str

# Helper functions
def model_state():
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded.")
    return model

def predict_sentiment(text: str):
    """Predict sentiment of input review"""
    model_state()
    return model.predict([text])[0]

def pred_proba(text: str):
    """Returns confidence score of prediction"""
    model_state()
    return model.predict_proba([text])[0]

# Middleware runs with each request to add headers
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.get("/health")
def health():
    return {"status": "ok", "message": "API is running"}


@app.post("/predict")
def post_pred(input: Review):
    """Performs a sentiment prediction on an input string"""
    predicted = predict_sentiment(input.text)
    return {"sentiment": predicted}


@app.post("/predict_proba")
def post_proba(input: Review):
    """Takes a text input and returns the predicted sentiment along with its confidence score."""
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded.")
    sentiment = predict_sentiment(input.text)
    probs = pred_proba(input.text)
    return {"sentiment": sentiment, "probability": round(probs.max(), 2)}
