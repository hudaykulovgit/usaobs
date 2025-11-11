# Income and Health Outcomes (Obesity Analysis)

A Machine Learning and Data Visualization project exploring how per capita income affects obesity and physical activity across U.S. states and countries worldwide.

## 📊 Features
- Interactive Plotly visualizations
- K-Means clustering of U.S. states by health and economic indicators
- Global comparison (income vs obesity, 2022)
- Clean Streamlit layout with sidebar navigation

## 📁 Folder Structure
Streamlit/
│
├── app.py
├── requirements.txt
├── README.md
│
├── data/
│ ├── us_health_income_2023.csv
│ ├── global_merged_obesity_income.csv
│ └── ...
│
├── results/
│ ├── us_clusters_2023.csv
│ └── us_cluster_summary.csv
│
└── plots/
├── us_clusters_map.html
└── global_income_obesity_interactive.html


## 🚀 Run Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/<yourusername>/Income-Obesity-Analysis.git
   cd Income-Obesity-Analysis


Install dependencies:

pip install -r requirements.txt


Launch Streamlit:

streamlit run app.py


Then open the provided local URL in your browser.
🌐 Deploy to Streamlit Cloud

Push all files to GitHub, then go to streamlit.io/cloud
 and connect your repo — Streamlit will automatically detect app.py and requirements.txt.

Data Sources:

Bureau of Economic Analysis (BEA)

CDC BRFSS

World Bank API

WHO Global Health Observatory / Our World in Data

Developed in Google Colab & Streamlit — 2025