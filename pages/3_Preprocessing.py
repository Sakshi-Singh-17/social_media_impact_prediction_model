# =============================================================================
# pages/3_⚙️_Preprocessing.py
# =============================================================================
import pandas as pd
import streamlit as st
from pathlib import Path
from utils.constants import APP_CSS, DATASET_PATH, NUM_COLS, CAT_COLS
from utils.data import load_data, build_and_train

st.set_page_config(page_title="Preprocessing", page_icon="⚙️", layout="wide")
st.markdown(APP_CSS, unsafe_allow_html=True)


if not Path(DATASET_PATH).exists():
    st.error(f"Dataset not found: `{DATASET_PATH}`.")
    st.stop()

with st.spinner("Loading data…"):
    df = load_data()
with st.spinner("Loading model artefacts…"):
    artefacts = build_and_train(df)

st.title("⚙️ Data Preprocessing")
st.divider()

col1, col2 = st.columns(2)
with col1:
    st.subheader("Missing Values")
    mv = df.isnull().sum().reset_index()
    mv.columns = ["Column", "Missing Count"]
    mv["Missing %"] = (mv["Missing Count"] / len(df) * 100).round(2)
    st.dataframe(mv[mv["Missing Count"] > 0], use_container_width=True)
with col2:
    st.subheader("Duplicate Records")
    st.metric("Duplicates Found", int(df.duplicated().sum()))

st.subheader("Numerical Features  →  StandardScaler")
st.code(str(NUM_COLS))

st.subheader("Categorical Features  →  OneHotEncoder")
st.code(str(CAT_COLS))

st.subheader("Target Variable Encoding")
le = artefacts["le"]
st.dataframe(pd.DataFrame({"Class": le.classes_,
                            "Encoded Value": range(len(le.classes_))}),
             use_container_width=True)

st.subheader("Train / Test Split")
col3, col4 = st.columns(2)
col3.metric("Training Samples", len(artefacts["X_train"]))
col4.metric("Testing Samples",  len(artefacts["X_test"]))

st.subheader("Class Distribution in Training Set")
train_dist = (pd.Series(artefacts["y_train"])
              .map(dict(enumerate(le.classes_)))
              .value_counts().reset_index())
train_dist.columns = ["Class", "Count"]
st.dataframe(train_dist, use_container_width=True)
