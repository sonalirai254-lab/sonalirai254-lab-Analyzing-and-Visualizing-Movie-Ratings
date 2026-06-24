"""
Generate a multi-page PDF EDA report for the Iris dataset.

Run from project root:
    python report/generate_report.py

Requires:
    - main.py (for visualizations) to have been run first, OR this script
      will regenerate them automatically into ./images/.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
from fpdf import FPDF

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

import main as eda  # noqa: E402

IMAGES = BASE_DIR / "images"
OUT = BASE_DIR / "report" / "EDA_Report.pdf"


def ensure_images(df: pd.DataFrame) -> None:
    """Generate all charts if they're missing."""
    needed = [
        "heatmap_correlation.png", "boxplots_by_species.png",
        "histograms.png", "pairplot.png", "scatter_sepal_petal.png",
    ]
    if not all((IMAGES / n).exists() for n in needed):
        eda.correlation_heatmap(df)
        eda.boxplots(df)
        eda.histograms(df)
        eda.pairplot(df)
        eda.scatter_petal_vs_sepal(df)


class Report(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, "EDA on the Iris Dataset", align="R")
        self.ln(10)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 8, f"Page {self.page_no()}", align="C")

    def h1(self, text: str) -> None:
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(20, 20, 20)
        self.ln(4)
        self.cell(0, 10, text, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(200, 200, 200)
        self.line(self.l_margin, self.get_y(), 210 - self.r_margin, self.get_y())
        self.ln(3)

    def h2(self, text: str) -> None:
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(40, 40, 40)
        self.ln(2)
        self.cell(0, 8, text, new_x="LMARGIN", new_y="NEXT")

    def body(self, text: str) -> None:
        self.set_font("Helvetica", "", 11)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 6, text)
        self.ln(1)

    def image_centered(self, path: Path, w: float = 170) -> None:
        if not path.exists():
            return
        x = (210 - w) / 2
        self.image(str(path), x=x, w=w)
        self.ln(4)


