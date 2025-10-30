import streamlit as st
import pandas as pd
import joblib

st.title("Movie Review Sentiment Analyzer")

st.write("This analyzer accepts movie reviews as input and determines if the review has positive or negative sentiment.")

@st.cache_data
def load_logs():
    """Loads the shared logs folder for analysis."""
    logs = pd.read_json("../logs/prediction_logs.json")
    logs["length"] = logs["request_text"].str.len()
    return logs

@st.cache_data
def load_imdb():
    """Loads the IMDB dataset"""
    imdb = pd.read_csv("../IMDB Dataset.csv")
    imdb["length"] = imdb["review"].str.len()
    return imdb

logs = load_logs()
imdb = load_imdb()

# --- App ---

st.text(
    logs
)

st.text(
    imdb
)