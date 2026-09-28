# =============================================================================
# pages/4_🤖_Model_Training.py
# =============================================================================
import pandas as pd
import streamlit as st
from pathlib import Path
from utils.constants import APP_CSS, DATASET_PATH
from utils.data import load_data, build_and_train

st.set_page_config(page_title="Model Training", page_icon="🤖", layout="wide")
st.markdown(APP_CSS, unsafe_allow_html=True)


if not Path(DATASET_PATH).exists():
    st.error(f"Dataset not found: `{DATASET_PATH}`.")
    st.stop()

with st.spinner("Loading data…"):
    df = load_data()
with st.spinner("Loading model artefacts…"):
    artefacts = build_and_train(df)

st.title("🤖 Model Training")
st.divider()
st.markdown("Three classifiers trained on an 80/20 stratified split with balanced class weights.")

st.subheader("Model Configuration")
st.dataframe(pd.DataFrame({
    "Model": ["Logistic Regression", "Decision Tree", "Random Forest"],
    "Key Hyperparameters": [
        "C=1.0, max_iter=1000, class_weight=balanced",
        "max_depth=8, min_samples_leaf=10, class_weight=balanced",
        "n_estimators=200, max_depth=10, min_samples_leaf=5, class_weight=balanced",
    ]
}), use_container_width=True)

st.subheader("5-Fold Stratified Cross-Validation — F1-Weighted")
for mname, cv_arr in artefacts["cv_scores"].items():
    st.markdown(f"**{mname}**: Mean = `{cv_arr.mean()*100:.2f}%` | Std = `{cv_arr.std()*100:.2f}%`")

st.subheader("Performance Comparison (Test Set)")
res = artefacts["results_df"].copy()
for col in ["Accuracy", "Precision", "Recall", "F1-Score"]:
    res[col] = res[col].apply(lambda x: f"{float(x)*100:.2f}%")
st.dataframe(res, use_container_width=True)

st.success(f"✅ Best Model: **{artefacts['best_name']}** (highest weighted F1-Score)")
