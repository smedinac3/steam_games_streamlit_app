import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_data

st.set_page_config(
    page_title="EDA Gallery | SteamScope",
    layout="wide"
)

st.title("Exploratory Data Analysis Gallery")

st.write("""
Explore patterns in Steam game pricing, player
ratings, genres, and estimated ownership.

Each visualization investigates a research question
using historical Steam Store Games data.
""")

st.divider()

df = load_data()

# -----------------------------------------
# CHART 1: FREE VS PAID GAME RATINGS
# -----------------------------------------
st.header("1. Free vs. Paid Game Ratings")

st.subheader(
    "Do free-to-play games receive more "
    "positive ratings than paid games?"
)

# Group games by pricing model and add ratings
rating_summary = (
    df.groupby("pricing_model")[
        ["positive_ratings", "negative_ratings"]
    ]
    .sum()
    .reset_index()
)

# Calculate total ratings in each group
rating_summary["total_ratings"] = (
    rating_summary["positive_ratings"]
    + rating_summary["negative_ratings"]
)

# Calculate percentages
rating_summary["Positive"] = (
    rating_summary["positive_ratings"]
    / rating_summary["total_ratings"]
    * 100
)

rating_summary["Negative"] = (
    rating_summary["negative_ratings"]
    / rating_summary["total_ratings"]
    * 100
)

# Wide data into long format
rating_long = rating_summary.melt(
    id_vars="pricing_model",
    value_vars=["Positive", "Negative"],
    var_name="Rating Type",
    value_name="Percentage"
)

# Interactive grouped bar chart
fig = px.bar(
    rating_long,
    x="pricing_model",
    y="Percentage",
    color="Rating Type",
    barmode="group",
    title="Player Rating Distribution by Pricing Model",
    labels={
        "pricing_model": "Pricing Model",
        "Percentage": "Share of Ratings (%)"
    },
    color_discrete_map={
        "Positive": "#0072B2",
        "Negative": "#E69F00"
    },
    category_orders={
        "pricing_model": ["Free", "Paid"]
    },
    text_auto=".1f"
)

fig.update_layout(
    yaxis_range=[0, 100],
    legend_title_text="Rating Type",
    hovermode="closest"
)

fig.update_traces(
    hovertemplate=(
        "%{x}<br>"
        "%{fullData.name}: %{y:.2f}%"
        "<extra></extra>"
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# HOW TO READ THE CHART
st.subheader("How to Read This Chart")

st.markdown("""
- **X-axis:** Separates games into free and paid
  categories.
- **Y-axis:** Shows the percentage of player ratings
  in each category.
- **Colors:** Blue represents positive ratings,
  while orange represents negative ratings.
  Hover over a bar to view its exact percentage.
""")

# OBSERVATIONS
st.subheader("Key Observations")

free_pct = rating_summary.loc[
    rating_summary["pricing_model"] == "Free",
    "Positive"
].iloc[0]

paid_pct = rating_summary.loc[
    rating_summary["pricing_model"] == "Paid",
    "Positive"
].iloc[0]

difference = free_pct - paid_pct

st.markdown(
    f"""
- Free games have **{free_pct:.2f}%**
  positive ratings.
- Paid games have **{paid_pct:.2f}%**
  positive ratings.
- The difference is **{abs(difference):.2f}
  percentage points**, indicating that
  the overall rating distributions are similar.
- These results describe aggregated rating counts,
  not the average rating percentage per game.
"""
)

st.caption(
    "Source: Steam Store Games dataset by Nik Davis "
    "(Kaggle). Historical data, approximately 2019. "
    "Rating percentages are calculated from recorded "
    "positive and negative rating counts."
)

st.markdown(
    "[View dataset source]"
    "(https://www.kaggle.com/datasets/nikdavis/steam-store-games)"
)


# -----------------------------------------
# CHART 2: ESTIMATED OWNERSHIP BY GENRE
# -----------------------------------------
st.divider()

st.header("2. Estimated Ownership by Genre")

st.subheader(
    "Which genres have the highest "
    "estimated ownership?"
)

st.write("""
Steam games can belong to multiple genres.
We will separate these genres and calculate
the combined estimated ownership for each.
""")

genre_df = df.copy()

genre_df["genre"] = (
    genre_df["genres"].str.split(";")
)

genre_df = genre_df.explode("genre")

genre_df["genre"] = genre_df["genre"].str.strip()

genre_summary = (
    genre_df.groupby("genre", as_index=False)
    .agg(
        estimated_owners=("estimated_owners", "sum"),
        game_count=("appid", "count")
    )
    .sort_values(
        "estimated_owners",
        ascending=False
    )
)

# Interactive control
top_n = st.slider(
    "Number of genres to display",
    min_value=5,
    max_value=15,
    value=10,
    key="genre_ownership_slider"
)

top_genres = genre_summary.head(top_n).copy()

fig2 = px.bar(
    top_genres,
    x="estimated_owners",
    y="genre",
    orientation="h",
    color="estimated_owners",
    color_continuous_scale="Blues",
    title="Estimated Ownership by Steam Game Genre",
    labels={
        "estimated_owners": "Summed Estimated Owners",
        "genre": "Game Genre"
    },
    hover_data={
        "estimated_owners": ":,.0f",
        "game_count": True,
        "genre": False
    }
)

fig2.update_layout(
    yaxis={
        "categoryorder": "total ascending"
    },
    coloraxis_showscale=False,
    height=max(450, top_n * 42),
    xaxis_tickformat="~s"
)

top_genre = top_genres.iloc[0]

fig2.add_annotation(
    x=top_genre["estimated_owners"],
    y=top_genre["genre"],
    text="Highest estimated ownership",
    showarrow=True,
    arrowhead=2,
    ax=-100,
    ay=-35
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# HOW TO READ THE CHART
st.subheader("📖 How to Read This Chart")

st.markdown("""
- **Y-axis:** Lists the Steam game genres.
- **X-axis:** Shows the summed estimated
  ownership across games in each genre.
- **Bars and colors:** Longer, darker blue
  bars indicate larger estimates. Hover
  over a bar to view its value and game count.
""")

# OBSERVATIONS
st.subheader("Key Observations")

second_genre = top_genres.iloc[1]

st.markdown(
    f"""
- **{top_genre['genre']}** has the highest
  summed estimated ownership at approximately
  **{top_genre['estimated_owners'] / 1e9:.2f}
  billion** game-owner counts.
- **{second_genre['genre']}** ranks second
  with approximately
  **{second_genre['estimated_owners'] / 1e9:.2f}
  billion**.
- Genres with many games may accumulate
  larger ownership totals.
- Because games can have multiple genres,
  ownership counts overlap across categories.
"""
)

st.caption(
    "Source: Steam Store Games dataset by Nik Davis "
    "(Kaggle), approximately 2019. Ownership "
    "values are midpoints of reported ranges, "
    "not verified sales or unique player counts."
)

st.markdown(
    "[View dataset source]"
    "(https://www.kaggle.com/datasets/nikdavis/steam-store-games)"
)
