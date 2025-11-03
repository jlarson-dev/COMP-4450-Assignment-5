import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt

from sklearn.metrics import confusion_matrix

st.title("Movie Review Sentiment Analyzer")

st.write("This analyzer accepts movie reviews as input and determines if the review has positive or negative sentiment.")

def load_logs():
    """Loads the shared logs folder for analysis."""
    logs = pd.read_json("../logs/prediction_logs.json")
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

# Data Drift Analysis - distribution of review lengths

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), sharey=True)

ax1.hist(logs['length'], bins=20, color='skyblue', edgecolor='black')
ax1.set_title("Logged Reviews")
ax1.set_xlabel("Review Length")

ax2.hist(imdb['length'], bins=20, color='lightgreen', edgecolor='black')
ax2.set_title("IMDB Dataset")
ax2.set_xlabel("Review Length")

st.pyplot(fig)

# Target Drift Analysis - distribution of predicted sentiments

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), sharey=True)


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


# Accuracy & Precision
 
cm = confusion_matrix(logs['true_sentiment'], logs['predicted_sentiment'])
st.write(cm)