def build() -> Path:
    df = eda.clean_data(eda.load_data())
    ensure_images(df)

    pdf = Report()
    pdf.set_auto_page_break(auto=True, margin=15)

    # ---- Cover ----
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 24)
    pdf.ln(60)
    pdf.cell(0, 14, "Exploratory Data Analysis", align="C",
             new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 14, "on the Iris Dataset", align="C",
             new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)
    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(110, 110, 110)
    pdf.cell(0, 8, "A Data Science Internship Report", align="C",
             new_x="LMARGIN", new_y="NEXT")
    pdf.ln(40)
    pdf.cell(0, 7, "Author: Your Name", align="C",
             new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, "Tools: Python, Pandas, Matplotlib, Seaborn", align="C",
             new_x="LMARGIN", new_y="NEXT")

    # ---- 1. Introduction ----
    pdf.add_page()
    pdf.h1("1. Introduction")
    pdf.body(
        "Exploratory Data Analysis (EDA) is a critical first step in any data "
        "science workflow. It enables an analyst to understand the underlying "
        "structure of a dataset, detect anomalies, test assumptions and form "
        "hypotheses prior to modeling. In this report we apply a complete EDA "
        "pipeline to the well-known Iris dataset, originally introduced by "
        "British statistician and biologist Ronald A. Fisher in 1936."
    )

    pdf.h1("2. Objective")
    pdf.body(
        "The objective of this project is to perform a thorough EDA on the Iris "
        "dataset in order to:\n"
        "  - Understand the distribution of each feature.\n"
        "  - Quantify the relationships between features.\n"
        "  - Identify which features best discriminate between species.\n"
        "  - Detect outliers, duplicates and missing values.\n"
        "  - Communicate the findings via clear, professional visualizations."
    )

    # ---- 3. Dataset ----
    pdf.h1("3. Dataset Description")
    pdf.body(
        f"The dataset contains {len(df)} samples evenly distributed across three "
        "Iris species: setosa, versicolor and virginica (50 samples each). "
        "Each sample is described by four numeric features measured in centimeters: "
        "sepal length, sepal width, petal length and petal width."
    )
    desc = df.describe().round(2)
    pdf.h2("Descriptive statistics")
    pdf.set_font("Courier", "", 9)
    pdf.multi_cell(0, 4.5, desc.to_string())
    pdf.ln(2)

    # ---- 4. Methodology ----
    pdf.add_page()
    pdf.h1("4. Methodology")
    pdf.body(
        "The analysis follows a standard EDA pipeline implemented in Python:\n"
        "  1. Load the CSV using Pandas.\n"
        "  2. Inspect shape, dtypes, missing values and duplicates.\n"
        "  3. Clean - remove duplicates, coerce dtypes, drop NaNs.\n"
        "  4. Compute descriptive statistics and class balance.\n"
        "  5. Compute pairwise correlations.\n"
        "  6. Detect outliers with the IQR rule.\n"
        "  7. Visualize distributions and relationships.\n"
        "  8. Summarize per-species behavior."
    )

    pdf.h1("5. Data Cleaning")
    miss = df.isnull().sum().sum()
    dups = df.duplicated().sum()
    pdf.body(
        f"Missing values: {miss}. Duplicate rows after deduplication: {dups}. "
        "Numeric columns were coerced to float; the species column was kept as "
        "a categorical string. No imputation was required."
    )

    # ---- 6. Exploratory Analysis & Visualizations ----
    pdf.add_page()
    pdf.h1("6. Exploratory Analysis & Visualizations")

    pdf.h2("6.1 Correlation Heatmap")
    pdf.image_centered(IMAGES / "heatmap_correlation.png", w=130)
    pdf.body(
        "Petal length and petal width are very strongly correlated (~0.96). "
        "Sepal width is weakly - and slightly negatively - correlated with the "
        "petal dimensions, suggesting it carries somewhat independent information."
    )

    pdf.add_page()
    pdf.h2("6.2 Boxplots by Species")
    pdf.image_centered(IMAGES / "boxplots_by_species.png", w=180)
    pdf.body(
        "The petal features (length and width) show clear, non-overlapping ranges "
        "between setosa and the other two species. A handful of mild outliers "
        "appear in sepal_width for setosa but are not extreme."
    )

    pdf.add_page()
    pdf.h2("6.3 Feature Distributions")
    pdf.image_centered(IMAGES / "histograms.png", w=170)
    pdf.body(
        "Petal length and width are bimodal across the full dataset, with setosa "
        "occupying the lower mode. Sepal length is roughly normal; sepal width is "
        "close to normal with slight right skew."
    )

    pdf.add_page()
    pdf.h2("6.4 Pairwise Relationships")
    pdf.image_centered(IMAGES / "pairplot.png", w=170)
    pdf.body(
        "The pairplot confirms that setosa is linearly separable from the other "
        "two species in any plot involving petal_length or petal_width. "
        "Versicolor and virginica overlap slightly but are still well-separated "
        "in the petal subspace."
    )

    pdf.add_page()
    pdf.h2("6.5 Sepal vs Petal Scatter")
    pdf.image_centered(IMAGES / "scatter_sepal_petal.png", w=180)
    pdf.body(
        "Petal-space scatter reveals three distinct clusters, while sepal-space "
        "scatter mixes versicolor and virginica - quantitative confirmation that "
        "petal measurements are the dominant discriminators."
    )

    # ---- 7. Findings ----
    pdf.add_page()
    pdf.h1("7. Findings")
    pdf.body(
        "  - The dataset is clean: no missing values and no duplicates after dedup.\n"
        "  - Petal length & width are the most informative features (corr ~0.96).\n"
        "  - Setosa is linearly separable from versicolor and virginica.\n"
        "  - Versicolor and virginica overlap on sepal features but separate on petals.\n"
        "  - A few mild outliers exist in sepal_width but do not warrant removal."
    )

    pdf.h1("8. Conclusion")
    pdf.body(
        "The Iris dataset, despite its small size, is an excellent teaching dataset. "
        "EDA alone is sufficient to suggest that a simple classifier using petal "
        "length and petal width could achieve very high accuracy. This makes Iris "
        "an ideal next step for supervised classification - logistic regression, "
        "KNN or decision trees would all be appropriate follow-up models."
    )

    pdf.h1("9. References")
    pdf.body(
        "  - Fisher, R. A. (1936). 'The use of multiple measurements in taxonomic "
        "problems.' Annals of Eugenics, 7(2), 179-188.\n"
        "  - UCI Machine Learning Repository: Iris Data Set.\n"
        "  - scikit-learn documentation: sklearn.datasets.load_iris.\n"
        "  - McKinney, W. (2010). Data Structures for Statistical Computing in Python.\n"
        "  - Waskom, M. (2021). Seaborn: statistical data visualization."
    )

    pdf.output(str(OUT))
    print(f"PDF report written to {OUT}")
    return OUT


if __name__ == "__main__":
    build()