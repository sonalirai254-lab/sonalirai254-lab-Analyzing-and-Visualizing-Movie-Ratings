"""
Exploratory Data Analysis (EDA) on the Iris Dataset
===================================================

End-to-end EDA pipeline:
    1. Load data
    2. Inspect & clean
    3. Descriptive statistics
    4. Correlation analysis
    5. Outlier detection
    6. Feature distribution & species-wise analysis
    7. Save all plots to ./images/

Run:
    python main.py
"""

from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "iris.csv"
IMAGES_DIR = BASE_DIR / "images"
IMAGES_DIR.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid", palette="Set2")
plt.rcParams["figure.dpi"] = 110

NUMERIC_COLS = ["sepal_length", "sepal_width", "petal_length", "petal_width"]


def save_fig(fig: plt.Figure, name: str) -> Path:
    """Save a matplotlib figure to the images directory."""
    out = IMAGES_DIR / name
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"  -> saved {out.relative_to(BASE_DIR)}")
    return out


# ---------------------------------------------------------------------------
# 1. Data loading & inspection
# ---------------------------------------------------------------------------
def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    print(f"\n[1/7] Loading dataset from {path}")
    df = pd.read_csv(path)
    print(f"      shape: {df.shape}")
    return df


def inspect_data(df: pd.DataFrame) -> None:
    print("\n[2/7] Data inspection")
    print("Head:\n", df.head())
    print("\nInfo:")
    df.info()
    print("\nMissing values per column:\n", df.isnull().sum())
    print(f"\nDuplicate rows: {df.duplicated().sum()}")


# ---------------------------------------------------------------------------
# 2. Cleaning
# ---------------------------------------------------------------------------
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    print("\n[3/7] Cleaning")
    before = len(df)
    df = df.drop_duplicates().reset_index(drop=True)
    for col in NUMERIC_COLS:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna().reset_index(drop=True)
    print(f"      rows: {before} -> {len(df)}")
    return df


# ---------------------------------------------------------------------------
# 3. Descriptive statistics & correlation
# ---------------------------------------------------------------------------
def describe(df: pd.DataFrame) -> None:
    print("\n[4/7] Descriptive statistics")
    print(df.describe().round(3))
    print("\nClass balance:\n", df["species"].value_counts())


def correlation_heatmap(df: pd.DataFrame) -> None:
    corr = df[NUMERIC_COLS].corr()
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1,
                fmt=".2f", linewidths=.5, ax=ax)
    ax.set_title("Correlation Heatmap of Iris Features")
    save_fig(fig, "heatmap_correlation.png")
    print("\nInsight: petal_length and petal_width are very strongly correlated (~0.96),")
    print("indicating they convey similar information — useful for species separation.")


# ---------------------------------------------------------------------------
# 4. Outlier detection
# ---------------------------------------------------------------------------
def outlier_summary(df: pd.DataFrame) -> None:
    print("\n[5/7] Outlier detection (IQR method)")
    for col in NUMERIC_COLS:
        q1, q3 = df[col].quantile([.25, .75])
        iqr = q3 - q1
        lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        n = ((df[col] < lo) | (df[col] > hi)).sum()
        print(f"  {col:14s}: {n} outliers (bounds {lo:.2f} – {hi:.2f})")


def boxplots(df: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 4, figsize=(14, 4))
    for ax, col in zip(axes, NUMERIC_COLS):
        sns.boxplot(x="species", y=col, data=df, ax=ax)
        ax.set_title(col)
    fig.suptitle("Feature Boxplots by Species", fontsize=14, y=1.02)
    save_fig(fig, "boxplots_by_species.png")
    print("Insight: sepal_width shows a few outliers in setosa; petal features cleanly separate species.")


# ---------------------------------------------------------------------------
# 5. Distributions & relationships
# ---------------------------------------------------------------------------
def histograms(df: pd.DataFrame) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(10, 7))
    for ax, col in zip(axes.ravel(), NUMERIC_COLS):
        sns.histplot(data=df, x=col, hue="species", kde=True,
                     element="step", ax=ax)
        ax.set_title(f"Distribution of {col}")
    fig.tight_layout()
    save_fig(fig, "histograms.png")
    print("Insight: petal_length & petal_width are bimodal across species,")
    print("making them the strongest predictors of class membership.")


def pairplot(df: pd.DataFrame) -> None:
    g = sns.pairplot(df, hue="species", diag_kind="kde", height=2.2)
    g.fig.suptitle("Pairwise Feature Relationships", y=1.02)
    g.fig.savefig(IMAGES_DIR / "pairplot.png", bbox_inches="tight")
    plt.close(g.fig)
    print("  -> saved images/pairplot.png")
    print("Insight: setosa is linearly separable from the other two species using petal features.")


def scatter_petal_vs_sepal(df: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    sns.scatterplot(data=df, x="sepal_length", y="sepal_width",
                    hue="species", style="species", ax=axes[0])
    axes[0].set_title("Sepal length vs width")
    sns.scatterplot(data=df, x="petal_length", y="petal_width",
                    hue="species", style="species", ax=axes[1])
    axes[1].set_title("Petal length vs width")
    save_fig(fig, "scatter_sepal_petal.png")
    print("Insight: petal space shows three clear clusters; sepal space mixes versicolor/virginica.")


# ---------------------------------------------------------------------------
# 6. Species-wise analysis
# ---------------------------------------------------------------------------
def species_summary(df: pd.DataFrame) -> None:
    print("\n[6/7] Species-wise statistics (mean values)")
    print(df.groupby("species")[NUMERIC_COLS].mean().round(3))


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------
def main() -> None:
    df = load_data()
    inspect_data(df)
    df = clean_data(df)
    describe(df)

    correlation_heatmap(df)
    outlier_summary(df)
    boxplots(df)
    histograms(df)
    pairplot(df)
    scatter_petal_vs_sepal(df)
    species_summary(df)

    print("\n[7/7] EDA complete. All visualizations saved under ./images/")


if __name__ == "__main__":
    main()