import pandas as pd
import streamlit as st
import pickle
import requests


def fetch_poster(movie_id):
    url = ("https://api.themoviedb.org/3/movie/{"
           "}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US").format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for k in movies_list:
        movie_id = movies.iloc[k[0]].movie_id
        recommended_movies.append(movies.iloc[k[0]].title)
        # fetch poster from api
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity2.pkl', 'rb'))
st.title('Movie Recommender System')
selected_movie_name = st.selectbox('Name the movie for which you want suggestions ', movies['title'].values)
if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
