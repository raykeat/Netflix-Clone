import requests

movies = []
n=0
while n<2:
    n+=1
    url = "https://api.themoviedb.org/3/discover/tv?api_key=d1d31863dc686d2de6b01bc1d2584b23&include_adult=false&include_null_first_air_dates=true&language=en-US&page={}&offset=20&sort_by=popularity.desc&with_genres=27".format(n)
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
print (movies[0]['first_air_date'])
print(len(movies))

