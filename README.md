# SteamScope Analytics

### Interactive Steam Game Market & Player Trends Dashboard

SteamScope Analytics is an interactive data visualization application built with **Python, Pandas, Plotly, and Streamlit**.

The project explores Steam game releases, pricing, genre popularity, estimated ownership, and player ratings using a dataset snapshot from March 2025.

Its purpose is to transform a large gaming dataset into understandable visualizations that help users explore patterns, compare categories, and investigate relationships.

---
## Live Application

[Open SteamScope Analytics](https://steamgamesappapp-y6d35miu8b7lkercj8uwhy.streamlit.app/)
## Research Questions

SteamScope Analytics investigates five primary questions:

1. Do free and paid Steam games receive different percentages of positive player ratings?
2. Which Steam game genres have the highest estimated ownership?
3. Which genres receive the highest percentages of positive player ratings?
4. How do game prices vary across different genres?
5. How has the number of Steam game releases changed over time?

The interactive Dashboard also allows users to explore these relationships using shared filters.

## Application Features

### Home Page

Introduces the project, its research questions, and the dataset.

Includes dataset statistics and a preview of the data.

### Bio Page

Introduces the developer, technical skills, and learning outcomes.

Explains the motivation behind SteamScope Analytics.

### EDA Gallery

Contains five interactive visualizations:

| Visualization | Chart Type | Purpose |
|---|---|---|
| Free vs. Paid Ratings | Grouped bar chart | Compare positive and negative rating shares |
| Estimated Ownership by Genre | Horizontal bar chart | Compare genre ownership estimates |
| Positive Ratings by Genre | Dot plot | Examine rating percentages and genre sizes |
| Game Prices by Genre | Box plot | Explore price distributions and outliers |
| Steam Releases Over Time | Line chart | Identify annual release trends |

The gallery includes interactive filters, explanations, observations, and source information.

### Interactive Dashboard

The Dashboard combines shared filters with reactive KPIs and linked visualizations.

**Sidebar filters:**
- Game genres
- Pricing model (Free or Paid)
- Release-year range

**Key performance indicators:**
- Total games
- Average game price
- Positive rating share
- Summed estimated ownership

**Linked visualizations:**
- Top genres by game count
- Positive rating share by release year

An expandable data explorer allows visitors to inspect the filtered game records.

### Future Work

Discusses possible improvements, including updated datasets, verified pricing information, additional filters, player popularity analysis, and accessibility enhancements.

---

## Dataset

**Dataset:** Steam Games Dataset  
**Source:** ArterMiloff on Kaggle  
**Snapshot:** March 2025  
**Prepared dataset:** `steam_2025_prepared.csv`

[View the original dataset on Kaggle](https://www.kaggle.com/datasets/artermiloff/steam-games-dataset)

The prepared dataset contains approximately **89,618 game records**.

Important variables include:

| Column | Description |
|---|---|
| `appid` | Unique Steam application identifier |
| `name` | Game title |
| `release_date` | Game release date |
| `genres` | Associated game genres |
| `price` | Recorded game price |
| `positive_ratings` | Number of positive ratings |
| `negative_ratings` | Number of negative ratings |
| `owners` | Estimated ownership range |
| `peak_ccu` | Recorded peak concurrent users |

Additional derived variables include release year, pricing model, total ratings, positive rating percentage, and estimated ownership midpoint.

## Technologies Used

- **Python:** Data processing and application development
- **Pandas:** Data cleaning, transformation, and aggregation
- **Plotly Express:** Interactive visualizations
- **Streamlit:** Web application and dashboard interface
- **GitHub:** Version control and project hosting
- **Streamlit Community Cloud:** Application deployment

## Project Structure

```text
steam_games_streamlit_app/
│
├── app.py
├── requirements.txt
├── README.md
│
├── assets/
│   └── profile.png
│
├── data/
│   ├── steam.csv
│   └── steam_2025_prepared.csv
│
├── utils/
│   └── data_loader.py
│
└── pages/
    ├── 1_Bio.py
    ├── 2_EDA_Gallery.py
    ├── 3_Dashboard.py
    └── 4_Future_Work.py
```

The structure above represents the intended application organization. Optional files may differ in the final repository.

## How to Run the Application

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/steam_games_streamlit_app.git
```

Replace `smedinac3` with the actual GitHub username.

### 2. Open the project folder

```bash
cd steam_games_streamlit_app
```

### 3. Install the required libraries

```bash
python -m pip install -r requirements.txt
```

### 4. Launch the application

```bash
python -m streamlit run app.py
```

Streamlit will display a local address in the terminal, typically:

`http://localhost:8501`

Open that address in a browser to explore the application.

**Note:** The prepared dataset must be available in the `data` folder for the application to run.

## Data Processing

The application uses a shared data-loading function in `utils/data_loader.py`.

The loader performs several transformations:

1. Reads the prepared March 2025 CSV file.
2. Converts release dates into datetime values.
3. Extracts release years.
4. Categorizes games as Free or Paid.
5. Calculates total recorded ratings.
6. Calculates positive rating percentages.
7. Estimates ownership using the midpoint of each ownership range.

Streamlit's caching system helps avoid repeatedly loading and processing the dataset unnecessarily.

## Data Limitations and Ethical Considerations

Several limitations affect how the visualizations should be interpreted.

**Estimated ownership:** Ownership ranges are approximations and should not be treated as verified sales or unique-player counts.

**Overlapping genres:** A game may belong to multiple genres, so aggregated genre totals can overlap.

**Player ratings:** Recorded ratings do not necessarily represent all players. Games with more reviews have greater influence on aggregated rating percentages.

**Currency uncertainty:** The prepared dataset's price currency has not been independently verified. Prices are therefore described using dataset units.

**Partial-year data:** The March 2025 snapshot does not contain a complete year of 2025 releases.

**Correlation versus causation:** Differences in ratings, ownership, or pricing between categories do not establish causal relationships.

The application uses chart labels, explanations, hover details, and written limitations to encourage responsible interpretation.

## Future Improvements

Potential improvements include:

- Integrating more recent Steam game data.
- Verifying currencies and adding historical price comparisons.
- Expanding filters for developers, publishers, and player activity.
- Comparing individual games and genres side by side.
- Adding historical concurrent-player trends.
- Improving automated data validation and accessibility.

## Learning Outcomes

Through this project, I practiced:

- Cleaning and preparing real-world data.
- Performing exploratory data analysis.
- Selecting appropriate chart types.
- Creating interactive Plotly visualizations.
- Developing responsive Streamlit dashboards.
- Communicating findings and limitations.
- Managing a project through GitHub.
- Deploying an interactive Python application.

## AI Assistance & Acknowledgments

This project used **ChatGPT (OpenAI)** as an educational and development resource.

**AI Tool:** ChatGPT by OpenAI  
**Website:** https://chatgpt.com  
**Model:** GPT-6  
**Project Development:** 2026

## Data Attribution

Steam Games Dataset by ArterMiloff, available through Kaggle:

https://www.kaggle.com/datasets/artermiloff/steam-games-dataset

This project is an educational data visualization portfolio and is not affiliated with Valve or Steam.
