
import pandas as pd
import streamlit as st
from pathlib import Path


@st.cache_data
def load_data():

    file_path = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "steam_2025_prepared.csv"
    )

    df = pd.read_csv(file_path)

    df["release_date"] = pd.to_datetime(
        df["release_date"],
        errors="coerce"
    )

    df["release_year"] = (
        df["release_date"].dt.year
    )

    df["genres"] = df["genres"].fillna("")

    df["pricing_model"] = df["price"].apply(
        lambda price: "Free" if price == 0 else "Paid"
    )

    df["total_ratings"] = (
        df["positive_ratings"]
        + df["negative_ratings"]
    )

    df["positive_rating_pct"] = (
        df["positive_ratings"]
        / df["total_ratings"].replace(
            0, float("nan")
        )
        * 100
    )

    ownership = df["owners"].str.split(
        "-",
        expand=True
    )

    lower_bound = pd.to_numeric(
        ownership[0].str.strip(),
        errors="coerce"
    )

    upper_bound = pd.to_numeric(
        ownership[1].str.strip(),
        errors="coerce"
    )

    df["estimated_owners"] = (
        lower_bound + upper_bound
    ) / 2
    
    return df
