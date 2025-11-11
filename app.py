import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# --- File Paths ---
BASE = Path(__file__).parent
DATA_DIR = BASE / "data"
RESULTS_DIR = BASE / "results"
PLOTS_DIR = BASE / "plots"

st.set_page_config(page_title="Income, Health & Obesity Analysis", layout="wide")

# --- Sidebar Navigation ---
tabs = st.sidebar.radio(
    "Navigation",
    ["About the Project", "Obesity Analysis and ML"]
)

# --- Tab 1: About the Project ---
if tabs == "About the Project":
    st.title("About the Project")

    readme_path = BASE / "README.md"
    if readme_path.exists():
        with open(readme_path, "r", encoding="utf-8") as f:
            st.markdown(f.read())
    else:
        st.warning("README.md not found. Please include the project description file.")

# --- Tab 2: Obesity Analysis and ML ---
elif tabs == "Obesity Analysis and ML":
    st.title("Obesity Analysis and Machine Learning Insights")

    # --- Section 1: State-level Relationships ---
    st.header("1. State-level Relationships (2023)")
    st.markdown("Exploring income, physical activity, and obesity at the U.S. state level.")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Income vs Obesity (2023)")
        us_income_obesity_html = PLOTS_DIR / "us_income_obesity_interactive.html"
        if us_income_obesity_html.exists():
            st.components.v1.html(us_income_obesity_html.read_text(), height=500)
        else:
            st.image(PLOTS_DIR / "us_income_obesity.png", caption="Income vs Obesity (2023)")

    with col2:
        st.subheader("Physical Activity vs Obesity (2023)")
        us_activity_html = PLOTS_DIR / "us_activity_obesity_interactive.html"
        if us_activity_html.exists():
            st.components.v1.html(us_activity_html.read_text(), height=500)
        else:
            st.info("Interactive chart not found. Please generate and save HTML plot.")

    st.divider()

    # --- Section 2: State Clustering ---
    st.header("2. State Clusters by Income and Health Indicators (2023)")
    st.markdown("Unsupervised learning (K-Means) identifies groups of states by income, obesity, and activity levels.")

    # Load cluster data
    clusters_path = RESULTS_DIR / "us_clusters_2023.csv"
    if clusters_path.exists():
        df_clusters = pd.read_csv(clusters_path)
        fig_clusters = px.scatter(
            df_clusters,
            x="PerCapitaIncome",
            y="ObesityRate",
            color="ClusterLabel",
            hover_name="Locationdesc",
            title="State Clusters by Income and Health Indicators (2023)",
            labels={"PerCapitaIncome": "Per Capita Income ($)", "ObesityRate": "Obesity Rate (%)"}
        )
        st.plotly_chart(fig_clusters, use_container_width=True)
    else:
        st.warning("us_clusters_2023.csv not found. Please run clustering step first.")

    st.subheader("U.S. Map: State Clusters by Income, Obesity, and Activity (2023)")
    us_map_html = PLOTS_DIR / "us_clusters_map.html"
    if us_map_html.exists():
        st.components.v1.html(us_map_html.read_text(), height=600)
    else:
        st.info("Map visualization missing. Please export 'us_clusters_map.html'.")

    st.divider()

    # --- Section 3: Global vs U.S. Comparison ---
    st.header("3. Global Relationship: Income vs Obesity (2022)")
    st.markdown("Comparing the U.S. state-level trends to global obesity-income dynamics.")

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("U.S. States: Income vs Obesity (2023)")
        if us_income_obesity_html.exists():
            st.components.v1.html(us_income_obesity_html.read_text(), height=500)
        else:
            st.image(PLOTS_DIR / "us_income_obesity.png", caption="U.S. States: Income vs Obesity (2023)")

    with col4:
        st.subheader("World: Income vs Obesity (2022)")
        global_html = PLOTS_DIR / "global_income_obesity_interactive.html"
        if global_html.exists():
            st.components.v1.html(global_html.read_text(), height=500)
        else:
            st.info("Global interactive chart missing. Please export global plot to HTML.")

    st.divider()
    st.markdown("**Interpretation:** Richer countries show an inverted-U pattern in obesity, while within the U.S., the relationship is linear and negative—wealthier states have lower obesity and higher physical activity levels.")

