import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

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
* { font-family: "Inter", "Segoe UI", system-ui, -apple-system, sans-serif; }
.block-container { padding-top: 1.5rem; }
</style>
""", unsafe_allow_html=True)

# ---------------- Paths ----------------
DATA = Path("data")
RESULTS = Path("results")
PLOTS = Path("plots")

# ---------------- Sidebar ----------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["About the Project", "Obesity Analysis & ML"])

# ---------------- Helpers ----------------
def try_read(path, **kw):
    try:
        return pd.read_csv(path, **kw)
    except Exception as e:
        st.warning(f"Missing or unreadable file: `{path}` ({e})")
        return None

def add_state_abbrev(df_states, df_with_abbrev):
    # attach 2-letter codes for maps if missing
    if "Locationabbr" not in df_states.columns:
        map_df = df_with_abbrev[["Locationdesc","Locationabbr"]].drop_duplicates()
        df_states = df_states.merge(map_df, on="Locationdesc", how="left")
    return df_states

# ---------------- Content ----------------
if page == "About the Project":
    st.title("About the Project")
    st.markdown("""
This dashboard examines how **income** and **physical activity** relate to **obesity** across U.S. states and globally, and uses **K-Means** to cluster U.S. states by health-economic profiles.

**Data folders expected** (`data/`, `results/`):
- `data/us_health_income_2023.csv` — state, income, obesity, activity (2023)
- `results/us_clusters_2023.csv` — state clusters with abbreviations + labels (2023)
- `data/global_merged_obesity_income.csv` — country, ISO3, obesity 2022, GDP pc 2022
- (optional, for animations)
  - `data/brfss_prevalence_full.csv` — full BRFSS prevalence (2011–present)
  - `data/us_income_long.csv` — BEA per-capita income by state (all years)
  - `data/global_obesity_full.csv` — OWID obesity timeseries
  - `data/global_income_full.csv` — World Bank GDP per capita timeseries
""")

else:
    st.title("Obesity Analysis & ML")

    # ---------- Load core datasets ----------
    us_df = try_read(DATA/"us_health_income_2023.csv")
    us_clusters = try_read(RESULTS/"us_clusters_2023.csv")
    global_2022 = try_read(DATA/"global_merged_obesity_income.csv")

    if us_df is None or us_clusters is None or global_2022 is None:
        st.stop()

    us_df = add_state_abbrev(us_df, us_clusters)

    # ===== 1) USA map: obesity by state =====
    st.subheader("U.S. Obesity Map (2023)")
    map_df = us_df.dropna(subset=["Locationabbr","ObesityRate"]).copy()
    fig_us_obesity_map = px.choropleth(
        map_df,
        locations="Locationabbr",
        locationmode="USA-states",
        color="ObesityRate",
        hover_name="Locationdesc",
        color_continuous_scale="Reds",
        scope="usa",
        title="Obesity Rate by State (2023)"
    )
    st.plotly_chart(fig_us_obesity_map, use_container_width=True)

    # ===== 2) Side-by-side: Income vs Obesity AND Activity vs Obesity =====
    st.subheader("State-level Relationships (2023)")
    c1, c2 = st.columns(2)

    with c1:
        fig_income_obesity = px.scatter(
            us_df, x="PerCapitaIncome", y="ObesityRate", text="Locationdesc",
            trendline="ols", title="State-level Relationship: Income vs Obesity (2023)",
            labels={"PerCapitaIncome":"Per Capita Income ($)","ObesityRate":"Obesity Rate (%)"}
        )
        fig_income_obesity.update_traces(textposition="top center")
        st.plotly_chart(fig_income_obesity, use_container_width=True)

    with c2:
        fig_pa_obesity = px.scatter(
            us_df, x="PhysicalActivityRate", y="ObesityRate", text="Locationdesc",
            trendline="ols", title="State-level Relationship: Physical Activity vs Obesity (2023)",
            labels={"PhysicalActivityRate":"Physical Activity Rate (%)","ObesityRate":"Obesity Rate (%)"}
        )
        fig_pa_obesity.update_traces(textposition="top center")
        st.plotly_chart(fig_pa_obesity, use_container_width=True)

    # ===== 3) Scatter: State Clusters by Income & Health =====
    st.subheader("State Clusters by Income and Health Indicators (2023)")
    scatter_df = us_clusters.copy()
    fig_cluster_scatter = px.scatter(
        scatter_df,
        x="PerCapitaIncome", y="ObesityRate",
        color="ClusterLabel", text="Locationdesc",
        labels={"PerCapitaIncome":"Per Capita Income ($)","ObesityRate":"Obesity Rate (%)"},
        title="Clusters in Feature Space (Income vs Obesity)"
    )
    fig_cluster_scatter.update_traces(textposition="top center")
    st.plotly_chart(fig_cluster_scatter, use_container_width=True)

    st.markdown("##### U.S. State Clusters by Income, Obesity & Activity")
    fig_map = px.choropleth(
        us_clusters,
        locations="Locationabbr",
        locationmode="USA-states",
        color="ClusterLabel",
        hover_name="Locationdesc",
        hover_data=["PerCapitaIncome", "ObesityRate", "PhysicalActivityRate"],
        scope="usa",
        color_discrete_sequence=px.colors.qualitative.Bold,
        title="K-Means Cluster Map (2023)"
    )
    st.plotly_chart(fig_cluster_map, use_container_width=True)

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

    fig_global = px.scatter(
        global_df,
        x="GDP_per_capita_USD",
        y="ObesityRate",
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