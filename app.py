import streamlit as st
import pandas as pd
import plotly.express as px
<<<<<<< HEAD
from pathlib import Path

# -------------------------
# Page configuration
# -------------------------
st.set_page_config(
    page_title="Income & Obesity Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
    * {font-family: 'Segoe UI', sans-serif;}
    h1, h2, h3, h4 {font-weight: 600;}
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------
# Paths
# -------------------------
BASE = Path("Streamlit")

# Load datasets
us_df = pd.read_csv(BASE / "data/us_health_income_2023.csv")
us_clusters = pd.read_csv(BASE / "results/us_clusters_2023.csv")
us_summary = pd.read_csv(BASE / "results/us_cluster_summary.csv")
global_df = pd.read_csv(BASE / "data/global_merged_obesity_income.csv")

# -------------------------
# Sidebar Navigation
# -------------------------
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to:", ["About the Project", "Obesity Analysis & ML"])

# -------------------------
# About Section
# -------------------------
if section == "About the Project":
    st.title("📘 About the Project")

    st.markdown("""
    ## 1. Research Question
    This study investigates **how per capita income affects health outcomes**, specifically **obesity prevalence**, 
    and whether **physical activity** mediates this relationship.  
    We examine:
    - Do richer U.S. states exhibit lower obesity rates?
    - Does physical activity explain this relationship?
    - How does this relationship differ globally?

    ---

    ## 2. Data Collection
    We combined **economic** and **health** data from official open sources:

    **U.S. Data:**
    - *BEA (Bureau of Economic Analysis)*: State-level annual per capita income (`SAINC1__ALL_AREAS_1929_2024.csv`)
    - *CDC BRFSS*: Health behavior and obesity prevalence (`Behavioral_Risk_Factor_Surveillance_System.csv`)
    - *Physical Activity & Obesity*: Extracted 2023 data on “BMI Categories” and “Physical Activity Index”

    **Global Data:**
    - *World Bank API*: GDP per capita (current US$)
    - *Our World in Data (OWID)*: Obesity prevalence (BMI ≥ 30, 2022)

    All files were stored and synchronized in Google Drive for persistence during Colab sessions:
    `/content/drive/MyDrive/US_ML` → `/content/drive/MyDrive/Streamlit`

    ---

    ## 3. Data Cleaning and Preprocessing
    The workflow was implemented in **Google Colab (Python)**.  
    Libraries used:
    - `pandas` for data handling and merging  
    - `numpy` for numerical transformations  
    - `matplotlib` and `plotly` for visualization  
    - `scikit-learn` for clustering and normalization  

    Key preprocessing steps:
    1. Filtered per capita income from BEA (`Per capita personal income`)
    2. Filtered BRFSS records by “BMI Categories” and “Physical Activity Index”
    3. Averaged multiple state-year records to get one value per state (2023)
    4. Merged datasets on state name (`Locationdesc`)
    5. Normalized features for ML using `StandardScaler()`

    For global analysis, 2022 records were selected and merged by ISO3 country codes.

    ---

    ## 4. Exploratory Data Analysis (EDA)
    We visualized two core relationships:
    - **Income vs. Obesity (U.S. 2023)** — negative linear correlation
    - **Physical Activity vs. Obesity (U.S. 2023)** — negative linear correlation

    These confirmed that higher-income and more-active states exhibit lower obesity prevalence.
    The `numpy.polyfit()` regression line showed a strong downward slope (R² ≈ 0.6).

    Global visualization (using `plotly.express`) of **log(GDP per capita)** vs **obesity rate** revealed a nonlinear “nutrition transition” curve — 
    obesity increases rapidly in low- and middle-income countries but plateaus among the richest economies.

    ---

    ## 5. Machine Learning Model
    We applied **K-Means Clustering** (`sklearn.cluster.KMeans`) on standardized variables:
    - Per Capita Income
    - Obesity Rate
    - Physical Activity Rate

    Using `n_clusters = 3`, states grouped into:
    1. **High Income / Low Obesity / High Activity**
    2. **Mid Income / Moderate Obesity / Moderate Activity**
    3. **Low Income / High Obesity / Low Activity**

    Cluster results were mapped via Plotly’s `choropleth` for an interactive U.S. heatmap.

    ---

    ## 6. Findings & Interpretation
    **U.S. Findings:**
    - A strong inverse correlation between income and obesity (wealthier = healthier)
    - States with higher activity levels had significantly lower obesity
    - The clustering model separated regions clearly along economic-health lines

    **Global Findings:**
    - Worldwide, obesity rises with GDP per capita up to a middle-income threshold
    - At very high incomes, obesity stabilizes or slightly declines (reflecting health awareness and better diets)
    - This difference demonstrates the *nutrition transition theory*: as countries industrialize, obesity grows before plateauing

    ---

    ## 7. Tools and Libraries
    - **Python** (Google Colab)
    - **pandas**, **numpy**, **plotly**, **matplotlib**
    - **scikit-learn** (StandardScaler, KMeans)
    - **World Bank API**, **OWID**, **CDC BRFSS**
    - **Streamlit** for deployment and visualization

    ---

    ## 8. Conclusion
    - In the U.S., **income and physical activity** strongly predict obesity outcomes.  
    - Globally, **income–obesity dynamics are nonlinear**, reflecting economic development stages.  
    - Machine learning clustering effectively summarized complex health–wealth interactions.  
    - This approach demonstrates how **public health and economics** can be modeled jointly using open data and accessible tools.

    ---
    **Developed:** Google Colab → Streamlit (2025)  
    **Project Authors:** Machine Learning Course Team  
    **Supervisor:** (Hongwei Chuang)
    """)

# -------------------------
# Obesity Analysis & ML Section
# -------------------------
elif section == "Obesity Analysis & ML":
    st.title("📊 Obesity Analysis & Machine Learning Results")

    # ===== USA Section =====
    st.header("🇺🇸 U.S. State-Level Analysis (2023)")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Income vs. Obesity")
        fig_us_income = px.scatter(
            us_df,
            x="PerCapitaIncome",
            y="ObesityRate",
            trendline="ols",
            hover_name="Locationdesc",
            title="Income vs Obesity Rate by State (2023)",
            labels={"PerCapitaIncome": "Per Capita Income ($)", "ObesityRate": "Obesity Rate (%)"}
        )
        st.plotly_chart(fig_us_income, use_container_width=True)

    with col2:
        st.subheader("Physical Activity vs. Obesity")
        fig_us_activity = px.scatter(
            us_df,
            x="PhysicalActivityRate",
            y="ObesityRate",
            trendline="ols",
            hover_name="Locationdesc",
            title="Physical Activity vs Obesity Rate (2023)",
            labels={"PhysicalActivityRate": "Physical Activity Rate (%)", "ObesityRate": "Obesity Rate (%)"}
        )
        st.plotly_chart(fig_us_activity, use_container_width=True)

    st.subheader("State Clusters (K-Means Results)")
    fig_us_clusters = px.choropleth(
=======

# ================================================
# PAGE CONFIG
# ================================================
st.set_page_config(
    page_title="Income, Health & Obesity Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
    <style>
        body, h1, h2, h3, h4, h5, h6, p, table, label {
            font-family: "Segoe UI", sans-serif;
        }
        .block-container {
            padding-top: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# ================================================
# SIDEBAR NAVIGATION
# ================================================
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["About the Project", "Obesity Analysis & ML"])

# ================================================
# PAGE 1: ABOUT
# ================================================
if page == "About the Project":
    st.title("About the Project")
    st.markdown("""
    This project explores how **per capita income** and **physical activity**
    affect **obesity prevalence** across U.S. states and globally.
    
    - **U.S. Analysis:** Uses BEA income data and CDC BRFSS health indicators.  
    - **Global Comparison:** Combines WHO/World Bank datasets (via OWID).  
    - **Machine Learning:** K-Means clustering classifies regions by economic and health status.  

    More detailed context and literature will be added later.
    """)

# ================================================
# PAGE 2: ANALYSIS & ML
# ================================================
elif page == "Obesity Analysis & ML":
    st.title("Obesity Analysis & Machine Learning")
    st.markdown("#### Explore the data-driven relationship between income, health, and obesity.")

    # -------- Load data --------
    DATA_PATH = "data/"
    RESULTS_PATH = "results/"
    PLOTS_PATH = "plots/"

    try:
        us_df = pd.read_csv(DATA_PATH + "us_health_income_2023.csv")
        us_clusters = pd.read_csv(RESULTS_PATH + "us_clusters_2023.csv")
        global_df = pd.read_csv(DATA_PATH + "global_merged_obesity_income.csv")
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()

    # -------- U.S. Section --------
    st.subheader("U.S. State-Level Analysis (2023)")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### Income vs Obesity")
        fig1 = px.scatter(
            us_df,
            x="PerCapitaIncome",
            y="ObesityRate",
            color="PhysicalActivityRate",
            text="Locationdesc",
            trendline="ols",
            title="Income vs Obesity Rate by State",
            color_continuous_scale="Viridis"
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.markdown("##### Physical Activity vs Obesity")
        fig2 = px.scatter(
            us_df,
            x="PhysicalActivityRate",
            y="ObesityRate",
            text="Locationdesc",
            trendline="ols",
            title="Physical Activity vs Obesity",
            color_continuous_scale="Viridis"
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("##### U.S. State Clusters by Income, Obesity & Activity")
    fig_map = px.choropleth(
>>>>>>> 08c88d8 (Initial Streamlit obesity analysis app)
        us_clusters,
        locations="Locationabbr",
        color="ClusterLabel",
        locationmode="USA-states",
        hover_name="Locationdesc",
        hover_data=["PerCapitaIncome", "ObesityRate", "PhysicalActivityRate"],
<<<<<<< HEAD
        title="U.S. State Clusters by Income and Health Indicators (2023)",
        color_discrete_sequence=px.colors.qualitative.Bold,
        scope="usa"
    )
    st.plotly_chart(fig_us_clusters, use_container_width=True)

    st.write("### Cluster Summary Table")
    st.dataframe(us_summary, use_container_width=True)

    st.divider()

    # ===== Global Section =====
    st.header("🌍 Global Income vs Obesity (2022)")
=======
        scope="usa",
        color_discrete_sequence=px.colors.qualitative.Bold,
        title="U.S. Health & Income Clusters (K-Means)"
    )
    st.plotly_chart(fig_map, use_container_width=True)

    # -------- Global Section --------
    st.subheader("Global Analysis (2022)")
    st.markdown("##### Global Income vs Obesity")
    global_df["log_GDP_per_capita"] = (
        global_df["GDP_per_capita_USD"].apply(lambda x: x if x > 0 else None)
    ).apply(lambda x: 0 if pd.isna(x) else x)
    global_df["log_GDP_per_capita"] = global_df["GDP_per_capita_USD"].apply(lambda x: pd.NA if x <= 0 else x)
    global_df["log_GDP_per_capita"] = global_df["GDP_per_capita_USD"].apply(lambda x: None if x <= 0 else x)
    global_df["log_GDP_per_capita"] = global_df["GDP_per_capita_USD"].apply(lambda x: None if x <= 0 else x)
    global_df["log_GDP_per_capita"] = global_df["GDP_per_capita_USD"].apply(lambda x: None if x <= 0 else x)
    global_df["log_GDP_per_capita"] = global_df["GDP_per_capita_USD"].apply(lambda x: None if x <= 0 else x)
    global_df["log_GDP_per_capita"] = global_df["GDP_per_capita_USD"].apply(lambda x: None if x <= 0 else x)
    global_df["log_GDP_per_capita"] = global_df["GDP_per_capita_USD"].apply(lambda x: None if x <= 0 else x)

>>>>>>> 08c88d8 (Initial Streamlit obesity analysis app)
    fig_global = px.scatter(
        global_df,
        x="GDP_per_capita_USD",
        y="ObesityRate",
<<<<<<< HEAD
        hover_name="CountryName",
        color="ObesityRate",
        color_continuous_scale="Viridis",
        trendline="ols",
        title="Global Relationship: Income vs Obesity (2022)",
        labels={"GDP_per_capita_USD": "GDP per Capita (USD)", "ObesityRate": "Obesity Rate (%)"}
    )
    fig_global.update_xaxes(type="log")
    st.plotly_chart(fig_global, use_container_width=True)

    st.markdown("""
    **Observation:**  
    - Within the U.S., obesity decreases as income and activity increase.  
    - Globally, obesity rises with income up to middle-income levels, then plateaus or drops — the “nutrition transition.”  
    """)

st.divider()
st.caption("© 2025 Machine Learning Course | Developed in Google Colab & Streamlit")
=======
        text="ISO3",
        trendline="ols",
        title="Global Relationship: GDP per Capita vs Obesity Rate (2022)",
        color="ObesityRate",
        color_continuous_scale="Viridis"
    )
    st.plotly_chart(fig_global, use_container_width=True)

    st.markdown("##### Sample Global Data")
    st.dataframe(global_df[["Country", "ObesityRate", "GDP_per_capita_USD"]].head(15))
    st.markdown("Data sources include WHO, World Bank, and Our World in Data (OWID).")
>>>>>>> 08c88d8 (Initial Streamlit obesity analysis app)
