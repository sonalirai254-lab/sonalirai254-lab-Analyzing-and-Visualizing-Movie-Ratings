"""
Movie Rating Analysis - Streamlit Application
==============================================
A professional dashboard for exploring and analyzing movie rating datasets.

Run:
    streamlit run app.py
"""

from __future__ import annotations

import io
from typing import Optional
from datetime import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from matplotlib.backends.backend_pdf import PdfPages

# ---------------------------------------------------------------------------
# Page configuration & global styling
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Movie Rating Analysis",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

sns.set_theme(style="whitegrid", palette="viridis")

CUSTOM_CSS = """
<style>
    .main { background-color: #0e1117; }
    .metric-card {
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
        padding: 1.25rem 1.5rem;
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.06);
        box-shadow: 0 4px 18px rgba(0,0,0,0.35);
        color: #f9fafb;
    }
    .metric-card h4 {
        margin: 0 0 .35rem 0;
        font-size: 0.85rem;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: .06em;
    }
    .metric-card .value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #fbbf24;
    }
    .section-title {
        border-left: 4px solid #fbbf24;
        padding-left: .75rem;
        margin: 1.25rem 0 .75rem 0;
    }
    .insight {
        background: #111827;
        padding: .9rem 1.1rem;
        border-radius: 10px;
        border-left: 3px solid #10b981;
        margin-bottom: .6rem;
        color: #e5e7eb;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

EXPECTED_COLUMNS = [
    "Movie_Name", "Genre", "Year", "Rating", "Votes", "Runtime", "Revenue", "Director",
]

# ---------------------------------------------------------------------------
# Data loading & cleaning
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_csv(file_bytes: bytes) -> pd.DataFrame:
    """Read CSV bytes into a DataFrame."""
    return pd.read_csv(io.BytesIO(file_bytes))


@st.cache_data(show_spinner=False)
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean dataset: deduplicate, coerce types, handle missing values."""
    df = df.copy()

    # Ensure all expected columns exist (create empty if missing)
    for col in EXPECTED_COLUMNS:
        if col not in df.columns:
            df[col] = np.nan

    # Remove duplicates
    df = df.drop_duplicates()

    # Coerce numeric columns
    numeric_cols = ["Year", "Rating", "Votes", "Runtime", "Revenue"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Clean text columns
    for col in ["Movie_Name", "Genre", "Director"]:
        df[col] = df[col].astype(str).str.strip().replace({"nan": np.nan, "": np.nan})

    # Fill missing values with sensible defaults
    df["Rating"] = df["Rating"].fillna(df["Rating"].median())
    df["Votes"] = df["Votes"].fillna(0).astype(int)
    df["Revenue"] = df["Revenue"].fillna(0.0)
    df["Runtime"] = df["Runtime"].fillna(df["Runtime"].median())
    df["Genre"] = df["Genre"].fillna("Unknown")
    df["Director"] = df["Director"].fillna("Unknown")
    df["Movie_Name"] = df["Movie_Name"].fillna("Untitled")

    # Drop rows with no Year (cannot trend)
    df = df.dropna(subset=["Year"])
    df["Year"] = df["Year"].astype(int)

    return df.reset_index(drop=True)


def explode_genres(df: pd.DataFrame) -> pd.DataFrame:
    """Split multi-genre rows (comma/pipe separated) into individual rows."""
    tmp = df.copy()
    tmp["Genre"] = tmp["Genre"].astype(str).str.split(r"[,|/]")
    tmp = tmp.explode("Genre")
    tmp["Genre"] = tmp["Genre"].str.strip()
    return tmp


# ---------------------------------------------------------------------------
# UI helpers
# ---------------------------------------------------------------------------
def metric_card(title: str, value: str) -> str:
    return f"<div class='metric-card'><h4>{title}</h4><div class='value'>{value}</div></div>"


def section(title: str) -> None:
    st.markdown(f"<h3 class='section-title'>{title}</h3>", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Visualizations
# ---------------------------------------------------------------------------
def plot_rating_histogram(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(df["Rating"], bins=20, kde=True, color="#fbbf24", ax=ax)
    ax.set_title("Distribution of Movie Ratings")
    ax.set_xlabel("Rating"); ax.set_ylabel("Count")
    return fig


def plot_genre_avg_rating(df: pd.DataFrame):
    g = explode_genres(df).groupby("Genre")["Rating"].mean().sort_values(ascending=False).head(15)
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x=g.values, y=g.index, ax=ax, palette="viridis")
    ax.set_title("Average Rating by Genre (Top 15)")
    ax.set_xlabel("Average Rating"); ax.set_ylabel("")
    return fig


def plot_rating_pie(df: pd.DataFrame):
    bins = [0, 4, 6, 7, 8, 10]
    labels = ["Poor (<4)", "Average (4-6)", "Good (6-7)", "Great (7-8)", "Excellent (8+)"]
    buckets = pd.cut(df["Rating"], bins=bins, labels=labels, include_lowest=True)
    counts = buckets.value_counts().reindex(labels).fillna(0)
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(counts, labels=labels, autopct="%1.1f%%", startangle=90,
           colors=sns.color_palette("viridis", len(labels)))
    ax.set_title("Ratings Distribution")
    return fig


def plot_year_trend(df: pd.DataFrame):
    yearly = df.groupby("Year").size()
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(yearly.index, yearly.values, marker="o", color="#10b981", linewidth=2)
    ax.fill_between(yearly.index, yearly.values, alpha=0.2, color="#10b981")
    ax.set_title("Movies Released per Year")
    ax.set_xlabel("Year"); ax.set_ylabel("Number of Movies")
    return fig


def plot_top_movies(df: pd.DataFrame):
    top = df.sort_values("Rating", ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x="Rating", y="Movie_Name", data=top, palette="rocket", ax=ax)
    ax.set_title("Top 10 Highest Rated Movies")
    ax.set_xlabel("Rating"); ax.set_ylabel("")
    return fig


# ---------------------------------------------------------------------------
# PDF report generation
# ---------------------------------------------------------------------------
def build_pdf_report(df: pd.DataFrame) -> bytes:
    """Render the dashboard (key insights + charts) as a multi-page PDF."""
    buf = io.BytesIO()

    # Pre-compute insights
    total = len(df)
    avg_rating = df["Rating"].mean()
    highest = df.loc[df["Rating"].idxmax()]
    lowest = df.loc[df["Rating"].idxmin()]
    exploded = explode_genres(df)
    pop_genre = exploded["Genre"].value_counts().idxmax()
    genre_stats = exploded.groupby("Genre")["Rating"].agg(["mean", "count"])
    genre_stats = genre_stats[genre_stats["count"] >= max(3, int(0.01 * len(df)))]
    best_genre = genre_stats["mean"].idxmax() if not genre_stats.empty else "N/A"
    worst_genre = genre_stats["mean"].idxmin() if not genre_stats.empty else "N/A"
    exceptional = (df["Rating"] >= 8.5).sum()
    year_span = f"{int(df['Year'].min())} – {int(df['Year'].max())}"

    with PdfPages(buf) as pdf:
        # Cover / insights page
        fig, ax = plt.subplots(figsize=(8.5, 11))
        ax.axis("off")
        ax.text(0.5, 0.95, "🎬 Movie Rating Analysis Report",
                ha="center", va="top", fontsize=22, fontweight="bold")
        ax.text(0.5, 0.91, f"Generated on {datetime.now().strftime('%B %d, %Y %H:%M')}",
                ha="center", va="top", fontsize=10, color="gray")

        lines = [
            ("Total Movies", f"{total:,}"),
            ("Year Range", year_span),
            ("Average Rating", f"{avg_rating:.2f}"),
            ("Most Popular Genre", str(pop_genre)),
            ("Best-Performing Genre", str(best_genre)),
            ("Lowest-Performing Genre", str(worst_genre)),
            ("Highest Rated Movie", f"{highest['Movie_Name']} ({highest['Rating']:.1f})"),
            ("Lowest Rated Movie", f"{lowest['Movie_Name']} ({lowest['Rating']:.1f})"),
            ("Exceptional Movies (≥ 8.5)", f"{exceptional}"),
        ]
        y = 0.82
        ax.text(0.08, y, "Key Insights", fontsize=15, fontweight="bold")
        y -= 0.04
        for label, value in lines:
            ax.text(0.08, y, f"{label}:", fontsize=11, fontweight="bold")
            ax.text(0.50, y, str(value), fontsize=11)
            y -= 0.035
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

        # Chart pages
        for plot_fn in (plot_rating_histogram, plot_top_movies,
                        plot_genre_avg_rating, plot_rating_pie, plot_year_trend):
            fig = plot_fn(df)
            pdf.savefig(fig, bbox_inches="tight")
            plt.close(fig)

        meta = pdf.infodict()
        meta["Title"] = "Movie Rating Analysis Report"
        meta["Author"] = "Movie Rating Analysis Dashboard"
        meta["CreationDate"] = datetime.now()

    return buf.getvalue()


# ---------------------------------------------------------------------------
# Sidebar — upload & filters
# ---------------------------------------------------------------------------
st.sidebar.title("🎬 Movie Analysis")
st.sidebar.caption("Upload a movie dataset and explore insights.")

page = st.sidebar.radio("Navigation", ["Dashboard", "Visualizations", "Analysis", "Data"])

uploaded = st.sidebar.file_uploader("Upload movies CSV", type=["csv"])

st.sidebar.markdown("---")
st.sidebar.caption("Tip: expected columns —")
st.sidebar.code(", ".join(EXPECTED_COLUMNS), language="text")


def get_dataframe() -> Optional[pd.DataFrame]:
    if uploaded is not None:
        try:
            raw = load_csv(uploaded.getvalue())
            return clean_data(raw)
        except Exception as exc:  # pragma: no cover
            st.sidebar.error(f"Failed to parse CSV: {exc}")
            return None
    # Fallback: try bundled sample
    try:
        raw = pd.read_csv("dataset/movies.csv")
        return clean_data(raw)
    except Exception:
        return None


df = get_dataframe()

if df is None or df.empty:
    st.title("🎬 Movie Rating Analysis")
    st.info("Upload a CSV file from the sidebar to get started. "
            "You can also drop a `dataset/movies.csv` next to `app.py`.")
    st.stop()

# Apply user filters
st.sidebar.markdown("---")
st.sidebar.subheader("Filters")

all_genres = sorted({g.strip() for row in df["Genre"].dropna()
                     for g in str(row).replace("|", ",").replace("/", ",").split(",") if g.strip()})
sel_genres = st.sidebar.multiselect("Genre", all_genres, default=[])

year_min, year_max = int(df["Year"].min()), int(df["Year"].max())
if year_min == year_max:
    year_max += 1
sel_year = st.sidebar.slider("Year range", year_min, year_max, (year_min, year_max))

sel_rating = st.sidebar.slider("Rating range", 0.0, 10.0, (0.0, 10.0), step=0.1)


def apply_filters(data: pd.DataFrame) -> pd.DataFrame:
    out = data.copy()
    if sel_genres:
        mask = out["Genre"].astype(str).apply(
            lambda g: any(s.strip() in sel_genres for s in g.replace("|", ",").replace("/", ",").split(","))
        )
        out = out[mask]
    out = out[(out["Year"] >= sel_year[0]) & (out["Year"] <= sel_year[1])]
    out = out[(out["Rating"] >= sel_rating[0]) & (out["Rating"] <= sel_rating[1])]
    return out


fdf = apply_filters(df)

if fdf.empty:
    st.warning("No movies match the current filters. Adjust them in the sidebar.")
    st.stop()

# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
st.title("🎬 Movie Rating Analysis")
st.caption("Interactive dashboard for exploring movie ratings, genres, and trends.")

if page == "Dashboard":
    section("Key Metrics")
    total = len(fdf)
    avg_rating = fdf["Rating"].mean()
    highest = fdf.loc[fdf["Rating"].idxmax()]
    lowest = fdf.loc[fdf["Rating"].idxmin()]
    pop_genre = explode_genres(fdf)["Genre"].value_counts().idxmax()

    c1, c2, c3 = st.columns(3)
    c1.markdown(metric_card("Total Movies", f"{total:,}"), unsafe_allow_html=True)
    c2.markdown(metric_card("Average Rating", f"{avg_rating:.2f}"), unsafe_allow_html=True)
    c3.markdown(metric_card("Most Popular Genre", pop_genre), unsafe_allow_html=True)

    c4, c5 = st.columns(2)
    c4.markdown(metric_card("Highest Rated",
                            f"{highest['Movie_Name']} ({highest['Rating']:.1f})"),
                unsafe_allow_html=True)
    c5.markdown(metric_card("Lowest Rated",
                            f"{lowest['Movie_Name']} ({lowest['Rating']:.1f})"),
                unsafe_allow_html=True)

    # PDF report download
    st.markdown("")
    dl_col1, dl_col2 = st.columns([1, 3])
    with dl_col1:
        try:
            pdf_bytes = build_pdf_report(fdf)
            st.download_button(
                "📄 Download PDF Report",
                data=pdf_bytes,
                file_name=f"movie_rating_report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        except Exception as exc:
            st.error(f"Could not generate PDF: {exc}")
    with dl_col2:
        st.caption("Exports the current filtered dashboard — key insights and all charts — as a multi-page PDF.")

    section("Quick Look")
    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(plot_rating_histogram(fdf))
    with col2:
        st.pyplot(plot_top_movies(fdf))

elif page == "Visualizations":
    section("Rating Histogram")
    st.pyplot(plot_rating_histogram(fdf))

    section("Average Rating by Genre")
    st.pyplot(plot_genre_avg_rating(fdf))

    section("Ratings Distribution")
    st.pyplot(plot_rating_pie(fdf))

    section("Yearly Release Trend")
    st.pyplot(plot_year_trend(fdf))

    section("Top 10 Highest Rated Movies")
    st.pyplot(plot_top_movies(fdf))

elif page == "Analysis":
    section("Automated Insights")

    genre_stats = explode_genres(fdf).groupby("Genre")["Rating"].agg(["mean", "count"])
    genre_stats = genre_stats[genre_stats["count"] >= max(3, int(0.01 * len(fdf)))]
    best_genre = genre_stats["mean"].idxmax() if not genre_stats.empty else "N/A"
    worst_genre = genre_stats["mean"].idxmin() if not genre_stats.empty else "N/A"

    yearly_avg = fdf.groupby("Year")["Rating"].mean()
    trend = "increasing 📈" if yearly_avg.iloc[-1] > yearly_avg.iloc[0] else "decreasing 📉"

    exceptional = fdf[fdf["Rating"] >= 8.5].sort_values("Rating", ascending=False)

    st.markdown(f"<div class='insight'>🏆 <b>Best-performing genre:</b> "
                f"{best_genre} (avg {genre_stats['mean'].max():.2f})</div>",
                unsafe_allow_html=True)
    st.markdown(f"<div class='insight'>⚠️ <b>Lowest-performing genre:</b> "
                f"{worst_genre} (avg {genre_stats['mean'].min():.2f})</div>",
                unsafe_allow_html=True)
    st.markdown(f"<div class='insight'>📊 <b>Rating trend over years:</b> {trend} "
                f"(from {yearly_avg.iloc[0]:.2f} in {yearly_avg.index[0]} "
                f"to {yearly_avg.iloc[-1]:.2f} in {yearly_avg.index[-1]})</div>",
                unsafe_allow_html=True)
    st.markdown(f"<div class='insight'>🌟 <b>Exceptional movies (rating ≥ 8.5):</b> "
                f"{len(exceptional)} titles</div>", unsafe_allow_html=True)

    section("Genre Performance")
    st.dataframe(genre_stats.sort_values("mean", ascending=False)
                 .rename(columns={"mean": "Avg Rating", "count": "Movies"})
                 .style.format({"Avg Rating": "{:.2f}"}),
                 use_container_width=True)

    section("Yearly Average Rating")
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(yearly_avg.index, yearly_avg.values, marker="o", color="#fbbf24", linewidth=2)
    ax.set_title("Average Rating per Year")
    ax.set_xlabel("Year"); ax.set_ylabel("Avg Rating")
    st.pyplot(fig)

    if not exceptional.empty:
        section("Exceptional Movies (Rating ≥ 8.5)")
        st.dataframe(exceptional[["Movie_Name", "Genre", "Year", "Rating", "Director"]]
                     .head(20).reset_index(drop=True),
                     use_container_width=True)

elif page == "Data":
    section("Cleaned Dataset")
    st.write(f"Showing **{len(fdf):,}** rows after filters.")
    st.dataframe(fdf, use_container_width=True, height=520)

    csv_bytes = fdf.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download cleaned CSV",
        data=csv_bytes,
        file_name="movies_cleaned.csv",
        mime="text/csv",
        use_container_width=True,
    )

st.sidebar.markdown("---")
st.sidebar.caption("Made with ❤️ using Streamlit")