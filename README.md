# ML Final Project: Income and Health Outcomes (Obesity)

**Course:** 2025 Machine Learning and Text Analytics in Business
**Tools:** Google Colab, pandas, scikit-learn, Plotly, Streamlit
**Focus:** Data Preprocessing, EDA, Clustering, and K-Means

---

## Research Question

**Hypothesis:** Does U.S. per capita income influence obesity levels, and how does physical activity mediate this relationship?

**Sub-questions:**
* Identify U.S. states with high income and low obesity rates.
* Determine the role of physical activity in the income-obesity link.
* Compare U.S. patterns to global trends.

---

## Data Sources

| Scope | Source | Data Type | Description |
|:---|:---|:---|:---|
| **U.S.** | BEA | **Personal Income** | Annual per capita income (by state) |
| **U.S.** | CDC (BRFSS) | **Health Indicators** | Obesity and Physical Activity rates |
| **U.S.** | BEA | **Metadata** | State summary statistics and GeoJSON files for mapping |
| **Global** | OWID (WHO) | **Obesity Rate** | Percentage of adults with BMI ≥ 30 |
| **Global** | World Bank API | **Income** | GDP per capita (current USD) |

---

## Data Pipeline (U.S.)

The analysis focuses on **2023** data for **47 U.S. states**.

**Steps:**
1.  **Income:** Filtered BEA data for `Per capita personal income (dollars)`.
2.  **Health:** Extracted *Obese (BMI ≥30)* and *Physical Activity (Yes)* rates from BRFSS, aggregated by mean.
3.  **Merge:** Combined `PerCapitaIncome`, `ObesityRate`, and `PhysicalActivityRate`.

*Final Merged Dataset Shape:* `(47, 4)` with columns: `['Locationdesc', 'PerCapitaIncome', 'ObesityRate', 'PhysicalActivityRate']`
