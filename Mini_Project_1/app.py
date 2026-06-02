import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from database import DatabaseManager
from data_loader import DataLoader
from visualizations import MovieVisualizations
from utils import format_duration, get_color_palette
import os

# Page configuration
st.set_page_config(
    page_title="2024 IMDb Movie Data Dashboard",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'preprocessed_data' not in st.session_state:
    st.session_state.preprocessed_data = None
if 'raw_data' not in st.session_state:
    st.session_state.raw_data = None
if 'db_manager' not in st.session_state:
    st.session_state.db_manager = None

@st.cache_data
def load_preprocessed_data():
    """Load and cache preprocessed data for visualizations"""
    loader = DataLoader()
    return loader.load_preprocessed_data()

@st.cache_data
def load_raw_data():
    """Load and cache raw data for database operations"""
    loader = DataLoader()
    return loader.load_raw_data()

@st.cache_resource
def initialize_database():
    """Initialize and cache database connection"""
    return DatabaseManager()

def main():
    # Header
    st.title("🎬 2024 IMDb Movie Data Dashboard")
    st.markdown("### Interactive Data Visualization and Analysis")
    
    # Data source information
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        st.info("📊 **Visualizations**: Using preprocessed data optimized for analysis")
    with col2:
        st.info("🗄️ **Database Queries**: Using raw data for flexible SQL operations")
    with col3:
        if st.button("🔄 Reload Data"):
            # Clear all cached data and session state
            st.cache_data.clear()
            st.cache_resource.clear()
            for key in ['data_loaded', 'preprocessed_data', 'raw_data', 'db_manager']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    
    # Initialize components
    try:
        if not st.session_state.data_loaded:
            with st.spinner("Loading data..."):
                try:
                    st.session_state.preprocessed_data = load_preprocessed_data()
                    st.session_state.raw_data = load_raw_data()
                    st.session_state.db_manager = initialize_database()
                    
                    # Load raw data into database
                    if not st.session_state.raw_data.empty and st.session_state.db_manager.is_connected():
                        try:
                            st.session_state.db_manager.insert_movies_from_dataframe(st.session_state.raw_data)
                        except Exception as db_error:
                            print(f"Database insertion error: {db_error}")
                            # Continue without database functionality
                    
                    st.session_state.data_loaded = True
                except Exception as e:
                    st.error(f"Error during data loading: {str(e)}")
                    # Reset session state on error
                    st.session_state.data_loaded = False
                    st.session_state.preprocessed_data = pd.DataFrame()
                    st.session_state.raw_data = pd.DataFrame()
                    return
        
        preprocessed_data = st.session_state.preprocessed_data
        raw_data = st.session_state.raw_data
        db_manager = st.session_state.db_manager
        
        if preprocessed_data is None or preprocessed_data.empty:
            st.error("No preprocessed data available. Please ensure the preprocessed_data.csv file exists and contains valid data.")
            st.info("Expected CSV columns: title, year, genre, rating, votes, duration, director")
            return
            
        # Initialize visualization class with preprocessed data
        viz = MovieVisualizations(preprocessed_data, db_manager)
        
        # Sidebar filters
        st.sidebar.header("🎛️ Filters")
        
        # Year filter
        if 'year' in preprocessed_data.columns:
            years = sorted(preprocessed_data['year'].dropna().unique())
            selected_years = st.sidebar.multiselect(
                "Select Years",
                years,
                default=[2024] if 2024 in years else years[-3:] if len(years) >= 3 else years
            )
        else:
            selected_years = []
        
        # Genre filter
        if 'genre' in preprocessed_data.columns:
            all_genres = set()
            for genres in preprocessed_data['genre'].dropna():
                if isinstance(genres, str):
                    all_genres.update([g.strip() for g in genres.split(',')])
            all_genres = sorted(list(all_genres))
            selected_genres = st.sidebar.multiselect(
                "Select Genres",
                all_genres,
                default=all_genres  # Select all genres by default
            )
        else:
            selected_genres = []
        
        # Rating filter
        if 'rating' in preprocessed_data.columns:
            rating_range = st.sidebar.slider(
                "Rating Range",
                min_value=float(preprocessed_data['rating'].min()) if not preprocessed_data['rating'].isna().all() else 0.0,
                max_value=float(preprocessed_data['rating'].max()) if not preprocessed_data['rating'].isna().all() else 10.0,
                value=(
                    float(preprocessed_data['rating'].min()) if not preprocessed_data['rating'].isna().all() else 0.0,
                    float(preprocessed_data['rating'].max()) if not preprocessed_data['rating'].isna().all() else 10.0
                ),
                step=0.1
            )
        else:
            rating_range = (0.0, 10.0)
        
        # Remove duration filter since data is not available
        duration_range = (0, 300)  # Default range, not used
        
        # Apply filters to data
        filtered_data = viz.apply_filters(
            selected_years, selected_genres, rating_range, duration_range
        )
        
        if filtered_data.empty:
            st.warning("No data matches the selected filters. Please adjust your criteria.")
            return
        
        # Main dashboard tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Overview", 
            "🏆 Top Movies", 
            "🎭 Genre Analysis", 
            "⭐ Ratings & Votes", 
            "🔗 Correlations"
        ])
        
        with tab1:
            st.header("Dataset Overview")
            
            # Data source status
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📊 Preprocessed Data Status")
                if not preprocessed_data.empty:
                    st.success(f"✅ Loaded: {len(preprocessed_data)} movies")
                    st.write(f"**Columns**: {', '.join(preprocessed_data.columns)}")
                else:
                    st.error("❌ Preprocessed data not found")
            
            with col2:
                st.subheader("🗄️ Raw Data Status")
                if not raw_data.empty:
                    st.success(f"✅ Loaded: {len(raw_data)} movies")
                    st.write(f"**Database**: {'Connected' if db_manager.is_connected() else 'Disconnected'}")
                else:
                    st.error("❌ Raw data not found")
            
            st.divider()
            
            # Metrics for filtered data
            st.subheader("Filtered Data Metrics")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Movies", len(filtered_data))
            with col2:
                avg_rating = filtered_data['rating'].mean() if 'rating' in filtered_data.columns else 0
                st.metric("Average Rating", f"{avg_rating:.1f}")
            with col3:
                total_votes = filtered_data['votes'].sum() if 'votes' in filtered_data.columns else 0
                st.metric("Total Votes", f"{total_votes:,}")
            with col4:
                unique_genres = len(set([g.strip() for genres in filtered_data['genre'].dropna() for g in str(genres).split(',') if g.strip()]))
                st.metric("Unique Genres", unique_genres)
            
            # Dataset sample
            st.subheader("Data Sample (Preprocessed)")
            st.dataframe(filtered_data.head(10), use_container_width=True)
        
        with tab2:
            st.header("Top 10 Movies")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("By Rating")
                viz.plot_top_movies_by_rating(filtered_data)
            
            with col2:
                st.subheader("By Voting Count")
                viz.plot_top_movies_by_votes(filtered_data)
        
        with tab3:
            st.header("Genre Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Genre Distribution")
                viz.plot_genre_distribution(filtered_data)
            
            with col2:
                st.subheader("Genre Vote Count")
                viz.plot_voting_trends_by_genre(filtered_data)
            
            
            st.subheader("Genre-based Rating Leaders")
            viz.plot_genre_rating_leaders(filtered_data)
        
        with tab4:
            st.header("Ratings & Voting Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Rating Distribution")
                viz.plot_rating_distribution(filtered_data)
            
            with col2:
                st.subheader("Most Popular Genre by Voting")
                viz.plot_most_popular_genre_by_voting(filtered_data)
            
            st.subheader("Ratings by Genre")
            viz.plot_ratings_by_genre(filtered_data)
        
        with tab5:
            st.header("Correlation Analysis")
            viz.plot_correlation_analysis(filtered_data)
            
            st.subheader("Scatter Plot Matrix")
            viz.plot_scatter_matrix(filtered_data)
        
        # SQL Database queries section
        st.header("🗄️ Database Queries")
        
        query_type = st.selectbox(
            "Select Query Type",
            ["Custom SQL", "Movies by Genre", "Top Rated Movies", "Movies by Year Range"]
        )
        
        if query_type == "Custom SQL":
            custom_query = st.text_area(
                "Enter your SQL query:",
                placeholder="SELECT * FROM movies WHERE rating > 8.0 LIMIT 10;"
            )
            
            if st.button("Execute Query"):
                if custom_query.strip():
                    try:
                        result = db_manager.execute_query(custom_query)
                        if result is not None and not result.empty:
                            st.dataframe(result, use_container_width=True)
                        else:
                            st.info("Query executed successfully but returned no results.")
                    except Exception as e:
                        st.error(f"Query execution failed: {str(e)}")
                else:
                    st.warning("Please enter a valid SQL query.")
        
        elif query_type == "Movies by Genre":
            genre_query = st.selectbox("Select Genre", all_genres if all_genres else ["Action", "Drama", "Comedy"])
            if st.button("Get Movies"):
                try:
                    result = db_manager.get_movies_by_genre(genre_query)
                    if result is not None and not result.empty:
                        st.dataframe(result, use_container_width=True)
                    else:
                        st.info("No movies found for the selected genre.")
                except Exception as e:
                    st.error(f"Database query failed: {str(e)}")
        
        elif query_type == "Top Rated Movies":
            limit = st.number_input("Number of movies", min_value=1, max_value=100, value=10)
            if st.button("Get Top Movies"):
                try:
                    result = db_manager.get_top_rated_movies(limit)
                    if result is not None and not result.empty:
                        st.dataframe(result, use_container_width=True)
                    else:
                        st.info("No movies found.")
                except Exception as e:
                    st.error(f"Database query failed: {str(e)}")
        
        elif query_type == "Movies by Year Range":
            col1, col2 = st.columns(2)
            with col1:
                start_year = st.number_input("Start Year", min_value=1900, max_value=2024, value=2020)
            with col2:
                end_year = st.number_input("End Year", min_value=1900, max_value=2024, value=2024)
            
            if st.button("Get Movies"):
                try:
                    result = db_manager.get_movies_by_year_range(start_year, end_year)
                    if result is not None and not result.empty:
                        st.dataframe(result, use_container_width=True)
                    else:
                        st.info("No movies found in the selected year range.")
                except Exception as e:
                    st.error(f"Database query failed: {str(e)}")
    
    except Exception as e:
        st.error(f"An error occurred while loading the dashboard: {str(e)}")
        st.info("Please check your data sources and database configuration.")

if __name__ == "__main__":
    main()
