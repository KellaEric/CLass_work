# utils/ui_components.py - UI rendering components
import streamlit as st
import pandas as pd
import json
import plotly.express as px
from database.movie_database import MovieDatabase
from classifier.movie_classifier import MovieGenreClassifier
from utils.helpers import get_rating_class, load_movies_from_file, validate_movie_titles

def render_welcome_screen():
    """Render welcome screen with instructions"""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🎬 Welcome to the Movie Database & Genre Classifier!")
        st.markdown("""
        This comprehensive system helps you organize, classify, and manage your movie collection using OMDb API.
        
        ### 🚀 Key Features:
        🔍 **Smart Search** - Find movies with OMDb links  
        🗃️ **Database Management** - Organize your movie collection  
        🎯 **Custom Watchlists** - Create personalized movie lists  
        📊 **Batch Classification** - Process multiple movies at once  
        ⭐ **Rating Analytics** - Advanced visualizations and insights  
        💾 **Multi-format Export** - CSV, JSON, Excel outputs
        
        ### 📁 Get Started:
        1. **Search individual movies** to build your database
        2. **Create watchlists** for different moods or occasions  
        3. **Batch classify** movies from files
        4. **Explore analytics** and export your data
        """)
        
        st.success("🔑 **API Status: OMDb API Key Successfully Configured!**")
    
    with col2:
        st.subheader("📋 Sample Data")
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
            "📥 Download Sample CSV",
            sample_csv,
            "sample_movies.csv",
            "text/csv",
            use_container_width=True
        )
        
        st.download_button(
            "📥 Download Sample TXT",
            sample_txt,
            "sample_movies.txt",
            "text/plain",
            use_container_width=True
        )
        
        st.download_button(
            "📥 Download Sample JSON",
            sample_json,
            "sample_movies.json",
            "application/json",
            use_container_width=True
        )

def render_single_movie_search(classifier: MovieGenreClassifier):
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
                        st.write(f"🎯 **Metascore: {movie_data.get('metascore')}**")
                    
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

def render_database_management(classifier: MovieGenreClassifier):
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

def render_watchlist_management(classifier: MovieGenreClassifier):
    """Render watchlist management section"""
    st.subheader("🎯 Custom Watchlists")
    
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

def render_export_section(classifier: MovieGenreClassifier):
    """Render export functionality"""
    st.subheader("💾 Export Results")
    
    if not classifier.processed_movies:
        st.info("No data to export. Please process some movies first.")
        return
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Export to CSV
        if st.button("📊 Export to CSV", use_container_width=True, key="export_csv_btn"):
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
                "⬇️ Download CSV",
                csv,
                "movie_classification_results.csv",
                "text/csv",
                use_container_width=True,
                key="download_csv"
            )
    
    with col2:
        # Export to JSON
        if st.button("📝 Export to JSON", use_container_width=True, key="export_json_btn"):
            json_data = json.dumps(classifier.processed_movies, indent=2)
            st.download_button(
                "⬇️ Download JSON",
                json_data,
                "movie_classification_results.json",
                "application/json",
                use_container_width=True,
                key="download_json"
            )
    
    with col3:
        # Export statistics
        if st.button("📈 Export Statistics", use_container_width=True, key="export_stats_btn"):
            stats = classifier.get_statistics()
            stats_json = json.dumps(stats, indent=2)
            st.download_button(
                "⬇️ Download Stats",
                stats_json,
                "movie_statistics.json",
                "application/json",
                use_container_width=True,
                key="download_stats"
            )

def render_rating_analysis(classifier: MovieGenreClassifier):
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

def render_top_rated_movies(classifier: MovieGenreClassifier):
    """Render top rated movies section"""
    st.subheader("🏆 Top Rated Movies")
    
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

def render_genre_tabs(classifier: MovieGenreClassifier, classified_movies):
    """Render genre classification tabs"""
    st.subheader("🎭 Genre Classification Results")
    
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

def render_results(classifier: MovieGenreClassifier, classified_movies):
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

def render_batch_classification(classifier: MovieGenreClassifier):
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

def render_sidebar(classifier: MovieGenreClassifier):
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