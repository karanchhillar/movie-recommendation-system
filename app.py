import pickle
import streamlit as st
import pandas as pd

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended_movie_names = []
    for i in distances[1:6]:
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names

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
        recommended_movie_names = recommend(selected_movie)

    st.write("### Top 5 Recommended Movies:")

    # Display recommendations in a single column
    for movie_name in recommended_movie_names:
        st.write(f"**{movie_name}**")

# Footer
st.markdown("""
    <hr style="border:2px solid #f1f1f1">
    <center>Created by Karan Chhillar</center>
""", unsafe_allow_html=True)
