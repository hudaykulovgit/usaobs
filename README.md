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

| Scope | Source | Dataset/Variable | Description |
|:---|:---|:---|:---|
| **U.S.** | BEA | `SAINC1__ALL_AREAS_1929_2024` | Annual per capita personal income (by state) |
| **U.S.** | CDC (BRFSS) | `Behavioral_Risk_Factor_Surveillance_System...` | Health indicators (Obesity, Physical Activity) |
| **U.S.** | BEA | `SASUMMARY__ALL_AREAS_1998_2024` | State summary statistics |
| **U.S.** | BEA | GeoJSON and definition files | For mapping and metadata |
| **Global** | OWID (WHO) | `share-of-adults-defined-as-obese` | % adults with BMI ≥ 30 (Obesity Rate) |
| **Global** | World Bank API | `NY.GDP.PCAP.CD` | GDP per capita (current USD) |

---

## Data Pipeline (U.S.)

The analysis focuses on **2023** data for **47 U.S. states**.

**Steps:**
1.  **Income:** Filtered BEA data for `Per capita personal income (dollars)`.
2.  **Health:** Extracted *Obese (BMI ≥30)* and *Physical Activity (Yes)* rates from BRFSS, aggregated by mean.
3.  **Merge:** Combined `PerCapitaIncome`, `ObesityRate`, and `PhysicalActivityRate`.

*Final Merged Dataset Shape:* `(47, 4)` with columns: `['Locationdesc', 'PerCapitaIncome', 'ObesityRate', 'PhysicalActivityRate']`
