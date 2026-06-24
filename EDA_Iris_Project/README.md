# 🌸 Exploratory Data Analysis (EDA) on the Iris Dataset

A complete, beginner-friendly yet professional **EDA project** on the classic
Iris flower dataset, built with Python, Pandas, Matplotlib, and Seaborn.

---

## 📌 Project Overview

The goal of this project is to perform a thorough Exploratory Data Analysis
on the Iris dataset to uncover patterns, relationships, and insights that
separate the three Iris species — *setosa*, *versicolor*, and *virginica*.

The project walks through the standard EDA workflow: loading, inspecting,
cleaning, describing, visualizing, and finally interpreting the data.

---

## 📊 Dataset Information

- **Name:** Iris Dataset
- **Source:** UCI Machine Learning Repository (also bundled with scikit-learn)
- **Rows:** 150
- **Features:** 4 numeric (sepal length, sepal width, petal length, petal width — all in cm)
- **Target:** `species` — `setosa`, `versicolor`, `virginica` (50 samples each)

---

## 🛠️ Technologies Used

- **Python 3.9+**
- **Pandas / NumPy** — data manipulation
- **Matplotlib / Seaborn** — visualization
- **scikit-learn** — dataset utility
- **Jupyter Notebook** — interactive analysis
- **fpdf2** — PDF report generation

---

## 🚀 Installation Steps

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/EDA_Iris_Project.git
cd EDA_Iris_Project

# 2. (Recommended) Create a virtual environment
python -m venv .venv
source .venv/bin/activate          # macOS / Linux
.venv\Scripts\activate             # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the EDA pipeline
python main.py

# 5. (Optional) Open the notebook
jupyter notebook notebooks/eda_iris.ipynb

# 6. (Optional) Generate the PDF report
python report/generate_report.py
```

---

## 🧭 Project Workflow

```
EDA_Iris_Project/
├── data/
│   └── iris.csv
├── notebooks/
│   └── eda_iris.ipynb
├── images/                 # auto-generated plots
├── report/
│   ├── generate_report.py
│   └── EDA_Report.pdf
├── README.md
├── requirements.txt
└── main.py
```

1. **Data Loading** — load `iris.csv` with Pandas.
2. **Data Inspection** — `.head()`, `.info()`, `.describe()`.
3. **Missing & Duplicate Check** — confirm a clean dataset.
4. **Descriptive Statistics** — central tendency & spread.
5. **Correlation Analysis** — heatmap of pairwise correlations.
6. **Outlier Detection** — IQR method + boxplots.
7. **Distributions** — histograms with KDE per species.
8. **Relationships** — pairplot & scatter plots.
9. **Species-wise Analysis** — grouped means and per-class behavior.
10. **Reporting** — PDF report + Markdown summary.

---

## 💡 Key Insights

- The dataset is **clean** — no missing values and no duplicates after deduplication.
- **Petal length** and **petal width** are very strongly correlated (~0.96) and
  are the two most discriminative features.
- ***Setosa*** is **linearly separable** from the other two species using petal features.
- ***Versicolor*** and ***virginica*** overlap on sepal features but separate
  cleanly on petal dimensions.
- A few mild outliers exist in `sepal_width` but they do not require removal.

---

## 📈 Results

- 7 high-quality visualizations saved to `images/`:
  heatmap, boxplots, histograms, pairplot, scatter plots.
- Species-level summary statistics computed.
- A multi-page PDF report summarizing findings, generated under `report/`.

---

## 🔮 Future Improvements

- Build a classifier (Logistic Regression / KNN / Random Forest) on top of the EDA.
- Apply PCA / t-SNE for dimensionality reduction & visualization.
- Wrap the analysis in a Streamlit dashboard.
- Compare against larger flower datasets (e.g. Iris-Extended).

---

## 👤 Author

**Your Name**
- GitHub: [@your-username](https://github.com/your-username)
- LinkedIn: [your-name](https://www.linkedin.com/in/your-name/)
- Email: your.email@example.com

> Built as part of a Data Science internship / portfolio project.

---

## 📝 License

MIT — free to use, modify, and distribute.