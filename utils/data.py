# =============================================================================
# data.py  — data loading, model training, prediction  (all @st.cache_*)
# =============================================================================
import warnings
import numpy as np
import pandas as pd
import streamlit as st

from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report,
)
from sklearn.utils.class_weight import compute_class_weight

from .constants import (
    DATASET_PATH, RANDOM_STATE, TEST_SIZE,
    TARGET, DROP_COLS, CAT_COLS, NUM_COLS,
)

warnings.filterwarnings("ignore")


@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATASET_PATH)
    df["Late_Night_Usage_int"] = df["Late_Night_Usage"].astype(int)
    return df


@st.cache_resource(show_spinner=False)
def build_and_train(df: pd.DataFrame) -> dict:
    """Full preprocessing → train three classifiers → return artefacts dict."""
    X = df.drop(columns=DROP_COLS + [TARGET, "Late_Night_Usage"])
    y = df[TARGET]

    le    = LabelEncoder()
    y_enc = le.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y_enc, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y_enc
    )

    num_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler",  StandardScaler()),
    ])
    preprocessor = ColumnTransformer(transformers=[
        ("num", num_pipeline, NUM_COLS),
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CAT_COLS),
    ])

    classes       = np.unique(y_enc)
    class_weights = compute_class_weight("balanced", classes=classes, y=y_enc)

    models = {
        "Logistic Regression": Pipeline([
            ("pre", preprocessor),
            ("clf", LogisticRegression(
                max_iter=1000, random_state=RANDOM_STATE,
                class_weight="balanced", C=1.0)),
        ]),
        "Decision Tree": Pipeline([
            ("pre", preprocessor),
            ("clf", DecisionTreeClassifier(
                max_depth=8, min_samples_leaf=10,
                random_state=RANDOM_STATE, class_weight="balanced")),
        ]),
        "Random Forest": Pipeline([
            ("pre", preprocessor),
            ("clf", RandomForestClassifier(
                n_estimators=200, max_depth=10, min_samples_leaf=5,
                random_state=RANDOM_STATE, class_weight="balanced", n_jobs=-1)),
        ]),
    }

    results   = {}
    trained   = {}
    cv_scores = {}
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)

    for name, pipe in models.items():
        pipe.fit(X_train, y_train)
        y_pred = pipe.predict(X_test)

        results[name] = {
            "Accuracy":  accuracy_score(y_test, y_pred),
            "Precision": precision_score(y_test, y_pred, average="weighted", zero_division=0),
            "Recall":    recall_score(y_test, y_pred, average="weighted", zero_division=0),
            "F1-Score":  f1_score(y_test, y_pred, average="weighted", zero_division=0),
            "cm":        confusion_matrix(y_test, y_pred),
            "cr":        classification_report(y_test, y_pred,
                                               target_names=le.classes_, zero_division=0),
        }
        trained[name]   = pipe
        cv_scores[name] = cross_val_score(
            pipe, X, y_enc, cv=skf, scoring="f1_weighted", n_jobs=-1
        )

    results_df = pd.DataFrame(
        {k: {m: v for m, v in v.items() if m not in ("cm", "cr")}
         for k, v in results.items()}
    ).T.reset_index().rename(columns={"index": "Model"})

    best_name  = results_df.sort_values("F1-Score", ascending=False).iloc[0]["Model"]

    return {
        "X_train": X_train, "X_test": X_test,
        "y_train": y_train, "y_test": y_test,
        "le": le,
        "models": trained, "results": results,
        "results_df": results_df, "cv_scores": cv_scores,
        "best_name": best_name, "best_model": trained[best_name],
        "feature_num_cols": NUM_COLS,
        "feature_cat_cols": CAT_COLS,
    }


def predict_impact(artefacts: dict, input_dict: dict) -> dict:
    row = pd.DataFrame([input_dict])
    for c in artefacts["feature_num_cols"]:
        if c in row.columns:
            row[c] = pd.to_numeric(row[c], errors="coerce")

    best_pipe = artefacts["best_model"]
    le        = artefacts["le"]
    pred_enc  = best_pipe.predict(row)[0]
    label     = le.inverse_transform([pred_enc])[0]

    proba = None
    if hasattr(best_pipe.named_steps["clf"], "predict_proba"):
        raw   = best_pipe.predict_proba(row)[0]
        proba = {le.inverse_transform([i])[0]: round(float(p), 4)
                 for i, p in enumerate(raw)}

    return {"label": label, "probabilities": proba}
