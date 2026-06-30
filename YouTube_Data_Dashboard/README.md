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
├── README.md
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