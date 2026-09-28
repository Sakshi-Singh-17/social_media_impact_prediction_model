# =============================================================================
# SakshiSingh_SocialMediaImpactPredictionModel.py
# Author  : Sakshi Singh
# Purpose : Entry-point / Home page for the multi-page Streamlit application.
#
# Project structure
# ─────────────────
# SakshiSingh_SocialMediaImpactPredictionModel.py   ← run this
# Social_media_impact_on_life.csv                   ← dataset (same folder)
# pages/
#   __init__.py
#   _constants.py      shared constants, CSS
#   _data.py           data loading, model training, prediction
#   _charts.py         EDA / CM / feature-importance chart generators
#   _assistant.py      AI chatbot response engine (EN + HI)
#   _report.py         Word report generator
#   1_📊_Dashboard.py
#   2_📈_EDA.py
#   3_⚙️_Preprocessing.py
#   4_🤖_Model_Training.py
#   5_📉_Model_Evaluation.py
#   6_🔮_Prediction.py
#   7_💬_AI_Assistant.py
#   8_📄_Report.py
#
# Run
# ───
#   streamlit run SakshiSingh_SocialMediaImpactPredictionModel.py
#
# Install dependencies
# ────────────────────
#   pip install pandas numpy matplotlib seaborn scikit-learn streamlit python-docx
# =============================================================================

import streamlit as st
from pathlib import Path

# Shared CSS & constants
from utils.constants import APP_CSS, DATASET_PATH

st.set_page_config(
    page_title="Social Media Impact Prediction",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(APP_CSS, unsafe_allow_html=True)


# ── Home / landing page ───────────────────────────────────────────────────────
st.title("📱 Social Media Impact Prediction")
st.markdown("### Machine Learning Classification Project")
st.divider()

st.markdown("""
Welcome! Use the **sidebar** to navigate between pages.

| Page | Description |
|---|---|
| 📊 Dashboard | Dataset preview, statistics, target distribution |
| 📈 EDA | 13 exploratory data analysis charts with insights |
| ⚙️ Preprocessing | Missing values, encoding, train/test split details |
| 🤖 Model Training | Model configs, CV scores, performance comparison |
| 📉 Model Evaluation | Confusion matrices, classification reports, feature importance |
| 🔮 Prediction | Enter student data → get ML prediction + probabilities |
| 💬 AI Assistant | Chat with the AI about your result (English & Hindi) |
| 📄 Report | Generate and download a full Word report (.docx) |
""")

st.divider()

# Quick dataset check
if Path(DATASET_PATH).exists():
    st.success(f"✅ Dataset found: `{DATASET_PATH}`")
else:
    st.error(
        f"❌ Dataset not found: `{DATASET_PATH}`\n\n"
        "Place `Social_media_impact_on_life.csv` in the **same folder** as this script, "
        "then refresh the page."
    )

st.info(
    "💡 **Tip:** Pages load instantly. The model trains once on first launch and is "
    "cached — subsequent page switches are near-instantaneous."
)

st.caption(
    "⚠️ This application provides educational and digital-wellbeing information only. "
    "All ML predictions are statistical patterns — not medical or psychological diagnoses."
)
