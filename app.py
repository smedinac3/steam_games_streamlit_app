import streamlit as st

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
