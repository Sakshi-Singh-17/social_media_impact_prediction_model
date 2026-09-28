# =============================================================================
# constants.py  — shared constants, palette, column lists, CSS
# =============================================================================
from pathlib import Path

DATASET_PATH = "Social_media_impact_on_life.csv"
REPORT_PATH  = "Social_Media_Impact_Report.docx"
RANDOM_STATE = 42
TEST_SIZE    = 0.20
CHART_DIR    = Path("report_charts")
CHART_DIR.mkdir(exist_ok=True)

TARGET     = "Overall_Impact"
DROP_COLS  = ["Student_ID"]

CAT_COLS = [
    "Gender", "Academic_Level", "Primary_Platform",
    "Device_Type", "Social_Comparison_Frequency",
]
NUM_COLS = [
    "Age", "Daily_Usage_Hours", "Weekend_Extra_Hours",
    "Sleep_Duration_Hours", "Sleep_Quality_Score",
    "Perceived_Stress_Score", "Mental_Health_Index",
    "Academic_Performance_GPA", "Late_Night_Usage_int",
]

PALETTE = {"Beneficial": "#4CAF50", "Neutral": "#FFC107", "Negative": "#F44336"}

PRED_EMOJI = {"Beneficial": "🟢", "Neutral": "🟡", "Negative": "🔴"}

# ---------------------------------------------------------------------------
# Shared CSS injected on every page
# ---------------------------------------------------------------------------
APP_CSS = """
<style>
/* ── Sidebar background ───────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background-color: #e8edf8 !important;
}

/* ── Hide the auto-generated app name / title banner ────────────────────── */
[data-testid="stSidebarHeader"],
[data-testid="stSidebarNavSeparator"],
[data-testid="stSidebarNavItems"] > div:first-child:not(:has([data-testid="stSidebarNavLink"])),
[data-testid="stSidebarNavItems"] > a:not([data-testid="stSidebarNavLink"]),
[data-testid="stSidebarNavItems"] > div > a:not([data-testid="stSidebarNavLink"]),
[data-testid="stSidebarNavItems"] a:not([data-testid="stSidebarNavLink"]):not(:has([data-testid="stSidebarNavLink"])) {
    height: 0 !important;
    max-height: 0 !important;
    overflow: hidden !important;
    margin: 0 !important;
    padding: 0 !important;
    pointer-events: none !important;
}

/* ── Replace app-name link with the label via ::before ─────────── */
[data-testid="stSidebarNavItems"]::before {
    content: "SIDEBAR";
    display: block;
    color: #1a237e;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 16px 12px 8px 12px;
    border-bottom: 2px solid #1a73e8;
    margin-bottom: 6px;
}
.stApp[data-theme="dark"] [data-testid="stSidebarNavItems"]::before {
    color: #93c5fd;
    border-bottom-color: #3b82f6;
}

/* ── Nav link text — light mode ──────────────────────────────────────────── */
[data-testid="stSidebarNavLink"] {
    border-radius: 6px;
}
[data-testid="stSidebarNavLink"] span {
    color: #1a237e !important;
    font-weight: 600 !important;
    font-size: 14px !important;
}
[data-testid="stSidebarNavLink"]:hover {
    background-color: #c9d4f5 !important;
}
[data-testid="stSidebarNavLink"]:hover span {
    color: #0d1857 !important;
}
[data-testid="stSidebarNavLink"][aria-current="page"] {
    background-color: #1a73e8 !important;
}
[data-testid="stSidebarNavLink"][aria-current="page"] span {
    color: #ffffff !important;
}

/* ── Nav link text — dark mode override ──────────────────────────────────── */
.stApp[data-theme="dark"] [data-testid="stSidebar"] {
    background-color: #0f172a !important;
}
.stApp[data-theme="dark"] [data-testid="stSidebarNavLink"] span {
    color: #93c5fd !important;
    font-weight: 500 !important;
}
.stApp[data-theme="dark"] [data-testid="stSidebarNavLink"]:hover {
    background-color: #1e3a5f !important;
}
.stApp[data-theme="dark"] [data-testid="stSidebarNavLink"][aria-current="page"] {
    background-color: #3b82f6 !important;
}
.stApp[data-theme="dark"] [data-testid="stSidebarNavLink"][aria-current="page"] span {
    color: #ffffff !important;
}

/* ── Metric cards ─────────────────────────────────────────────────────────── */
.metric-card {
    background: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px;
    padding: 12px 16px; text-align: center;
}
.metric-card h3 { margin: 0; font-size: 28px; color: #1a73e8; }
.metric-card p  { margin: 0; color: #666; font-size: 13px; }

/* ── Chat bubbles ─────────────────────────────────────────────────────────── */
.chat-user {
    background: #1a73e8; color: white; border-radius: 12px 12px 2px 12px;
    padding: 10px 14px; margin: 4px 0; display: inline-block;
    max-width: 85%; float: right; clear: both; font-size: 14px; line-height: 1.5;
}
.chat-wrapper { overflow: hidden; margin-bottom: 6px; }
</style>
"""
