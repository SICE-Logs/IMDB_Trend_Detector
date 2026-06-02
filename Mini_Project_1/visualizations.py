import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from utils import format_duration, get_color_palette

class MovieVisualizations:
    def __init__(self, data, db_manager=None):
        self.data = data
        self.db_manager = db_manager
        self.color_palette = get_color_palette()
    
    def apply_filters(self, selected_years, selected_genres, rating_range, duration_range):
        """Apply filters to the data"""
        filtered_data = self.data.copy()
        
        # Filter by year
        if selected_years and 'year' in filtered_data.columns:
            filtered_data = filtered_data[filtered_data['year'].isin(selected_years)]
        
        # Filter by genre
        if selected_genres and 'genre' in filtered_data.columns:
            genre_mask = filtered_data['genre'].str.contains('|'.join(selected_genres), na=False, case=False)
            filtered_data = filtered_data[genre_mask]
        
        # Filter by rating - ensure numeric comparison
        if 'rating' in filtered_data.columns:
            filtered_data['rating'] = pd.to_numeric(filtered_data['rating'], errors='coerce')
            filtered_data = filtered_data[
                (filtered_data['rating'] >= rating_range[0]) & 
                (filtered_data['rating'] <= rating_range[1])
            ]
        
        # Filter by duration - ensure numeric comparison, skip if all NaN
        if 'duration' in filtered_data.columns:
            filtered_data['duration'] = pd.to_numeric(filtered_data['duration'], errors='coerce')
            # Only apply duration filter if there are valid duration values
            valid_durations = filtered_data['duration'].dropna()
            if not valid_durations.empty:
                filtered_data = filtered_data[
                    (filtered_data['duration'] >= duration_range[0]) & 
                    (filtered_data['duration'] <= duration_range[1])
                ]
        
        return filtered_data
    
    def plot_top_movies_by_rating(self, data):
        """Plot top 10 movies by rating"""
        if 'rating' not in data.columns or 'title' not in data.columns:
            st.warning("Required columns (rating, title) not found in data.")
            return
        
        top_movies = data.nlargest(10, 'rating')[['title', 'rating', 'votes']].copy()
        
        if top_movies.empty:
            st.info("No movies found with rating data.")
            return
        
        # Truncate long titles
        top_movies['short_title'] = top_movies['title'].apply(lambda x: x[:30] + '...' if len(x) > 30 else x)
        
        fig = px.bar(
            top_movies, 
            x='rating', 
            y='short_title',
            orientation='h',
            title='Top 10 Movies by Rating',
            labels={'rating': 'IMDb Rating', 'short_title': 'Movie Title'},
            color='rating',
            color_continuous_scale='viridis'
        )
        
        fig.update_layout(height=500)
        fig.update_yaxes(categoryorder='total ascending')
        
        st.plotly_chart(fig, use_container_width=True)
    
    def plot_top_movies_by_votes(self, data):
        """Plot top 10 movies by voting count"""
        if 'votes' not in data.columns or 'title' not in data.columns:
            st.warning("Required columns (votes, title) not found in data.")
            return
        
        top_movies = data.nlargest(10, 'votes')[['title', 'votes', 'rating']].copy()
        
        if top_movies.empty:
            st.info("No movies found with voting data.")
            return
        
        # Truncate long titles
        top_movies['short_title'] = top_movies['title'].apply(lambda x: x[:30] + '...' if len(x) > 30 else x)
        
        fig = px.bar(
            top_movies, 
            x='votes', 
            y='short_title',
            orientation='h',
            title='Top 10 Movies by Voting Count',
            labels={'votes': 'Number of Votes', 'short_title': 'Movie Title'},
            color='votes',
            color_continuous_scale='plasma'
        )
        
        fig.update_layout(height=500)
        fig.update_yaxes(categoryorder='total ascending')
        
        st.plotly_chart(fig, use_container_width=True)
    
    def plot_genre_distribution(self, data):
        """Plot genre distribution"""
        if 'genre' not in data.columns:
            st.warning("Genre column not found in data.")
            return
        
        # Extract individual genres
        all_genres = []
        for genres in data['genre'].dropna():
            if isinstance(genres, str):
                all_genres.extend([g.strip() for g in genres.split(',')])
        
        if not all_genres:
            st.info("No genre data available.")
            return
        
        genre_counts = pd.Series(all_genres).value_counts().head(15)
        
        fig = px.pie(
            values=genre_counts.values, 
            names=genre_counts.index,
            title='Genre Distribution (Top 15)',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=500)
        
        st.plotly_chart(fig, use_container_width=True)
    
    def plot_average_duration_by_genre(self, data):
        """Plot average duration by genre"""
        if 'genre' not in data.columns or 'duration' not in data.columns:
            st.warning("Required columns (genre, duration) not found in data.")
            return
        
        # Calculate average duration by primary genre
        genre_duration = []
        for _, row in data.dropna(subset=['genre', 'duration']).iterrows():
            primary_genre = row['genre'].split(',')[0].strip()
            genre_duration.append({'genre': primary_genre, 'duration': row['duration']})
        
        if not genre_duration:
            st.info("No duration data available by genre.")
            return
        
        genre_df = pd.DataFrame(genre_duration)
        avg_duration = genre_df.groupby('genre')['duration'].mean().sort_values(ascending=False).head(10)
        
        fig = px.bar(
            x=avg_duration.index,
            y=avg_duration.values,
            title='Average Movie Duration by Genre (Top 10)',
            labels={'x': 'Genre', 'y': 'Average Duration (minutes)'},
            color=avg_duration.values,
            color_continuous_scale='viridis'
        )
        
        fig.update_layout(height=500, xaxis_tickangle=-45)
        
        st.plotly_chart(fig, use_container_width=True)
    
    def plot_voting_trends_by_genre(self, data):
        """Plot voting trends by genre"""
        if 'genre' not in data.columns or 'votes' not in data.columns:
            st.warning("Required columns (genre, votes) not found in data.")
            return
        
        # Calculate total votes by primary genre
        genre_votes = []
        for _, row in data.dropna(subset=['genre', 'votes']).iterrows():
            primary_genre = row['genre'].split(',')[0].strip()
            genre_votes.append({'genre': primary_genre, 'votes': row['votes']})
        
        if not genre_votes:
            st.info("No voting data available by genre.")
            return
        
        genre_df = pd.DataFrame(genre_votes)
        total_votes = genre_df.groupby('genre')['votes'].sum().sort_values(ascending=False).head(10)
        
        fig = px.bar(
            x=total_votes.index,
            y=total_votes.values,
            title='Total Votes by Genre (Top 10)',
            labels={'x': 'Genre', 'y': 'Total Votes'},
            color=total_votes.values,
            color_continuous_scale='plasma'
        )
        
        fig.update_layout(height=500, xaxis_tickangle=-45)
        
        st.plotly_chart(fig, use_container_width=True)
    
    def plot_rating_distribution(self, data):
        """Plot rating distribution"""
        if 'rating' not in data.columns:
            st.warning("Rating column not found in data.")
            return
        
        ratings = data['rating'].dropna()
        
        if ratings.empty:
            st.info("No rating data available.")
            return
        
        fig = px.histogram(
            x=ratings,
            nbins=30,
            title='Rating Distribution',
            labels={'x': 'IMDb Rating', 'y': 'Frequency'},
            color_discrete_sequence=['skyblue']
        )
        
        # Add vertical line for mean
        fig.add_vline(x=ratings.mean(), line_dash="dash", line_color="red", 
                      annotation_text=f"Mean: {ratings.mean():.1f}")
        
        fig.update_layout(height=400)
        
        st.plotly_chart(fig, use_container_width=True)
    
    def plot_genre_rating_leaders(self, data):
        """Plot genre-based rating leaders"""
        if 'genre' not in data.columns or 'rating' not in data.columns:
            st.warning("Required columns (genre, rating) not found in data.")
            return
        
        # Get highest rated movie per genre
        genre_leaders = []
        for _, row in data.dropna(subset=['genre', 'rating', 'title']).iterrows():
            primary_genre = row['genre'].split(',')[0].strip()
            genre_leaders.append({
                'genre': primary_genre,
                'title': row['title'],
                'rating': row['rating']
            })
        
        if not genre_leaders:
            st.info("No data available for genre rating leaders.")
            return
        
        leaders_df = pd.DataFrame(genre_leaders)
        top_by_genre = leaders_df.loc[leaders_df.groupby('genre')['rating'].idxmax()]
        top_by_genre = top_by_genre.sort_values('rating', ascending=False).head(10)
        
        fig = px.scatter(
            top_by_genre,
            x='genre',
            y='rating',
            size=[1]*len(top_by_genre),
            hover_name='title',
            title='Highest Rated Movie by Genre (Top 10)',
            labels={'genre': 'Genre', 'rating': 'Rating'}
        )
        
        fig.update_layout(height=500, xaxis_tickangle=-45)
        
        st.plotly_chart(fig, use_container_width=True)
    
    def plot_most_popular_genre_by_voting(self, data):
        """Plot most popular genre by voting"""
        if 'genre' not in data.columns or 'votes' not in data.columns:
            st.warning("Required columns (genre, votes) not found in data.")
            return
        
        # Calculate average votes by genre
        genre_votes = []
        for _, row in data.dropna(subset=['genre', 'votes']).iterrows():
            primary_genre = row['genre'].split(',')[0].strip()
            genre_votes.append({'genre': primary_genre, 'votes': row['votes']})
        
        if not genre_votes:
            st.info("No voting data available by genre.")
            return
        
        genre_df = pd.DataFrame(genre_votes)
        avg_votes = genre_df.groupby('genre')['votes'].mean().sort_values(ascending=False).head(10)
        
        fig = px.bar(
            x=avg_votes.index,
            y=avg_votes.values,
            title='Average Votes by Genre (Top 10)',
            labels={'x': 'Genre', 'y': 'Average Votes'},
            color=avg_votes.values,
            color_continuous_scale='viridis'
        )
        
        fig.update_layout(height=500, xaxis_tickangle=-45)
        
        st.plotly_chart(fig, use_container_width=True)
    
    def show_duration_extremes(self, data):
        """Show duration extremes (shortest and longest movies)"""
        if 'duration' not in data.columns or 'title' not in data.columns:
            st.warning("Required columns (duration, title) not found in data.")
            return
        
        duration_data = data.dropna(subset=['duration', 'title'])
        
        if duration_data.empty:
            st.info("No duration data available.")
            return
        
        shortest = duration_data.nsmallest(5, 'duration')[['title', 'duration', 'rating']]
        longest = duration_data.nlargest(5, 'duration')[['title', 'duration', 'rating']]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Shortest Movies")
            for _, movie in shortest.iterrows():
                rating_str = f" ({movie['rating']:.1f}⭐)" if pd.notna(movie['rating']) else ""
                st.write(f"**{movie['title']}** - {format_duration(movie['duration'])}{rating_str}")
        
        with col2:
            st.subheader("Longest Movies")
            for _, movie in longest.iterrows():
                rating_str = f" ({movie['rating']:.1f}⭐)" if pd.notna(movie['rating']) else ""
                st.write(f"**{movie['title']}** - {format_duration(movie['duration'])}{rating_str}")
    
    def plot_duration_distribution(self, data):
        """Plot duration distribution"""
        if 'duration' not in data.columns:
            st.warning("Duration column not found in data.")
            return
        
        durations = data['duration'].dropna()
        
        if durations.empty:
            st.info("No duration data available.")
            return
        
        fig = px.histogram(
            x=durations,
            nbins=30,
            title='Movie Duration Distribution',
            labels={'x': 'Duration (minutes)', 'y': 'Frequency'},
            color_discrete_sequence=['lightcoral']
        )
        
        # Add vertical line for mean
        fig.add_vline(x=durations.mean(), line_dash="dash", line_color="blue", 
                      annotation_text=f"Mean: {format_duration(durations.mean())}")
        
        fig.update_layout(height=400)
        
        st.plotly_chart(fig, use_container_width=True)
    
    def plot_ratings_by_genre(self, data):
        """Plot ratings by genre using box plot"""
        if 'genre' not in data.columns or 'rating' not in data.columns:
            st.warning("Required columns (genre, rating) not found in data.")
            return
        
        # Create data for box plot
        plot_data = []
        for _, row in data.dropna(subset=['genre', 'rating']).iterrows():
            primary_genre = row['genre'].split(',')[0].strip()
            plot_data.append({'genre': primary_genre, 'rating': row['rating']})
        
        if not plot_data:
            st.info("No data available for ratings by genre.")
            return
        
        plot_df = pd.DataFrame(plot_data)
        
        # Get top 10 genres by count
        top_genres = plot_df['genre'].value_counts().head(10).index
        plot_df = plot_df[plot_df['genre'].isin(top_genres)]
        
        fig = px.box(
            plot_df,
            x='genre',
            y='rating',
            title='Rating Distribution by Genre (Top 10)',
            labels={'genre': 'Genre', 'rating': 'Rating'}
        )
        
        fig.update_layout(height=500, xaxis_tickangle=-45)
        
        st.plotly_chart(fig, use_container_width=True)
    
    def plot_correlation_analysis(self, data):
        """Plot correlation matrix"""
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) < 2:
            st.info("Not enough numeric columns for correlation analysis.")
            return
        
        corr_matrix = data[numeric_cols].corr()
        
        fig = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            title="Correlation Matrix of Numeric Variables",
            color_continuous_scale='RdBu'
        )
        
        fig.update_layout(height=600)
        
        st.plotly_chart(fig, use_container_width=True)
    
    def plot_scatter_matrix(self, data):
        """Plot scatter plot matrix"""
        numeric_cols = ['rating', 'votes', 'duration', 'year']
        available_cols = [col for col in numeric_cols if col in data.columns]
        
        if len(available_cols) < 2:
            st.info("Not enough numeric columns for scatter plot matrix.")
            return
        
        # Sample data if too large
        sample_data = data[available_cols].dropna()
        if len(sample_data) > 1000:
            sample_data = sample_data.sample(1000, random_state=42)
        
        fig = px.scatter_matrix(
            sample_data,
            dimensions=available_cols,
            title="Scatter Plot Matrix of Movie Metrics"
        )
        
        fig.update_layout(height=800)
        
        st.plotly_chart(fig, use_container_width=True)
