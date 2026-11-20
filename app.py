import streamlit as st
from utils.data_loader import load_data

st.set_page_config(
    page_title="SteamScope Analytics",
    layout="wide"
)

st.title("SteamScope Analytics")
st.subheader("Steam Games Data Visualization Portfolio")

st.write("""
Welcome to my data visualization portfolio!

This project explores Steam video games using
Python, Pandas, Plotly, and Streamlit.
""")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.header("EDA Gallery")
    st.write("Explore patterns in Steam game data.")

with col2:
    st.header("Dashboard")
    st.write("Analyze game pricing, genres, and ratings.")

st.info("Use the sidebar to explore the portfolio.")

st.divider()
st.header("Steam Dataset Overview")

df = load_data()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Games", f"{len(df):,}")

with col2:
    st.metric("Total Columns", len(df.columns))

with col3:
    st.metric(
        "Average Price",
        f"£{df['price'].mean():.2f}"
    )

st.subheader("Dataset Preview")
st.dataframe(df.head(10), use_container_width=True)
