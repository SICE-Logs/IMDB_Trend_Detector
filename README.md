# 🎬 IMDb 2024 Data Analytics & Visualization Dashboard

> Transforming raw IMDb movie data into actionable insights through data engineering, analytics, and interactive visualization.

---

## 📖 Overview

This project collects, processes, and analyzes IMDb 2024 movie data to uncover trends in ratings, genres, voting patterns, and movie characteristics.

Using automated web scraping, structured data storage, exploratory data analysis (EDA), and an interactive Streamlit dashboard, the project provides a deeper understanding of the modern movie landscape beyond IMDb's standard browsing experience.

---

## 🎯 Project Objectives

The project aims to:

* Extract real-world movie data from IMDb
* Store and organize datasets efficiently
* Perform exploratory data analysis
* Identify patterns in ratings and voting behavior
* Visualize insights through an interactive dashboard
* Demonstrate an end-to-end data analytics workflow

---

## 🚀 Features

### 🌐 Automated Data Collection

* Scrapes IMDb 2024 movie data using Selenium
* Collects:

  * Movie Name
  * Genre
  * Rating
  * Vote Count
  * Duration

> ⚠️ Selenium is used because IMDb employs dynamic page rendering and anti-bot mechanisms.

---

### 🗄️ Data Storage

The project stores data in two formats:

#### CSV Files

* Cleaned datasets for analytics
* Easy integration with Pandas

#### SQL Database

* Structured storage
* Querying and filtering capabilities
* Efficient data management

---

### 📊 Exploratory Data Analysis

Using Pandas, Matplotlib, and Seaborn:

* Genre popularity analysis
* Rating distributions
* Vote count analysis
* Runtime comparisons
* Correlation studies

---

### 📈 Interactive Dashboard

Built with Streamlit.

Dashboard capabilities include:

* Top-rated movie rankings
* Genre distribution visualizations
* Rating vs vote analysis
* Statistical summaries
* Interactive filtering and exploration

---

## 🏗️ Project Architecture

```text
IMDb Website
      │
      ▼
 Selenium Scraper
      │
      ▼
 Raw Dataset
      │
 ┌────┴────┐
 │         │
 ▼         ▼
CSV      SQL Database
 │         │
 └────┬────┘
      ▼
 Data Analysis
      │
      ▼
 Streamlit Dashboard
      │
      ▼
 User Insights
```

---

## ⚙️ Tech Stack

### Programming Language

* Python

### Data Analysis

* Pandas
* NumPy

### Visualization

* Matplotlib
* Seaborn

### Web Scraping

* Selenium

### Dashboard

* Streamlit

### Database

* SQLite
* SQLAlchemy

---

## 📂 Repository Structure

```text
IMDb-2024-Analytics/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   └── exploratory_analysis.ipynb
│
├── src/
│   ├── scraper.py
│   ├── database.py
│   └── analysis.py
│
├── app.py
├── requirements.txt
└── README.md
```

---

## 🔧 Installation

### Clone Repository

```bash
git clone https://github.com/SICE_Logs/IMDB_Trend_Detector.git
cd imdb-2024-dashboard
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Launch Dashboard

```bash
streamlit run app.py
```

---

## 📊 Insights Generated

The dashboard enables users to explore:

* Highest-rated movies
* Most-voted movies
* Genre popularity trends
* Average duration by genre
* Rating and vote correlations
* Distribution of movie ratings

---

## 📸 Dashboard Preview

Add screenshots here.

Examples:

* Genre Distribution Chart
* Top Movies Dashboard
* Rating Analysis Dashboard
* Correlation Heatmaps

---

## 🌍 Real-World Applications

### 🎥 Movie Enthusiasts

Discover top-performing genres and hidden gems.

### 📺 OTT Platforms

Analyze audience preferences and content trends.

### 🎬 Producers & Studios

Understand genre popularity and viewer behavior.

### 📚 Students & Researchers

Learn web scraping, data engineering, analytics, and visualization workflows.

---

## 📈 Future Enhancements

* [ ] Sentiment Analysis using movie reviews
* [ ] Machine Learning based rating prediction
* [ ] Trend forecasting models
* [ ] Integration with Rotten Tomatoes and Metacritic
* [ ] Cloud deployment
* [ ] Real-time dashboard updates

---

## 🏆 Key Learning Outcomes

Through this project:

* Implemented automated web scraping
* Built structured data pipelines
* Performed exploratory data analysis
* Designed interactive dashboards
* Worked with SQL databases
* Applied data visualization best practices

---

## 👨‍💻 Author

**S Logajit**

AI & Data Science Student

Project Lead & Developer

---

## ⭐ Support

If you found this project useful, consider giving it a star and sharing feedback.

👨‍💻 Contributors

S Logajit (Project Lead)
