import pandas as pd
import streamlit as st
from pathlib import Path


@st.cache_data
def load_data():
    # Locate the CSV file
    file_path = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "steam.csv"
    )

    # Read the dataset
    df = pd.read_csv(file_path)

    # Convert release dates
    df["release_date"] = pd.to_datetime(
        df["release_date"],
        errors="coerce"
    )

    # Create a release year column
    df["release_year"] = df["release_date"].dt.year

    # Identify free-to-play games
    df["pricing_model"] = df["price"].apply(
        lambda price: "Free" if price == 0 else "Paid"
    )

    # Calculate total ratings
    df["total_ratings"] = (
        df["positive_ratings"] +
        df["negative_ratings"]
    )

    # Calculate positive rating percentage
    df["positive_rating_pct"] = (
        df["positive_ratings"]
        / df["total_ratings"].replace(0, float("nan"))
        * 100
    )

    # Convert ownership ranges into estimates
    ownership = df["owners"].str.split(
        "-", expand=True
    )

    df["estimated_owners"] = (
        pd.to_numeric(ownership[0].str.strip())
        + pd.to_numeric(ownership[1].str.strip())
    ) / 2

    return df
