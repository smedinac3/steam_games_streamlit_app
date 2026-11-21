import pandas as pd
import plotly.express as px
import streamlit as st
from utils.data_loader import load_data

st.set_page_config(
    page_title="SteamScope | Dashboard",
    layout="wide"
)

# -----------------------------------------
# DASHBOARD HEADER
# -----------------------------------------
st.title("SteamScope Analytics")

st.markdown(
    "### Steam Game Market & Player Trends"
)

st.write(
    "An interactive exploration of Steam games, "
    "genre popularity, pricing, and player ratings "
    "using a March 2025 dataset snapshot."
)

st.info(
    "Use the sidebar filters to explore "
    "different genres, pricing models, and "
    "release periods. All dashboard metrics "
    "and visualizations update automatically."
)

st.caption(
    "Dataset: Steam Games Dataset | "
    "Snapshot: March 2025"
)

df = load_data().copy()

df["price"] = pd.to_numeric(
    df["price"], errors="coerce"
)

df["positive_ratings"] = pd.to_numeric(
    df["positive_ratings"], errors="coerce"
).fillna(0)

df["negative_ratings"] = pd.to_numeric(
    df["negative_ratings"], errors="coerce"
).fillna(0)

df["estimated_owners"] = pd.to_numeric(
    df["estimated_owners"], errors="coerce"
)

df["release_year"] = pd.to_numeric(
    df["release_year"], errors="coerce"
)

df["genres"] = df["genres"].fillna("")

df["genre_list"] = df["genres"].apply(
    lambda value: [
        genre.strip()
        for genre in value.split(";")
        if genre.strip()
    ]
)

st.sidebar.header("Dashboard Filters")

all_genres = sorted({
    genre
    for genres in df["genre_list"]
    for genre in genres
})

selected_genres = st.sidebar.multiselect(
    "Select game genres",
    options=all_genres,
    default=[],
    help="Leave empty to include every genre."
)

selected_pricing = st.sidebar.multiselect(
    "Pricing model",
    options=["Free", "Paid"],
    default=["Free", "Paid"]
)

valid_years = df["release_year"].dropna()

min_year = int(valid_years.min())
max_year = int(valid_years.max())

selected_years = st.sidebar.slider(
    "Release year range",
    min_value=min_year,
    max_value=max_year,
    value=(max(min_year, 2010), max_year),
    step=1
)

st.sidebar.caption(
    "All charts and KPIs respond to "
    "the selected filters."
)

filtered_df = df.copy()

if selected_genres:
    filtered_df = filtered_df[
        filtered_df["genre_list"].apply(
            lambda genres: any(
                genre in genres
                for genre in selected_genres
            )
        )
    ]

filtered_df = filtered_df[
    filtered_df["pricing_model"].isin(
        selected_pricing
    )
]

filtered_df = filtered_df[
    filtered_df["release_year"].between(
        selected_years[0],
        selected_years[1]
    )
]

st.subheader("Key Performance Indicators (KPI)")

game_count = filtered_df["appid"].nunique()

average_price = filtered_df["price"].mean()

positive_total = filtered_df[
    "positive_ratings"
].sum()

negative_total = filtered_df[
    "negative_ratings"
].sum()

total_ratings = positive_total + negative_total

positive_share = (
    positive_total / total_ratings * 100
    if total_ratings > 0
    else None
)

estimated_ownership = filtered_df[
    "estimated_owners"
].sum(min_count=1)


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Games",
        value=f"{game_count:,}",
        help=(
            "Number of distinct Steam games "
            "matching the selected filters."
        )
    )

with col2:
    st.metric(
        label="Average Game Price",
        value=(
            f"{average_price:,.2f}"
            if pd.notna(average_price)
            else "N/A"
        ),
        help=(
            "Average recorded game price in "
            "dataset units. Currency is not "
            "yet independently verified."
        )
    )

with col3:
    st.metric(
        label="Positive Rating Share",
        value=(
            f"{positive_share:.1f}%"
            if positive_share is not None
            else "N/A"
        ),
        help=(
            "Percentage of recorded ratings "
            "that are positive, calculated "
            "from total rating counts."
        )
    )

with col4:
    st.metric(
        label="Estimated Ownership",
        value=(
            f"{estimated_ownership / 1e9:.2f}B"
            if pd.notna(estimated_ownership)
            else "N/A"
        ),
        help=(
            "Sum of ownership-range midpoints "
            "across selected games. This is "
            "not a count of unique players."
        )
    )

st.caption(
    "Prices are in unverified dataset units. "
    "Ownership values are estimates summed "
    "across games, not unique people."
)

st.divider()

st.subheader("Exploring the Filtered Data")

if filtered_df.empty:
    st.warning(
        "No games match the selected filters. "
        "Try changing the genre, pricing, "
        "or release-year selections."
    )

