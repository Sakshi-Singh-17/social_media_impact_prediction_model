# =============================================================================
# pages/6_🔮_Prediction.py
# =============================================================================
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import streamlit as st
from pathlib import Path
from utils.constants import APP_CSS, DATASET_PATH
from utils.data import load_data, build_and_train, predict_impact

st.set_page_config(page_title="Prediction", page_icon="🔮", layout="wide")
st.markdown(APP_CSS, unsafe_allow_html=True)


if not Path(DATASET_PATH).exists():
    st.error(f"Dataset not found: `{DATASET_PATH}`.")
    st.stop()

with st.spinner("Loading data…"):
    df = load_data()
with st.spinner("Loading model artefacts…"):
    artefacts = build_and_train(df)

st.title("🔮 Predict Overall Impact")
st.markdown("Fill in the student details and click **Predict**.")
st.divider()

with st.form("prediction_form"):
    c1, c2, c3 = st.columns(3)
    with c1:
        age        = st.number_input("Age", 14, 30, 19)
        gender     = st.selectbox("Gender",
                       ["Female", "Male", "Non-Binary", "Prefer not to say"])
        acad_level = st.selectbox("Academic Level",
                       ["High School", "Undergraduate", "Postgraduate"])
        platform   = st.selectbox("Primary Platform",
                       ["Instagram", "TikTok", "YouTube", "Snapchat",
                        "LinkedIn", "Reddit", "X (Twitter)"])
    with c2:
        daily_hrs  = st.slider("Daily Usage Hours", 0.0, 16.0, 5.0, 0.5)
        wknd_hrs   = st.slider("Weekend Extra Hours", 0.0, 8.0, 1.5, 0.5)
        device     = st.selectbox("Device Type",
                       ["Smartphone", "Tablet", "Laptop/PC"])
        sleep_hrs  = st.slider("Sleep Duration Hours", 3.0, 11.0, 7.0, 0.5)
    with c3:
        sleep_qual = st.slider("Sleep Quality Score (1–5)", 1, 5, 3)
        late_night = st.selectbox("Late Night Usage", ["Yes", "No"])
        soc_comp   = st.selectbox("Social Comparison Frequency",
                       ["Never", "Rarely", "Sometimes", "Frequently", "Always"])
        stress     = st.slider("Perceived Stress Score", 5.0, 30.0, 17.0, 0.5)
        mhi        = st.slider("Mental Health Index", 30, 100, 75)
        gpa        = st.slider("Academic Performance GPA", 1.9, 4.0, 3.4, 0.05)

    submit = st.form_submit_button("🔮 Predict Overall Impact", use_container_width=True)

if submit:
    input_dict = {
        "Age": age, "Gender": gender, "Academic_Level": acad_level,
        "Primary_Platform": platform, "Daily_Usage_Hours": daily_hrs,
        "Weekend_Extra_Hours": wknd_hrs, "Device_Type": device,
        "Sleep_Duration_Hours": sleep_hrs, "Sleep_Quality_Score": sleep_qual,
        "Late_Night_Usage_int": 1 if late_night == "Yes" else 0,
        "Social_Comparison_Frequency": soc_comp,
        "Perceived_Stress_Score": stress,
        "Mental_Health_Index": mhi, "Academic_Performance_GPA": gpa,
    }
    result = predict_impact(artefacts, input_dict)
    label  = result["label"]

    # Persist for AI Assistant
    st.session_state["last_prediction"] = {
        "label": label, "input_dict": input_dict,
        "probabilities": result.get("probabilities"),
    }
    st.session_state["chat_history"] = []   # reset chat on new prediction

    color_map = {"Beneficial": "🟢", "Neutral": "🟡", "Negative": "🔴"}
    st.success(f"## {color_map.get(label,'🔵')} Predicted Overall Impact: **{label}**")

    if result["probabilities"]:
        import pandas as pd
        st.subheader("Prediction Probabilities")
        prob_df = (pd.DataFrame(list(result["probabilities"].items()),
                                columns=["Class", "Probability"])
                   .sort_values("Probability", ascending=False))
        prob_df["Probability %"] = (prob_df["Probability"] * 100).round(2)
        st.dataframe(prob_df[["Class", "Probability %"]], use_container_width=True)

        fig, ax = plt.subplots(figsize=(5, 2.5))
        ax.barh(prob_df["Class"], prob_df["Probability"],
                color=["#4CAF50", "#FFC107", "#F44336"][:len(prob_df)])
        ax.set_xlim(0, 1); ax.set_xlabel("Probability"); ax.set_title("Class Probabilities")
        st.pyplot(fig, use_container_width=False)
        plt.close(fig)

    st.info("💬 Navigate to **AI Assistant** in the sidebar to ask questions about your result in English or Hindi!")
    st.warning("⚠️ **Disclaimer**: Statistical prediction only — not a medical or psychological diagnosis.")
