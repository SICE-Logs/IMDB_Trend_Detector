🎬 Interactive IMDb 2024 Data Visualization Framework
📖 Overview

This project extracts and analyzes IMDb 2024 movie data to uncover trends like top movies, genre popularity, average durations, and voting patterns. It provides an interactive Streamlit dashboard for exploring insights that go beyond IMDb’s basic search and filter features.

🚀 Features

Scrape movie details (name, genre, rating, votes, duration) from IMDb 2024 using Selenium. (And this tool is the reason why "capcha" thingy exists 😂)

Store datasets in CSV & SQL databases. ( EDA ready data as CSV, raw data as SQL database)

Perform data analysis with Pandas, Matplotlib, Seaborn.

Interactive Streamlit dashboard with visualizations:

Top 10 movies by ratings & votes

Genre distributions

Average duration per genre

Voting & rating correlations

🛠️ Tech Stack

Python (Pandas, Matplotlib, Seaborn)

Selenium – Web scraping

Streamlit – Interactive dashboard

SQL/SQLite + SQLAlchemy – Data storage & querying

📂 Project Structure
├── data/                # Raw & cleaned data (CSV/SQL)  
├── notebooks/           # Jupyter notebooks for analysis  
├── src/                 # Python scripts for scraping & processing  
├── app.py               # Streamlit dashboard  
├── requirements.txt     # Dependencies  
└── README.md            # Project documentation  

⚡ Getting Started
1. Clone the repository
git clone https://github.com/your-username/imdb-2024-visualization.git
cd imdb-2024-visualization

2. Install dependencies
pip install -r requirements.txt

3. Run the Streamlit dashboard
streamlit run app.py

📊 Sample Output

Bar charts of genre distribution

Heatmaps of ratings vs. genres

Scatter plots showing ratings vs. votes

Tables of top 10 movies & extremes

🌍 Use Cases

Movie Enthusiasts → Discover top genres & hidden gems.

Filmmakers/Producers → Analyze trends for better decisions.

OTT Platforms → Identify popular genres for curation.

Researchers/Students → Learn data scraping, visualization, and analysis.

📌 Future Improvements (Just in case this "mini" can become "mega")

Add ML models for trend predictions.

Integrate reviews + sentiment analysis.

Compare IMDb with Rotten Tomatoes/Metacritic data.

Deploy as a web app for public access.

👨‍💻 Contributors

S Logajit (Project Lead)
