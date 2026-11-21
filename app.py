import streamlit as st
from utils.data_loader import load_data

st.set_page_config(
    page_title="SteamScope Analytics",
    layout="wide"
)

df = load_data()

st.subheader("Dataset Diagnostics")

st.write("Loaded game records:", len(df))
st.write("Loaded columns:", len(df.columns))

st.write(
    "Latest release date:",
    df["release_date"].max()
)

st.write(
    "First 5 games:",
    df["name"].head()
)

st.title("SteamScope Analytics")
st.subheader(
    "Exploring Steam Games, Player Ratings, "
    "Pricing, and Popularity"
)
st.write("""
Welcome to SteamScope Analytics!

This interactive data visualization portfolio
explores Steam games using a historical dataset
updated through March 2025.

Explore game releases, genres, prices, player
ratings, and estimated ownership through
interactive charts and a filterable dashboard.
""")

st.divider()

st.header("Dataset Overview")
total_games = df["appid"].nunique()
total_columns = len(df.columns)
earliest_date = df["release_date"].min()
latest_date = df["release_date"].max()
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Games",
        f"{total_games:,}"
    )

with col2:
    st.metric(
        "Dataset Columns",
        total_columns
    )

with col3:
    st.metric(
        "Latest Release",
        latest_date.strftime("%b %Y")
        if not df["release_date"].isna().all()
        else "Unknown"
    )

st.caption(
    "Source: Steam Games Dataset, March 2025 "
    "snapshot. Dataset columns include both "
    "original fields and calculated variables."
)

st.divider()

st.header("Research Questions")
st.markdown("""
1. How do positive player ratings compare
   between free and paid games?

2. Which game genres have the highest
   estimated ownership?

3. Which genres have the highest percentage
   of positive player ratings?

4. How do game prices vary across genres?

5. How has the number of Steam game releases
   changed over time?
""")

st.divider()

st.header("Data Preview")

st.write(
    "Below is a preview of the prepared "
    "March 2025 Steam dataset."
)

preview_columns = [
    "appid",
    "name",
    "release_date",
    "genres",
    "price",
    "positive_ratings",
    "negative_ratings",
    "estimated_owners"
]

st.dataframe(
    df[preview_columns].head(10),
    use_container_width=True,
    hide_index=True
)

st.caption(
    "Prices are displayed in the dataset's "
    "original units. Currency verification "
    "is pending."
)

st.divider()

st.header("Explore SteamScope")

st.markdown("""
**Bio** — Learn about the project creator,
their skills, and visualization philosophy.

**EDA Gallery** — Explore five interactive
charts investigating Steam game trends.

**Dashboard** — Filter games by genre,
pricing model, and release year.

**Future Work** — Explore limitations,
improvements, and project reflections.
""")

st.divider()

st.header("Data Source & Limitations")

st.markdown("""
The project uses the March 2025 Steam Games
Dataset compiled by ArterMiloff.

The data represents a historical snapshot,
not live Steam store information.

Estimated ownership values are approximate,
and games may belong to multiple genres.

The 2025 release counts represent a partial
year and should not be interpreted as a
complete annual total.
""")

st.markdown(
    "[View the original dataset on Kaggle]"
    "(https://www.kaggle.com/datasets/artermiloff/steam-games-dataset)"
)
