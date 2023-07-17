import requests

url = "https://api.themoviedb.org/3/discover/tv?include_adult=false&include_null_first_air_dates=true&language=en-US&page=1&sort_by=popularity.desc"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkMWQzMTg2M2RjNjg2ZDJkZTZiMDFiYzFkMjU4NGIyMyIsInN1YiI6IjY0OGRlNzUzMjYzNDYyMDE0ZTU3YzVhNiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Dwpm5j_yAILTOKx93IPc5dj8rabkxx-ea7lgpD0ajdE"
}

response = requests.get(url, headers=headers)

print(response.text)