import os
import pickle
from pathlib import Path

import requests
import streamlit as st

# Folder that contains this file, so the app works no matter where you start it from
BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "model"

# TMDB key: uses your own key if you set TMDB_API_KEY, otherwise the one from the original project
TMDB_API_KEY = os.environ.get("TMDB_API_KEY", "8265bd1679663a7ea12ac168da84d2e8")
NO_POSTER = "https://placehold.co/500x750?text=No+Poster"


@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
    """Get the poster URL from TMDB. Falls back to a placeholder if anything goes wrong."""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    try:
        data = requests.get(url, timeout=10).json()
        poster_path = data.get("poster_path")
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
    except (requests.RequestException, ValueError):
        pass
    return NO_POSTER


@st.cache_resource(show_spinner="Loading model...")
def load_model():
    """Load the files created by the notebook (loaded once, not on every click)."""
    movies_file = MODEL_DIR / "movie_list.pkl"
    similarity_file = MODEL_DIR / "similarity.pkl"
    if not movies_file.exists() or not similarity_file.exists():
        st.error(
            "Model files not found. Run all cells in the notebook first. "
            "It creates model/movie_list.pkl and model/similarity.pkl."
        )
        st.stop()
    with open(movies_file, "rb") as f:
        movies = pickle.load(f)
    with open(similarity_file, "rb") as f:
        similarity = pickle.load(f)
    return movies, similarity


def recommend(movie):
    index = movies[movies["title"] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters


st.header("Movie Recommender System")
movies, similarity = load_model()

movie_list = movies["title"].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

if st.button("Show Recommendation"):
    with st.spinner("Finding similar movies..."):
        names, posters = recommend(selected_movie)
    # st.beta_columns was removed from Streamlit; st.columns is the current name
    cols = st.columns(5)
    for col, name, poster in zip(cols, names, posters):
        with col:
            st.markdown(f"**{name}**")
            st.image(poster)