else:
    chart_col1, chart_col2 = st.columns(2)

    genre_chart_df = filtered_df[
        ["appid", "genre_list"]
    ].explode("genre_list")

    genre_chart_df = genre_chart_df.dropna(
        subset=["genre_list"]
    )

    genre_counts = (
        genre_chart_df.groupby(
            "genre_list",
            as_index=False
        )
        .agg(
            game_count=("appid", "nunique")
        )
        .sort_values(
            "game_count",
            ascending=False
        )
        .head(10)
    )

    with chart_col1:

        st.markdown(
            "#### Top 10 Genres by Game Count"
        )

        if genre_counts.empty:
            st.info(
                "No genre information is "
                "available for this selection."
            )
        else:
            fig_genres = px.bar(
                genre_counts,
                x="game_count",
                y="genre_list",
                orientation="h",
                color="game_count",
                color_continuous_scale="Blues",
                labels={
                    "game_count": "Number of Games",
                    "genre_list": "Genre"
                }
            )

            fig_genres.update_layout(
                yaxis={
                    "categoryorder": "total ascending"
                },
                coloraxis_showscale=False,
                height=480,
                margin=dict(
                    l=10, r=10, t=20, b=40
                )
            )

            st.plotly_chart(
                fig_genres,
                use_container_width=True
            )

    yearly_ratings = (
        filtered_df.dropna(
            subset=["release_year"]
        )
        .groupby(
            "release_year",
            as_index=False
        )
        .agg(
            positive=("positive_ratings", "sum"),
            negative=("negative_ratings", "sum"),
            game_count=("appid", "nunique")
        )
    )

    yearly_ratings["total_ratings"] = (
        yearly_ratings["positive"]
        + yearly_ratings["negative"]
    )

    yearly_ratings["positive_pct"] = (
        yearly_ratings["positive"]
        / yearly_ratings[
            "total_ratings"
        ].replace(0, float("nan"))
        * 100
    )

    yearly_ratings = yearly_ratings.dropna(
        subset=["positive_pct"]
    )

    with chart_col2:

        st.markdown(
            "#### Positive Rating Share by Year"
        )

        if yearly_ratings.empty:
            st.info(
                "No rating data is available "
                "for this selection."
            )
        else:
            fig_ratings = px.line(
                yearly_ratings,
                x="release_year",
                y="positive_pct",
                markers=True,
                labels={
                    "release_year": "Release Year",
                    "positive_pct": (
                        "Positive Rating Share (%)"
                    )
                },
                hover_data={
                    "game_count": True,
                    "total_ratings": ":,"
                }
            )

            fig_ratings.update_traces(
                line=dict(
                    color="#0072B2",
                    width=3
                ),
                marker=dict(size=7)
            )

            fig_ratings.update_layout(
                yaxis=dict(
                    range=[0, 100],
                    ticksuffix="%"
                ),
                xaxis=dict(
                    tickformat="d"
                ),
                height=480,
                margin=dict(
                    l=10, r=10, t=20, b=40
                )
            )

            st.plotly_chart(
                fig_ratings,
                use_container_width=True
            )

st.caption(
    "Both charts respond to the same sidebar "
    "filters. Genre counts may overlap because "
    "games can belong to multiple genres. "
    "Rating percentages are weighted by "
    "recorded review counts."
)

# -----------------------------------------
# FILTERED DATA EXPLORER
# -----------------------------------------
st.divider()

with st.expander("Explore Filtered Game Data"):

    st.write(
        "View the games currently included "
        "in your dashboard filters."
    )

    display_columns = [
        "name",
        "release_year",
        "genres",
        "pricing_model",
        "price",
        "positive_rating_pct",
        "estimated_owners"
    ]

    game_table = filtered_df[
        display_columns
    ].copy()

    game_table = game_table.rename(
        columns={
            "name": "Game",
            "release_year": "Release Year",
            "genres": "Genres",
            "pricing_model": "Pricing Model",
            "price": "Price (Dataset Units)",
            "positive_rating_pct": "Positive Rating (%)",
            "estimated_owners": "Estimated Owners"
        }
    )

    st.dataframe(
        game_table,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Positive Rating (%)": st.column_config.NumberColumn(
                format="%.1f%%"
            ),
            "Estimated Owners": st.column_config.NumberColumn(
                format="%,.0f"
            )
        }
    )

    st.caption(
        f"Displaying {len(game_table):,} "
        "games matching the current filters."
    )

st.divider()

st.subheader("Dashboard Insights")

if not filtered_df.empty:

    free_count = int(
        (filtered_df["pricing_model"] == "Free").sum()
    )

    paid_count = int(
        (filtered_df["pricing_model"] == "Paid").sum()
    )

    st.markdown(
        f"""
1. **Game availability:** The selected
   filters include **{game_count:,} games**.

2. **Pricing models:** The selection contains
   **{free_count:,} free games** and
   **{paid_count:,} paid games**.

3. **Player ratings:** The overall positive
   rating share is
   **{f'{positive_share:.1f}%' if positive_share is not None else 'unavailable'}**.

4. **Genre popularity:** Games may belong
   to multiple genres, so genre counts
   overlap.

5. **Release trends:** The annual rating
   chart shows how recorded player ratings
   vary by game release year, not when
   those reviews were posted.
"""
    )

else:
    st.info(
        "Select a broader set of filters "
        "to generate dashboard insights."
    )

st.subheader("Note: Data Limitations")

st.markdown("""
- **Ownership:** Estimated ownership ranges
  are approximations, not verified sales
  or counts of unique players.
- **Genre overlap:** Games can appear in
  several genres.
- **Rating bias:** Review counts differ
  substantially between games. Ratings
  may not represent all players.
- **Currency:** The dataset's price currency
  has not been independently verified.
- **Coverage:** The March 2025 snapshot
  does not represent every game released
  after its collection date.
- **Partial year:** 2025 is incomplete
  and should not be directly compared
  with full calendar years.
""")

st.caption(
    "Chart labels, hover details, and "
    "written explanations supplement color "
    "to support accessible interpretation."
)

st.markdown(
    "**Dataset source:** "
    "[Steam Games Dataset — ArterMiloff]"
    "(https://www.kaggle.com/datasets/artermiloff/steam-games-dataset)"
)
