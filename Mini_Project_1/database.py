import os
import pandas as pd
from sqlalchemy import create_engine, text, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import streamlit as st

Base = declarative_base()

class Movie(Base):
    __tablename__ = 'movies'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    year = Column(Integer)
    genre = Column(String)
    rating = Column(Float)
    votes = Column(Integer)
    duration = Column(Integer)
    director = Column(String)

class DatabaseManager:
    def __init__(self):
        self.engine = None
        self.Session = None
        self.connection_status = False
        self._initialize_connection()
    
    def _initialize_connection(self):
        """Initialize database connection"""
        try:
            # Try to get database URL from environment
            database_url = os.getenv('DATABASE_URL')
            
            if database_url:
                # Use provided database URL (for production)
                self.engine = create_engine(database_url)
            else:
                # Fallback to local SQLite database
                self.engine = create_engine('sqlite:///movies.db', echo=False)
            
            # Test connection
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            self.Session = sessionmaker(bind=self.engine)
            self.connection_status = True
            
            # Create tables if they don't exist
            Base.metadata.create_all(self.engine)
            
        except Exception as e:
            print(f"Database connection failed: {str(e)}. Using limited functionality.")
            self.connection_status = False
    
    def is_connected(self):
        """Check if database is connected"""
        return self.connection_status
    
    def execute_query(self, query):
        """Execute a custom SQL query"""
        if not self.connection_status:
            raise Exception("Database not connected")
        
        try:
            with self.engine.connect() as conn:
                result = pd.read_sql(query, conn)
                return result
        except Exception as e:
            raise Exception(f"Query execution failed: {str(e)}")
    
    def insert_movies_from_dataframe(self, df):
        """Insert movies from a pandas DataFrame"""
        if not self.connection_status:
            return False
        
        try:
            # Ensure the DataFrame has the required columns
            required_cols = ['title', 'year', 'genre', 'rating', 'votes', 'duration', 'director']
            for col in required_cols:
                if col not in df.columns:
                    df[col] = None
            
            # Insert data
            df[required_cols].to_sql('movies', self.engine, if_exists='replace', index=False)
            return True
        except Exception as e:
            st.error(f"Failed to insert data: {str(e)}")
            return False
    
    def get_movies_by_genre(self, genre):
        """Get movies by genre"""
        if not self.connection_status:
            return pd.DataFrame()
        
        try:
            query = """
            SELECT title, year, rating, votes, duration, director 
            FROM movies 
            WHERE genre LIKE ? 
            ORDER BY rating DESC 
            LIMIT 50
            """
            
            with self.engine.connect() as conn:
                result = pd.read_sql(query, conn, params=[f'%{genre}%'])
                return result
        except Exception as e:
            st.error(f"Database query failed: {str(e)}")
            return pd.DataFrame()
    
    def get_top_rated_movies(self, limit=10):
        """Get top rated movies"""
        if not self.connection_status:
            return pd.DataFrame()
        
        try:
            query = """
            SELECT title, year, genre, rating, votes, duration, director 
            FROM movies 
            WHERE rating IS NOT NULL 
            ORDER BY rating DESC, votes DESC 
            LIMIT ?
            """
            
            with self.engine.connect() as conn:
                result = pd.read_sql(query, conn, params=[limit])
                return result
        except Exception as e:
            st.error(f"Database query failed: {str(e)}")
            return pd.DataFrame()
    
    def get_movies_by_year_range(self, start_year, end_year):
        """Get movies within a year range"""
        if not self.connection_status:
            return pd.DataFrame()
        
        try:
            query = """
            SELECT title, year, genre, rating, votes, duration, director 
            FROM movies 
            WHERE year BETWEEN ? AND ? 
            ORDER BY year DESC, rating DESC 
            LIMIT 100
            """
            
            with self.engine.connect() as conn:
                result = pd.read_sql(query, conn, params=[start_year, end_year])
                return result
        except Exception as e:
            st.error(f"Database query failed: {str(e)}")
            return pd.DataFrame()
    
    def get_genre_statistics(self):
        """Get statistics by genre"""
        if not self.connection_status:
            return pd.DataFrame()
        
        try:
            query = """
            SELECT 
                genre,
                COUNT(*) as movie_count,
                AVG(rating) as avg_rating,
                AVG(duration) as avg_duration,
                SUM(votes) as total_votes
            FROM movies 
            WHERE genre IS NOT NULL 
            GROUP BY genre 
            ORDER BY movie_count DESC
            """
            
            with self.engine.connect() as conn:
                result = pd.read_sql(query, conn)
                return result
        except Exception as e:
            st.error(f"Database query failed: {str(e)}")
            return pd.DataFrame()
    
    def close_connection(self):
        """Close database connection"""
        if self.engine:
            self.engine.dispose()
            self.connection_status = False
