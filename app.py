import pickle
import streamlit as st
import pandas as pd
import requests

# Function to fetch movie details (poster, description, genre, vote average)
def get_movie_details(movie_name):
    api_key = "f9160d595192c3f901ccde3d14f796c1"
    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_name}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if "results" in data and len(data["results"]) > 0:
            result = data["results"][0]
            movie_poster = f"https://image.tmdb.org/t/p/w500{result['poster_path']}" if result["poster_path"] else ""
            description = result["overview"]
            genre_ids = result["genre_ids"]
            vote_average = result["vote_average"]
            return movie_poster, description, genre_ids, vote_average
        else:
            print(f"No results found for movie: {movie_name}")
            return "", "", [], 0.0

    except requests.exceptions.RequestException as e:
        print(f"Error while fetching movie data: {e}")
        return "", "", [], 0.0

# Function to map genre_ids to genre names
def get_genres(genre_ids):
    genre_map = {
        28: "Action", 12: "Adventure", 16: "Animation", 35: "Comedy", 80: "Crime",
        99: "Documentary", 18: "Drama", 10751: "Family", 14: "Fantasy", 36: "History",
        27: "Horror", 10402: "Music", 9648: "Mystery", 10749: "Romance", 878: "Science Fiction",
        10770: "TV Movie", 53: "Thriller", 10752: "War", 37: "Western"
    }
    return [genre_map.get(genre_id, "Unknown") for genre_id in genre_ids]

# Recommendation function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended_movies = []
    for i in distances[1:6]:
        movie_name = movies.iloc[i[0]].title
        movie_poster, description, genre_ids, vote_average = get_movie_details(movie_name)
        genres = get_genres(genre_ids)
        recommended_movies.append({
            "name": movie_name,
            "poster": movie_poster,
            "description": description,
            "genres": genres,
            "vote_average": vote_average
        })
    
    return recommended_movies

# Load movie data and similarity matrix
movies = pickle.load(open('movie_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movies = pd.DataFrame(movies)
movie_list = movies['title'].values

# Improved UI
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title('🎬 Movie Recommender System')

# Sidebar for better organization
with st.sidebar:
    st.header("Select Your Movie")
    selected_movie = st.selectbox(
        "Type or select a movie from the dropdown",
        movie_list
    )

st.subheader("Discover movies similar to your choice!")

# Show recommendations in rows with details and posters side-by-side
if st.button('Show Recommendation'):
    with st.spinner("Fetching recommendations..."):
        recommended_movies = recommend(selected_movie)

    st.write("### Top 5 Recommended Movies:")

    # Loop through recommended movies and display them with details and poster
    for i, movie in enumerate(recommended_movies):
        col1, col2 = st.columns([3, 2])  # Set the ratio for text and image
        with col1:
            # st.write(f"**{i+1}. {movie['name']}**")  # Numbering the movies
            st.markdown(f"""
            <h3 style='font-size:24px; font-weight:bold;'>{i+1}. {movie['name']}</h3>
            """, unsafe_allow_html=True)
            st.write(f"**Genres**: {', '.join(movie['genres'])}")
            st.write(f"**Rating**: {movie['vote_average']} / 10")
            st.write(f"**Overview**: {movie['description']}")
        with col2:
            st.image(movie['poster'], width=200)
        st.write("---")

# Improved Footer with Better UI and Shorter Height
st.markdown("""
    <style>
    footer {visibility: hidden;}
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #262730;
        color: white;
        text-align: center;
        padding: 10px 0;  /* Reduced height of the footer */
        font-size: 14px;
        border-top: 1px solid #f1f1f1;
    }
    </style>
    <div class="footer">
        <p>Created by <strong>Karan Chhillar</strong> | © 2024 All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)
