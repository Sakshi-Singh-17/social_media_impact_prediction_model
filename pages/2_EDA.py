# =============================================================================
# pages/2_📈_EDA.py
# =============================================================================
import streamlit as st
from pathlib import Path
from utils.constants import APP_CSS, DATASET_PATH
from utils.data import load_data
from utils.charts import eda_charts

st.set_page_config(page_title="EDA", page_icon="📈", layout="wide")
st.markdown(APP_CSS, unsafe_allow_html=True)


if not Path(DATASET_PATH).exists():
    st.error(f"Dataset not found: `{DATASET_PATH}`.")
    st.stop()

with st.spinner("Loading data…"):
    df = load_data()

# Charts are written to disk on first run and reused thereafter — instant reload
with st.spinner("Preparing charts…"):
    chart_paths = eda_charts(df)

st.title("📈 Exploratory Data Analysis")
st.markdown("All charts are generated from the actual dataset and cached to disk.")
st.divider()

chart_meta = [
    ("target_dist",     "Overall Impact Distribution",
     "Dataset is heavily skewed toward 'Beneficial' (≈82%). Class imbalance must be handled during training."),
    ("daily_usage",     "Daily Usage Hours Distribution",
     "Usage hours follow a roughly bell-shaped distribution centred around 5–7 hours."),
    ("sleep_dur",       "Sleep Duration Distribution",
     "Most students sleep 6–8 hours."),
    ("stress",          "Perceived Stress Score Distribution",
     "Stress clusters at 15–22. Higher scores correlate with Negative impact."),
    ("gpa",             "Academic Performance GPA Distribution",
     "GPA concentrated between 3.0–4.0."),
    ("usage_vs_impact", "Daily Usage Hours vs Overall Impact",
     "Negative-impact students show slightly higher median usage — but overlap is large."),
    ("sleep_vs_impact", "Sleep Duration vs Overall Impact",
     "Better-rested students trend toward Beneficial impact."),
    ("stress_vs_impact","Perceived Stress Score vs Overall Impact",
     "Negative-impact students report notably higher stress."),
    ("mhi_vs_impact",   "Mental Health Index vs Overall Impact",
     "Higher Mental Health Index is clearly associated with Beneficial impact."),
    ("gpa_vs_impact",   "GPA vs Overall Impact",
     "Modest but consistent GPA differences across categories."),
    ("cat_features",    "Categorical Feature Distributions",
     "No single platform dominates the Negative category — behavioural patterns matter more."),
    ("corr_heatmap",    "Correlation Heatmap",
     "MHI and Sleep Quality positively correlate with GPA; Stress inversely."),
    ("lnu_vs_impact",   "Late Night Usage vs Overall Impact",
     "Late-night users appear more frequently in Neutral and Negative categories."),
]

for key, title, insight in chart_meta:
    path = chart_paths.get(key)
    st.subheader(title)
    if path and Path(path).exists():
        st.image(str(path), use_container_width=True)
    st.info(f"💡 {insight}")
    st.divider()
