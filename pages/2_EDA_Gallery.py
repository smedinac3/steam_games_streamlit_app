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
    "Which Steam game genres have the "
    "highest estimated ownership?"
)

st.write("""
This chart compares summed estimated ownership
across Steam game genres using the March 2025
dataset.

Ownership estimates are calculated from
SteamSpy-style ownership ranges.
""")

genre_df = df.copy()

genre_df["genre"] = genre_df["genres"].str.split(";")

genre_df = genre_df.explode("genre")

genre_df["genre"] = genre_df["genre"].str.strip()

genre_df = genre_df[
    genre_df["genre"].notna()
    & (genre_df["genre"] != "")
]

genre_summary = (
    genre_df.groupby("genre", as_index=False)
    .agg(
        estimated_owners=("estimated_owners", "sum"),
        game_count=("appid", "nunique")
    )
    .sort_values(
        "estimated_owners",
        ascending=False
    )
)

top_n = st.slider(
    "Number of genres to display",
    min_value=5,
    max_value=20,
    value=10,
    step=1,
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
    title="Estimated Steam Game Ownership by Genre",
    labels={
        "estimated_owners": "Summed Estimated Owners",
        "genre": "Game Genre"
    },
    hover_data={
        "estimated_owners": ":,.0f",
        "game_count": ":,",
        "genre": False
    }
)

