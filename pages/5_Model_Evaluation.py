# =============================================================================
# pages/5_📉_Model_Evaluation.py
# =============================================================================
import streamlit as st
from pathlib import Path
from utils.constants import APP_CSS, DATASET_PATH, CHART_DIR
from utils.data import load_data, build_and_train
from utils.charts import cm_chart, feature_importance_chart

st.set_page_config(page_title="Model Evaluation", page_icon="📉", layout="wide")
st.markdown(APP_CSS, unsafe_allow_html=True)


if not Path(DATASET_PATH).exists():
    st.error(f"Dataset not found: `{DATASET_PATH}`.")
    st.stop()

with st.spinner("Loading data…"):
    df = load_data()
with st.spinner("Loading model artefacts…"):
    artefacts = build_and_train(df)

# Generate feature importance chart to disk (skipped if already exists)
fi_path = feature_importance_chart(artefacts)

st.title("📉 Model Evaluation")
st.divider()

le_classes = list(artefacts["le"].classes_)

for mname, mres in artefacts["results"].items():
    st.subheader(f"🔹 {mname}")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Accuracy",  f"{mres['Accuracy']*100:.2f}%")
    c2.metric("Precision", f"{mres['Precision']*100:.2f}%")
    c3.metric("Recall",    f"{mres['Recall']*100:.2f}%")
    c4.metric("F1-Score",  f"{mres['F1-Score']*100:.2f}%")

    cm_buf = cm_chart(mres["cm"], le_classes, mname)
    col_cm, col_cr = st.columns([1, 1.6])
    with col_cm:
        st.image(cm_buf, caption=f"Confusion Matrix — {mname}", use_container_width=True)
    with col_cr:
        st.text("Classification Report")
        st.code(mres["cr"])
    st.divider()

if fi_path and Path(fi_path).exists():
    st.subheader("Feature Importance (Random Forest)")
    st.image(str(fi_path), use_container_width=True)
    st.info("💡 Mental Health Index and Perceived Stress Score are the strongest predictors, "
            "followed by Sleep Duration and GPA.")
