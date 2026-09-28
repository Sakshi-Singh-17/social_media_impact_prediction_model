# =============================================================================
# pages/8_📄_Report.py
# =============================================================================
import streamlit as st
from pathlib import Path
from utils.constants import APP_CSS, DATASET_PATH, REPORT_PATH
from utils.data import load_data, build_and_train
from utils.charts import eda_charts, feature_importance_chart
from utils.report import generate_word_report

st.set_page_config(page_title="Report", page_icon="📄", layout="wide")
st.markdown(APP_CSS, unsafe_allow_html=True)


if not Path(DATASET_PATH).exists():
    st.error(f"Dataset not found: `{DATASET_PATH}`.")
    st.stop()

with st.spinner("Loading data…"):
    df = load_data()
with st.spinner("Loading model artefacts…"):
    artefacts = build_and_train(df)

st.title("📄 Word Report Generation")
st.markdown("Generates a comprehensive `.docx` report with EDA charts, model results, source code, and AI assistant documentation.")
st.divider()

if st.button("📝 Generate Word Report", use_container_width=True):
    with st.spinner("Generating report — please wait…"):
        try:
            chart_paths      = eda_charts(df)
            feature_importance_chart(artefacts)   # ensures chart exists on disk
            report_bytes     = generate_word_report(df, artefacts, chart_paths)
            st.success("✅ Report generated!")
            st.download_button(
                label="⬇️ Download Report (.docx)",
                data=report_bytes,
                file_name=REPORT_PATH,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
            )
            st.info(
                "Report includes: Cover Page · Abstract · Problem Statement · "
                "Dataset Description · EDA with Charts · Preprocessing · Models · "
                "Evaluation Metrics · Confusion Matrices · Feature Importance · "
                "Prediction System · AI Assistant · Complete Source Code · "
                "Results & Insights · Conclusion."
            )
        except Exception as e:
            st.error(f"Report generation failed: {e}")
            st.exception(e)