fig2.update_layout(
    yaxis={
        "categoryorder": "total ascending"
    },
    coloraxis_showscale=False,
    xaxis_tickformat="~s",
    height=max(480, top_n * 42)
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

st.subheader("Reading This Chart")

st.markdown("""
- **Y-axis:** Lists Steam game genres, ordered
  from highest to lowest estimated ownership.
- **X-axis:** Shows the sum of estimated
  ownership across games in each genre.
- **Bar length and color:** Longer, darker bars
  represent larger estimated ownership totals.
  Hover to see exact values and game counts.
""")

st.subheader("Key Observations")

highest = top_genres.iloc[0]

most_games = top_genres.loc[
    top_genres["game_count"].idxmax()
]

st.markdown(
    f"""
- **{highest['genre']}** has the highest
  summed estimated ownership, at approximately
  **{highest['estimated_owners'] / 1e9:.2f}
  billion**.
- **{most_games['genre']}** has the most
  games among the displayed genres, with
  **{int(most_games['game_count']):,} games**.
- The genre with the most games does not
  necessarily have the highest estimated
  ownership.
- Games can belong to multiple genres,
  so ownership totals overlap between
  categories.
"""
)

st.caption(
    "Source: Steam Games Dataset, March 2025 "
    "(ArterMiloff, Kaggle). Ownership values "
    "are approximated using range midpoints. "
    "Genre totals may overlap and do not "
    "represent unique players or sales."
)

st.markdown(
    "[View dataset source]"
    "(https://www.kaggle.com/datasets/artermiloff/steam-games-dataset)"
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
This interactive dot plot compares positive
rating percentages across Steam game genres.

Use the filters to explore how genre rankings
change when smaller categories are excluded.
""")

ratings_genre_df = df.copy()

ratings_genre_df["genre"] = (
    ratings_genre_df["genres"].fillna("").str.split(";")
)

ratings_genre_df = ratings_genre_df.explode("genre")

ratings_genre_df["genre"] = (
    ratings_genre_df["genre"].str.strip()
)

ratings_genre_df = ratings_genre_df[
    ratings_genre_df["genre"].notna()
    & (ratings_genre_df["genre"] != "")
]

genre_ratings = (
    ratings_genre_df.groupby("genre", as_index=False)
    .agg(
        positive=("positive_ratings", "sum"),
        negative=("negative_ratings", "sum"),
        game_count=("appid", "nunique")
    )
)

genre_ratings["total_ratings"] = (
    genre_ratings["positive"]
    + genre_ratings["negative"]
)

genre_ratings["positive_pct"] = (
    genre_ratings["positive"]
    / genre_ratings["total_ratings"].replace(
        0, float("nan")
    )
    * 100
)

min_games = st.slider(
    "Minimum number of games per genre",
    min_value=1,
    max_value=10000,
    value=1000,
    step=100,
    key="genre_rating_min_games"
)

include_software = st.checkbox(
    "Include software-related categories",
    value=False,
    key="include_software_genres"
)

software_genres = [
    "Photo Editing",
    "Animation & Modeling",
    "Design & Illustration",
    "Utilities",
    "Audio Production",
    "Video Production",
    "Game Development",
    "Education",
    "Software Training"
]

filtered_ratings = genre_ratings[
    (genre_ratings["game_count"] >= min_games)
    & (genre_ratings["total_ratings"] > 0)
].copy()

if not include_software:
    filtered_ratings = filtered_ratings[
        ~filtered_ratings["genre"].isin(
            software_genres
        )
    ]

filtered_ratings = filtered_ratings.sort_values(
    "positive_pct",
    ascending=False
)

fig3 = px.scatter(
    filtered_ratings,
    x="positive_pct",
    y="genre",
    size="game_count",
    color="positive_pct",
    size_max=32,
    color_continuous_scale="Viridis",
    title="Positive Rating Percentage by Steam Genre",
    labels={
        "positive_pct": "Positive Ratings (%)",
        "genre": "Game Genre",
        "game_count": "Number of Games"
    },
    hover_data={
        "positive_pct": ":.2f",
        "game_count": ":,",
        "total_ratings": ":,",
        "positive": ":,",
        "negative": ":,"
    }
)


min_rating = filtered_ratings["positive_pct"].min()
max_rating = filtered_ratings["positive_pct"].max()

x_min = max(0, min_rating - 5)
x_max = min(100, max_rating + 5)

fig3.update_layout(
    xaxis=dict(
        range=[x_min, x_max],
        title="Positive Ratings (%)",
        ticksuffix="%",
        showgrid=True
    ),
    yaxis=dict(
        categoryorder="array",
        categoryarray=filtered_ratings[
            "genre"
        ].tolist()[::-1],
        title="Game Genre"
    ),
    coloraxis_showscale=False,
    height=max(450, len(filtered_ratings) * 35),
    margin=dict(l=40, r=30, t=60, b=40)
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

st.subheader("Reading This Chart")

st.markdown("""
- **X-axis:** Shows the percentage of
  recorded ratings that are positive.
- **Y-axis:** Lists game genres, sorted
  from highest to lowest positive rating share.
- **Dots:** Larger dots represent more games.
  Dot color represents rating percentage.
  Hover to inspect exact values.
""")

st.subheader("Key Observations")

if not filtered_ratings.empty:

    highest = filtered_ratings.iloc[0]
    lowest = filtered_ratings.iloc[-1]

    difference = (
        highest["positive_pct"]
        - lowest["positive_pct"]
    )

    st.markdown(
        f"""
- **{highest['genre']}** has the highest
  positive rating share among displayed
  genres, at **{highest['positive_pct']:.2f}%**.
- **{lowest['genre']}** has the lowest
  displayed positive rating share,
  at **{lowest['positive_pct']:.2f}%**.
- The difference between the highest and
  lowest displayed values is
  **{difference:.2f} percentage points**.
- Changing the minimum game count or
  including software categories can
  change the rankings.
"""
    )

else:
    st.info(
        "No genres meet the selected criteria. "
        "Try lowering the minimum game count."
    )

st.caption(
    "Source: Steam Games Dataset, March 2025 "
    "(ArterMiloff, Kaggle). Percentages use "
    "aggregated rating counts. Genres overlap, "
    "and heavily reviewed games contribute "
    "more to each percentage. Ratings do not "
    "establish game quality or causation."
)

st.markdown(
    "[View dataset source]"
    "(https://www.kaggle.com/datasets/artermiloff/steam-games-dataset)"
)

# -----------------------------------------
# CHART 4: GAME PRICES BY GENRE
# -----------------------------------------
st.divider()

st.header("4. Game Prices by Genre")

st.subheader(
    "How do Steam game prices vary "
    "across different genres?"
)

st.write("""
This interactive box plot compares game
price distributions across Steam genres.

Use the controls to explore the median,
interquartile range, and potential outliers.
""")

price_df = df.copy()

price_df["price"] = pd.to_numeric(
    price_df["price"],
    errors="coerce"
)

price_df = price_df[
    price_df["price"].notna()
    & (price_df["price"] >= 0)
].copy()

price_df["genre"] = (
    price_df["genres"].fillna("").str.split(";")
)

price_df = price_df.explode("genre")

price_df["genre"] = price_df["genre"].str.strip()

price_df = price_df[
    price_df["genre"].notna()
    & (price_df["genre"] != "")
]

exclude_free = st.checkbox(
    "Exclude free games",
    value=True,
    key="price_exclude_free"
)

show_outliers = st.checkbox(
    "Show individual outlier points",
    value=False,
    key="price_show_outliers"
)

max_available_price = float(
    price_df["price"].max()
)

max_price = st.slider(
    "Maximum game price to include",
    min_value=0.0,
    max_value=max(10.0, max_available_price),
    value=min(100.0, max(10.0, max_available_price)),
    step=1.0,
    key="price_max_slider"
)

filtered_prices = price_df[
    price_df["price"] <= max_price
].copy()

if exclude_free:
    filtered_prices = filtered_prices[
        filtered_prices["price"] > 0
    ]

genre_counts = (
    filtered_prices.groupby("genre")["appid"]
    .nunique()
    .sort_values(ascending=False)
)

top_genre_names = genre_counts.head(12).index

filtered_prices = filtered_prices[
    filtered_prices["genre"].isin(top_genre_names)
].copy()

if not filtered_prices.empty:

    genre_order = (
        filtered_prices.groupby("genre")["price"]
        .median()
        .sort_values(ascending=False)
        .index.tolist()
    )

    fig4 = px.box(
        filtered_prices,
        x="price",
        y="genre",
        orientation="h",
        color="genre",
        points="outliers" if show_outliers else False,
        category_orders={
            "genre": genre_order
        },
        title="Steam Game Price Distribution by Genre",
        labels={
            "price": "Game Price (Dataset Units)",
            "genre": "Game Genre"
        }
    )

    fig4.update_layout(
        showlegend=False,
        height=650,
        margin=dict(
            l=40,
            r=30,
            t=60,
            b=40
        )
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

else:
    st.warning(
        "No games match the selected price filters. "
        "Try increasing the maximum price."
    )

st.subheader("Reading This Chart")

st.markdown("""
- **Middle line inside each box:** Represents
  the median price for that genre.
- **Box boundaries:** Represent the 25th and
  75th percentiles, containing the middle
  50% of prices.
- **Whiskers and outliers:** Show the spread
  of prices and unusually high or low values.
  Hover to inspect the statistics.
""")

st.subheader("Key Observations")

if not filtered_prices.empty:

    price_summary = (
        filtered_prices.groupby("genre")["price"]
        .agg(["median", "mean", "count"])
        .sort_values("median", ascending=False)
    )

    highest_median_genre = price_summary.index[0]
    highest_median = price_summary.iloc[0]["median"]

    lowest_median_genre = price_summary.index[-1]
    lowest_median = price_summary.iloc[-1]["median"]

    st.markdown(
        f"""
- **{highest_median_genre}** has the highest
  median price among the displayed genres,
  at **{highest_median:.2f} dataset units**.
- **{lowest_median_genre}** has the lowest
  median price among the displayed genres,
  at **{lowest_median:.2f} dataset units**.
- Changing the price limit or including
  free games can substantially change
  the price distribution.
- Genres can overlap because individual
  games may belong to multiple categories.
"""
    )

    st.dataframe(
        price_summary.rename(
            columns={
                "median": "Median Price",
                "mean": "Mean Price",
                "count": "Game Count"
            }
        ).round(2),
        use_container_width=True
    )

st.caption(
    "Source: Steam Games Dataset, March 2025 "
    "(ArterMiloff, Kaggle). Price currency "
    "has not been independently verified. "
    "The maximum-price filter excludes games "
    "above the selected threshold, and genres "
    "may overlap."
)

st.markdown(
    "[View dataset source]"
    "(https://www.kaggle.com/datasets/artermiloff/steam-games-dataset)"
)

# -----------------------------------------
# CHART 5: STEAM GAME RELEASES OVER TIME
# -----------------------------------------
st.divider()

st.header("5. Steam Game Releases Over Time")

st.subheader(
    "How has the number of Steam game "
    "releases changed over time?"
)

st.write("""
This interactive line chart shows the number
of games released each year in the March 2025
Steam dataset.

Use the year-range slider to explore release
trends across different periods.
""")

release_df = df.copy()

release_df["release_date"] = pd.to_datetime(
    release_df["release_date"],
    errors="coerce"
)

release_df = release_df.dropna(
    subset=["release_date"]
).copy()

release_df["release_year"] = (
    release_df["release_date"].dt.year
)

yearly_releases = (
    release_df.groupby(
        "release_year",
        as_index=False
    )
    .agg(
        game_count=("appid", "nunique")
    )
    .sort_values("release_year")
)

latest_date = release_df["release_date"].max()

latest_year = int(latest_date.year)

latest_year_is_partial = (
    latest_date.month != 12
    or latest_date.day != 31
)

min_year = int(
    yearly_releases["release_year"].min()
)

max_year = int(
    yearly_releases["release_year"].max()
)

year_range = st.slider(
    "Select release year range",
    min_value=min_year,
    max_value=max_year,
    value=(
        max(min_year, 2010),
        max_year
    ),
    step=1,
    key="release_year_range"
)

filtered_years = yearly_releases[
    yearly_releases["release_year"].between(
        year_range[0],
        year_range[1]
    )
].copy()

fig5 = px.line(
    filtered_years,
    x="release_year",
    y="game_count",
    markers=True,
    title="Annual Steam Game Releases",
    labels={
        "release_year": "Release Year",
        "game_count": "Number of Games"
    }
)

fig5.update_traces(
    line=dict(
        color="#0072B2",
        width=3
    ),
    marker=dict(
        size=8
    ),
    hovertemplate=(
        "Year: %{x}<br>"
        "Games released: %{y:,}"
        "<extra></extra>"
    )
)

fig5.update_layout(
    height=500,
    xaxis=dict(
        dtick=1 if year_range[1] - year_range[0] <= 15 else 2,
        tickformat="d"
    ),
    yaxis=dict(
        rangemode="tozero",
        tickformat=","
    ),
    margin=dict(
        l=40,
        r=40,
        t=70,
        b=50
    )
)

complete_years = filtered_years.copy()

if latest_year_is_partial:
    complete_years = complete_years[
        complete_years["release_year"] < latest_year
    ]

if not complete_years.empty:

    peak_row = complete_years.loc[
        complete_years["game_count"].idxmax()
    ]

    peak_year = int(peak_row["release_year"])
    peak_count = int(peak_row["game_count"])

    fig5.add_annotation(
        x=peak_year,
        y=peak_count,
        text=f"Peak complete year: {peak_year}",
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=-55
    )

if (
    latest_year_is_partial
    and latest_year in filtered_years["release_year"].values
):

    partial_row = filtered_years[
        filtered_years["release_year"] == latest_year
    ].iloc[0]

    fig5.add_annotation(
        x=latest_year,
        y=partial_row["game_count"],
        text="Partial year",
        showarrow=True,
        arrowhead=2,
        ax=-65,
        ay=-45
    )

st.plotly_chart(
    fig5,
    use_container_width=True
)

st.subheader("Reading This Chart")

st.markdown("""
- **X-axis:** Shows the year in which
  Steam games were released.
- **Y-axis:** Shows the number of distinct
  games released during each year.
- **Line and markers:** An upward slope
  indicates more releases than the previous
  displayed year; a downward slope indicates
  fewer releases. Hover for exact counts.
""")

st.subheader("Key Observations")

if not complete_years.empty:

    first_row = complete_years.iloc[0]
    last_row = complete_years.iloc[-1]

    first_year = int(first_row["release_year"])
    last_year = int(last_row["release_year"])

    first_count = int(first_row["game_count"])
    last_count = int(last_row["game_count"])

    st.markdown(
        f"""
- The highest release count among the
  selected complete years occurred in
  **{peak_year}**, with **{peak_count:,} games**.
- In **{first_year}**, the dataset records
  **{first_count:,} releases**.
- In **{last_year}**, the dataset records
  **{last_count:,} releases**.
- The chart allows viewers to examine how
  annual release counts change when different
  time periods are selected.
"""
    )

else:
    st.info(
        "No complete years are included in "
        "the selected range."
    )

if latest_year_is_partial:

    st.warning(
        f"The dataset ends on "
        f"{latest_date.strftime('%B %d, %Y')}. "
        f"Therefore, {latest_year} is a partial "
        "year and should not be directly "
        "compared with complete calendar years."
    )

st.caption(
    "Source: Steam Games Dataset, March 2025 "
    "(ArterMiloff, Kaggle). Counts reflect "
    "games present in the dataset, not "
    "necessarily every game released on Steam. "
    "Missing or invalid release dates are "
    "excluded. Earlier years may also have "
    "incomplete coverage."
)

st.markdown(
    "[View dataset source]"
    "(https://www.kaggle.com/datasets/artermiloff/steam-games-dataset)"
)

st.caption(
    "Data source: Steam Games Dataset by ArterMiloff "
    "(Kaggle). Dataset preparation assisted by "
    "ChatGPT (OpenAI, 2026)."
)
