"""
YouTube Data Dashboard — Streamlit Application
===============================================
Interactive dashboard to explore YouTube video data: views, likes,
comments, engagement, publishing trends, and top performers.

Run:
    streamlit run app.py
"""

from __future__ import annotations

import io
from typing import Optional

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# ---------------------------------------------------------------------------
# Page configuration & styling
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="YouTube Data Dashboard",
    page_icon="📺",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
    .main { background-color: #0e1117; }
    .metric-card {
        background: linear-gradient(135deg, #1f1f2e 0%, #111827 100%);
        padding: 1.25rem 1.5rem;
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.06);
        box-shadow: 0 4px 18px rgba(0,0,0,0.4);
        color: #f9fafb;
    }
    .metric-card h4 {
        margin: 0 0 .35rem 0;
        font-size: 0.8rem;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: .06em;
    }
    .metric-card .value {
        font-size: 1.7rem;
        font-weight: 700;
        color: #ef4444;
    }
    .section-title {
        border-left: 4px solid #ef4444;
        padding-left: .75rem;
        margin: 1.25rem 0 .75rem 0;
    }
    .insight {
        background: #111827;
        padding: .9rem 1.1rem;
        border-radius: 10px;
        border-left: 3px solid #ef4444;
        margin-bottom: .6rem;
        color: #e5e7eb;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

EXPECTED_COLUMNS = [
    "Video_ID", "Title", "Channel", "Category", "Published_Date",
    "Views", "Likes", "Comments", "Duration_Minutes",
]


# ---------------------------------------------------------------------------
# Data loading & cleaning
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_csv(file_bytes: bytes) -> pd.DataFrame:
    return pd.read_csv(io.BytesIO(file_bytes))


@st.cache_data(show_spinner=False)
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Deduplicate, coerce types and handle missing values."""
    df = df.copy()

    for col in EXPECTED_COLUMNS:
        if col not in df.columns:
            df[col] = np.nan

    df = df.drop_duplicates()

    # Numeric coercion
    for col in ["Views", "Likes", "Comments", "Duration_Minutes"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Dates
    df["Published_Date"] = pd.to_datetime(df["Published_Date"], errors="coerce")

    # Text columns
    for col in ["Video_ID", "Title", "Channel", "Category"]:
        df[col] = df[col].astype(str).str.strip().replace({"nan": np.nan, "": np.nan})

    # Fill missing
    df["Views"] = df["Views"].fillna(0).astype(int)
    df["Likes"] = df["Likes"].fillna(0).astype(int)
    df["Comments"] = df["Comments"].fillna(0).astype(int)
    df["Duration_Minutes"] = df["Duration_Minutes"].fillna(df["Duration_Minutes"].median())
    df["Category"] = df["Category"].fillna("Unknown")
    df["Channel"] = df["Channel"].fillna("Unknown")
    df["Title"] = df["Title"].fillna("Untitled")

    df = df.dropna(subset=["Published_Date"])
    df["Year"] = df["Published_Date"].dt.year
    df["Month"] = df["Published_Date"].dt.to_period("M").astype(str)

    # Derived metric — engagement rate (%)
    df["Engagement_Rate"] = np.where(
        df["Views"] > 0,
        (df["Likes"] + df["Comments"]) / df["Views"] * 100,
        0.0,
    )

    return df.reset_index(drop=True)


# ---------------------------------------------------------------------------
# UI helpers
# ---------------------------------------------------------------------------
def metric_card(title: str, value: str) -> str:
    return f"<div class='metric-card'><h4>{title}</h4><div class='value'>{value}</div></div>"


def section(title: str) -> None:
    st.markdown(f"<h3 class='section-title'>{title}</h3>", unsafe_allow_html=True)


def fmt_num(n: float) -> str:
    n = float(n)
    for unit in ["", "K", "M", "B"]:
        if abs(n) < 1000:
            return f"{n:.1f}{unit}" if unit else f"{int(n):,}"
        n /= 1000
    return f"{n:.1f}T"


# ---------------------------------------------------------------------------
# Sidebar — upload & navigation
# ---------------------------------------------------------------------------
st.sidebar.title("📺 YouTube Dashboard")
st.sidebar.caption("Upload a YouTube CSV and explore the data.")

page = st.sidebar.radio("Navigation", ["Dashboard", "Visualizations", "Top Performers", "Insights", "Data"])
uploaded = st.sidebar.file_uploader("Upload CSV", type=["csv"])

st.sidebar.markdown("---")
st.sidebar.caption("Expected columns:")
st.sidebar.code(", ".join(EXPECTED_COLUMNS), language="text")


def get_dataframe() -> Optional[pd.DataFrame]:
    if uploaded is not None:
        try:
            return clean_data(load_csv(uploaded.getvalue()))
        except Exception as exc:
            st.sidebar.error(f"Failed to parse CSV: {exc}")
            return None
    try:
        return clean_data(pd.read_csv("data/youtube_data.csv"))
    except Exception:
        return None


df = get_dataframe()

if df is None or df.empty:
    st.title("📺 YouTube Data Dashboard")
    st.info("Upload a CSV from the sidebar to get started, "
            "or drop a `data/youtube_data.csv` next to `app.py`.")
    st.stop()

# Filters
st.sidebar.markdown("---")
st.sidebar.subheader("Filters")

cats = sorted(df["Category"].dropna().unique().tolist())
sel_cats = st.sidebar.multiselect("Category", cats, default=[])

dmin, dmax = df["Published_Date"].min().date(), df["Published_Date"].max().date()
sel_dates = st.sidebar.date_input("Date range", (dmin, dmax), min_value=dmin, max_value=dmax)

min_views = int(df["Views"].min())
max_views = int(df["Views"].max())
sel_views = st.sidebar.slider("Views range", min_views, max_views, (min_views, max_views))


def apply_filters(data: pd.DataFrame) -> pd.DataFrame:
    out = data.copy()
    if sel_cats:
        out = out[out["Category"].isin(sel_cats)]
    if isinstance(sel_dates, tuple) and len(sel_dates) == 2:
        d0, d1 = sel_dates
        out = out[(out["Published_Date"].dt.date >= d0) & (out["Published_Date"].dt.date <= d1)]
    out = out[(out["Views"] >= sel_views[0]) & (out["Views"] <= sel_views[1])]
    return out


fdf = apply_filters(df)
if fdf.empty:
    st.warning("No videos match the current filters. Adjust them in the sidebar.")
    st.stop()

# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
st.title("📺 YouTube Data Dashboard")
st.caption("Explore views, engagement, categories, and trends across your YouTube data.")

if page == "Dashboard":
    section("Key Metrics")
    total_videos = len(fdf)
    total_views = fdf["Views"].sum()
    total_likes = fdf["Likes"].sum()
    total_comments = fdf["Comments"].sum()
    avg_engage = fdf["Engagement_Rate"].mean()
    top_cat = fdf.groupby("Category")["Views"].sum().idxmax()

    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(metric_card("Total Videos", f"{total_videos:,}"), unsafe_allow_html=True)
    c2.markdown(metric_card("Total Views", fmt_num(total_views)), unsafe_allow_html=True)
    c3.markdown(metric_card("Total Likes", fmt_num(total_likes)), unsafe_allow_html=True)
    c4.markdown(metric_card("Avg Engagement", f"{avg_engage:.2f}%"), unsafe_allow_html=True)

    c5, c6 = st.columns(2)
    c5.markdown(metric_card("Total Comments", fmt_num(total_comments)), unsafe_allow_html=True)
    c6.markdown(metric_card("Top Category (by views)", top_cat), unsafe_allow_html=True)

    section("Views Over Time")
    monthly = fdf.groupby("Month")["Views"].sum().reset_index()
    fig = px.area(monthly, x="Month", y="Views", template="plotly_dark",
                  color_discrete_sequence=["#ef4444"])
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig, use_container_width=True)

    section("Top 10 Videos by Views")
    top = fdf.nlargest(10, "Views")[["Title", "Channel", "Category", "Views", "Likes"]]
    st.dataframe(top.reset_index(drop=True), use_container_width=True)

elif page == "Visualizations":
    section("Views by Category")
    cat_views = fdf.groupby("Category")["Views"].sum().sort_values(ascending=True).reset_index()
    st.plotly_chart(
        px.bar(cat_views, x="Views", y="Category", orientation="h", template="plotly_dark",
               color="Views", color_continuous_scale="Reds"),
        use_container_width=True,
    )

    section("Category Share (Videos)")
    cat_count = fdf["Category"].value_counts().reset_index()
    cat_count.columns = ["Category", "Videos"]
    st.plotly_chart(
        px.pie(cat_count, values="Videos", names="Category", template="plotly_dark", hole=0.4),
        use_container_width=True,
    )

    section("Likes vs Views")
    st.plotly_chart(
        px.scatter(fdf, x="Views", y="Likes", color="Category", size="Comments",
                   hover_data=["Title", "Channel"], template="plotly_dark"),
        use_container_width=True,
    )

    section("Engagement Rate Distribution")
    st.plotly_chart(
        px.histogram(fdf, x="Engagement_Rate", nbins=30, template="plotly_dark",
                     color_discrete_sequence=["#ef4444"]),
        use_container_width=True,
    )

    section("Videos Published per Month")
    pub = fdf.groupby("Month").size().reset_index(name="Videos")
    st.plotly_chart(
        px.line(pub, x="Month", y="Videos", markers=True, template="plotly_dark",
                color_discrete_sequence=["#10b981"]),
        use_container_width=True,
    )

elif page == "Top Performers":
    section("Top 10 Channels by Total Views")
    ch = fdf.groupby("Channel").agg(Views=("Views", "sum"),
                                    Videos=("Video_ID", "count"),
                                    Likes=("Likes", "sum")).sort_values("Views", ascending=False).head(10)
    st.dataframe(ch.reset_index(), use_container_width=True)
    st.plotly_chart(
        px.bar(ch.reset_index(), x="Channel", y="Views", template="plotly_dark",
               color="Views", color_continuous_scale="Reds"),
        use_container_width=True,
    )

    section("Top 10 Most-Liked Videos")
    most_liked = fdf.nlargest(10, "Likes")[["Title", "Channel", "Category", "Likes", "Views"]]
    st.dataframe(most_liked.reset_index(drop=True), use_container_width=True)

    section("Top 10 Most-Commented Videos")
    most_comm = fdf.nlargest(10, "Comments")[["Title", "Channel", "Category", "Comments", "Views"]]
    st.dataframe(most_comm.reset_index(drop=True), use_container_width=True)

elif page == "Insights":
    section("Automated Insights")

    best_cat = fdf.groupby("Category")["Engagement_Rate"].mean().idxmax()
    best_cat_val = fdf.groupby("Category")["Engagement_Rate"].mean().max()
    top_channel = fdf.groupby("Channel")["Views"].sum().idxmax()
    top_video = fdf.loc[fdf["Views"].idxmax()]
    viral = fdf[fdf["Views"] >= fdf["Views"].quantile(0.95)]
    avg_dur = fdf["Duration_Minutes"].mean()

    st.markdown(f"<div class='insight'>🏆 <b>Top channel by views:</b> {top_channel} "
                f"({fmt_num(fdf.groupby('Channel')['Views'].sum().max())} views)</div>",
                unsafe_allow_html=True)
    st.markdown(f"<div class='insight'>💬 <b>Most engaging category:</b> {best_cat} "
                f"(avg engagement {best_cat_val:.2f}%)</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='insight'>🚀 <b>Most-viewed video:</b> {top_video['Title']} — "
                f"{fmt_num(top_video['Views'])} views</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='insight'>🔥 <b>Viral videos (top 5%):</b> {len(viral)} titles "
                f"above {fmt_num(fdf['Views'].quantile(0.95))} views</div>",
                unsafe_allow_html=True)
    st.markdown(f"<div class='insight'>⏱️ <b>Average video duration:</b> {avg_dur:.1f} minutes</div>",
                unsafe_allow_html=True)

    section("Category Performance")
    perf = fdf.groupby("Category").agg(
        Videos=("Video_ID", "count"),
        Total_Views=("Views", "sum"),
        Avg_Views=("Views", "mean"),
        Avg_Engagement=("Engagement_Rate", "mean"),
    ).sort_values("Total_Views", ascending=False)
    st.dataframe(perf.style.format({"Avg_Views": "{:,.0f}", "Total_Views": "{:,.0f}",
                                    "Avg_Engagement": "{:.2f}%"}),
                 use_container_width=True)

elif page == "Data":
    section("Cleaned Dataset")
    st.write(f"Showing **{len(fdf):,}** rows after filters.")
    st.dataframe(fdf, use_container_width=True, height=520)
    st.download_button(
        "⬇️ Download cleaned CSV",
        data=fdf.to_csv(index=False).encode("utf-8"),
        file_name="youtube_cleaned.csv",
        mime="text/csv",
        use_container_width=True,
    )

st.sidebar.markdown("---")
st.sidebar.caption("Made with ❤️ using Streamlit")