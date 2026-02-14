import os
import requests
import streamlit as st

API_URL = os.environ.get("API_URL", "http://api:8000")

st.set_page_config(page_title="Sentiment Demo")
st.title("Sentiment Analysis Demo")

text = st.text_area("Enter text to analyze", height=200)
if st.button("Analyze"):
    if not text.strip():
        st.error("Please enter some text.")
    else:
        try:
            resp = requests.post(f"{API_URL}/predict", json={"text": text}, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            st.write("**Sentiment:**", data.get("sentiment"))
            st.write("**Confidence:**", data.get("confidence"))
        except Exception as e:
            st.error(f"Request failed: {e}")
