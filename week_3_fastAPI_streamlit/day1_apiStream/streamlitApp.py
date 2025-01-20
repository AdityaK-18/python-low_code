import streamlit as st
import requests
import pandas as pd

# FastAPI endpoint
API_URL = "http://127.0.0.1:8000/students"

st.title("Student Data Viewer")
st.write("This app fetches and displays data from a FastAPI backend.")

# Fetch data from FastAPI
try:
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        # Convert data to a DataFrame
        df = pd.DataFrame(data)
        st.write("### Student Data Table")
        st.dataframe(df)

        # Optionally display a chart
        st.write("### Age Distribution")
        st.bar_chart(df['age'])
    else:
        st.error(f"Failed to fetch data: {response.status_code}")
except Exception as e:
    st.error(f"An error occurred: {e}")
