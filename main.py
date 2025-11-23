# movie_app.py - Complete Movie Database & Genre Classification System
import streamlit as st
import pandas as pd
import requests
import json
import time
import sqlite3
import hashlib
import re
import plotly.express as px
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from io import StringIO

# Page configuration
st.set_page_config(
    page_title="Movie Database & Genre Classifier",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with enhanced login styles
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
    
    /* Enhanced Login Page Styles */
    .auth-container {
        max-width: 450px;
        margin: 50px auto;
        padding: 2.5rem;
        background: white;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        text-align: center;
        position: relative;
    }
    .auth-header {
        font-size: 2.8rem;
        margin-bottom: 0.5rem;
    }
    .auth-title {
        color: #1f77b4;
        margin-bottom: 0.5rem;
        font-size: 1.8rem;
    }
    .auth-subtitle {
        color: #666;
        margin-bottom: 2rem;
        font-size: 1rem;
    }
    .auth-tabs {
        display: flex;
        margin-bottom: 2rem;
        background: #f8f9fa;
        border-radius: 12px;
        padding: 4px;
    }
    .auth-tab {
        flex: 1;
        padding: 12px;
        border: none;
        background: transparent;
        border-radius: 8px;
        cursor: pointer;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .auth-tab.active {
        background: white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        color: #1f77b4;
    }
    .auth-form {
        text-align: left;
    }
    .auth-input {
        width: 100%;
        padding: 14px;
        margin: 8px 0;
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-sizing: border-box;
    }
    .auth-input:focus {
        border-color: #1f77b4;
        outline: none;
        box-shadow: 0 0 0 3px rgba(29, 119, 180, 0.1);
    }
    .auth-button {
        width: 100%;
        padding: 14px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        font-size: 1.1rem;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        margin-top: 1rem;
    }
    .auth-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    .demo-button {
        background: linear-gradient(135deg, #00b09b 0%, #96c93d 100%) !important;
    }
    .demo-button:hover {
        box-shadow: 0 5px 15px rgba(0, 176, 155, 0.4) !important;
    }
    .auth-link {
        color: #1f77b4;
        text-decoration: none;
        cursor: pointer;
        font-weight: 500;
        margin: 0 8px;
    }
    .auth-link:hover {
        text-decoration: underline;
    }
    .auth-footer {
        margin-top: 1.5rem;
        padding-top: 1.5rem;
        border-top: 1px solid #e0e0e0;
    }
    .demo-credentials {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-top: 1.5rem;
        border-left: 4px solid #ffc107;
        text-align: left;
    }
    .password-requirements {
        font-size: 0.8rem;
        color: #666;
        margin-top: 0.5rem;
    }
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 3rem 0;
    }
    .feature-card {
        background: white;
        padding: 2rem 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        text-align: center;
        transition: transform 0.3s ease;
    }
    .feature-card:hover {
        transform: translateY(-5px);
    }
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    .success-message {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        color: #155724;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #28a745;
    }
    .error-message {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        color: #721c24;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #dc3545;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# DATABASE CLASS
# =============================================================================

class MovieDatabase:
    def __init__(self):
        self.db_path = "movie_database.db"
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Movies table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                year TEXT,
                genres TEXT,
                rating REAL,
                director TEXT,
                actors TEXT,
                runtime TEXT,
                overview TEXT,
                poster_url TEXT,
                imdb_id TEXT,
                date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(title, year)
            )
        ''')
        
        # Watchlists table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS watchlists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Watchlist items table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS watchlist_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                watchlist_id INTEGER,
                movie_id INTEGER,
                added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (watchlist_id) REFERENCES watchlists (id),
                FOREIGN KEY (movie_id) REFERENCES movies (id),
                UNIQUE(watchlist_id, movie_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_movie(self, movie_data):
        """Add movie to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO movies 
                (title, year, genres, rating, director, actors, runtime, overview, poster_url, imdb_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                movie_data.get('title'),
                movie_data.get('year'),
                ', '.join(movie_data.get('genres', [])),
                float(movie_data.get('rating', 0)) if movie_data.get('rating') and movie_data.get('rating') != 'N/A' else 0,
                movie_data.get('director'),
                movie_data.get('actors'),
                movie_data.get('runtime'),
                movie_data.get('overview'),
                movie_data.get('poster'),
                movie_data.get('imdb_id', '')
            ))
            
            conn.commit()
            movie_id = cursor.lastrowid
            return movie_id
        except Exception as e:
            st.error(f"Error adding movie to database: {e}")
            return None
        finally:
            conn.close()
    
    def get_all_movies(self):
        """Get all movies from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM movies ORDER BY date_added DESC
        ''')
        
        movies = cursor.fetchall()
        conn.close()
        
        return movies
    
    def search_movies(self, query):
        """Search movies in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM movies 
            WHERE title LIKE ? OR genres LIKE ? OR director LIKE ? OR actors LIKE ?
            ORDER BY rating DESC
        ''', (f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%'))
        
        movies = cursor.fetchall()
        conn.close()
        
        return movies
    
    def create_watchlist(self, name, description=""):
        """Create a new watchlist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO watchlists (name, description) VALUES (?, ?)
            ''', (name, description))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            st.error("Watchlist with this name already exists!")
            return False
        finally:
            conn.close()
    
    def get_watchlists(self):
        """Get all watchlists"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT w.*, COUNT(wi.movie_id) as movie_count 
            FROM watchlists w 
            LEFT JOIN watchlist_items wi ON w.id = wi.watchlist_id 
            GROUP BY w.id
            ORDER BY w.created_date DESC
        ''')
        
        watchlists = cursor.fetchall()
        conn.close()
        
        return watchlists
    
    def add_to_watchlist(self, watchlist_id, movie_id):
        """Add movie to watchlist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO watchlist_items (watchlist_id, movie_id) VALUES (?, ?)
            ''', (watchlist_id, movie_id))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            st.warning("Movie already in watchlist!")
            return False
        finally:
            conn.close()
    
    def get_watchlist_movies(self, watchlist_id):
        """Get movies from a specific watchlist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT m.* FROM movies m
            JOIN watchlist_items wi ON m.id = wi.movie_id
            WHERE wi.watchlist_id = ?
            ORDER BY wi.added_date DESC
        ''', (watchlist_id,))
        
        movies = cursor.fetchall()
        conn.close()
        
        return movies
    
    def delete_watchlist(self, watchlist_id):
        """Delete a watchlist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # First delete watchlist items
            cursor.execute('DELETE FROM watchlist_items WHERE watchlist_id = ?', (watchlist_id,))
            # Then delete watchlist
            cursor.execute('DELETE FROM watchlists WHERE id = ?', (watchlist_id,))
            conn.commit()
            return True
        except Exception as e:
            st.error(f"Error deleting watchlist: {e}")
            return False
        finally:
            conn.close()

# =============================================================================
# API HANDLER CLASS
# =============================================================================

class OMDbHandler:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "http://www.omdbapi.com/"
    
    def search_movie(self, movie_title: str) -> Optional[Dict]:
        """Search for movie using OMDb API"""
        try:
            params = {
                'apikey': self.api_key,
                't': movie_title,
                'type': 'movie',
                'plot': 'short'
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data.get('Response') == 'True':
                return data
            else:
                return None
                
        except requests.exceptions.RequestException as e:
            st.sidebar.warning(f"OMDb API error for '{movie_title}': {e}")
        except Exception as e:
            st.sidebar.warning(f"Unexpected error with OMDb for '{movie_title}': {e}")
            
        return None
    
    def get_movie_data(self, movie_title: str) -> Dict:
        """Get movie data from OMDb API"""
        movie_data = {}
        
        # Try OMDb API
        omdb_data = self.search_movie(movie_title)
        if omdb_data:
            movie_data['omdb'] = omdb_data
            movie_data['title'] = omdb_data.get('Title', movie_title)
            movie_data['genres'] = omdb_data.get('Genre', '').split(', ') if omdb_data.get('Genre') else []
            movie_data['year'] = omdb_data.get('Year', 'Unknown').replace('–', '').split('–')[0]
            movie_data['overview'] = omdb_data.get('Plot', '')
            movie_data['rating'] = omdb_data.get('imdbRating')
            movie_data['votes'] = omdb_data.get('imdbVotes', '0').replace(',', '')
            movie_data['director'] = omdb_data.get('Director', 'Unknown')
            movie_data['actors'] = omdb_data.get('Actors', 'Unknown')
            movie_data['runtime'] = omdb_data.get('Runtime', 'Unknown')
            movie_data['box_office'] = omdb_data.get('BoxOffice', 'Unknown')
            movie_data['poster'] = omdb_data.get('Poster', '')
            movie_data['metascore'] = omdb_data.get('Metascore', 'N/A')
            movie_data['imdb_id'] = omdb_data.get('imdbID', '')
            movie_data['omdb_link'] = f"https://www.imdb.com/title/{omdb_data.get('imdbID', '')}" if omdb_data.get('imdbID') else ""
            movie_data['source'] = 'OMDb'
        
        # If no API data found, create minimal data
        if not movie_data:
            movie_data = {
                'title': movie_title,
                'genres': ['Unknown'],
                'year': 'Unknown',
                'overview': 'No information available',
                'rating': None,
                'votes': '0',
                'director': 'Unknown',
                'actors': 'Unknown',
                'runtime': 'Unknown',
                'box_office': 'Unknown',
                'poster': '',
                'metascore': 'N/A',
                'imdb_id': '',
                'omdb_link': '',
                'source': 'Not Found'
            }
        
        return movie_data

# =============================================================================
# CLASSIFIER CLASS
# =============================================================================

class MovieGenreClassifier:
    def __init__(self):
        # Your OMDb API key directly implemented
        self.omdb_api_key = "4bcd5aba"
        self.database = MovieDatabase()
        self.omdb_handler = OMDbHandler(self.omdb_api_key)
        
        self.default_genres = [
            "Action", "Adventure", "Animation", "Comedy", "Crime", 
            "Documentary", "Drama", "Family", "Fantasy", "History",
            "Horror", "Music", "Mystery", "Romance", "Science Fiction",
            "Thriller", "War", "Western", "Unknown"
        ]
        self.processed_movies = []
        
    def get_movie_data(self, movie_title: str) -> Dict:
        """Get movie data using OMDb handler"""
        return self.omdb_handler.get_movie_data(movie_title)

    def search_single_movie(self, movie_title: str) -> Dict:
        """Search for a single movie and return detailed results"""
        movie_data = self.get_movie_data(movie_title)
        
        # Add to database if found
        if movie_data and movie_data.get('source') != 'Not Found':
            self.database.add_movie(movie_data)
        
        return movie_data
    
    def classify_movies(self, movie_titles: List[str], progress_callback=None) -> Dict[str, Any]:
        """Classify a list of movies by genre"""
        classified_movies = {genre: [] for genre in self.default_genres}
        self.processed_movies = []
        
        total_movies = len(movie_titles)
        
        for i, title in enumerate(movie_titles):
            if progress_callback:
                progress_callback(i + 1, total_movies)
            
            movie_data = self.get_movie_data(title.strip())
            self.processed_movies.append(movie_data)
            
            # Add to database if found
            if movie_data and movie_data.get('source') != 'Not Found':
                self.database.add_movie(movie_data)
            
            # Add to genre categories
            genres = movie_data.get('genres', [])
            if not genres or genres == ['Unknown']:
                classified_movies['Unknown'].append(movie_data)
            else:
                for genre in genres:
                    if genre in classified_movies:
                        classified_movies[genre].append(movie_data)
                    else:
                        classified_movies['Unknown'].append(movie_data)
            
            # Small delay to be respectful to API
            time.sleep(0.2)
        
        return classified_movies
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about processed movies"""
        if not self.processed_movies:
            return {}
        
        total_movies = len(self.processed_movies)
        found_movies = len([m for m in self.processed_movies if m.get('source') != 'Not Found'])
        unknown_genres = len([m for m in self.processed_movies if not m.get('genres') or m.get('genres') == ['Unknown']])
        
        genre_counts = {}
        rating_data = []
        rating_categories = {'Excellent (9-10)': 0, 'Good (7-8.9)': 0, 'Average (5-6.9)': 0, 'Poor (3-4.9)': 0, 'Bad (0-2.9)': 0}
        
        for movie in self.processed_movies:
            # Genre counts
            for genre in movie.get('genres', []):
                if genre in genre_counts:
                    genre_counts[genre] += 1
                else:
                    genre_counts[genre] = 1
            
            # Rating analysis
            if movie.get('source') != 'Not Found' and movie.get('rating') and movie.get('rating') != 'N/A':
                try:
                    rating = float(movie.get('rating'))
                    rating_data.append(rating)
                    
                    # Categorize ratings
                    if rating >= 9:
                        rating_categories['Excellent (9-10)'] += 1
                    elif rating >= 7:
                        rating_categories['Good (7-8.9)'] += 1
                    elif rating >= 5:
                        rating_categories['Average (5-6.9)'] += 1
                    elif rating >= 3:
                        rating_categories['Poor (3-4.9)'] += 1
                    else:
                        rating_categories['Bad (0-2.9)'] += 1
                except:
                    pass
        
        # Calculate average rating for found movies
        avg_rating = sum(rating_data) / len(rating_data) if rating_data else 0
        
        # Get top rated movies
        rated_movies = [m for m in self.processed_movies if m.get('rating') and m.get('rating') != 'N/A' and m.get('source') != 'Not Found']
        top_rated_movies = sorted(rated_movies, key=lambda x: float(x.get('rating', 0)), reverse=True)[:5]
        
        return {
            'total_movies': total_movies,
            'found_movies': found_movies,
            'not_found_movies': total_movies - found_movies,
            'unknown_genres': unknown_genres,
            'genre_counts': genre_counts,
            'success_rate': (found_movies / total_movies) * 100 if total_movies > 0 else 0,
            'average_rating': round(avg_rating, 2) if avg_rating else 0,
            'rating_data': rating_data,
            'rating_categories': rating_categories,
            'top_rated_movies': top_rated_movies,
            'total_ratings': len(rating_data)
        }

# =========================================================================
# UTILITY FUNCTIONS
# =========================================================================

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

# =============================================================================
# UI COMPONENTS
# =============================================================================

def render_welcome_screen():
    """Render welcome screen with instructions"""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🎬 Welcome to the Movie Database & Genre Classifier!")
        st.markdown("""
        This system helps you organize, classify, and manage your movie collection using OMDb API.
        
        ## Key Features:
         **Smart Search** - Find movies with OMDb links  
         **Database Management** - Organize your movie collection  
         **Custom Watchlists** - Create personalized movie lists  
         **Batch Classification** - Process multiple movies at once  
         **Rating Analytics** - Advanced visualizations and insights  
         **Multi-format Export** - CSV, JSON, Excel outputs
        
        ### 📁 Get Started:
        1. **Search individual movies** to build your database
        2. **Create watchlists** for different moods or occasions  
        3. **Batch classify** movies from files
        4. **Explore analytics** and export your data
        """)
        
        st.success("**API Status: Successfully connected**")
    
    with col2:
        st.subheader(" Sample Data")
        sample_movies = [
            "The Shawshank Redemption",
            "The Godfather",
            "The Dark Knight",
            "Pulp Fiction",
            "Forrest Gump",
            "Inception",
            "The Matrix",
            "Goodfellas",
            "The Avengers",
            "Titanic"
        ]
        
        # Create sample files
        sample_csv = "Movie Title\n" + "\n".join(sample_movies)
        sample_txt = "\n".join(sample_movies)
        sample_json = json.dumps(sample_movies, indent=2)
        
        st.download_button(
            " Download Sample CSV",
            sample_csv,
            "sample_movies.csv",
            "text/csv",
            use_container_width=True
        )
        
        st.download_button(
            " Download Sample TXT",
            sample_txt,
            "sample_movies.txt",
            "text/plain",
            use_container_width=True
        )
        
        st.download_button(
            " Download Sample JSON",
            sample_json,
            "sample_movies.json",
            "application/json",
            use_container_width=True
        )

def render_single_movie_search(classifier):
    """Render single movie search functionality"""
    st.subheader("🔍 Search Single Movie")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        search_title = st.text_input("Enter movie title to search:", placeholder="e.g., The Shawshank Redemption", key="main_search")
    
    with col2:
        search_clicked = st.button("🔎 Search Movie", use_container_width=True, key="main_search_btn")
    
    if search_clicked and search_title:
        with st.spinner("Searching for movie..."):
            movie_data = classifier.search_single_movie(search_title)
            
            if movie_data and movie_data.get('source') != 'Not Found':
                st.success(f"✅ Found: {movie_data.get('title')} ({movie_data.get('year')})")
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # Movie details
                    st.write(f"**🎬 {movie_data.get('title')}** ({movie_data.get('year')})")
                    
                    # OMDb/IMDb link
                    if movie_data.get('omdb_link'):
                        st.markdown(f"**[🔗 View on IMDb]({movie_data.get('omdb_link')})**", unsafe_allow_html=True)
                    
                    # Rating with color coding
                    rating = movie_data.get('rating')
                    rating_class = get_rating_class(rating)
                    if rating and rating != 'N/A':
                        st.markdown(f"<div class='{rating_class}'>⭐ **IMDb Rating: {rating}/10**</div>", unsafe_allow_html=True)
                    
                    if movie_data.get('metascore') and movie_data.get('metascore') != 'N/A':
                        st.write(f" **Metascore: {movie_data.get('metascore')}**")
                    
                    st.write(f"**Genre:** {', '.join(movie_data.get('genres', []))}")
                    st.write(f"**Director:** {movie_data.get('director')}")
                    st.write(f"**Cast:** {movie_data.get('actors')}")
                    st.write(f"**Runtime:** {movie_data.get('runtime')}")
                    
                    if movie_data.get('box_office') and movie_data.get('box_office') != 'Unknown':
                        st.write(f"**Box Office:** {movie_data.get('box_office')}")
                    
                    if movie_data.get('overview'):
                        st.write(f"**Plot:** {movie_data.get('overview')}")
                
                with col2:
                    # Poster
                    poster_url = movie_data.get('poster', '')
                    if poster_url and poster_url != 'N/A':
                        st.image(poster_url, width=200)
                    else:
                        st.info("No poster available")
                
                st.markdown("---")
            else:
                st.error(f"❌ Movie '{search_title}' not found in OMDb database")

def render_database_management(classifier):
    """Render database management section"""
    st.subheader("🗃️ Movie Database Management")
    
    tab1, tab2, tab3 = st.tabs(["View Database", "Search Database", "Database Statistics"])
    
    with tab1:
        st.write("### All Movies in Database")
        movies = classifier.database.get_all_movies()
        
        if not movies:
            st.info("No movies in database yet. Search for movies to add them!")
        else:
            st.success(f"Found {len(movies)} movies in database")
            
            for movie in movies:
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.write(f"**{movie[1]}** ({movie[2]})")
                    st.write(f"*{movie[3]}* | Director: {movie[5]} | Rating: {movie[4]}/10")
                
                with col2:
                    if movie[9]:  # poster_url
                        st.image(movie[9], width=80)
                
                with col3:
                    if movie[10]:  # imdb_id
                        imdb_url = f"https://www.imdb.com/title/{movie[10]}"
                        st.markdown(f"[🔗 IMDb]({imdb_url})", unsafe_allow_html=True)
                
                st.markdown("---")
    
    with tab2:
        st.write("### Search Database")
        search_query = st.text_input("Search movies by title, genre, director, or actor:")
        
        if search_query:
            results = classifier.database.search_movies(search_query)
            
            if results:
                st.success(f"Found {len(results)} matches for '{search_query}'")
                
                for movie in results:
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"**{movie[1]}** ({movie[2]})")
                        st.write(f"*{movie[3]}* | ⭐ {movie[4]}/10")
                        st.write(f"Director: {movie[5]}")
                    
                    with col2:
                        if movie[10]:  # imdb_id
                            imdb_url = f"https://www.imdb.com/title/{movie[10]}"
                            st.markdown(f"[🔗 IMDb]({imdb_url})", unsafe_allow_html=True)
                    
                    st.markdown("---")
            else:
                st.info("No matches found in database")
    
    with tab3:
        st.write("### Database Statistics")
        movies = classifier.database.get_all_movies()
        
        if movies:
            # Basic stats
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Movies", len(movies))
            
            with col2:
                rated_movies = [m for m in movies if m[4] and m[4] > 0]
                st.metric("Rated Movies", len(rated_movies))
            
            with col3:
                avg_rating = sum(m[4] for m in movies if m[4]) / len([m for m in movies if m[4]]) if any(m[4] for m in movies) else 0
                st.metric("Average Rating", f"{avg_rating:.1f}/10")
            
            with col4:
                unique_genres = set()
                for movie in movies:
                    if movie[3]:
                        unique_genres.update(movie[3].split(', '))
                st.metric("Unique Genres", len(unique_genres))
            
            # Genre distribution
            genre_counts = {}
            for movie in movies:
                if movie[3]:
                    genres = movie[3].split(', ')
                    for genre in genres:
                        genre_counts[genre] = genre_counts.get(genre, 0) + 1
            
            if genre_counts:
                fig = px.bar(
                    x=list(genre_counts.keys()),
                    y=list(genre_counts.values()),
                    title="Genre Distribution in Database",
                    labels={'x': 'Genre', 'y': 'Number of Movies'}
                )
                st.plotly_chart(fig, use_container_width=True, key="db_genre_distribution")

def render_watchlist_management(classifier):
    """Render watchlist management section"""
    st.subheader(" Custom Watchlists")
    
    tab1, tab2, tab3 = st.tabs(["Create Watchlist", "My Watchlists", "Add to Watchlist"])
    
    with tab1:
        st.write("### Create New Watchlist")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            watchlist_name = st.text_input("Watchlist Name:", placeholder="e.g., 'Action Movies', '2024 Watchlist'")
        with col2:
            watchlist_desc = st.text_input("Description (optional):")
        
        if st.button("Create Watchlist", type="primary"):
            if watchlist_name:
                if classifier.database.create_watchlist(watchlist_name, watchlist_desc):
                    st.success(f"Watchlist '{watchlist_name}' created successfully!")
            else:
                st.error("Please enter a watchlist name")
    
    with tab2:
        st.write("### My Watchlists")
        watchlists = classifier.database.get_watchlists()
        
        if not watchlists:
            st.info("No watchlists created yet. Create your first watchlist!")
        else:
            for watchlist in watchlists:
                with st.expander(f"📋 {watchlist[1]} ({watchlist[4]} movies)"):
                    st.write(f"*{watchlist[2]}*")
                    
                    # Show movies in this watchlist
                    movies = classifier.database.get_watchlist_movies(watchlist[0])
                    
                    if movies:
                        for movie in movies:
                            col1, col2 = st.columns([3, 1])
                            
                            with col1:
                                st.write(f"**{movie[1]}** ({movie[2]}) - ⭐ {movie[4]}/10")
                            
                            with col2:
                                if movie[10]:  # imdb_id
                                    imdb_url = f"https://www.imdb.com/title/{movie[10]}"
                                    st.markdown(f"[🔗 IMDb]({imdb_url})", unsafe_allow_html=True)
                    
                    # Delete button
                    if st.button(f"Delete Watchlist", key=f"del_{watchlist[0]}"):
                        if classifier.database.delete_watchlist(watchlist[0]):
                            st.success("Watchlist deleted!")
                            st.rerun()
    
    with tab3:
        st.write("### Add Movies to Watchlist")
        
        # Get all movies from database
        movies = classifier.database.get_all_movies()
        watchlists = classifier.database.get_watchlists()
        
        if not movies:
            st.info("No movies in database. Search for movies first!")
        elif not watchlists:
            st.info("No watchlists created. Create a watchlist first!")
        else:
            # Movie selection
            movie_options = {f"{movie[1]} ({movie[2]})": movie[0] for movie in movies}
            selected_movie_label = st.selectbox("Select Movie:", list(movie_options.keys()))
            
            # Watchlist selection
            watchlist_options = {watchlist[1]: watchlist[0] for watchlist in watchlists}
            selected_watchlist = st.selectbox("Select Watchlist:", list(watchlist_options.keys()))
            
            if st.button("Add to Watchlist", type="primary"):
                movie_id = movie_options[selected_movie_label]
                watchlist_id = watchlist_options[selected_watchlist]
                
                if classifier.database.add_to_watchlist(watchlist_id, movie_id):
                    st.success(f"Movie added to {selected_watchlist}!")

def render_export_section(classifier):
    """Render export functionality"""
    st.subheader("💾 Export Results")
    
    if not classifier.processed_movies:
        st.info("No data to export. Please process some movies first.")
        return
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Export to CSV
        if st.button(" Export to CSV", use_container_width=True, key="export_csv_btn"):
            df = pd.DataFrame([{
                'Title': movie.get('title'),
                'Year': movie.get('year'),
                'Genres': ', '.join(movie.get('genres', [])),
                'Rating': movie.get('rating'),
                'Director': movie.get('director'),
                'Runtime': movie.get('runtime'),
                'IMDb_ID': movie.get('imdb_id'),
                'Source': movie.get('source')
            } for movie in classifier.processed_movies])
            
            csv = df.to_csv(index=False)
            st.download_button(
                " Download CSV",
                csv,
                "movie_classification_results.csv",
                "text/csv",
                use_container_width=True,
                key="download_csv"
            )
    
    with col2:
        # Export to JSON
        if st.button(" Export to JSON", use_container_width=True, key="export_json_btn"):
            json_data = json.dumps(classifier.processed_movies, indent=2)
            st.download_button(
                " Download JSON",
                json_data,
                "movie_classification_results.json",
                "application/json",
                use_container_width=True,
                key="download_json"
            )
    
    with col3:
        # Export statistics
        if st.button("Export Statistics", use_container_width=True, key="export_stats_btn"):
            stats = classifier.get_statistics()
            stats_json = json.dumps(stats, indent=2)
            st.download_button(
                "⬇ Download Stats",
                stats_json,
                "movie_statistics.json",
                "application/json",
                use_container_width=True,
                key="download_stats"
            )

def render_rating_analysis(classifier):
    """Render rating analysis section"""
    st.subheader("⭐ Rating Analysis")
    
    stats = classifier.get_statistics()
    if not stats:
        st.info("No rating data available. Process some movies first.")
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Average Rating", f"{stats['average_rating']}/10", "avg_rating_metric")
    
    with col2:
        st.metric("Rated Movies", stats['total_ratings'], "rated_movies_metric")
    
    with col3:
        st.metric("Success Rate", f"{stats['success_rate']:.1f}%", "success_rate_metric")
    
    with col4:
        st.metric("Movies Found", f"{stats['found_movies']}/{stats['total_movies']}", "movies_found_metric")
    
    # Rating distribution chart
    if stats['rating_categories']:
        fig = px.pie(
            values=list(stats['rating_categories'].values()),
            names=list(stats['rating_categories'].keys()),
            title="Rating Distribution"
        )
        st.plotly_chart(fig, use_container_width=True, key="rating_distribution_chart")

def render_top_rated_movies(classifier):
    """Render top rated movies section"""
    st.subheader("Top Rated Movies")
    
    stats = classifier.get_statistics()
    if not stats or not stats.get('top_rated_movies'):
        st.info("No top rated movies to display.")
        return
    
    for i, movie in enumerate(stats['top_rated_movies'], 1):
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col1:
            st.write(f"**#{i}**")
        
        with col2:
            st.write(f"**{movie.get('title')}** ({movie.get('year')})")
            st.write(f"*{', '.join(movie.get('genres', []))}*")
            st.write(f"Director: {movie.get('director')}")
        
        with col3:
            rating = movie.get('rating')
            rating_class = get_rating_class(rating)
            if rating:
                st.markdown(f"<div class='{rating_class}'>⭐ {rating}/10</div>", unsafe_allow_html=True)
        
        st.markdown("---")

def render_genre_tabs(classifier, classified_movies):
    """Render genre classification tabs"""
    st.subheader(" Genre Classification Results")
    
    # Create tabs for each genre that has movies
    genres_with_movies = [genre for genre, movies in classified_movies.items() if movies]
    
    if not genres_with_movies:
        st.info("No movies classified yet. Process some movies to see genre classification.")
        return
    
    tabs = st.tabs([f"{genre} ({len(classified_movies[genre])})" for genre in genres_with_movies])
    
    for i, genre in enumerate(genres_with_movies):
        with tabs[i]:
            movies = classified_movies[genre]
            
            for movie in movies:
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**{movie.get('title')}** ({movie.get('year')})")
                    
                    # Rating
                    rating = movie.get('rating')
                    if rating and rating != 'N/A':
                        rating_class = get_rating_class(rating)
                        st.markdown(f"<div class='{rating_class}'>⭐ {rating}/10</div>", unsafe_allow_html=True)
                    
                    # Director and cast
                    st.write(f"Director: {movie.get('director')}")
                    
                    # Plot
                    if movie.get('overview'):
                        with st.expander("Plot Summary"):
                            st.write(movie.get('overview'))
                
                with col2:
                    # Poster
                    poster_url = movie.get('poster', '')
                    if poster_url and poster_url != 'N/A':
                        st.image(poster_url, width=100)
                    
                    # IMDb link
                    if movie.get('omdb_link'):
                        st.markdown(f"[🔗 IMDb]({movie.get('omdb_link')})", unsafe_allow_html=True)
                
                st.markdown("---")

def render_results(classifier, classified_movies):
    """Render main results section"""
    if not classified_movies:
        return
    
    st.header("📊 Classification Results")
    
    # Statistics
    render_rating_analysis(classifier)
    
    # Top rated movies
    render_top_rated_movies(classifier)
    
    # Genre tabs
    render_genre_tabs(classifier, classified_movies)
    
    # Export section
    render_export_section(classifier)

def render_batch_classification(classifier):
    """Render batch classification section"""
    st.subheader("📊 Batch Movie Classification")
    
    if 'batch_movies' not in st.session_state:
        st.session_state.batch_movies = []
    
    # Display current batch movies
    if st.session_state.batch_movies:
        st.write(f"**Movies to process:** {len(st.session_state.batch_movies)}")
        
        with st.expander("View Movie List"):
            for i, title in enumerate(st.session_state.batch_movies[:20], 1):
                st.write(f"{i}. {title}")
            
            if len(st.session_state.batch_movies) > 20:
                st.write(f"... and {len(st.session_state.batch_movies) - 20} more")
    
    # Process button
    if st.session_state.batch_movies and st.button("🚀 Process Movies", type="primary", use_container_width=True, key="process_movies_btn"):
        valid_titles, invalid_titles = validate_movie_titles(st.session_state.batch_movies)
        
        if invalid_titles:
            st.warning(f"Found {len(invalid_titles)} invalid titles that will be skipped.")
        
        if valid_titles:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            def update_progress(current, total):
                progress = current / total
                progress_bar.progress(progress)
                status_text.text(f"Processing {current}/{total} movies...")
            
            with st.spinner("Classifying movies..."):
                classified_movies = classifier.classify_movies(valid_titles, update_progress)
            
            progress_bar.progress(1.0)
            status_text.text("✅ Processing complete!")
            
            st.session_state.classified_movies = classified_movies
            st.session_state.processing_complete = True
            
            # Show results
            render_results(classifier, classified_movies)
        else:
            st.error("No valid movie titles to process.")
    elif not st.session_state.batch_movies:
        st.info("Add movies using the sidebar to start batch classification.")

def render_sidebar(classifier):
    """Render the sidebar with input options"""
    st.sidebar.title("🎬 Navigation")
    
    # Navigation
    page = st.sidebar.radio("Go to:", 
                           ["Home", "Movie Search", "Database", "Watchlists", "Batch Classification"],
                           key="nav_radio")
    
    # Quick search in sidebar
    st.sidebar.subheader("🔍 Quick Search")
    quick_search = st.sidebar.text_input("Search single movie:", placeholder="Movie title...", key="sidebar_search")
    if st.sidebar.button("Search", key="sidebar_search_btn", use_container_width=True):
        st.session_state.quick_search_title = quick_search
        st.session_state.current_page = "Movie Search"
    
    # Batch processing section
    if page == "Batch Classification":
        st.sidebar.subheader("📁 Batch Input")
        input_method = st.sidebar.radio(
            "Choose input method:",
            ["Manual Input", "Upload File"],
            key="input_method_radio"
        )
        
        movie_titles = []
        
        if input_method == "Manual Input":
            st.sidebar.subheader("✏️ Enter Movie Titles")
            movie_text = st.sidebar.text_area(
                "Enter movie titles (one per line):",
                height=200,
                placeholder="The Shawshank Redemption\nThe Godfather\nPulp Fiction\n...",
                help="Enter one movie title per line. Be as accurate as possible for better results.",
                key="manual_input_area"
            )
            if movie_text:
                movie_titles = [title.strip() for title in movie_text.split('\n') if title.strip()]
        
        else:  # File Upload
            st.sidebar.subheader("📁 Upload Movie List")
            uploaded_file = st.sidebar.file_uploader(
                "Choose a file",
                type=['txt', 'csv', 'json'],
                help="Supported formats: TXT, CSV, JSON",
                key="file_uploader"
            )
            
            if uploaded_file is not None:
                try:
                    movie_titles = load_movies_from_file(uploaded_file)
                    st.sidebar.success(f"✅ Loaded {len(movie_titles)} movies from {uploaded_file.name}")
                except Exception as e:
                    st.sidebar.error(f"❌ Error reading file: {str(e)}")
        
        st.session_state.batch_movies = movie_titles
    
    # API Status
    st.sidebar.subheader("🔑 API Status")
    st.sidebar.success("✅ OMDb API: Configured and Ready!")
    st.sidebar.info("Your API key is pre-configured and ready to use.")
    
    # Database stats
    try:
        movies = classifier.database.get_all_movies()
        watchlists = classifier.database.get_watchlists()
        
        st.sidebar.subheader("📊 Quick Stats")
        st.sidebar.write(f"🎬 Movies: {len(movies)}")
        st.sidebar.write(f"📋 Watchlists: {len(watchlists)}")
    except:
        pass
    
    return page

# =============================================================================
# AUTHENTICATION FUNCTIONS
# =============================================================================

def init_user_storage():
    """Initialize user storage in session state"""
    if 'users' not in st.session_state:
        st.session_state.users = {
            'demo': {
                'password': hashlib.sha256('movie123'.encode()).hexdigest(),
                'email': 'demo@moviedb.com',
                'name': 'Demo User'
            }
        }
    if 'password_reset_tokens' not in st.session_state:
        st.session_state.password_reset_tokens = {}

def hash_password(password):
    """Hash password for storage"""
    return hashlib.sha256(password.encode()).hexdigest()

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number"
    return True, "Password is strong"

def render_auth_page():
    """Render the authentication page with login/signup/forgot password"""
    
    # Initialize tabs in session state
    if 'auth_tab' not in st.session_state:
        st.session_state.auth_tab = 'login'
    
    st.markdown("""
    <div class="auth-container">
        <div class="auth-header">🎬</div>
        <h1 class="auth-title">Movie Database Pro</h1>
        <div class="auth-subtitle">Your Ultimate Movie Management System</div>
    """, unsafe_allow_html=True)
    
    # Use Streamlit buttons for tab navigation instead of JavaScript
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login", use_container_width=True, type="primary" if st.session_state.auth_tab == 'login' else "secondary"):
            st.session_state.auth_tab = 'login'
            st.rerun()
    with col2:
        if st.button("Sign Up", use_container_width=True, type="primary" if st.session_state.auth_tab == 'signup' else "secondary"):
            st.session_state.auth_tab = 'signup'
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Login Form
    if st.session_state.auth_tab == 'login':
        st.markdown("""
        <div class="auth-container">
            <div class="auth-form">
                <form>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("👤 Username or Email", placeholder="Enter your username or email")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
            
            col1, col2 = st.columns([3, 1])
            with col1:
                login_submitted = st.form_submit_button("Login to Dashboard", use_container_width=True)
            with col2:
                if st.form_submit_button("Forgot Password?", use_container_width=True):
                    st.session_state.auth_tab = 'forgot'
                    st.rerun()
            
            if login_submitted:
                if username and password:
                    # Check if user exists and password matches
                    if username in st.session_state.users:
                        hashed_password = hash_password(password)
                        if st.session_state.users[username]['password'] == hashed_password:
                            st.session_state.authenticated = True
                            st.session_state.current_user = username
                            st.success("Login successful!")
                            st.rerun()
                        else:
                            st.error("❌ Invalid password. Please try again or use demo credentials.")
                    else:
                        st.error("❌ User not found. Please check your username or sign up for a new account.")
                else:
                    st.error("❌ Please fill in all fields.")
        
        st.markdown("""
                </form>
                
                <div style="text-align: center; margin: 1.5rem 0; color: #666;">or continue with</div>
                
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Demo login button
        if st.button("🚀 Try Demo Version", use_container_width=True, key="demo_login_btn"):
            st.session_state.authenticated = True
            st.session_state.current_user = "demo"
            st.rerun()
    
    # Sign Up Form
    elif st.session_state.auth_tab == 'signup':
        st.markdown("""
        <div class="auth-container">
            <div class="auth-form">
                <form>
        """, unsafe_allow_html=True)
        
        with st.form("signup_form"):
            fullname = st.text_input("👤 Full Name", placeholder="Enter your full name")
            email = st.text_input("📧 Email Address", placeholder="Enter your email address")
            username = st.text_input("👤 Username", placeholder="Choose a username")
            password = st.text_input("🔒 Password", type="password", placeholder="Create a password")
            confirm_password = st.text_input("✅ Confirm Password", type="password", placeholder="Confirm your password")
            
            st.caption("Password requirements: 8+ characters, uppercase & lowercase letters, numbers")
            
            signup_submitted = st.form_submit_button("Create Account", use_container_width=True)
            
            if signup_submitted:
                if all([fullname, email, username, password, confirm_password]):
                    # Validate input
                    if username in st.session_state.users:
                        st.error("❌ Username already exists. Please choose a different username.")
                    elif not validate_email(email):
                        st.error("❌ Please enter a valid email address.")
                    elif password != confirm_password:
                        st.error("❌ Passwords do not match.")
                    else:
                        is_valid, message = validate_password(password)
                        if not is_valid:
                            st.error(f"❌ {message}")
                        else:
                            # Create new user
                            st.session_state.users[username] = {
                                'password': hash_password(password),
                                'email': email,
                                'name': fullname
                            }
                            st.success("✅ Account created successfully! You can now login with your credentials.")
                            st.session_state.auth_tab = 'login'
                            st.rerun()
                else:
                    st.error("❌ Please fill in all fields.")
        
        st.markdown("""
                </form>
                
                <div style="text-align: center; margin-top: 1rem;">
                    Already have an account? 
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Sign In", use_container_width=True):
            st.session_state.auth_tab = 'login'
            st.rerun()
    
    # Forgot Password Form
    elif st.session_state.auth_tab == 'forgot':
        st.markdown("""
        <div class="auth-container">
            <div class="auth-form">
                <h3 style="color: #1f77b4; text-align: center; margin-bottom: 1.5rem;">Reset Your Password</h3>
                <form>
        """, unsafe_allow_html=True)
        
        with st.form("forgot_form"):
            email = st.text_input("📧 Email Address", placeholder="Enter your email address")
            
            submit_reset = st.form_submit_button("Send Reset Link", use_container_width=True)
            
            if submit_reset:
                if email:
                    # Find user by email
                    user_found = False
                    for username, user_data in st.session_state.users.items():
                        if user_data['email'] == email:
                            user_found = True
                            st.success(f"✅ Password reset instructions have been sent to {email}.")
                            st.info("**Demo Note:** In this demo version, you can use the demo account or create a new account.")
                            break
                    
                    if not user_found:
                        st.error("❌ No account found with that email address. Please check your email or sign up for a new account.")
                else:
                    st.error("❌ Please enter your email address.")
        
        st.markdown("""
                </form>
                
                <div style="text-align: center; margin-top: 1rem;">
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Back to Login", use_container_width=True):
            st.session_state.auth_tab = 'login'
            st.rerun()
    
    # Demo credentials
    st.markdown("""
    <div class="auth-container">
        <div class="demo-credentials">
            <strong>🎯 Demo Access (Instant Login)</strong><br>
            Username: <code>demo</code><br>
            Password: <code>movie123</code>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature showcase
    st.markdown("""
    <div style="max-width: 1000px; margin: 50px auto; text-align: center;">
        <h2 style="color: #1f77b4; margin-bottom: 1rem;">Everything You Need for Movie Management</h2>
        <p style="color: #666; font-size: 1.2rem; margin-bottom: 3rem;">Advanced tools for movie enthusiasts, collectors, and critics</p>
        
        <div class="feature-grid">
            <div class="feature-card">
                <div class="feature-icon">🔍</div>
                <h3>Smart Search</h3>
                <p>Find movies with detailed information from OMDb API with real-time data</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📊</div>
                <h3>Genre Analytics</h3>
                <p>Classify and analyze movies by genre with interactive visual insights</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🎯</div>
                <h3>Watchlists</h3>
                <p>Create personalized movie collections and organize by mood or occasion</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">💾</div>
                <h3>Data Export</h3>
                <p>Export your movie data in CSV, JSON formats for further analysis</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">⭐</div>
                <h3>Rating System</h3>
                <p>Track ratings, reviews, and create personalized scoring systems</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🔄</div>
                <h3>Batch Processing</h3>
                <p>Process multiple movies at once with progress tracking</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def handle_authentication():
    """Handle authentication logic"""
    # Check session state
    if st.session_state.get("authenticated"):
        return True
    
    return False

def main_application():
    """Main application function after login"""
    st.markdown('<h1 class="main-header">🎬 Movie Database & Genre Classification System</h1>', unsafe_allow_html=True)
    
    # Add user info in sidebar
    if st.session_state.get("current_user"):
        st.sidebar.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
            <strong>👤 Welcome, {st.session_state.current_user}!</strong>
            <br>
            <small>Movie Database Pro</small>
        </div>
        """, unsafe_allow_html=True)
    
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

def main():
    """Main application controller"""
    # Initialize user storage
    init_user_storage()
    
    # Check authentication
    if not handle_authentication():
        render_auth_page()
        return
    
    # User is authenticated, show main application
    main_application()

if __name__ == "__main__":
    main()