# app.py
import os
import json
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Income & Obesity Analysis", layout="wide")

# ----------------------------
# Helpers & cached loaders
# ----------------------------
@st.cache_data
def read_text(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"**README not found or unreadable.**\n\n{e}"

@st.cache_data
def load_csv(path):
    return pd.read_csv(path)

@st.cache_data
def safe_load_csv(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    return None

def show_html_plot(path, height=650):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            components.html(f.read(), height=height, scrolling=True)
    else:
        st.info(f"Plot HTML not found: `{path}`")

def money_fmt(x):
    try:
        return f"${int(x):,}"
    except Exception:
        return x

# ----------------------------
# Paths
# ----------------------------
DATA_DIR = "data"
RESULTS_DIR = "results"
PLOTS_DIR = "plots"

PATH_README = "README.md"
PATH_US_MERGED = os.path.join(DATA_DIR, "us_health_income_2023.csv")
PATH_US_OBE_RAW = os.path.join(DATA_DIR, "us_brfss_obesity_raw.csv")
PATH_US_ACT_RAW = os.path.join(DATA_DIR, "us_brfss_activity_raw.csv")
PATH_US_INCOME_LONG = os.path.join(DATA_DIR, "us_income_long.csv")

PATH_GLOBAL_OB = os.path.join(DATA_DIR, "global_obesity_2022.csv")
PATH_GLOBAL_INC = os.path.join(DATA_DIR, "global_income_2022.csv")
PATH_GLOBAL_MERGED = os.path.join(DATA_DIR, "global_merged_obesity_income.csv")

PATH_US_CLUSTERS = os.path.join(RESULTS_DIR, "us_clusters_2023.csv")
PATH_US_CLUSTER_SUM = os.path.join(RESULTS_DIR, "us_cluster_summary.csv")

# Optional pre-rendered HTMLs
PATH_PLOT_US_INCOME_OB_HTML = os.path.join(PLOTS_DIR, "us_income_obesity_interactive.html")
PATH_PLOT_US_ACT_OB_HTML = os.path.join(PLOTS_DIR, "us_activity_obesity_interactive.html")
PATH_PLOT_US_MAP_HTML = os.path.join(PLOTS_DIR, "us_clusters_map.html")
PATH_PLOT_GLOBAL_HTML = os.path.join(PLOTS_DIR, "global_income_obesity_interactive.html")

# ----------------------------
# Sidebar navigation (2 tabs)
# ----------------------------
st.sidebar.title("Navigation")
section = st.sidebar.radio(
    "Go to", 
    ["About the project", "Obesity analysis and ML"], 
    index=0
)

# ============================
# About
# ============================
if section == "About the project":
    st.title("About the Project")
    st.markdown(read_text(PATH_README))

# ============================
# Analysis
# ============================
else:
    st.title("Obesity Analysis & Machine Learning")

    # ------------------------
    # Load USA base datasets
    # ------------------------
    us_df = safe_load_csv(PATH_US_MERGED)  # expected cols: Locationdesc, PerCapitaIncome, ObesityRate, PhysicalActivityRate, [Locationabbr?]
    if us_df is None:
        st.error(f"Missing `{PATH_US_MERGED}`. Please export the merged U.S. dataset.")
        st.stop()

    # Try to attach state abbreviations if missing
    if "Locationabbr" not in us_df.columns:
        brfss_any = safe_load_csv(PATH_US_OBE_RAW) or safe_load_csv(PATH_US_ACT_RAW)
        if brfss_any is not None and {"Locationdesc", "Locationabbr"}.issubset(brfss_any.columns):
            abbrev_map = brfss_any[["Locationdesc", "Locationabbr"]].drop_duplicates()
            us_df = us_df.merge(abbrev_map, on="Locationdesc", how="left")

    # Tidy/formatting
    for col in ["PerCapitaIncome", "ObesityRate", "PhysicalActivityRate"]:
        if col in us_df.columns:
            us_df[col] = pd.to_numeric(us_df[col], errors="coerce")

    # ------------------------
    # 1) Income vs Obesity (US, 2023)
    # ------------------------
    st.subheader("1) State-level Relationship: Income vs Obesity (2023)")
    c1, c2 = st.columns([3, 2])
    with c1:
        fig_us_income_ob = px.scatter(
            us_df,
            x="PerCapitaIncome", y="ObesityRate",
            text="Locationdesc",
            trendline="ols",
            labels={"PerCapitaIncome": "Per Capita Income ($)", "ObesityRate": "Obesity Rate (%)"},
            title="Income vs Obesity (U.S. States, 2023)"
        )
        fig_us_income_ob.update_traces(textposition="top center")
        fig_us_income_ob.update_layout(margin=dict(l=10, r=10, t=60, b=10))
        st.plotly_chart(fig_us_income_ob, use_container_width=True)
    with c2:
        st.dataframe(
            us_df[["Locationdesc", "PerCapitaIncome", "ObesityRate"]]
            .sort_values("PerCapitaIncome", ascending=False)
            .reset_index(drop=True)
            .style.format({"PerCapitaIncome": money_fmt, "ObesityRate": "{:.1f}%"}),
            use_container_width=True, height=450
        )
    with st.expander("Show saved HTML (if available)"):
        show_html_plot(PATH_PLOT_US_INCOME_OB_HTML, height=600)

    # ------------------------
    # 2) Physical Activity vs Obesity (US, 2023)
    # ------------------------
    st.subheader("2) State-level Relationship: Physical Activity vs Obesity (2023)")
    fig_us_act_ob = px.scatter(
        us_df,
        x="PhysicalActivityRate", y="ObesityRate",
        text="Locationdesc",
        trendline="ols",
        labels={"PhysicalActivityRate": "Physical Activity Rate (%)", "ObesityRate": "Obesity Rate (%)"},
        title="Physical Activity vs Obesity (U.S. States, 2023)"
    )
    fig_us_act_ob.update_traces(textposition="top center")
    fig_us_act_ob.update_layout(margin=dict(l=10, r=10, t=60, b=10))
    st.plotly_chart(fig_us_act_ob, use_container_width=True)
    with st.expander("Show saved HTML (if available)"):
        show_html_plot(PATH_PLOT_US_ACT_OB_HTML, height=600)

    # ------------------------
    # 3) State Clusters (scatter)
    # ------------------------
    st.subheader("3) State Clusters by Income and Health Indicators (2023)")
    clusters_df = safe_load_csv(PATH_US_CLUSTERS)
    if clusters_df is None:
        # If results not saved, synthesize clusters from us_df (expect a 'Cluster' column if already computed)
        clusters_df = us_df.copy()
    cluster_col = "Cluster" if "Cluster" in clusters_df.columns else None

    # Try to attach cluster labels if summary exists
    cluster_labels = None
    summ_df = safe_load_csv(PATH_US_CLUSTER_SUM)
    if summ_df is not None and "Cluster" in summ_df.columns:
        # Optionally construct readable labels from summary ranks
        # Expect columns: Cluster, PerCapitaIncome, ObesityRate, PhysicalActivityRate
        try:
            lab_map = {}
            for _, r in summ_df.iterrows():
                lab_map[int(r["Cluster"])] = (
                    f"Cluster {int(r['Cluster'])} | "
                    f"Income≈{money_fmt(round(float(r['PerCapitaIncome'])))}, "
                    f"Obesity≈{round(float(r['ObesityRate']),1)}%, "
                    f"Activity≈{round(float(r['PhysicalActivityRate']),1)}%"
                )
            cluster_labels = lab_map
        except Exception:
            pass

    if cluster_col and cluster_labels:
        clusters_df["ClusterLabel"] = clusters_df["Cluster"].map(cluster_labels)
        color_arg = "ClusterLabel"
    elif cluster_col:
        color_arg = clusters_df["Cluster"].astype(str)
    else:
        color_arg = None

    fig_cluster_scatter = px.scatter(
        clusters_df,
        x="PerCapitaIncome", y="ObesityRate",
        color=color_arg,
        text="Locationdesc" if "Locationdesc" in clusters_df.columns else None,
        labels={"PerCapitaIncome": "Per Capita Income ($)", "ObesityRate": "Obesity Rate (%)"},
        title="State Clusters: Income vs Obesity (with Activity as feature)"
    )
    fig_cluster_scatter.update_traces(textposition="top center")
    fig_cluster_scatter.update_layout(margin=dict(l=10, r=10, t=60, b=10))
    st.plotly_chart(fig_cluster_scatter, use_container_width=True)

    # ------------------------
    # 4) U.S. Map of State Clusters
    # ------------------------
    st.subheader("4) U.S. State Clusters by Income, Obesity, and Activity (2023) — Map")
    # If pre-built HTML present, show and also render a live map if we have abbreviations
    with st.expander("Show saved HTML (if available)"):
        show_html_plot(PATH_PLOT_US_MAP_HTML, height=650)

    map_df = clusters_df.copy()
    if "Locationabbr" not in map_df.columns and "Locationdesc" in map_df.columns:
        # Try attaching abbreviations from the raw BRFSS
        brfss_any = safe_load_csv(PATH_US_OBE_RAW) or safe_load_csv(PATH_US_ACT_RAW)
        if brfss_any is not None and {"Locationdesc", "Locationabbr"}.issubset(brfss_any.columns):
            ab = brfss_any[["Locationdesc", "Locationabbr"]].drop_duplicates()
            map_df = map_df.merge(ab, on="Locationdesc", how="left")

    if "Locationabbr" in map_df.columns:
        # Prefer readable legend if available
        color_arg_map = "ClusterLabel" if "ClusterLabel" in map_df.columns else (map_df["Cluster"].astype(str) if "Cluster" in map_df.columns else None)
        fig_map = px.choropleth(
            map_df,
            locations="Locationabbr",
            locationmode="USA-states",
            color=color_arg_map,
            hover_name="Locationdesc" if "Locationdesc" in map_df.columns else None,
            hover_data={"PerCapitaIncome": True, "ObesityRate": True, "PhysicalActivityRate": True} if set(["PerCapitaIncome","ObesityRate","PhysicalActivityRate"]).issubset(map_df.columns) else None,
            scope="usa",
            title="U.S. State Clusters by Income, Obesity, and Activity (2023)"
        )
        fig_map.update_layout(margin=dict(l=10, r=10, t=60, b=10))
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.info("Could not map states (missing `Locationabbr`). Please ensure abbreviations exist in the data.")

    # ------------------------
    # 5) Global Relationship (2022)
    # ------------------------
    st.subheader("5) Global Relationship: Income vs Obesity (2022)")
    # Prefer merged if present
    global_df = safe_load_csv(PATH_GLOBAL_MERGED)
    if global_df is None:
        g_ob = safe_load_csv(PATH_GLOBAL_OB)
        g_inc = safe_load_csv(PATH_GLOBAL_INC)
        if g_ob is not None and g_inc is not None and "ISO3" in g_ob.columns and "ISO3" in g_inc.columns:
            global_df = g_ob.merge(g_inc, on="ISO3", how="inner")
        else:
            st.error("Global merged data not found and raw components missing. Provide `global_merged_obesity_income.csv` or both raw files.")
            st.stop()

    # Normalize names and columns
    # expected: ISO3, Country (or CountryName), ObesityRate, GDP_per_capita_USD
    col_map = {
        "country_name": "CountryName",
        "Country": "CountryName",
        "NY.GDP.PCAP.CD": "GDP_per_capita_USD"
    }
    global_df = global_df.rename(columns=col_map)
    if "CountryName" not in global_df.columns and "country" in global_df.columns:
        global_df = global_df.rename(columns={"country": "CountryName"})
    if "GDP_per_capita_USD" not in global_df.columns and "value" in global_df.columns:
        global_df = global_df.rename(columns={"value": "GDP_per_capita_USD"})

    # Coerce numerics
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
        labels={"log_GDP_per_capita": "Log10 GDP per Capita (USD)", "ObesityRate": "Obesity Rate (%)"},
        title="Global: Income vs Obesity (2022)"
    )
    fig_global.update_traces(textposition="top center")
    fig_global.update_layout(margin=dict(l=10, r=10, t=60, b=10))
    st.plotly_chart(fig_global, use_container_width=True)
    with st.expander("Show saved HTML (if available)"):
        show_html_plot(PATH_PLOT_GLOBAL_HTML, height=650)

    # Footer
    st.caption("Built with Streamlit • Data: BEA, CDC BRFSS, World Bank, OWID/WHO")
