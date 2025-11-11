import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path

# ---------------- Page config & style ----------------
st.set_page_config(page_title="Income & Obesity — USA & World", layout="wide")
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

    # ===== 4) Map: U.S. State Clusters =====
    st.subheader("U.S. State Clusters by Income, Obesity & Activity (Map)")
    fig_cluster_map = px.choropleth(
        us_clusters,
        locations="Locationabbr",
        locationmode="USA-states",
        color="ClusterLabel",
        hover_name="Locationdesc",
        hover_data=["PerCapitaIncome","ObesityRate","PhysicalActivityRate"],
        scope="usa",
        color_discrete_sequence=px.colors.qualitative.Bold,
        title="K-Means Cluster Map (2023)"
    )
    st.plotly_chart(fig_cluster_map, use_container_width=True)

    # ===== 5) Global Relationship: Income vs Obesity (2022) =====
    st.subheader("Global Relationship: Income vs Obesity (2022)")
    world_df = global_2022.dropna(subset=["GDP_per_capita_USD","ObesityRate"]).copy()
    world_df["log_GDP_pc"] = np.log10(world_df["GDP_per_capita_USD"].astype(float))
    fig_world = px.scatter(
        world_df, x="log_GDP_pc", y="ObesityRate", text="ISO3",
        trendline="ols",
        color="ObesityRate", color_continuous_scale="Viridis",
        labels={"log_GDP_pc":"Log10 GDP per Capita (USD)","ObesityRate":"Obesity Rate (%)"},
        title="World: Income vs Obesity (2022)"
    )
    fig_world.update_traces(textposition="top center")
    st.plotly_chart(fig_world, use_container_width=True)

    # ===== 6) Side-by-side: U.S. vs World =====
    st.subheader("Side-by-side: U.S. States vs World (2023 vs 2022)")
    s1, s2 = st.columns(2)
    with s1:
        st.markdown("**U.S. States: Income vs Obesity (2023)**")
        # CREATE A NEW FIGURE INSTANCE instead of reusing fig_income_obesity
        fig_income_obesity_duplicate = px.scatter(
            us_df, x="PerCapitaIncome", y="ObesityRate", text="Locationdesc",
            trendline="ols", title="State-level Relationship: Income vs Obesity (2023)",
            labels={"PerCapitaIncome":"Per Capita Income ($)","ObesityRate":"Obesity Rate (%)"}
        )
        fig_income_obesity_duplicate.update_traces(textposition="top center")
        st.plotly_chart(fig_income_obesity_duplicate, use_container_width=True)
    with s2:
        st.markdown("**World: Income vs Obesity (2022)**")
        # CREATE A NEW FIGURE INSTANCE instead of reusing fig_world
        fig_world_duplicate = px.scatter(
            world_df, x="log_GDP_pc", y="ObesityRate", text="ISO3",
            trendline="ols",
            color="ObesityRate", color_continuous_scale="Viridis",
            labels={"log_GDP_pc":"Log10 GDP per Capita (USD)","ObesityRate":"Obesity Rate (%)"},
            title="World: Income vs Obesity (2022)"
        )
        fig_world_duplicate.update_traces(textposition="top center")
        st.plotly_chart(fig_world_duplicate, use_container_width=True)

    # ===== 7) Animations =====
    st.subheader("Animations")

    # --- U.S. Smoothed 2011–2024 animation (requires BRFSS + income long) ---
    brfss_full = try_read(DATA/"brfss_prevalence_full.csv")
    income_long = try_read(DATA/"us_income_long.csv")
    if brfss_full is not None and income_long is not None:
        obese = (brfss_full[(brfss_full["Topic"]=="BMI Categories") &
                            (brfss_full["Response"].str.contains("Obese", case=False, na=False))]
                 .copy())
        obese = obese.rename(columns={"Locationdesc":"State","Data_value":"ObesityRate"})
        obese = obese[["Year","State","ObesityRate"]]

        inc = income_long.rename(columns={"GeoName":"State","PerCapitaIncome":"Income"})
        inc = inc[["Year","State","Income"]]

        us_ts = obese.merge(inc, on=["Year","State"], how="inner")
        us_ts = us_ts.sort_values(["State","Year"])
        us_ts["ObesityRate_smooth"] = us_ts.groupby("State")["ObesityRate"].transform(lambda s: s.rolling(3, min_periods=1).mean())
        us_ts["Income_smooth"] = us_ts.groupby("State")["Income"].transform(lambda s: s.rolling(3, min_periods=1).mean())

        fig_us_anim = px.scatter(
            us_ts, x="Income_smooth", y="ObesityRate_smooth",
            animation_frame="Year", animation_group="State",
            text="State", range_x=[us_ts["Income_smooth"].min()*0.95, us_ts["Income_smooth"].max()*1.05],
            range_y=[us_ts["ObesityRate_smooth"].min()*0.95, us_ts["ObesityRate_smooth"].max()*1.05],
            title="U.S. States: Income vs Obesity (Smoothed 2011–2024)",
            labels={"Income_smooth":"Per Capita Income ($, 3y MA)", "ObesityRate_smooth":"Obesity Rate (%, 3y MA)"},
            color="State", height=600
        )
        st.plotly_chart(fig_us_anim, use_container_width=True)
    else:
        st.info("U.S. animation skipped — expecting `data/brfss_prevalence_full.csv` and `data/us_income_long.csv`.")

    # --- Global animation (requires global timeseries) ---
    glob_ob_full = try_read(DATA/"global_obesity_full.csv")
    glob_inc_full = try_read(DATA/"global_income_full.csv")
    if glob_ob_full is not None and glob_inc_full is not None:
        g_ob = glob_ob_full.rename(columns={"prevalence_of_obesity":"ObesityRate"})
        g_inc = glob_inc_full.rename(columns={"value":"GDP_per_capita_USD"})
        g_inc["Year"] = g_inc["Year"].astype(int)
        g = g_ob.merge(g_inc[["ISO3","Year","GDP_per_capita_USD"]], on=["ISO3","Year"], how="inner").dropna()
        g["log_GDP_pc"] = np.log10(g["GDP_per_capita_USD"].astype(float))
        fig_world_anim = px.scatter(
            g, x="log_GDP_pc", y="ObesityRate", animation_frame="Year", animation_group="ISO3",
            text="ISO3", color="ObesityRate", color_continuous_scale="Viridis",
            title="Global Relationship: Income vs Obesity (Animation)",
            labels={"log_GDP_pc":"Log10 GDP per Capita (USD)","ObesityRate":"Obesity Rate (%)"},
            height=600
        )
        st.plotly_chart(fig_world_anim, use_container_width=True)
    else:
        st.info("Global animation skipped — expecting `data/global_obesity_full.csv` and `data/global_income_full.csv`.")
