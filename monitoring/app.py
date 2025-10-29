import streamlit as st
import joblib

st.title("Movie Review Sentiment Analyzer")

st.write("This analyzer accepts movie reviews as input and determines if the review has positive or negative sentiment.")

@st.cache_data
def load_model():
    """Loads the pre-trained sentiment analyzer."""
    model = joblib.load('sentiment_model.pkl')
    return model

def get_sentiment(input: str, model):
    """Performs a prediction on a string and cleans up the output."""
    predicted = model.predict([input])
    output = predicted[0]
    return output

model = load_model()

# --- App ---

user_input = st.text_area(label='Input movie review for analysis:')

analyze_button = st.button(label='Analyse')

if analyze_button:
    if len(user_input) == 0:
        st.write("Please input a movie review for analysis.")
    else:
        results = get_sentiment(user_input, model)
        if results == 'positive':
            st.success('Positive')
        elif results == 'negative':
            st.error('Negative')
        probs = model.predict_proba([user_input])
        prob_neg = probs[0][0]
        prob_pos = probs[0][1]
        st.write(f"Negative sentiment prob: {prob_neg}")
        st.write(f"Positive sentiment prob: {prob_pos}")