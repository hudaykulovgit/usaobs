# Machine Learning Final Project Report  
**Course:** 2025 Machine Learning and Text Analytics in Business  
**Instructor:** Assoc. Prof. Hongwei Chuang (GSIM, IUJ)  
**Toolchain:** Google Colab · pandas · scikit-learn · Plotly · Streamlit-ready workflow  
**Slides Referenced:** Data Preprocessing, EDA, Clustering, and K-Means Concepts:contentReference[oaicite:0]{index=0}:contentReference[oaicite:1]{index=1}  

---

## 1. Research Question
**Main Hypothesis:**  
Does per capita income in the United States influence health outcomes—specifically obesity levels—and how does physical activity mediate this relationship?  
Sub-questions:
1. Which U.S. states show high income and low obesity rates?  
2. Does physical activity explain the link between income and obesity?  
3. How does the U.S. pattern compare to global countries?  

---

## 2. Data Collection

### USA Data (from Google Drive)
| Dataset | Description | Source |
|----------|--------------|--------|
| `SAINC1__ALL_AREAS_1929_2024.csv` | Annual personal income by state | BEA |
| `Behavioral_Risk_Factor_Surveillance_System_(BRFSS)_Prevalence_Data_(2011_to_present).csv` | Health indicators (obesity, activity) | CDC |
| `SASUMMARY__ALL_AREAS_1998_2024.csv` | State summary statistics | BEA |
| GeoJSON and definition files | For mapping and metadata | BEA |

### Global Data
| Dataset | Variable | Source |
|----------|-----------|--------|
| `share-of-adults-defined-as-obese.csv` | % adults BMI ≥ 30 | Our World in Data (WHO) |
| World Bank API (`NY.GDP.PCAP.CD`) | GDP per capita (current USD) | World Bank |

All datasets were verified for structure and completeness before processing (as per *Data Preprocessing* step in lecture slides:contentReference[oaicite:2]{index=2}).

---

## 3. Data Cleaning & Merging

### U.S. Data Pipeline
1. **Income:**  
   - Filtered `Per capita personal income (dollars)` from BEA table.  
   - Reshaped wide → long format by year and state.  
   - Focused on **2023** data.

2. **Health:**  
   - Extracted *“BMI Categories” → “Obese (BMI ≥30)”* from BRFSS (2023).  
   - Extracted *“Physical Activity Index / Aerobic Activity” → “Yes”* responses.  
   - Aggregated multiple records per state using mean values.  

3. **Merge:**  
   Combined 2023 `PerCapitaIncome`, `ObesityRate`, and `PhysicalActivityRate` for 47 U.S. states.

```python
Merged dataset shape: (47, 4)
['Locationdesc', 'PerCapitaIncome', 'ObesityRate', 'PhysicalActivityRate']
