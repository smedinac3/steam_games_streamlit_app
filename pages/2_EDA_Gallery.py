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
    "Do free and paid Steam games receive "
    "different percentages of positive ratings?"
)

st.write("""
This grouped bar chart compares the proportion
of positive and negative player ratings for
free and paid games in the March 2025 dataset.
""")

rating_summary = (
    df.groupby("pricing_model", as_index=False)
    .agg(
        game_count=("appid", "nunique"),
        positive=("positive_ratings", "sum"),
        negative=("negative_ratings", "sum")
    )
)

rating_summary["total_ratings"] = (
    rating_summary["positive"]
    + rating_summary["negative"]
)

rating_summary["Positive"] = (
    rating_summary["positive"]
    / rating_summary["total_ratings"].replace(
        0, float("nan")
    )
    * 100
)

rating_summary["Negative"] = (
    rating_summary["negative"]
    / rating_summary["total_ratings"].replace(
        0, float("nan")
    )
    * 100
)

rating_long = rating_summary.melt(
    id_vars=["pricing_model", "game_count"],
    value_vars=["Positive", "Negative"],
    var_name="Rating Type",
    value_name="Percentage"
)

fig1 = px.bar(
    rating_long,
    x="pricing_model",
    y="Percentage",
    color="Rating Type",
    barmode="group",
    text_auto=".1f",
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
    hover_data={
        "game_count": True
    }
)

fig1.update_layout(
    yaxis_range=[0, 100],
    height=480,
    legend_title_text="Rating Type"
)

