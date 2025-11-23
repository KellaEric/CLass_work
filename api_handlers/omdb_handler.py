# api_handlers/omdb_handler.py - OMDb API handler
import requests
from typing import Dict, Optional

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
            import streamlit as st
            st.sidebar.warning(f"OMDb API error for '{movie_title}': {e}")
        except Exception as e:
            import streamlit as st
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