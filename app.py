# app.py
import os
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Income & Obesity Analysis", layout="wide")

# ---------- Helpers ----------
@st.cache_data
def read_text(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"**README not found.** {e}"

@st.cache_data
def load_csv(path):
    return pd.read_csv(path)

@st.cache_data
def safe_load_csv(path):
    return pd.read_csv(path) if os.path.exists(path) else None

def money_fmt(x):
    try:
        return f"${int(x):,}"
    except Exception:
        return x

# ---------- Paths ----------
DATA_DIR = "data"
RESULTS_DIR = "results"
PLOTS_DIR = "plots"

PATH_README = "README.md"
PATH_US_MERGED = os.path.join(DATA_DIR, "us_health_income_2023.csv")
PATH_US_OBE_RAW = os.path.join(DATA_DIR, "us_brfss_obesity_raw.csv")
PATH_US_ACT_RAW = os.path.join(DATA_DIR, "us_brfss_activity_raw.csv")
PATH_US_CLUSTERS = os.path.join(RESULTS_DIR, "us_clusters_2023.csv")
PATH_US_CLUSTER_SUM = os.path.join(RESULTS_DIR, "us_cluster_summary.csv")
PATH_GLOBAL_OB = os.path.join(DATA_DIR, "global_obesity_2022.csv")
PATH_GLOBAL_INC = os.path.join(DATA_DIR, "global_income_2022.csv")
PATH_GLOBAL_MERGED = os.path.join(DATA_DIR, "global_merged_obesity_income.csv")

# ---------- Sidebar ----------
st.sidebar.title("Navigation")
section = st.sidebar.radio(
    "Go to",
    ["About the project", "Obesity analysis and ML"],
    index=0
)

# =============== About Section ===============
if section == "About the project":
    st.title("About the Project")
    st.markdown(read_text(PATH_README))

# =============== Analysis Section ===============
else:
    st.title("Obesity Analysis and Machine Learning")

    # --- Load US merged data ---
    us_df = safe_load_csv(PATH_US_MERGED)
    if us_df is None:
        st.error("Missing `data/us_health_income_2023.csv`. Please add dataset.")
        st.stop()

    # Attach abbreviations if missing
    if "Locationabbr" not in us_df.columns:
        brfss_any = safe_load_csv(PATH_US_OBE_RAW)
        if brfss_any is None:
            brfss_any = safe_load_csv(PATH_US_ACT_RAW)
        if brfss_any is not None and {"Locationdesc", "Locationabbr"}.issubset(brfss_any.columns):
            abbrev_map = brfss_any[["Locationdesc", "Locationabbr"]].drop_duplicates()
            us_df = us_df.merge(abbrev_map, on="Locationdesc", how="left")

    # Ensure numeric
    for col in ["PerCapitaIncome", "ObesityRate", "PhysicalActivityRate"]:
        us_df[col] = pd.to_numeric(us_df[col], errors="coerce")

    # ---------- 1. State-level: Income vs Obesity ----------
    st.subheader("1. State-level Relationship: Income vs Obesity (2023)")
    fig_us_income_ob = px.scatter(
        us_df,
        x="PerCapitaIncome", y="ObesityRate",
        text="Locationdesc",
        trendline="ols",
        labels={
            "PerCapitaIncome": "Per Capita Income ($)",
            "ObesityRate": "Obesity Rate (%)"
        },
        title="State-level: Income vs Obesity (2023)"
    )
    fig_us_income_ob.update_traces(textposition="top center")
    st.plotly_chart(fig_us_income_ob, use_container_width=True)

    # ---------- 2. Physical Activity vs Obesity ----------
    st.subheader("2. State-level Relationship: Physical Activity vs Obesity (2023)")
    fig_us_act_ob = px.scatter(
        us_df,
        x="PhysicalActivityRate", y="ObesityRate",
        text="Locationdesc",
        trendline="ols",
        labels={
            "PhysicalActivityRate": "Physical Activity Rate (%)",
            "ObesityRate": "Obesity Rate (%)"
        },
        title="State-level: Physical Activity vs Obesity (2023)"
    )
    fig_us_act_ob.update_traces(textposition="top center")
    st.plotly_chart(fig_us_act_ob, use_container_width=True)

    # ---------- 3. State Clusters Scatter ----------
    st.subheader("3. State Clusters by Income and Health Indicators (2023)")
    clusters_df = safe_load_csv(PATH_US_CLUSTERS)
    if clusters_df is None:
        clusters_df = us_df.copy()
    cluster_sum = safe_load_csv(PATH_US_CLUSTER_SUM)

    cluster_labels = None
    if cluster_sum is not None and "Cluster" in cluster_sum.columns:
        try:
            lab_map = {}
            for _, r in cluster_sum.iterrows():
                lab_map[int(r["Cluster"])] = (
                    f"Cluster {int(r['Cluster'])}: "
                    f"Income≈{money_fmt(round(r['PerCapitaIncome']))}, "
                    f"Obesity≈{round(r['ObesityRate'],1)}%, "
                    f"Activity≈{round(r['PhysicalActivityRate'],1)}%"
                )
            cluster_labels = lab_map
        except Exception:
            pass

    if "Cluster" in clusters_df.columns:
        clusters_df["ClusterLabel"] = clusters_df["Cluster"].map(cluster_labels) if cluster_labels else clusters_df["Cluster"].astype(str)
        color_arg = "ClusterLabel"
    else:
        color_arg = None

    fig_clusters = px.scatter(
        clusters_df,
        x="PerCapitaIncome", y="ObesityRate",
        color=color_arg,
        text="Locationdesc" if "Locationdesc" in clusters_df.columns else None,
        labels={"PerCapitaIncome": "Per Capita Income ($)", "ObesityRate": "Obesity Rate (%)"},
        title="State Clusters by Income and Health Indicators (2023)"
    )
    fig_clusters.update_traces(textposition="top center")
    st.plotly_chart(fig_clusters, use_container_width=True)

    # ---------- 4. U.S. Map of State Clusters ----------
    st.subheader("4. U.S. State Clusters by Income, Obesity, and Activity (2023) — US Map")
    if "Locationabbr" in clusters_df.columns:
        fig_map = px.choropleth(
            clusters_df,
            locations="Locationabbr",
            locationmode="USA-states",
            color="ClusterLabel" if "ClusterLabel" in clusters_df.columns else None,
            hover_name="Locationdesc" if "Locationdesc" in clusters_df.columns else None,
            hover_data={"PerCapitaIncome": True, "ObesityRate": True, "PhysicalActivityRate": True},
            scope="usa",
            title="U.S. State Clusters by Income, Obesity, and Activity (2023)"
        )
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.info("No `Locationabbr` found — cannot render U.S. map.")

    # ---------- 5. Global Relationship: Income vs Obesity ----------
    st.subheader("5. Global Relationship: Income vs Obesity (2022)")
    global_df = safe_load_csv(PATH_GLOBAL_MERGED)
    if global_df is None:
        g1, g2 = safe_load_csv(PATH_GLOBAL_OB), safe_load_csv(PATH_GLOBAL_INC)
        if g1 is not None and g2 is not None and "ISO3" in g1.columns and "ISO3" in g2.columns:
            global_df = g1.merge(g2, on="ISO3", how="inner")
        else:
            st.error("Missing global data (merged or components).")
            st.stop()

    # Deduplicate columns to avoid Plotly DuplicateError
    global_df = global_df.loc[:, ~global_df.columns.duplicated()].copy()

    rename_map = {
        "country_name": "CountryName",
        "Country": "CountryName",
        "country": "CountryName",
        "value": "GDP_per_capita_USD",
        "NY.GDP.PCAP.CD": "GDP_per_capita_USD"
    }
    global_df.rename(columns=rename_map, inplace=True)
    
    # FIX: Re-deduplicate columns in case the rename operation created duplicates.
    global_df = global_df.loc[:, ~global_df.columns.duplicated()].copy()

    for c in ["ObesityRate", "GDP_per_capita_USD"]:
        if c in global_df.columns:
            global_df[c] = pd.to_numeric(global_df[c], errors="coerce")

    global_df["log_GDP_per_capita"] = np.log10(global_df["GDP_per_capita_USD"])

    fig_global = px.scatter(
        global_df.dropna(subset=["log_GDP_per_capita", "ObesityRate"]),
        x="log_GDP_per_capita", y="ObesityRate",
        text="ISO3" if "ISO3" in global_df.columns else None,
        hover_name="CountryName" if "CountryName" in global_df.columns else None,
        trendline="ols",
        color="ObesityRate",
        color_continuous_scale="Viridis",
        labels={
            "log_GDP_per_capita": "Log10 GDP per Capita (USD)",
            "ObesityRate": "Obesity Rate (%)"
        },
        title="Global Relationship: Income vs Obesity (2022)"
    )
    fig_global.update_traces(textposition="top center")
    st.plotly_chart(fig_global, use_container_width=True)

    st.caption("Built with Streamlit • Data: BEA, CDC BRFSS, World Bank, OWID/WHO")
