# =============================================================================
# charts.py  — all chart generators: EDA, confusion matrix, feature importance
# =============================================================================
import io
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from .constants import TARGET, PALETTE, CHART_DIR


# ── helpers ──────────────────────────────────────────────────────────────────
def _fig_to_buf(fig) -> io.BytesIO:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=120)
    buf.seek(0)
    plt.close(fig)
    return buf


def _save(fig, name: str):
    path = CHART_DIR / f"{name}.png"
    fig.savefig(path, bbox_inches="tight", dpi=120)
    plt.close(fig)
    return path


# ── EDA charts (cached to disk; only regenerated when files are absent) ──────
def eda_charts(df) -> dict:
    """
    Generate all 13 EDA charts. Returns {key: Path} dict.
    If the PNG already exists on disk it is reused — making EDA page instant
    on every reload after the first run.
    """
    charts = {}
    sns.set_theme(style="whitegrid")
    order  = ["Beneficial", "Neutral", "Negative"]
    colors = [PALETTE[o] for o in order]

    def _need(name: str):
        p = CHART_DIR / f"{name}.png"
        return not p.exists(), p

    # 01 target distribution
    regen, path = _need("01_target_dist")
    if regen:
        fig, ax = plt.subplots(figsize=(7, 4))
        counts = df[TARGET].value_counts().reindex(order)
        ax.bar(order, counts.values, color=colors, edgecolor="white", linewidth=0.8)
        for i, v in enumerate(counts.values):
            ax.text(i, v + 20, str(v), ha="center", fontsize=10, fontweight="bold")
        ax.set_title("Overall Impact Distribution", fontsize=13, fontweight="bold")
        ax.set_xlabel("Overall Impact"); ax.set_ylabel("Count")
        _save(fig, "01_target_dist")
    charts["target_dist"] = path

    # 02 daily usage hours
    regen, path = _need("02_daily_usage")
    if regen:
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.hist(df["Daily_Usage_Hours"].dropna(), bins=25, color="#3F51B5",
                edgecolor="white", linewidth=0.6)
        ax.set_title("Daily Usage Hours Distribution", fontsize=13, fontweight="bold")
        ax.set_xlabel("Hours"); ax.set_ylabel("Count")
        _save(fig, "02_daily_usage")
    charts["daily_usage"] = path

    # 03 sleep duration
    regen, path = _need("03_sleep_dur")
    if regen:
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.hist(df["Sleep_Duration_Hours"].dropna(), bins=25, color="#009688",
                edgecolor="white", linewidth=0.6)
        ax.set_title("Sleep Duration Distribution", fontsize=13, fontweight="bold")
        ax.set_xlabel("Hours"); ax.set_ylabel("Count")
        _save(fig, "03_sleep_dur")
    charts["sleep_dur"] = path

    # 04 stress
    regen, path = _need("04_stress")
    if regen:
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.hist(df["Perceived_Stress_Score"].dropna(), bins=20, color="#E91E63",
                edgecolor="white", linewidth=0.6)
        ax.set_title("Perceived Stress Score Distribution", fontsize=13, fontweight="bold")
        ax.set_xlabel("Score"); ax.set_ylabel("Count")
        _save(fig, "04_stress")
    charts["stress"] = path

    # 05 GPA
    regen, path = _need("05_gpa")
    if regen:
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.hist(df["Academic_Performance_GPA"].dropna(), bins=25, color="#FF9800",
                edgecolor="white", linewidth=0.6)
        ax.set_title("Academic Performance GPA Distribution", fontsize=13, fontweight="bold")
        ax.set_xlabel("GPA"); ax.set_ylabel("Count")
        _save(fig, "05_gpa")
    charts["gpa"] = path

    # 06-10 box plots
    boxplots = [
        ("06_usage_vs_impact",  "Daily_Usage_Hours",         "usage_vs_impact",  "Daily Usage Hours vs Overall Impact"),
        ("07_sleep_vs_impact",  "Sleep_Duration_Hours",      "sleep_vs_impact",  "Sleep Duration vs Overall Impact"),
        ("08_stress_vs_impact", "Perceived_Stress_Score",    "stress_vs_impact", "Perceived Stress Score vs Overall Impact"),
        ("09_mhi_vs_impact",    "Mental_Health_Index",       "mhi_vs_impact",    "Mental Health Index vs Overall Impact"),
        ("10_gpa_vs_impact",    "Academic_Performance_GPA",  "gpa_vs_impact",    "Academic Performance GPA vs Overall Impact"),
    ]
    for fname, col, key, title in boxplots:
        regen, path = _need(fname)
        if regen:
            fig, ax = plt.subplots(figsize=(7, 4))
            sns.boxplot(data=df, x=TARGET, y=col, order=order, palette=PALETTE, ax=ax)
            ax.set_title(title, fontsize=13, fontweight="bold")
            ax.set_xlabel("Overall Impact"); ax.set_ylabel(col)
            _save(fig, fname)
        charts[key] = path

    # 11 categorical features
    regen, path = _need("11_cat_features")
    if regen:
        cat_cols = ["Gender", "Academic_Level", "Primary_Platform",
                    "Device_Type", "Social_Comparison_Frequency"]
        fig, axes = plt.subplots(2, 3, figsize=(16, 9))
        axes = axes.flatten()
        for i, col in enumerate(cat_cols):
            ct = df.groupby([col, TARGET]).size().unstack(fill_value=0)
            ct = ct.reindex(columns=[c for c in order if c in ct.columns])
            ct.plot(kind="bar", ax=axes[i],
                    color=[PALETTE[c] for c in ct.columns],
                    edgecolor="white", linewidth=0.6, legend=(i == 0))
            axes[i].set_title(f"{col} vs Overall Impact", fontsize=10, fontweight="bold")
            axes[i].set_xlabel(col); axes[i].set_ylabel("Count")
            axes[i].tick_params(axis="x", rotation=30)
        axes[5].axis("off")
        fig.suptitle("Categorical Feature Distributions by Overall Impact",
                     fontsize=13, fontweight="bold", y=1.01)
        fig.tight_layout()
        _save(fig, "11_cat_features")
    charts["cat_features"] = path

    # 12 correlation heatmap
    regen, path = _need("12_corr_heatmap")
    if regen:
        num_df = df[["Age", "Daily_Usage_Hours", "Weekend_Extra_Hours",
                     "Sleep_Duration_Hours", "Sleep_Quality_Score",
                     "Perceived_Stress_Score", "Mental_Health_Index",
                     "Academic_Performance_GPA"]].dropna()
        fig, ax = plt.subplots(figsize=(9, 7))
        mask = np.triu(np.ones_like(num_df.corr(), dtype=bool))
        sns.heatmap(num_df.corr(), mask=mask, annot=True, fmt=".2f",
                    cmap="coolwarm", linewidths=0.5, ax=ax, annot_kws={"size": 8})
        ax.set_title("Correlation Heatmap (Numerical Features)", fontsize=13, fontweight="bold")
        _save(fig, "12_corr_heatmap")
    charts["corr_heatmap"] = path

    # 13 late night usage
    regen, path = _need("13_lnu_vs_impact")
    if regen:
        fig, ax = plt.subplots(figsize=(6, 4))
        lnu = df.groupby(["Late_Night_Usage", TARGET]).size().unstack(fill_value=0)
        lnu = lnu.reindex(columns=[c for c in order if c in lnu.columns])
        lnu.index = ["No Late Night", "Late Night"]
        lnu.plot(kind="bar", ax=ax, color=[PALETTE[c] for c in lnu.columns],
                 edgecolor="white", linewidth=0.6)
        ax.set_title("Late Night Usage vs Overall Impact", fontsize=13, fontweight="bold")
        ax.set_xlabel("Late Night Usage"); ax.set_ylabel("Count")
        ax.tick_params(axis="x", rotation=0)
        _save(fig, "13_lnu_vs_impact")
    charts["lnu_vs_impact"] = path

    return charts


