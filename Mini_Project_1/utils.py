import pandas as pd
import numpy as np
from typing import List, Dict, Any

def format_duration(minutes):
    """Format duration in minutes to hours and minutes"""
    if pd.isna(minutes) or minutes == 0:
        return "N/A"
    
    hours = int(minutes // 60)
    mins = int(minutes % 60)
    
    if hours == 0:
        return f"{mins}m"
    elif mins == 0:
        return f"{hours}h"
    else:
        return f"{hours}h {mins}m"

def get_color_palette():
    """Get a color palette for visualizations"""
    return [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
        '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5'
    ]

def clean_genre_string(genre_string):
    """Clean and standardize genre strings"""
    if pd.isna(genre_string):
        return []
    
    if isinstance(genre_string, str):
        genres = [g.strip() for g in genre_string.split(',')]
        return [g for g in genres if g]  # Remove empty strings
    
    return []

def extract_year_from_title(title):
    """Extract year from movie title if present"""
    import re
    
    if pd.isna(title):
        return None
    
    # Look for year in parentheses at the end
    match = re.search(r'\((\d{4})\)$', title)
    if match:
        return int(match.group(1))
    
    return None

def validate_rating(rating):
    """Validate and clean rating values"""
    if pd.isna(rating):
        return None
    
    try:
        rating = float(rating)
        if 0 <= rating <= 10:
            return rating
        else:
            return None
    except (ValueError, TypeError):
        return None

def validate_votes(votes):
    """Validate and clean vote counts"""
    if pd.isna(votes):
        return 0
    
    try:
        votes = int(votes)
        return max(0, votes)  # Ensure non-negative
    except (ValueError, TypeError):
        return 0

def validate_duration(duration):
    """Validate and clean duration values"""
    if pd.isna(duration):
        return None
    
    try:
        duration = float(duration)
        if 1 <= duration <= 1000:  # Reasonable range for movie duration
            return duration
        else:
            return None
    except (ValueError, TypeError):
        return None

def calculate_genre_statistics(data, genre_col='genre'):
    """Calculate comprehensive statistics by genre"""
    if genre_col not in data.columns:
        return {}
    
    stats = {}
    all_genres = set()
    
    # Extract all unique genres
    for genres in data[genre_col].dropna():
        if isinstance(genres, str):
            all_genres.update(clean_genre_string(genres))
    
    # Calculate statistics for each genre
    for genre in all_genres:
        genre_data = data[data[genre_col].str.contains(genre, na=False, case=False)]
        
        if not genre_data.empty:
            stats[genre] = {
                'count': len(genre_data),
                'avg_rating': genre_data['rating'].mean() if 'rating' in genre_data.columns else None,
                'avg_duration': genre_data['duration'].mean() if 'duration' in genre_data.columns else None,
                'total_votes': genre_data['votes'].sum() if 'votes' in genre_data.columns else 0,
                'avg_votes': genre_data['votes'].mean() if 'votes' in genre_data.columns else 0
            }
    
    return stats

def format_number(number):
    """Format large numbers with appropriate suffixes"""
    if pd.isna(number):
        return "N/A"
    
    if abs(number) >= 1_000_000:
        return f"{number/1_000_000:.1f}M"
    elif abs(number) >= 1_000:
        return f"{number/1_000:.1f}K"
    else:
        return f"{number:,.0f}"

def get_top_items(data, column, n=10, ascending=False):
    """Get top N items from a column"""
    if column not in data.columns:
        return pd.Series(dtype='object')
    
    return data[column].value_counts(ascending=ascending).head(n)

def filter_data_by_criteria(data, criteria):
    """Filter data based on multiple criteria"""
    filtered_data = data.copy()
    
    for key, value in criteria.items():
        if key in data.columns and value is not None:
            if isinstance(value, (list, tuple)):
                if len(value) == 2:  # Range filter
                    filtered_data = filtered_data[
                        (filtered_data[key] >= value[0]) & 
                        (filtered_data[key] <= value[1])
                    ]
                else:  # List filter
                    filtered_data = filtered_data[filtered_data[key].isin(value)]
            else:  # Single value filter
                filtered_data = filtered_data[filtered_data[key] == value]
    
    return filtered_data

def create_summary_stats(data):
    """Create summary statistics for the dataset"""
    if data.empty:
        return {}
    
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    
    summary = {
        'total_records': len(data),
        'total_columns': len(data.columns),
        'missing_values_pct': (data.isnull().sum() / len(data) * 100).to_dict(),
        'numeric_summary': data[numeric_cols].describe().to_dict() if len(numeric_cols) > 0 else {}
    }
    
    return summary
