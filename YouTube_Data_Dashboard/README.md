# 📺 YouTube Data Dashboard

An interactive Streamlit dashboard to explore and analyze YouTube channel/video
data — views, likes, comments, engagement, publishing trends, and top performers.

## 🎯 Project Objective
Turn raw YouTube CSV exports into actionable insights through a clean,
interactive dashboard with KPIs, charts, and filters.

## ✨ Features
- 📤 Upload your own YouTube CSV (or use the bundled sample)
- 🧹 Automatic data cleaning (deduplication, type coercion, missing values)
- 📊 KPI cards — total videos, total views, avg likes, engagement rate
- 📈 Interactive Plotly charts — views over time, top videos, category mix
- 🔍 Sidebar filters — category, date range, view/like ranges
- 🏆 Automated insights — top channel, best category, viral videos
- ⬇️ Download cleaned dataset as CSV
- 🎨 Modern dark-themed UI with sidebar navigation

## 📁 Folder Structure
```
YouTube_Data_Dashboard/
├── app.py
├── requirements.txt
├── runtime.txt
├── README.md
├── .streamlit/
│   └── config.toml
├── data/
│   └── youtube_data.csv
├── assets/
└── screenshots/
```

## 🧰 Tech Stack
Python · Streamlit · Pandas · NumPy · Matplotlib · Seaborn · Plotly

## 🚀 Installation
```bash
cd YouTube_Data_Dashboard
pip install -r requirements.txt
streamlit run app.py
```

## ☁️ Deploy to Streamlit Community Cloud

Deploy this dashboard for free at **[share.streamlit.io](https://share.streamlit.io)**.

### 1. Push the project to GitHub
```bash
git init
git add .
git commit -m "Initial commit — YouTube Data Dashboard"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

Make sure these files are committed at the repo root (or inside this folder
if the repo contains multiple projects):

- `app.py` — the Streamlit entry point
- `requirements.txt` — Python dependencies
- `runtime.txt` — pins Python 3.11 for the Cloud build
- `.streamlit/config.toml` — theme and server settings
- `data/youtube_data.csv` — sample dataset bundled with the app

### 2. Create the Streamlit Cloud app
1. Sign in at <https://share.streamlit.io> with your GitHub account.
2. Click **"New app"**.
3. Select your repository and branch (e.g. `main`).
4. Set **Main file path** to:
   ```
   YouTube_Data_Dashboard/app.py
   ```
   (or just `app.py` if the project sits at the repo root).
5. Choose **Python 3.11** (matches `runtime.txt`).
6. Click **Deploy**.

The first build installs the requirements and launches the app at
`https://<your-app-name>.streamlit.app`.

### 3. (Optional) Add secrets
If you later add API keys (e.g. the YouTube Data API), open **App → Settings →
Secrets** in the Streamlit Cloud dashboard and add them in TOML format:
```toml
YOUTUBE_API_KEY = "your-key-here"
```
Access them in `app.py` via `st.secrets["YOUTUBE_API_KEY"]`. Never commit
`.streamlit/secrets.toml` — it is git-ignored by default.

### 4. Updating the deployed app
Push new commits to the same branch — Streamlit Cloud auto-rebuilds and
redeploys within seconds. Use the **Manage app → Reboot** option if a
dependency change requires a clean install.

## 📦 Expected CSV Columns
`Video_ID, Title, Channel, Category, Published_Date, Views, Likes, Comments, Duration_Minutes`

Missing columns are handled gracefully.

## 🖼️ Screenshots
Add screenshots of the dashboard to the `screenshots/` folder.

## 🔮 Future Improvements
- YouTube Data API integration for live data
- Sentiment analysis on comments
- Channel comparison mode
- ML-based view prediction
- PDF export of the dashboard

## 📝 License
MIT