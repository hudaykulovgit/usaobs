# ===========================
# app.py
# ===========================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="Income & Obesity ML Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Simple consistent styling
st.markdown("""
<style>
    * {font-family: 'Arial', sans-serif;}
    h1, h2, h3 {color: #003366;}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Sidebar navigation
# -----------------------------
menu = st.sidebar.radio(
    "Navigation",
    ["About the Project", "Obesity Analysis & ML"]
)

# -----------------------------
# Tab 1: About
# -----------------------------
if menu == "About the Project":
    st.title("About the Project")
    st.markdown("""
    This interactive dashboard explores how **income levels influence health outcomes**, 
    particularly obesity and physical activity, across **U.S. states** and **global countries**.

    **Datasets used:**
    - U.S.: BEA, BRFSS  
    - Global: World Bank (GDP per capita), WHO/OWID (obesity prevalence)  

    **Methods:**  
    - Data cleaning and merging in Python (pandas)  
    - Exploratory analysis with Plotly  
    - Machine Learning clustering (K-Means)  
    """)

# -----------------------------
# Tab 2: Obesity Analysis and ML
# -----------------------------
elif menu == "Obesity Analysis & ML":
    st.title("Obesity Analysis and Machine Learning Results")

    # ===========================
    # Load data
    # ===========================
    data_path = "data/"
    results_path = "results/"

    us_df = pd.read_csv(data_path + "us_health_income_2023.csv")
    global_df = pd.read_csv(data_path + "global_merged_obesity_income.csv")
    clusters_us = pd.read_csv(results_path + "us_clusters_2023.csv")
    cluster_summary = pd.read_csv(results_path + "us_cluster_summary.csv")

    # --- U.S. Section ---
    st.header("🇺🇸 U.S. Analysis (2023)")
    st.write("Exploring relationships among income, obesity, and physical activity across states.")

    # Income vs Obesity
    fig_us_income = px.scatter(
        us_df,
        x="PerCapitaIncome",
        y="ObesityRate",
        text="Locationdesc",
        trendline="ols",
        title="Income vs Obesity (U.S. States, 2023)",
        labels={
            "PerCapitaIncome": "Per Capita Income ($)",
            "ObesityRate": "Obesity Rate (%)"
        }
    )
    st.plotly_chart(fig_us_income, use_container_width=True, key="fig_us_income")

    # Physical Activity vs Obesity
    fig_us_activity = px.scatter(
        us_df,
        x="PhysicalActivityRate",
        y="ObesityRate",
        text="Locationdesc",
        trendline="ols",
        title="Physical Activity vs Obesity (U.S. States, 2023)",
        labels={
            "PhysicalActivityRate": "Physical Activity Rate (%)",
            "ObesityRate": "Obesity Rate (%)"
        },
        color_discrete_sequence=["green"]
    )
    st.plotly_chart(fig_us_activity, use_container_width=True, key="fig_us_activity")

    # Cluster summary table
    st.subheader("Cluster Summary (U.S. States)")
    st.dataframe(cluster_summary)

    # Choropleth map
    fig_us_map = px.choropleth(
        clusters_us,
        locations="Locationabbr",
        color="ClusterLabel",
        locationmode="USA-states",
        hover_name="Locationdesc",
        scope="usa",
        title="State Clusters by Income, Obesity, and Activity (2023)",
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    st.plotly_chart(fig_us_map, use_container_width=True, key="fig_us_map")

    # ===========================
    # Global analysis
    # ===========================
    st.header("🌍 Global Analysis (2022)")
    st.write("Examining the global relationship between income and obesity across 190 countries.")

    global_df["log_GDP_per_capita"] = np.log10(global_df["GDP_per_capita_USD"].replace(0, np.nan))

    fig_global_income = px.scatter(
        global_df,
        x="log_GDP_per_capita",
        y="ObesityRate",
        text="ISO3",
        hover_name="Country",
        trendline="ols",
        title="Global Relationship: Income vs Obesity (2022)",
        labels={
            "log_GDP_per_capita": "Log10 GDP per Capita (USD)",
            "ObesityRate": "Obesity Rate (%)"
        },
        color="ObesityRate",
        color_continuous_scale="Viridis"
    )
    st.plotly_chart(fig_global_income, use_container_width=True, key="fig_global_income")

    # Observations
    st.markdown("### Key Observations")
    st.markdown("""
    - Within the **U.S.**, higher income is clearly associated with **lower obesity**.  
    - Globally, obesity **rises with income** in developing nations, then **levels off** among wealthier economies.  
    - Physical activity plays a mediating role, explaining much of this income–health gradient.  
    """)

    st.success("✅ Visualizations and clustering results loaded successfully.")
