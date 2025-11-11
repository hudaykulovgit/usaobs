import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- Page setup ---
st.set_page_config(page_title="Income and Obesity Analysis", layout="wide")

# --- Sidebar Navigation ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["About the Project", "Obesity Analysis & ML"])

# --- Load Data ---
@st.cache_data
def load_data():
    us_df = pd.read_csv("data/us_health_income_2023.csv")
    us_clusters = pd.read_csv("results/us_clusters_2023.csv")
    global_df = pd.read_csv("data/global_merged_obesity_income.csv")
    return us_df, us_clusters, global_df

us_df, us_clusters, global_df = load_data()

# =======================================================
# TAB 1 — ABOUT THE PROJECT
# =======================================================
if page == "About the Project":
    st.title("📊 U.S. and Global Obesity Analysis")
    st.markdown("""
    This Streamlit app explores the relationship between **income**, **obesity**, 
    and **physical activity** across **U.S. states** and **countries globally**.
    
    **Data Sources**
    - U.S. data: BEA (Income), CDC BRFSS (Health indicators)
    - Global data: World Bank (GDP per capita), WHO via Our World In Data (Obesity rates)
    
    **Objective**
    - Investigate whether higher income correlates with lower obesity.
    - Examine how physical activity mediates that relationship.
    - Compare domestic (U.S.) and international patterns.
    
    **Machine Learning**
    - Applied K-Means clustering to group U.S. states by income and health metrics.
    - Visualized patterns using interactive Plotly charts and choropleth maps.
    """)

# =======================================================
# TAB 2 — OBESITY ANALYSIS & ML
# =======================================================
elif page == "Obesity Analysis & ML":
    st.title("🏥 Obesity and Machine Learning Analysis")

    col1, col2 = st.columns(2)

    # --- Scatter 1: Income vs Obesity ---
    with col1:
        st.subheader("State-level Relationship: Income vs Obesity (2023)")
        fig1 = px.scatter(
            us_df, x="PerCapitaIncome", y="ObesityRate", trendline="ols",
            text="Locationdesc", labels={
                "PerCapitaIncome": "Per Capita Income ($)",
                "ObesityRate": "Obesity Rate (%)"
            }
        )
        fig1.update_traces(textposition="top center")
        st.plotly_chart(fig1, use_container_width=True)

    # --- Scatter 2: Physical Activity vs Obesity ---
    with col2:
        st.subheader("State-level Relationship: Physical Activity vs Obesity (2023)")
        fig2 = px.scatter(
            us_df, x="PhysicalActivityRate", y="ObesityRate", trendline="ols",
            text="Locationdesc", labels={
                "PhysicalActivityRate": "Physical Activity Rate (%)",
                "ObesityRate": "Obesity Rate (%)"
            }
        )
        fig2.update_traces(textposition="top center")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # --- Scatter 3: Clusters by Income and Health ---
    st.subheader("State Clusters by Income and Health Indicators (2023)")
    fig3 = px.scatter(
        us_clusters, x="PerCapitaIncome", y="ObesityRate",
        color=us_clusters["Cluster"].astype(str),
        text="Locationdesc",
        labels={"PerCapitaIncome": "Per Capita Income ($)", "ObesityRate": "Obesity Rate (%)"}
    )
    fig3.update_traces(textposition="top center")
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")

    # --- Choropleth: U.S. Cluster Map ---
    st.subheader("U.S. State Clusters by Income, Obesity, and Activity (2023)")
    fig4 = px.choropleth(
        us_clusters, locations="Locationabbr", color="ClusterLabel",
        locationmode="USA-states", hover_name="Locationdesc",
        hover_data={
            "PerCapitaIncome": True,
            "ObesityRate": True,
            "PhysicalActivityRate": True
        },
        color_discrete_sequence=px.colors.qualitative.Bold,
        scope="usa"
    )
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")

    # --- Global Scatter: Income vs Obesity ---
    st.subheader("Global Relationship: Income vs Obesity (2022)")

    # Use numpy safely instead of deprecated pd.np
    global_df["log_GDP_per_capita"] = np.where(
        global_df["GDP_per_capita_USD"] > 0,
        np.log10(global_df["GDP_per_capita_USD"]),
        np.nan
    )

    fig5 = px.scatter(
        global_df, x="log_GDP_per_capita", y="ObesityRate",
        trendline="ols", color="ObesityRate", color_continuous_scale="Viridis",
        text="ISO3", hover_name="country_name",
        labels={
            "log_GDP_per_capita": "Log10 GDP per Capita (USD)",
            "ObesityRate": "Obesity Rate (%)"
        }
    )
    fig5.update_traces(textposition="top center")
    st.plotly_chart(fig5, use_container_width=True)

    st.markdown("---")

    st.subheader("📈 Comparison: U.S. States vs Global Patterns")
    st.write("""
    - **U.S. States:** show a *negative* correlation — higher income → lower obesity.  
    - **Global Countries:** show a *positive then flattening* relationship — as economies grow, obesity rises then stabilizes.  
    - Together, these trends highlight how economic stage and lifestyle infrastructure shape public health outcomes.
    """)
