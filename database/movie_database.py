# database/movie_database.py - Database operations
import sqlite3
from typing import List, Tuple, Optional

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
            import streamlit as st
            st.error(f"Error adding movie to database: {e}")
            return None
        finally:
            conn.close()
    
    def get_all_movies(self) -> List[Tuple]:
        """Get all movies from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM movies ORDER BY date_added DESC
        ''')
        
        movies = cursor.fetchall()
        conn.close()
        
        return movies
    
    def search_movies(self, query: str) -> List[Tuple]:
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
    
    def create_watchlist(self, name: str, description: str = "") -> bool:
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
            import streamlit as st
            st.error("Watchlist with this name already exists!")
            return False
        finally:
            conn.close()
    
    def get_watchlists(self) -> List[Tuple]:
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
    
    def add_to_watchlist(self, watchlist_id: int, movie_id: int) -> bool:
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
            import streamlit as st
            st.warning("Movie already in watchlist!")
            return False
        finally:
            conn.close()
    
    def get_watchlist_movies(self, watchlist_id: int) -> List[Tuple]:
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
    
    def delete_watchlist(self, watchlist_id: int) -> bool:
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
            import streamlit as st
            st.error(f"Error deleting watchlist: {e}")
            return False
        finally:
            conn.close()