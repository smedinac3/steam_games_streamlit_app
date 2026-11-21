import streamlit as st

st.set_page_config(
    page_title="SteamScope | Future Work",
    layout="wide"
)

st.title("Future Work")

st.write("""
SteamScope Analytics currently provides
interactive visualizations of Steam game
trends using a March 2025 dataset.

Several improvements could make the
application more informative, accurate,
and useful for future analysis.
""")
st.divider()

st.header("Improvements")

with st.expander(
    "1. More Recent and Automatically Updated Data",
    expanded=True
):

    st.write("""
    The current application uses a static
    March 2025 dataset.

    A future version could retrieve updated
    game information from a maintained data
    source or supported API.

    This would allow users to explore
    changes in Steam games over time
    without manually replacing the CSV.
    """)

with st.expander(
    "2. Improved Financial Analysis"
):

    st.write("""
    A future version could verify price
    currencies and historical pricing
    information.

    Additional analysis could compare
    price distributions, discounts, and
    potential revenue scenarios.

    Revenue estimates would require
    careful assumptions because ownership
    estimates do not represent verified
    purchases.
    """)

with st.expander(
    "3. More Advanced Interactive Filters"
):

    st.write("""
    The dashboard could include additional
    filters for developers, publishers,
    review counts, and estimated ownership.

    Users could also compare selected games
    or genres side by side.
    """)

with st.expander(
    "4. Time-Based Player Popularity Analysis"
):

    st.write("""
    Future research could examine concurrent
    player counts and changes in popularity
    across different release periods.

    Historical player-count data would be
    needed to analyze actual player trends
    over time.
    """)

with st.expander(
    "5. Improved Data Quality and Accessibility"
):

    st.write("""
    Future development could include more
    automated data validation, clearer
    uncertainty indicators, and additional
    accessible chart descriptions.

    These improvements would make the
    dashboard more reliable and easier
    for different audiences to use.
    """)
st.divider()

st.header("Development Roadmap")

roadmap = [
    {
        "Phase": "Phase 1",
        "Goal": "Interactive Steam dashboard",
        "Status": "Implemented"
    },
    {
        "Phase": "Phase 2",
        "Goal": "Improve data validation and currency documentation",
        "Status": "Planned"
    },
    {
        "Phase": "Phase 3",
        "Goal": "Add additional filters and comparisons",
        "Status": "Planned"
    },
    {
        "Phase": "Phase 4",
        "Goal": "Integrate newer data sources",
        "Status": "Future"
    }
]

st.dataframe(
    roadmap,
    use_container_width=True,
    hide_index=True
)
st.divider()

st.header("Final Reflection")

st.write("""
Developing SteamScope Analytics demonstrates
how data analysis and visualization can
transform a large dataset into an interactive
research experience.

The project also highlights the importance
of understanding data limitations, selecting
appropriate charts, and communicating
results responsibly.

Future improvements would focus on making
the application more current, interactive,
and transparent.
""")

st.caption(
    "SteamScope Analytics | "
    "Data Visualization Portfolio Project"
)
