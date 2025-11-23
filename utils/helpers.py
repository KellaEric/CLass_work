# utils/helpers.py - Utility functions
import pandas as pd
import json
from typing import List, Tuple

def get_rating_class(rating):
    """Get CSS class for rating display"""
    if not rating or rating == 'N/A':
        return ""
    try:
        rating_val = float(rating)
        if rating_val >= 8:
            return "rating-excellent"
        elif rating_val >= 7:
            return "rating-good"
        elif rating_val >= 6:
            return "rating-average"
        elif rating_val >= 5:
            return "rating-poor"
        else:
            return "rating-bad"
    except:
        return ""

def load_movies_from_file(uploaded_file) -> List[str]:
    """Load movie titles from various file formats"""
    movie_titles = []
    
    try:
        if uploaded_file.name.endswith('.csv'):
            # Read CSV file
            df = pd.read_csv(uploaded_file)
            # Assume first column contains movie titles
            movie_titles = df.iloc[:, 0].dropna().astype(str).tolist()
            
        elif uploaded_file.name.endswith('.txt'):
            # Read text file
            content = uploaded_file.getvalue().decode("utf-8")
            movie_titles = [line.strip() for line in content.split('\n') if line.strip()]
                
        elif uploaded_file.name.endswith('.json'):
            # Read JSON file
            content = uploaded_file.getvalue().decode("utf-8")
            data = json.loads(content)
            if isinstance(data, list):
                movie_titles = [item if isinstance(item, str) else str(item) for item in data]
            elif isinstance(data, dict):
                # Try to extract titles from common keys
                for key in ['movies', 'titles', 'items']:
                    if key in data and isinstance(data[key], list):
                        movie_titles = [item if isinstance(item, str) else str(item) for item in data[key]]
                        break
                
    except Exception as e:
        import streamlit as st
        st.error(f"Error reading file: {str(e)}")
    
    return movie_titles

def validate_movie_titles(movie_titles: List[str]) -> Tuple[List[str], List[str]]:
    """Validate and clean movie titles"""
    valid_titles = []
    invalid_titles = []
    
    for title in movie_titles:
        cleaned_title = title.strip()
        if cleaned_title and len(cleaned_title) >= 1:
            valid_titles.append(cleaned_title)
        else:
            invalid_titles.append(title)
    
    return valid_titles, invalid_titles