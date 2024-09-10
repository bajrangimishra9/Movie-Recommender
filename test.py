import streamlit as st
import pandas as pd
import pickle
import requests

# Function to fetch the poster using the TMDB API
def fetch_poster(movie_id):
    try:
        # Sending request to fetch movie poster from the TMDB API
        response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=a6553ff93fd9068aec3a5931f811cbf0&language=en-US')
        response.raise_for_status()  # Check if the request was successful
        data = response.json()
        return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"
    except:
        # Return a placeholder image in case of an error
        return "https://via.placeholder.com/500x750?text=No+Poster+Available"

# Function to recommend movies based on the selected movie
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # Fetch poster from API and append
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# Loading movie data and similarity matrix
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Title of the Streamlit app
st.title('Movie Recommender System')

# Dropdown to select a movie
selected_movie_name = st.selectbox(
    'Select a movie to get recommendations',
    movies['title'].values
)

# Button to get recommendations
if st.button('Recommend'):
    name, posters = recommend(selected_movie_name)

    # Layout for displaying the movie names and their posters
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.text(name[idx])
            st.image(posters[idx])
