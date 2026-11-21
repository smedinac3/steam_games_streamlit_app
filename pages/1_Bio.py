import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="SteamScope | About Me",
    layout="wide"
)

st.title("About Me")

st.write(
    "Welcome to my data visualization portfolio!"
)

col1, col2 = st.columns([1, 2], gap="large")

with col1:

    image_path = (
        Path(__file__).resolve().parent.parent
        / "assets"
        / "profile.png"
    )

    if image_path.exists():
        st.image(
            str(image_path),
            caption="Portfolio profile image",
            width=260
        )
    else:
        st.info(
            "Profile image coming soon."
        )

with col2:

    st.subheader("Hello! my name is Sergio and I'm currently a student at Metropolitan State University of Denver.")

    st.write("""
    I'm interested in software
    development, data analytics, and
    interactive data visualization.

    I enjoy exploring how programming and
    visual storytelling can transform large
    datasets into meaningful insights.

    For this portfolio, I combined my
    interest in video games with data
    analysis to create SteamScope Analytics.
    """)

    st.write("""
    This project allows visitors to explore
    Steam game trends, pricing, genre
    popularity, and player ratings through
    interactive visualizations.
    """)
st.divider()

st.header("Technical Skills")

skill_col1, skill_col2, skill_col3 = st.columns(3)

with skill_col1:
    st.subheader("Programming")
    st.markdown("""
    - Python
    - Pandas
    - Data cleaning
    - Exploratory data analysis
    """)

with skill_col2:
    st.subheader("Visualization")
    st.markdown("""
    - Plotly
    - Matplotlib
    - Interactive dashboards
    - Data storytelling
    """)

with skill_col3:
    st.subheader("Development")
    st.markdown("""
    - Streamlit
    - GitHub
    - CSV data processing
    - Web application deployment
    """)
st.divider()

st.header("About SteamScope Analytics")

st.write("""
SteamScope Analytics is an interactive
data visualization project built using
Python, Pandas, Plotly, and Streamlit.

The application analyzes a March 2025
Steam games dataset to explore questions
about the gaming marketplace.
""")

st.markdown("""
**Key research questions:**

1. How do player ratings compare between
   free and paid Steam games?

2. Which genres have the highest
   estimated ownership?

3. Which genres receive the highest
   percentage of positive player ratings?

4. How do game prices differ by genre?

5. How have Steam game releases changed
   over time?
""")
st.divider()

st.header("What I Learned")

st.markdown("""
Through this project, I practiced:

- Preparing and transforming a large
  real-world dataset.
- Creating interactive visualizations
  with Plotly.
- Building reactive dashboards using
  Streamlit.
- Applying filters to explore data.
- Explaining visualization limitations
  and avoiding misleading conclusions.
- Managing and deploying a Python
  project using GitHub.
""")
st.divider()

st.caption(
    "Project dataset: Steam Games Dataset, "
    "March 2025 snapshot."
)

st.markdown(
    "[Dataset source — Kaggle]"
    "(https://www.kaggle.com/datasets/artermiloff/steam-games-dataset)"
)