fig1.update_traces(
    hovertemplate=(
        "Percentage: %{y:.2f}%"
        "<extra></extra>"
    )
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

st.subheader("Reading This Chart")

st.markdown("""
- **X-axis:** Separates free and paid games.
- **Y-axis:** Shows the percentage of recorded
  player ratings, from 0% to 100%.
- **Bar colors:** Blue represents positive
  ratings, while orange represents negative
  ratings. Hover for exact percentages.
""")

st.subheader("Key Observations")

free_data = rating_summary[
    rating_summary["pricing_model"] == "Free"
].iloc[0]

paid_data = rating_summary[
    rating_summary["pricing_model"] == "Paid"
].iloc[0]

difference = (
    paid_data["Positive"] - free_data["Positive"]
)

st.markdown(
    f"""
- Free games have a positive rating share of
  **{free_data['Positive']:.2f}%** across
  **{int(free_data['game_count']):,} games**.
- Paid games have a positive rating share of
  **{paid_data['Positive']:.2f}%** across
  **{int(paid_data['game_count']):,} games**.
- Paid games have a positive rating share
  **{difference:.2f} percentage points higher**
  than free games.
- These percentages are calculated from total
  recorded ratings, not the average rating
  percentage of individual games.
"""
)

st.caption(
    "Source: Steam Games Dataset, March 2025 "
    "(ArterMiloff, Kaggle). Results describe "
    "recorded ratings in this historical dataset. "
    "Differences do not establish causation."
)

st.markdown(
    "[View dataset source]"
    "(https://www.kaggle.com/datasets/artermiloff/steam-games-dataset)"
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
st.subheader("How to Read This Chart")

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


# -----------------------------------------
# CHART 3: POSITIVE RATINGS BY GENRE
# -----------------------------------------
st.divider()

st.header("3. Positive Ratings by Genre")

st.subheader(
    "Which genres have the highest percentage "
    "of positive player ratings?"
)

st.write("""
This visualization compares the percentage of
positive ratings across Steam game genres.

A minimum game-count filter helps us avoid
overemphasizing very small categories.
""")

ratings_genre_df = df.copy()

ratings_genre_df["genre"] = (
    ratings_genre_df["genres"].str.split(";")
)

ratings_genre_df = ratings_genre_df.explode("genre")

ratings_genre_df["genre"] = (
    ratings_genre_df["genre"].str.strip()
)

genre_ratings = (
    ratings_genre_df.groupby("genre", as_index=False)
    .agg(
        positive=("positive_ratings", "sum"),
        negative=("negative_ratings", "sum"),
        game_count=("appid", "count")
    )
)

genre_ratings["total_ratings"] = (
    genre_ratings["positive"]
    + genre_ratings["negative"]
)

genre_ratings["positive_pct"] = (
    genre_ratings["positive"]
    / genre_ratings["total_ratings"].replace(0, float("nan"))
    * 100
)

min_games = st.slider(
    "Minimum number of games per genre",
    min_value=1,
    max_value=1000,
    value=100,
    step=25,
    key="genre_rating_min_games"
)

filtered_ratings = genre_ratings[
    (genre_ratings["game_count"] >= min_games)
    & (genre_ratings["total_ratings"] > 0)
].copy()

filtered_ratings = filtered_ratings.sort_values(
    "positive_pct",
    ascending=False
)

fig3 = px.scatter(
    filtered_ratings,
    x="positive_pct",
    y="genre",
    color="positive_pct",
    size="game_count",
    size_max=20,
    color_continuous_scale="Viridis",
    title="Positive Player Rating Percentage by Genre",
    labels={
        "positive_pct": "Positive Ratings (%)",
        "genre": "Game Genre",
        "game_count": "Number of Games"
    },
    hover_data={
        "positive_pct": ":.2f",
        "game_count": ":,",
        "total_ratings": ":,"
    }
)

fig3.update_layout(
    yaxis={
        "categoryorder": "array",
        "categoryarray": filtered_ratings[
            "genre"
        ].tolist()[::-1]
    },
    xaxis_range=[0, 100],
    coloraxis_showscale=False,
    height=max(500, len(filtered_ratings) * 30)
)

fig3.update_traces(
    marker=dict(
        line=dict(width=1, color="white")
    )
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

st.subheader("How to Read This Chart")

st.markdown("""
- **X-axis:** Shows the percentage of positive
  player ratings, from 0% to 100%.
- **Y-axis:** Lists Steam game genres, ordered
  by their positive rating percentages.
- **Dot size and color:** Larger dots represent
  genres containing more games. Color also
  represents positive rating percentage.
  Hover to see exact values.
""")

st.subheader("Key Observations")

if not filtered_ratings.empty:

    highest = filtered_ratings.iloc[0]
    lowest = filtered_ratings.iloc[-1]

    st.markdown(
        f"""
- **{highest['genre']}** has the highest
  positive rating percentage among the
  displayed genres, at
  **{highest['positive_pct']:.2f}%**.
- **{lowest['genre']}** has the lowest
  percentage among the displayed genres,
  at **{lowest['positive_pct']:.2f}%**.
- Changing the minimum game count can
  affect which genres appear in the chart.
- These percentages are based on combined
  rating counts, not an average of each
  game's individual rating percentage.
"""
    )

st.caption(
    "Source: Steam Store Games dataset by Nik Davis "
    "(Kaggle), approximately 2019. Genres may "
    "overlap. Rating percentages use aggregated "
    "positive and negative review counts."
)

st.markdown(
    "[View dataset source]"
    "(https://www.kaggle.com/datasets/nikdavis/steam-store-games)"
)

# -----------------------------------------
# CHART 4: GAME PRICES BY GENRE
# -----------------------------------------
st.divider()

st.header("4. Game Prices by Genre")

st.subheader(
    "How do game prices vary across "
    "different Steam genres?"
)

st.write("""
This box plot compares the distribution of
game prices across popular Steam genres.

Use the controls to explore how free games
and unusually high prices affect the results.
""")

price_df = df.copy()

price_df["genre"] = price_df["genres"].str.split(";")

price_df = price_df.explode("genre")

price_df["genre"] = price_df["genre"].str.strip()

top_price_genres = (
    price_df["genre"]
    .value_counts()
    .head(10)
    .index
    .tolist()
)

price_df = price_df[
    price_df["genre"].isin(top_price_genres)
].copy()

exclude_free = st.checkbox(
    "Exclude free games (£0)",
    value=False,
    key="exclude_free_price"
)

show_outliers = st.checkbox(
    "Show outlier points",
    value=True,
    key="show_price_outliers"
)

max_price = st.slider(
    "Maximum game price (£)",
    min_value=10,
    max_value=100,
    value=100,
    step=5,
    key="maximum_game_price"
)

if exclude_free:
    price_df = price_df[price_df["price"] > 0]

price_df = price_df[
    price_df["price"] <= max_price
]

fig4 = px.box(
    price_df,
    x="genre",
    y="price",
    color="genre",
    points="outliers" if show_outliers else False,
    title="Steam Game Price Distribution by Genre",
    labels={
        "genre": "Game Genre",
        "price": "Game Price (£)"
    },
    color_discrete_sequence=px.colors.qualitative.Safe
)

fig4.update_layout(
    showlegend=False,
    xaxis_tickangle=-35,
    height=550,
    yaxis_tickprefix="£"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

st.subheader("How to Read This Chart")

st.markdown("""
- **X-axis:** Lists the 10 most common genres
  in the Steam dataset.
- **Y-axis:** Shows game prices in British pounds
  (£). The line inside each box represents the
  median price.
- **Boxes, whiskers, and dots:** Boxes show the
  middle 50% of prices, whiskers show the
  typical range, and individual dots identify
  potential outliers.
""")

st.subheader("Key Observations")

price_summary = (
    price_df.groupby("genre")["price"]
    .agg(["median", "mean", "count"])
    .sort_values("median", ascending=False)
)

if not price_summary.empty:

    highest_genre = price_summary.index[0]
    highest_median = price_summary.iloc[0]["median"]

    lowest_genre = price_summary.index[-1]
    lowest_median = price_summary.iloc[-1]["median"]

    st.markdown(
        f"""
- **{highest_genre}** has the highest median
  price among the displayed genres, at
  **£{highest_median:.2f}**.
- **{lowest_genre}** has the lowest median
  price, at **£{lowest_median:.2f}**.
- Some genres show wide price distributions,
  indicating substantial differences between
  inexpensive and premium-priced games.
- Removing free games changes the distribution
  and may change the median price rankings.
"""
    )

st.caption(
    "Source: Steam Store Games dataset by Nik Davis "
    "(Kaggle), approximately 2019. Prices are "
    "recorded in GBP. Games may belong to "
    "multiple genres. Price filters exclude "
    "games outside the selected range."
)

st.markdown(
    "[View dataset source]"
    "(https://www.kaggle.com/datasets/nikdavis/steam-store-games)"
)


# -----------------------------------------
# CHART 5: STEAM GAME RELEASES OVER TIME
# -----------------------------------------
st.divider()

st.header("5. Steam Game Releases Over Time")

st.subheader(
    "How has the number of games released "
    "on Steam changed over time?"
)

st.write("""
This line chart examines the number of Steam
games released each year.

Use the year range slider to explore different
periods and identify changes in release activity.
""")

release_summary = (
    df.dropna(subset=["release_year"])
    .groupby("release_year")
    .agg(game_count=("appid", "nunique"))
    .reset_index()
    .sort_values("release_year")
)

release_summary["release_year"] = (
    release_summary["release_year"].astype(int)
)

min_year = int(release_summary["release_year"].min())
max_year = int(release_summary["release_year"].max())

year_range = st.slider(
    "Select release year range",
    min_value=min_year,
    max_value=max_year,
    value=(2005, max_year),
    key="release_year_range"
)

filtered_releases = release_summary[
    release_summary["release_year"].between(
        year_range[0],
        year_range[1]
    )
].copy()

fig5 = px.line(
    filtered_releases,
    x="release_year",
    y="game_count",
    markers=True,
    title="Number of Steam Games Released Each Year",
    labels={
        "release_year": "Release Year",
        "game_count": "Number of Games Released"
    },
    color_discrete_sequence=["#0072B2"]
)

fig5.update_traces(
    line=dict(width=3),
    marker=dict(size=7),
    hovertemplate=(
        "Year: %{x}<br>"
        "Games Released: %{y:,}"
        "<extra></extra>"
    )
)

fig5.update_layout(
    height=500,
    hovermode="x unified",
    xaxis=dict(
        dtick=1,
        tickformat="d"
    ),
    yaxis=dict(
        rangemode="tozero",
        tickformat=","
    )
)

if not filtered_releases.empty:
    peak = filtered_releases.loc[
        filtered_releases["game_count"].idxmax()
    ]

    fig5.add_annotation(
        x=peak["release_year"],
        y=peak["game_count"],
        text="Highest count in selected period",
        showarrow=True,
        arrowhead=2,
        ax=-90,
        ay=-45
    )

st.plotly_chart(
    fig5,
    use_container_width=True
)

st.subheader("How to Read This Chart")

st.markdown("""
- **X-axis:** Shows the year in which games
  were released.
- **Y-axis:** Shows the number of games in
  the dataset released during each year.
- **Blue line and markers:** Connect annual
  counts to show changes over time. Hover
  over a marker to view the exact count.
""")

st.subheader("Key Observations")

if not filtered_releases.empty:

    peak_year = int(peak["release_year"])
    peak_count = int(peak["game_count"])

    first_row = filtered_releases.iloc[0]
    last_row = filtered_releases.iloc[-1]

    st.markdown(
        f"""
- **{peak_year}** has the highest number of
  recorded releases within the selected
  period, with **{peak_count:,} games**.
- The dataset records
  **{int(first_row['game_count']):,} games**
  in {int(first_row['release_year'])}
  and **{int(last_row['game_count']):,} games**
  in {int(last_row['release_year'])}.
- Annual release counts increased substantially
  during the mid-to-late 2010s.
- **2019 is incomplete** because the dataset
  ends on May 1, 2019. Its count should not
  be compared with full years as evidence
  of a decline.
"""
    )

st.caption(
    "Source: Steam Store Games dataset by Nik Davis "
    "(Kaggle). Historical records through "
    "May 1, 2019. Counts represent games "
    "included in this dataset, not necessarily "
    "all Steam releases."
)

st.markdown(
    "[View dataset source]"
    "(https://www.kaggle.com/datasets/nikdavis/steam-store-games)"
)
