import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_data

st.set_page_config(
    page_title="Dashboard | SteamScope",
    layout="wide"
)

st.title("Steam Games Analytics Dashboard")

st.write("""
Explore how game genres, prices, player ratings,
and estimated ownership vary across Steam games.

Use the filters to update the dashboard.
""")

df = load_data()

df["genre_list"] = df["genres"].fillna("").str.split(";")

all_genres = sorted({
    genre.strip()
    for genres in df["genre_list"]
    for genre in genres
    if genre.strip()
})

st.sidebar.header("Dashboard Filters")

selected_genres = st.sidebar.multiselect(
    "Select game genres",
    options=all_genres,
    default=[],
    help="Leave empty to include all genres."
)

pricing_filter = st.sidebar.selectbox(
    "Pricing model",
    options=["All Games", "Free", "Paid"]
)

min_year = int(df["release_year"].min())
max_year = int(df["release_year"].max())

selected_years = st.sidebar.slider(
    "Release year range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

filtered_df = df.copy()

if selected_genres:
    filtered_df = filtered_df[
        filtered_df["genre_list"].apply(
            lambda genres: any(
                genre.strip() in selected_genres
                for genre in genres
            )
        )
    ]

if pricing_filter != "All Games":
    filtered_df = filtered_df[
        filtered_df["pricing_model"] == pricing_filter
    ]

filtered_df = filtered_df[
    filtered_df["release_year"].between(
        selected_years[0],
        selected_years[1]
    )
]

st.caption(
    f"Showing {len(filtered_df):,} of {len(df):,} games"
)

if filtered_df.empty:
    st.warning(
        "No games match these filters. "
        "Try selecting a wider range."
    )
    st.stop()

total_games = filtered_df["appid"].nunique()

avg_price = filtered_df["price"].mean()

positive_count = filtered_df["positive_ratings"].sum()

negative_count = filtered_df["negative_ratings"].sum()

total_ratings = positive_count + negative_count

positive_pct = (
    positive_count / total_ratings * 100
    if total_ratings > 0
    else 0
)

estimated_owners = filtered_df[
    "estimated_owners"
].sum()

st.subheader("Key Performance Indicators")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(
        "Total Games",
        f"{total_games:,}"
    )

with kpi2:
    st.metric(
        "Average Price",
        f"£{avg_price:.2f}"
    )

with kpi3:
    st.metric(
        "Positive Ratings",
        f"{positive_pct:.1f}%"
    )

with kpi4:
    st.metric(
        "Summed Est. Owners",
        f"{estimated_owners / 1e6:,.1f}M"
    )

st.caption(
    "Positive rating percentage is weighted by "
    "recorded rating counts. Estimated ownership "
    "is summed across games and does not represent "
    "unique players."
)

st.divider()

chart_df = filtered_df.explode("genre_list").copy()

chart_df["genre"] = (
    chart_df["genre_list"].str.strip()
)

chart_df = chart_df[
    chart_df["genre"].notna()
    & (chart_df["genre"] != "")
]

genre_summary = (
    chart_df.groupby("genre", as_index=False)
    .agg(
        game_count=("appid", "nunique"),
        avg_price=("price", "mean")
    )
    .sort_values(
        "game_count",
        ascending=False
    )
    .head(10)
)

year_summary = (
    filtered_df.dropna(subset=["release_year"])
    .groupby("release_year", as_index=False)
    .agg(
        positive=("positive_ratings", "sum"),
        negative=("negative_ratings", "sum")
    )
)

year_summary["total_ratings"] = (
    year_summary["positive"]
    + year_summary["negative"]
)

year_summary["positive_pct"] = (
    year_summary["positive"]
    / year_summary["total_ratings"].replace(
        0, float("nan")
    )
    * 100
)

st.subheader("Interactive Visualizations")

left, right = st.columns(2)

with left:
    fig_genre = px.bar(
        genre_summary,
        x="game_count",
        y="genre",
        orientation="h",
        title="Top 10 Genres by Game Count",
        labels={
            "game_count": "Number of Games",
            "genre": "Genre"
        },
        color_discrete_sequence=["#0072B2"],
        hover_data={
            "avg_price": ":.2f"
        }
    )

    fig_genre.update_layout(
        yaxis={
            "categoryorder": "total ascending"
        },
        height=480
    )

    st.plotly_chart(
        fig_genre,
        use_container_width=True
    )

with right:
    fig_year = px.line(
        year_summary,
        x="release_year",
        y="positive_pct",
        markers=True,
        title="Positive Rating Share by Release Year",
        labels={
            "release_year": "Release Year",
            "positive_pct": "Positive Ratings (%)"
        },
        color_discrete_sequence=["#E69F00"]
    )

    fig_year.update_layout(
        height=480,
        yaxis_range=[0, 100],
        xaxis=dict(
            dtick=2,
            tickformat="d"
        )
    )

    fig_year.update_traces(
        hovertemplate=(
            "Year: %{x:.0f}<br>"
            "Positive Ratings: %{y:.2f}%"
            "<extra></extra>"
        )
    )

    st.plotly_chart(
        fig_year,
        use_container_width=True
    )

st.caption(
    "Both charts use the same filtered dataset. "
    "Changing any sidebar filter updates both."
)

st.divider()

st.subheader("Dashboard Insights")

if not genre_summary.empty:
    top_genre = genre_summary.iloc[0]

    st.markdown(
        f"- **{top_genre['genre']}** is the most "
        f"common genre in the current selection, "
        f"with {int(top_genre['game_count']):,} games."
    )

st.markdown(
    f"- The average game price in the current "
    f"selection is **£{avg_price:.2f}**."
)

st.markdown(
    f"- **{positive_pct:.1f}%** of recorded "
    f"ratings in the selected games are positive."
)

st.markdown(
    f"- The selection includes **{total_games:,}** "
    f"games released between "
    f"**{selected_years[0]} and "
    f"{selected_years[1]}**."
)

st.markdown("""
- **Limitations:** Ownership figures are
  approximate, genres overlap, and the dataset
  ends in May 2019. These patterns describe
  associations, not causal relationships.
""")

st.divider()

st.subheader("Data Source")

st.markdown(
    "[Steam Store Games — Kaggle]"
    "(https://www.kaggle.com/datasets/nikdavis/steam-store-games)"
)

st.caption(
    "Historical Steam dataset through May 1, 2019. "
    "The app reads the CSV from its GitHub repository. "
    "Changes to filters do not refresh the source data."
)
