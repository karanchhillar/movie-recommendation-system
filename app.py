import pickle
import streamlit as st
import pandas as pd
import requests

def poster(movie_name):
    api_key = "f9160d595192c3f901ccde3d14f796c1"
    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_name}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for request errors
        data = response.json()

        if "results" in data and len(data["results"]) > 0:
            movie_poster = data["results"][0]["poster_path"]
            return f"https://image.tmdb.org/t/p/w500{movie_poster}"
        else:
            print(f"No results found for movie: {movie_name}")
            return ""

    except requests.exceptions.RequestException as e:
        print(f"Error while fetching movie data: {e}")
        return ""

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_name = movies.iloc[i[0]].title
        poster_path = poster(movie_name)
        recommended_movie_names.append(movie_name)
        recommended_movie_posters.append(poster_path)

    return recommended_movie_names, recommended_movie_posters

movies = pickle.load(open('movie_dict.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

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
        movies['title'].values
    )

st.subheader("Discover movies similar to your choice!")

# Show recommendations in a column
if st.button('Show Recommendation'):
    with st.spinner("Fetching recommendations..."):
        names, posters = recommend(selected_movie)

    st.write("### Top 5 Recommended Movies:")

    # Set fixed image width for consistency
    image_width = 180  # Adjust this width according to your needs

    # Adjust spacing between columns
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1], gap="medium")

    with col1:
        st.write(names[0], align="center")
        st.image(posters[0], width=image_width)

    with col2:
        st.write(names[1], align="center")
        st.image(posters[1], width=image_width)

    with col3:
        st.write(names[2], align="center")
        st.image(posters[2], width=image_width)

    with col4:
        st.write(names[3], align="center")
        st.image(posters[3], width=image_width)

    with col5:
        st.write(names[4], align="center")
        st.image(posters[4], width=image_width)

# Footer
st.markdown("""
    <hr style="border:2px solid #f1f1f1">
    <center>Created by Karan Chhillar</center>
""", unsafe_allow_html=True)
