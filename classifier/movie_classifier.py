# classifier/movie_classifier.py - Movie classification logic
import time
from typing import List, Dict, Any, Optional
from database.movie_database import MovieDatabase
from api_handlers.omdb_handler import OMDbHandler

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