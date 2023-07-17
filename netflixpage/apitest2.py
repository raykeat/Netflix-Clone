import requests

n=0
tvshows = []
while n<2:
    n+=1
    headers = {
        "accept": "application/json",
        #FOR CS50 GRADING STAFF, YOU MUST OBTAIN YOUR OWN HEADERS AUTHORIZATION BY
    #SIGNING UP FOR AN ACCOUNT AT https://developer.themoviedb.org/reference/discover-tv
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkMWQzMTg2M2RjNjg2ZDJkZTZiMDFiYzFkMjU4NGIyMyIsInN1YiI6IjY0OGRlNzUzMjYzNDYyMDE0ZTU3YzVhNiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Dwpm5j_yAILTOKx93IPc5dj8rabkxx-ea7lgpD0ajdE"
    }
    url = "https://api.themoviedb.org/3/discover/tv?&include_adult=false&include_null_first_air_dates=true&language=en-US&page={}&offset=20&sort_by=popularity.desc&with_genres={}".format(n,37)
    response = requests.get(url,headers=headers)
    jsonresponse = response.json()
    tvshows.extend(jsonresponse['results'])


print(len(tvshows))
print (tvshows[0]['id'])



