# app.py - Main Streamlit Application
import streamlit as st
import pandas as pd
import json
import time
from database.movie_database import MovieDatabase
from classifier.movie_classifier import MovieGenreClassifier
from utils.helpers import get_rating_class, load_movies_from_file, validate_movie_titles
from utils.ui_components import (
    render_welcome_screen,
    render_single_movie_search,
    render_database_management,
    render_watchlist_management,
    render_batch_classification,
    render_results,
    render_sidebar
)

# Page configuration
st.set_page_config(
    page_title="Movie Database & Genre Classifier",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .genre-card {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f0f2f6;
        margin: 0.5rem 0;
    }
    .stat-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .movie-item {
        padding: 0.5rem;
        margin: 0.25rem 0;
        border-left: 4px solid #1f77b4;
        background-color: #f8f9fa;
    }
    .rating-excellent { color: #00ff00; font-weight: bold; }
    .rating-good { color: #aaff00; font-weight: bold; }
    .rating-average { color: #ffff00; font-weight: bold; }
    .rating-poor { color: #ffaa00; font-weight: bold; }
    .rating-bad { color: #ff0000; font-weight: bold; }
    .watchlist-item { 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function"""
    st.markdown('<h1 class="main-header">🎬 Movie Database & Genre Classification System</h1>', unsafe_allow_html=True)
    
    # Initialize session state
    if 'classified_movies' not in st.session_state:
        st.session_state.classified_movies = None
    if 'processed_movies' not in st.session_state:
        st.session_state.processed_movies = None
    if 'processing_complete' not in st.session_state:
        st.session_state.processing_complete = False
    if 'classifier' not in st.session_state:
        st.session_state.classifier = MovieGenreClassifier()
    if 'quick_search_title' not in st.session_state:
        st.session_state.quick_search_title = None
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"
    if 'batch_movies' not in st.session_state:
        st.session_state.batch_movies = []
    
    classifier = st.session_state.classifier
    
    # Render sidebar and get current page
    page = render_sidebar(classifier)
    
    # Handle quick search redirect
    if st.session_state.quick_search_title and page != "Movie Search":
        page = "Movie Search"
        st.session_state.current_page = "Movie Search"
    
    # Render the appropriate page based on navigation
    if page == "Home":
        render_welcome_screen()
    
    elif page == "Movie Search":
        # Handle quick search from sidebar
        if st.session_state.quick_search_title:
            render_single_movie_search(classifier)
            st.session_state.quick_search_title = None  # Reset after processing
        else:
            render_single_movie_search(classifier)
    
    elif page == "Database":
        render_database_management(classifier)
    
    elif page == "Watchlists":
        render_watchlist_management(classifier)
    
    elif page == "Batch Classification":
        render_batch_classification(classifier)
        
        # Show results if processing was completed
        if st.session_state.processing_complete and st.session_state.classified_movies:
            render_results(classifier, st.session_state.classified_movies)

if __name__ == "__main__":
    main()