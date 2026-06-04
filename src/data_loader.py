import pandas as pd
import streamlit as st
import config


class DataLoader:
    def __init__(self):
        
        self.raw_data_path = config.RAW_DATA_PATH 
        self.preprocessed_data_path = config.PREPROCESSED_DATA_PATH 
    
    def load_preprocessed_data(self):
        """Load preprocessed data from CSV file for visualizations"""
        try:
            if self.preprocessed_data_path.exists() and self.preprocessed_data_path.is_file():
                df = pd.read_csv(self.preprocessed_data_path)
                # Map column names to expected format
                df = self._standardize_columns(df)
                return df
            else:
                st.warning(f"Preprocessed CSV file '{self.preprocessed_data_path}' not found.")
                return pd.DataFrame()
                
        except Exception as e:
            st.error(f"Error loading preprocessed data: {str(e)}")
            return pd.DataFrame()
    
    def load_raw_data(self):
        """Load raw data from CSV file for database operations"""
        try:
            if self.raw_data_path.exists() and self.raw_data_path.is_file():
                df = pd.read_csv(self.raw_data_path)
                
                # Map column names to expected format
                df = self._standardize_columns(df)
                
                # Basic data cleaning for database insertion
                df = self._clean_data(df)
                
                return df
            else:
                st.warning(f"Raw CSV file '{self.raw_data_path}' not found.")
                return pd.DataFrame()
                
        except Exception as e:
            st.error(f"Error loading raw data: {str(e)}")
            return pd.DataFrame()
    
    def load_csv_data(self):
        """Load data from CSV file - defaults to preprocessed for backward compatibility"""
        return self.load_preprocessed_data()
    
    def _standardize_columns(self, df):
        """Standardize column names to match expected format"""
        # Column name mapping from your CSV format to expected format
        column_mapping = {
            'Title': 'title',
            'Rating': 'rating', 
            'Votes': 'votes',
            'Duration': 'duration',
            'Genre': 'genre'
        }
        
        # Rename columns if they exist
        df = df.rename(columns=column_mapping)
        
        # Add missing columns with default values
        required_columns = ['title', 'year', 'genre', 'rating', 'votes', 'duration', 'director']
        for col in required_columns:
            if col not in df.columns:
                if col == 'year':
                    df[col] = 2024  # Default to 2024
                elif col == 'director':
                    df[col] = 'Unknown Director'
                else:
                    df[col] = None
        
        # Force convert all numeric columns to proper types immediately
        for col in ['year', 'rating', 'votes', 'duration']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df
    
    def _clean_data(self, df):
        """Clean and preprocess the data"""
        try:
            # Convert data types
            if 'year' in df.columns:
                df['year'] = pd.to_numeric(df['year'], errors='coerce')
            
            if 'rating' in df.columns:
                df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
            
            if 'votes' in df.columns:
                # Clean votes column - handle formats like "(253K)" or "253K"
                df['votes'] = df['votes'].astype(str).str.replace(r'[(),]', '', regex=True)
                df['votes'] = df['votes'].str.replace('K', '000', regex=False)
                df['votes'] = df['votes'].str.replace('M', '000000', regex=False)
                df['votes'] = pd.to_numeric(df['votes'], errors='coerce')
            
            if 'duration' in df.columns:
                # Clean duration column - handle formats like "2h 28m" or "1h 35m"
                df['duration'] = df['duration'].astype(str)
                # Extract hours and minutes, convert to total minutes
                def parse_duration(dur_str):
                    if pd.isna(dur_str) or dur_str == 'nan':
                        return None
                    
                    try:
                        hours = 0
                        minutes = 0
                        dur_str = str(dur_str).strip()
                        
                        if 'h' in dur_str and 'm' in dur_str:
                            # Format: "2h 28m"
                            parts = dur_str.split('h')
                            hours = int(parts[0].strip()) if parts[0].strip().isdigit() else 0
                            if len(parts) > 1:
                                min_part = parts[1].replace('m', '').strip()
                                minutes = int(min_part) if min_part.isdigit() else 0
                        elif 'h' in dur_str:
                            # Format: "2h"
                            hour_part = dur_str.replace('h', '').strip()
                            hours = int(hour_part) if hour_part.isdigit() else 0
                        elif 'm' in dur_str:
                            # Format: "15m"
                            min_part = dur_str.replace('m', '').strip()
                            minutes = int(min_part) if min_part.isdigit() else 0
                        else:
                            # Try to parse as plain number (assume minutes)
                            if dur_str.isdigit():
                                minutes = int(dur_str)
                        
                        return hours * 60 + minutes
                    except (ValueError, AttributeError):
                        return None
                
                df['duration'] = df['duration'].apply(parse_duration)
            
            # Remove rows with all NaN values
            df = df.dropna(how='all')
            
            # Fill missing values with appropriate defaults
            if 'title' in df.columns:
                df['title'] = df['title'].fillna('Unknown Title')
            
            if 'genre' in df.columns:
                df['genre'] = df['genre'].fillna('Unknown')
            
            if 'director' in df.columns:
                df['director'] = df['director'].fillna('Unknown Director')
            
            # Remove duplicates based on title and year
            if 'title' in df.columns and 'year' in df.columns:
                df = df.drop_duplicates(subset=['title', 'year'], keep='first')
            
            return df
            
        except Exception as e:
            st.error(f"Error cleaning data: {str(e)}")
            return df
    
    def validate_data(self, df):
        """Validate the loaded data"""
        if df.empty:
            return False, "Dataset is empty"
        
        required_columns = ['title']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return False, f"Missing required columns: {missing_columns}"
        
        return True, "Data validation passed"
    
    def get_data_info(self, df):
        """Get information about the dataset"""
        if df.empty:
            return {}
        
        info = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'columns': list(df.columns),
            'memory_usage': df.memory_usage(deep=True).sum(),
            'missing_values': df.isnull().sum().to_dict()
        }
        
        return info
    
    def sample_data_for_display(self, df, n_rows=5):
        """Get a sample of data for display purposes"""
        if df.empty:
            return pd.DataFrame()
        
        return df.head(n_rows)


