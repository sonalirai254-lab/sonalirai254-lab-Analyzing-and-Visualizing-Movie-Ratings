# 🎬 Movie Rating Analysis

A professional, interactive **Streamlit** dashboard for exploring and analyzing
movie rating datasets. Upload a CSV, clean it automatically, and explore
ratings, genres, directors, and yearly trends through rich visualizations and
automated insights.

---

## 🎯 Project Objective

Provide a single, easy-to-use web app that lets analysts, students, and movie
enthusiasts upload any movie dataset and instantly get:

- Cleaned data (no nulls, no duplicates, correct types)
- Key performance metrics
- Beautiful visualizations
- Automated insights about genres, years, and outliers
- Downloadable cleaned dataset

---

## ✨ Features

### 📤 Upload & Clean
- Upload any CSV with columns like
  `Movie_Name, Genre, Year, Rating, Votes, Runtime, Revenue, Director`
- Automatic missing-value handling, deduplication, and type coercion

### 📊 Dashboard
- Total movie count
- Average rating
- Highest & lowest rated movies
- Most popular genre

### 📈 Visualizations
- Histogram of movie ratings
- Genre-wise average ratings (bar chart)
- Ratings distribution (pie chart)
- Yearly release trend (line chart)
- Top 10 highest rated movies (bar chart)

### 🧠 Analysis
- Best & worst performing genres
- Rating trend over years
- Highlights movies with exceptional ratings (≥ 8.5)

### 🎛️ Filters
- Genre (multi-select)
- Year range
- Rating range

### 💾 Export
- Download the cleaned dataset as CSV

---

## 🛠️ Tech Stack

- **Python 3.9+**
- **Streamlit** — UI framework
- **Pandas / NumPy** — data wrangling
- **Matplotlib / Seaborn** — visualizations

---

## 📁 Folder Structure

```
Movie_Rating_Analysis/
├── app.py
├── requirements.txt
├── README.md
├── dataset/
│   └── movies.csv        # optional sample data
├── assets/               # logos, icons, etc.
└── screenshots/          # UI screenshots for docs
```

---

## 🚀 Installation & Usage

1. **Clone the repo**
   ```bash
   git clone <your-repo-url>
   cd Movie_Rating_Analysis
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv .venv
   source .venv/bin/activate          # macOS / Linux
   .venv\Scripts\activate             # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

5. Open your browser at `http://localhost:8501` and upload a movie CSV
   from the sidebar (or drop one at `dataset/movies.csv`).

---

## 📸 Screenshots

Place UI screenshots inside the `screenshots/` folder and reference them here:

| Dashboard | Visualizations | Analysis |
|-----------|----------------|----------|
| ![Dashboard](screenshots/dashboard.png) | ![Charts](screenshots/visualizations.png) | ![Insights](screenshots/analysis.png) |

---

## 🧪 Sample Dataset

Any CSV with the following (case-sensitive) columns works out of the box.
Missing columns are auto-filled.

```
Movie_Name, Genre, Year, Rating, Votes, Runtime, Revenue, Director
```

`Genre` may contain multiple values separated by `,`, `|`, or `/`
(e.g. `Action, Adventure, Sci-Fi`) — the app explodes them automatically
for genre-level analytics.

---

## 🔮 Future Improvements

- 🔍 Director-level analytics & leaderboards
- 🤖 ML-powered rating prediction
- 🌐 Multi-language UI
- 🗂️ Persistent storage (SQLite / Postgres) instead of per-session CSV
- 🔐 User authentication for saved dashboards
- 📤 PDF report export
- 🎨 Theming options (light / dark / custom)

---

## 📝 License

MIT — free to use, modify, and distribute.

---

Made with ❤️ using Python & Streamlit.