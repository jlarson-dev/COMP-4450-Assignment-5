import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

from pathlib import Path
from sklearn.metrics import accuracy_score

st.title("Movie Review Sentiment Data Drift Analyzer")

def load_logs():
    """Loads the shared logs folder for analysis."""
    logs = pd.read_json('prediction_logs.json')
    return logs

@st.cache_data
def load_imdb():
    """Loads the IMDB dataset"""
    imdb = pd.read_csv("IMDB Dataset.csv")
    imdb["length"] = imdb["review"].str.len()
    return imdb

logs = load_logs()
imdb = load_imdb()

# --- App ---
# Accuracy & Precision

acc = accuracy_score(logs['true_sentiment'], logs['predicted_sentiment'])
if acc < 0.8:
    st.error("Warning: Accuracy is below 80%.")
st.write(f"Accuracy: {acc}")

# Data Drift Analysis - distribution of review lengths

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

ax1.hist(logs['length'], bins=20, color='skyblue', edgecolor='black')
ax1.set_title("Logged Reviews")
ax1.set_xlabel("Review Length")

ax2.hist(imdb['length'], bins=20, color='lightgreen', edgecolor='black')
ax2.set_title("IMDB Dataset")
ax2.set_xlabel("Review Length")

st.pyplot(fig)

# Target Drift Analysis - distribution of predicted sentiments

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))


color_map = {
    "positive": "green",
    "negative": "red"
}

    #Logs
log_pred_counts = logs['predicted_sentiment'].value_counts()
log_true_counts = logs['true_sentiment'].value_counts()
log_colors = [color_map[label] for label in log_pred_counts.index]

ax1.bar(log_pred_counts.index, log_pred_counts.values, color=log_colors)
ax1.set_title("Logged Reviews")
ax1.set_xlabel("Sentiment")
ax1.set_ylabel("Count")

    #IMDB
imdb_counts = imdb['sentiment'].value_counts()
imdb_colors = [color_map[label] for label in imdb_counts.index]

ax2.bar(imdb_counts.index, imdb_counts.values, color=imdb_colors)
ax2.set_title("IMDB Dataset")
ax2.set_xlabel("Sentiment")

st.pyplot(fig)
