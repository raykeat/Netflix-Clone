#import tmdbsimple as tmdb
#tmdb.API_KEY = 'd1d31863dc686d2de6b01bc1d2584b23'
#discover = tmdb.Discover()
#response = discover.movie()
#for s in discover.results:
    #print(s['title'], s['id'], s['release_date'], s['popularity'])

import requests
url = "https://api.themoviedb.org/3/discover/movie?api_key=d1d31863dc686d2de6b01bc1d2584b23&include_adult=false&include_video=true&language=en-US&page=1&sort_by=popularity.desc&with_genres=horror"
headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkMWQzMTg2M2RjNjg2ZDJkZTZiMDFiYzFkMjU4NGIyMyIsInN1YiI6IjY0OGRlNzUzMjYzNDYyMDE0ZTU3YzVhNiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Dwpm5j_yAILTOKx93IPc5dj8rabkxx-ea7lgpD0ajdE"
}

movies = []
n=0
while n<2:
    n+=1
    url = "https://api.themoviedb.org/3/discover/movie?api_key=d1d31863dc686d2de6b01bc1d2584b23&include_adult=false&include_video=true&language=en-US&page={}&offset=20&sort_by=popularity.desc&with_genres=27".format(n)
    response = requests.get(url)
    jsonresponse = response.json()
    movies.extend(jsonresponse['results'])

#for movie in movies:
    #print(movie['title'])
print (movies[0])
print (movies[0]['title'])
print (movies[0]['popularity'])
print (movies[0]['genre_ids'])
print (movies[0]['overview'])
print (movies[0]['poster_path'])
print (movies[0]['release_date'])
print(len(movies))



