from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

TMDB_API_KEY = os.getenv('TMDB_API_KEY')

# Hardcoded genre mapping
genre_mapping = {
    28: "Action",
    12: "Adventure",
    16: "Animation",
    35: "Comedy",
    80: "Crime",
    99: "Documentary",
    18: "Drama",
    10751: "Family",
    14: "Fantasy",
    36: "History",
    27: "Horror",
    10402: "Music",
    9648: "Mystery",
    10749: "Romance",
    878: "Science Fiction",
    10770: "TV Movie",
    53: "Thriller",
    10752: "War",
    37: "Western"
}

@app.route('/')
def index():
    return render_template('index.html')




@app.route('/search', methods=['POST'])
def search_movie():
    movie_name = request.form.get('movie_name')
    genre = request.form.get('genre', '')
    language = request.form.get('language', '')

    api_url = f'https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_name}'

    if genre:
        api_url += f'&with_genres={genre}'
    if language:
        api_url += f'&language={language}'

    response = requests.get(api_url)
    movie_data = response.json()

    if not movie_data['results']:
        return render_template('index.html', error_message='No movies found for the selected criteria.')

    movie = movie_data['results'][0]

    # Get genre names
    movie_genres = [genre_mapping[genre_id] for genre_id in movie['genre_ids']]

    movie_details = {
        'title': movie.get('title'),
        'plot': movie.get('overview'),
        'genres': movie_genres,
        'poster_url': f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}",
    }

    return render_template('movie_details.html', movie=movie_details)
@app.route('/action_movies', methods=["GET"])
def action_movies():
    api_url = f'https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&with_genres=28'
    movies_data = requests.get(api_url).json()

    if 'results' in movies_data:
        movies = movies_data['results']
        print("movies", movies)
    else:
        movies = []
    return render_template('action_movies.html', movies=movies)



@app.route('/romantic_movies', methods=["GET"])
def romantic_movies():
    api_url = f'https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&with_genres=10749'
    movies_data = requests.get(api_url).json()

    if 'results' in movies_data:
        movies = movies_data['results']
        print("movies", movies)
    else:
        movies = []
    return render_template('romantic_movies.html', movies=movies)


@app.route('/comedy_movies', methods=["GET"])
def comedy_movies():
    api_url = f'https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&with_genres=35'
    movies_data = requests.get(api_url).json()

    if 'results' in movies_data:
        movies = movies_data['results']
        print("movies", movies)
    else:
        movies = []
    return render_template('comedy_movies.html', movies=movies)

@app.route("/thriller_movies", methods=["GET"])
def thriller_movies():
    api_url = f'https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&with_genres=53'
    movies_data = requests.get(api_url).json()

    if 'results' in movies_data:
        movies = movies_data['results']
        print("movies", movies)
    else:
        movies = []
    return render_template('thriller_movies.html', movies=movies)


@app.route('/popular_movies', methods=["GET"])
def get_popular_movies():
    url = 'https://api.themoviedb.org/3/discover/movie'
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3ZDQ2ZWNlOGFlOWNhOGFkMGYxMWI5M2JkZWZiNjJiMCIsIm5iZiI6MTcyMzE0NDY4MS4xMTYyOTYsInN1YiI6IjY2YjRjOTdiNzRjM2MxMzE1NGFkZmI2NiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.3mrkFYFavj3zIrbfVFMMVlH_2Xjf-baJ6Vl--56QRag',
        'accept': 'application/json'
    }
    params = {
        'include_adult': 'false',
        'include_video': 'false',
        'language': 'en-US',
        'page': 1,
        'sort_by': 'popularity.desc'
    }

    response = requests.get(url, headers=headers, params=params)
    print("response:", response)
    if response.status_code == 200:
        popular_movies = response.json().get('results', [])
        return render_template('popular_movies.html', movies=popular_movies)
    else:
        return jsonify({"error": "Failed to retrieve popular movies"}), response.status_code



if __name__ == '__main__':
    app.run(debug=True)
