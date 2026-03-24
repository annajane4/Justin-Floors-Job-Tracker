import streamlit as st
import pandas as pd

st.set_page_config(page_title="JustinFloors Job Tracker", layout="wide")

st.title("JustinFloors Job Tracker")

st.header("Dashboard")

# Dummy data for now (so app runs without database)
data = [
    {"Job": "Kitchen Remodel - Smith", "Status": "Waiting on Materials"},
    {"Job": "Bathroom Tile - Johnson", "Status": "Scheduled"},
    {"Job": "Basement Flooring - Lee", "Status": "Install Complete"},
]

df = pd.DataFrame(data)

st.subheader("All Jobs")
st.dataframe(df, use_container_width=True)

st.subheader("Jobs Waiting on Materials")
st.write("Coming soon...")

st.subheader("Upcoming Installs")
st.write("Coming soon...")

st.success("App is running")
