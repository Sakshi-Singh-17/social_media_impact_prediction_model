# =============================================================================
# pages/1_📊_Dashboard.py
# =============================================================================
import streamlit as st
from pathlib import Path
from utils.constants import APP_CSS, DATASET_PATH, TARGET
from utils.data import load_data, build_and_train

st.set_page_config(page_title="Dashboard", page_icon="🏠", layout="wide")
st.markdown(APP_CSS, unsafe_allow_html=True)


if not Path(DATASET_PATH).exists():
    st.error(f"Dataset not found: `{DATASET_PATH}`. Place the CSV in the same folder as the main script.")
    st.stop()

with st.spinner("Loading data…"):
    df = load_data()
with st.spinner("Loading model results…"):
    artefacts = build_and_train(df)

st.title("📱 Social Media Impact Prediction")
st.markdown("**Machine Learning Classification Project**")
st.divider()

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown('<div class="metric-card"><h3>4,500</h3><p>Total Records</p></div>',
                unsafe_allow_html=True)
with c2:
    st.markdown('<div class="metric-card"><h3>15</h3><p>Feature Columns</p></div>',
                unsafe_allow_html=True)
with c3:
    st.markdown('<div class="metric-card"><h3>3</h3><p>Impact Classes</p></div>',
                unsafe_allow_html=True)
with c4:
    best_f1 = artefacts["results"][artefacts["best_name"]]["F1-Score"]
    st.markdown(
        f'<div class="metric-card"><h3>{best_f1*100:.1f}%</h3><p>Best Model F1</p></div>',
        unsafe_allow_html=True)

st.divider()
st.subheader("Dataset Preview")
st.dataframe(df.head(10), use_container_width=True)

st.subheader("Descriptive Statistics")
st.dataframe(df.describe(), use_container_width=True)

st.subheader("Target Distribution")
tc = df[TARGET].value_counts().reset_index()
tc.columns = ["Category", "Count"]
tc["Percentage"] = (tc["Count"] / len(df) * 100).round(2)
st.dataframe(tc, use_container_width=True)