def cm_chart(cm, classes: list, title: str) -> io.BytesIO:
    """Return a BytesIO PNG of a confusion-matrix heatmap."""
    fig, ax = plt.subplots(figsize=(5, 4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=classes, yticklabels=classes,
                ax=ax, linewidths=0.5)
    ax.set_title(title, fontsize=11, fontweight="bold")
    ax.set_xlabel("Predicted"); ax.set_ylabel("Actual")
    fig.tight_layout()
    buf  = _fig_to_buf(fig)
    # also save to disk for report
    path = CHART_DIR / f"cm_{title.replace(' ', '_').lower()}.png"
    if not path.exists():
        fig2, ax2 = plt.subplots(figsize=(5, 4))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                    xticklabels=classes, yticklabels=classes,
                    ax=ax2, linewidths=0.5)
        ax2.set_title(title, fontsize=11, fontweight="bold")
        ax2.set_xlabel("Predicted"); ax2.set_ylabel("Actual")
        fig2.tight_layout()
        _save(fig2, f"cm_{title.replace(' ', '_').lower()}")
    return buf


def feature_importance_chart(artefacts: dict):
    """Save and return path of feature importance bar chart (RF only)."""
    path = CHART_DIR / "14_feature_importance.png"
    if path.exists():
        return path
    rf_pipe = artefacts["models"].get("Random Forest")
    if rf_pipe is None:
        return None
    ohe_cats   = (rf_pipe.named_steps["pre"]
                         .named_transformers_["cat"]
                         .get_feature_names_out(artefacts["feature_cat_cols"]))
    feat_names = list(artefacts["feature_num_cols"]) + list(ohe_cats)
    importances= rf_pipe.named_steps["clf"].feature_importances_
    import pandas as pd
    imp_df = (pd.DataFrame({"Feature": feat_names, "Importance": importances})
                .sort_values("Importance", ascending=False).head(15))
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(imp_df["Feature"][::-1], imp_df["Importance"][::-1],
            color="#3F51B5", edgecolor="white")
    ax.set_title("Top 15 Feature Importances (Random Forest)", fontsize=13, fontweight="bold")
    ax.set_xlabel("Importance")
    fig.tight_layout()
    _save(fig, "14_feature_importance")
    return path
