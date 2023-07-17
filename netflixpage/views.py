from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import User, Movies, GenresMovies, TVShows, GenresTVShows
import requests, os
from django.http import JsonResponse
import requests
from django.db.models import Q
import json, random


class NewTaskForm(forms.Form):
    username = forms.CharField(label="username", widget=forms.TextInput(attrs={'class': 'rounded-lg opacity-75 bg-white text-black text-bold'}))
    password = forms.CharField(label="password", widget=forms.PasswordInput(attrs={'class': 'rounded-lg opacity-75 bg-white text-black text-bold'}))
    confirmpassword = forms.CharField(label="confirm password", widget=forms.PasswordInput(attrs={'class': 'rounded-lg opacity-75 bg-white text-black text-bold'}))
    email = forms.CharField(label="email", widget=forms.EmailInput(attrs={'class': 'rounded-lg opacity-75 bg-white text-black text-bold'}))

class SignInForm(forms.Form):
    username = forms.CharField(label="username", widget=forms.TextInput(attrs={'class': 'rounded-lg opacity-75 bg-white text-black text-bold'}))
    password = forms.CharField(label="password", widget=forms.PasswordInput(attrs={'class': 'rounded-lg opacity-75 bg-white text-black text-bold'}))
    email = forms.CharField(label="email", widget=forms.EmailInput(attrs={'class': 'rounded-lg opacity-75 bg-white text-black text-bold'}))

# Create your views here.
def index(request):
    message = "Welcome to Ray's Netflix Clone"
    return render(request,"netflixpage/index.html",{
        "message":message,
    })

def index2(request,type):
    message = "Welcome to Ray's Netflix Clone" if type=="home" else "Movies"
    return render(request,"netflixpage/index.html",{
        "message":message,
    })

#checking if user is logged in to selectively display react components
def isloggedin(request):
    return JsonResponse({"isLoggedIn":request.user.is_authenticated})

#to retrieve movie data using TMDB API
def retrieve(request,genreid,genrename):
    
    #saving genres and their respective ids into backend GenresMovies database
    url = "https://api.themoviedb.org/3/genre/movie/list?language=en"
    headers = {
        "accept": "application/json",
        #FOR CS50 GRADING STAFF, YOU MUST OBTAIN YOUR OWN HEADERS AUTHORIZATION BY
        #SIGNING UP FOR AN ACCOUNT AT https://developer.themoviedb.org/reference/genre-movie-list
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkMWQzMTg2M2RjNjg2ZDJkZTZiMDFiYzFkMjU4NGIyMyIsInN1YiI6IjY0OGRlNzUzMjYzNDYyMDE0ZTU3YzVhNiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Dwpm5j_yAILTOKx93IPc5dj8rabkxx-ea7lgpD0ajdE"
    }
    response = requests.get(url, headers=headers)
    jsonresponse = response.json()
    #accessing value of "genres" key
    genres_data = jsonresponse['genres']
    for genre in genres_data:
        if not GenresMovies.objects.filter(genreid= genre['id'],genre= genre['name']).exists():
            GenresMovies(genreid= genre['id'],genre= genre['name']).save()



    #fetch real time movie data from TMDB Database for specific genre before saving it into Movies Model
    #only fetch data if data for that genre hasn't been fetched
    if not GenresMovies.objects.filter(genre = genrename, genreid = genreid).first().movie_data_retrieved:
        genreobject = GenresMovies.objects.filter(genre = genrename).first()
        genreobject.movie_data_retrieved = True
        genreobject.save()
        movies = []
        n=0
        while n<4:
            n+=1
            #FOR CS50 STAFF, you might have to obtain your own api key and replace mine with yours in the url below
            url = "https://api.themoviedb.org/3/discover/movie?api_key=d1d31863dc686d2de6b01bc1d2584b23&include_adult=false&include_video=true&language=en-US&page={}&offset=20&sort_by=popularity.desc&with_genres={}".format(n,genreid)
            response = requests.get(url)
            jsonresponse = response.json()
            movies.extend(jsonresponse['results'])
        
        for movie in movies:
            movieid = movie['id']
            title = movie['title']
            overview = movie['overview']
            genre_ids = movie['genre_ids']
            rating = movie['vote_average']
            poster_path = movie['poster_path']
            release_date = movie['release_date']

            #additional API request to retrieve short videos/trailers for each movie
            video_url = f"https://api.themoviedb.org/3/movie/{movieid}/videos?api_key=d1d31863dc686d2de6b01bc1d2584b23"
            response = requests.get(video_url)
            jsonresponse = response.json()
            if len(jsonresponse['results'])>0:
                #Retrieve key of first video
                video_key = jsonresponse['results'][0]['key']
                # Construct YouTube embed url
                embed_url = f"https://www.youtube.com/embed/{video_key}"


            #create a new movie object if movie doesn't yet exist in backend django model/database
            if not Movies.objects.filter(movieid=movieid, title=title).exists():
                newmovie = Movies(title=title,overview=overview,rating=rating,releasedate=release_date,movieid=movieid,embedurl=embed_url)
                newmovie.save()

                #getting genres corresponding to genre_ids
                #getting genreobjects whose genreid is in genre_ids retrieved from TMDB API
                genre_ids = movie['genre_ids']
                genreobjects = GenresMovies.objects.filter(genreid__in=genre_ids)
                genre_names = [genreobject.genre for genreobject in genreobjects]
                newmovie.genres = ", ".join(genre_names)
                newmovie.save()

                """saving the image found at poster path to project directory"""
                image_url = 'https://image.tmdb.org/t/p/w500' + poster_path
                response = requests.get(image_url)

                #if request is successful
                if response.status_code == 200:
                    # Create a directory to store the images if it doesn't exist
                    os.makedirs(r'C:\Users\teohr\Downloads\netflixclone\netflixpage\static\netflixpage', exist_ok=True)

                    # Get the file name from the image URL
                    file_name = os.path.basename(image_url)

                    # Save the image to the specified directory
                    image_path = os.path.join(r'C:\Users\teohr\Downloads\netflixclone\netflixpage\static\netflixpage', file_name)
                    #with open(image_path, 'wb') as f:
                        #f.write(response.content)

                    #save the image path to the new_movie object 
                    newmovie.posterpath = image_url
                    newmovie.save()
    
    #response data when react components make fetch request to backend here
    movies_data=[]
    movies = Movies.objects.filter(genres__contains=genrename)
    for movie in movies:

        #checking if movie has been liked by user
        if not movie in request.user.liked_movies.all():
            liked_button_message = "Like"
        else:
            liked_button_message = "Unlike"
        #checking if movie has been added to watchlist
        if not movie in request.user.watchlist_movies.all():
            watchlist_message = "Add to watchlist"
            watchlist_class = "fa fa-plus"
        else:
            watchlist_message = "Remove from watchlist"
            watchlist_class = "fa fa-minus"
        dictionary = {
            'title':movie.title,
            'overview':movie.overview,
            'rating':movie.rating,
            'releasedate':movie.releasedate,
            'genres':movie.genres,
            'posterpath':movie.posterpath,
            'movieid':movie.movieid,
            "liked_button_message": liked_button_message,
            "watchlist_message":watchlist_message,
            "watchlist_class":watchlist_class,
            "embed_url":movie.embedurl,
            "iframe_loaded": False,
            "iframe_message": "View Movie Trailer"
        }
        movies_data.append(dictionary)
    #JSON response to AJAX requests
    return JsonResponse(movies_data,safe=False)



#retrieve TV shows data using TMDB API
def retrieve_tvshows(request,genreid,genrename):

    #saving genres and their respective ids into backend GenresTVShows database
    url = "https://api.themoviedb.org/3/genre/tv/list?language=en"
    headers = {
        "accept": "application/json",
        #FOR CS50 GRADING STAFF, YOU MUST OBTAIN YOUR OWN HEADERS AUTHORIZATION BY
        #SIGNING UP FOR AN ACCOUNT AT https://developer.themoviedb.org/reference/genre-tv-list
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkMWQzMTg2M2RjNjg2ZDJkZTZiMDFiYzFkMjU4NGIyMyIsInN1YiI6IjY0OGRlNzUzMjYzNDYyMDE0ZTU3YzVhNiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Dwpm5j_yAILTOKx93IPc5dj8rabkxx-ea7lgpD0ajdE"
    }
    
    response = requests.get(url, headers=headers)
    jsonresponse = response.json()
    #accessing value of "genres" key
    genres_data = jsonresponse['genres']
    for genre in genres_data:
        if not GenresTVShows.objects.filter(genreid= genre['id'],genre= genre['name']).exists():
            GenresTVShows(genreid= genre['id'],genre= genre['name']).save()

    
    #fetch real time TVShow data from TMDB Database for specific genre before saving it into TVShows Model
    #only fetch data if data for that genre hasn't been fetched
    if not GenresTVShows.objects.filter(genre = genrename).first().tvshow_data_retrieved:
        genreobject = GenresTVShows.objects.filter(genre = genrename).first()
        genreobject.tvshow_data_retrieved = True
        genreobject.save()

        tvshows = []
        n=0
        while n<3:
            n+=1
            headers = {
                "accept": "application/json",
                #FOR CS50 GRADING STAFF, YOU MUST OBTAIN YOUR OWN HEADERS AUTHORIZATION BY
        #SIGNING UP FOR AN ACCOUNT AT https://developer.themoviedb.org/reference/discover-tv
                "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkMWQzMTg2M2RjNjg2ZDJkZTZiMDFiYzFkMjU4NGIyMyIsInN1YiI6IjY0OGRlNzUzMjYzNDYyMDE0ZTU3YzVhNiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Dwpm5j_yAILTOKx93IPc5dj8rabkxx-ea7lgpD0ajdE"
            }
            url = "https://api.themoviedb.org/3/discover/tv?&include_adult=false&include_null_first_air_dates=true&language=en-US&page={}&offset=20&sort_by=popularity.desc&with_genres={}".format(n,genreid)
            response = requests.get(url,headers=headers)
            jsonresponse = response.json()
            tvshows.extend(jsonresponse['results'])
        
        for tvshow in tvshows:
            tvshowid = tvshow['id']
            title = tvshow['name']
            overview = tvshow['overview']
            genre_ids = tvshow['genre_ids']
            rating = tvshow['vote_average']
            poster_path = tvshow['poster_path']
            release_date = tvshow['first_air_date']
        
            #additional API request to retrieve short videos/trailers for each tv show
            video_url = f"https://api.themoviedb.org/3/tv/{tvshowid}/videos?api_key=d1d31863dc686d2de6b01bc1d2584b23"
            response = requests.get(video_url)
            jsonresponse = response.json()
            if len(jsonresponse['results'])>0:
                #Retrieve key of first video
                video_key = jsonresponse['results'][0]['key']
                # Construct YouTube embed url
                embed_url = f"https://www.youtube.com/embed/{video_key}"
            else:
                continue


            #create a new TVShow object if movie doesn't yet exist in backend django model/database
            if not TVShows.objects.filter(tvshowid=tvshowid, title=title).exists():
                newtvshow = TVShows(title=title,overview=overview,rating=rating,releasedate=release_date,tvshowid=tvshowid,embedurl=embed_url)
                newtvshow.save()

                #getting genres corresponding to genre_ids
                #getting genreobjects whose genreid is in genre_ids retrieved from TMDB API
                genre_ids = tvshow['genre_ids']
                genreobjects = GenresTVShows.objects.filter(genreid__in=genre_ids)
                genre_names = [genreobject.genre for genreobject in genreobjects]
                newtvshow.genres = ", ".join(genre_names)
                newtvshow.save()

                #save the image path to the newtvshow object 
                image_url = 'https://image.tmdb.org/t/p/w500' + poster_path 
                newtvshow.posterpath = image_url
                newtvshow.save()
    

    #response data when react components make fetch request to backend here
    tvshows_data=[]
    tvshows = TVShows.objects.filter(genres__contains=genrename)
    for tvshow in tvshows:

        #checking if movie has been liked by user
        if not tvshow in request.user.liked_tvshows.all():
            liked_button_message = "Like"
        else:
            liked_button_message = "Unlike"
        #checking if movie has been added to watchlist
        if not tvshow in request.user.watchlist_tvshows.all():
            watchlist_message = "Add to watchlist"
            watchlist_class = "fa fa-plus"
        else:
            watchlist_message = "Remove from watchlist"
            watchlist_class = "fa fa-minus"
        dictionary = {
            'title':tvshow.title,
            'overview':tvshow.overview,
            'rating':tvshow.rating,
            'releasedate':tvshow.releasedate,
            'genres':tvshow.genres,
            'posterpath':tvshow.posterpath,
            'tvshowid':tvshow.tvshowid,
            "liked_button_message": liked_button_message,
            "watchlist_message":watchlist_message,
            "watchlist_class":watchlist_class,
            "embed_url":tvshow.embedurl,
            "iframe_loaded": False,
            "iframe_message": "View Movie Trailer"
        }
        tvshows_data.append(dictionary)
    #JSON response to AJAX requests
    return JsonResponse(tvshows_data,safe=False)
    

#to display iframe at top of page
def mainmovie(request, type):
    if type == "movie":
        #filtering for movies with rating >7.5
        movies = Movies.objects.filter(rating__gt=7.5)
        movie = random.choice(movies)

        #checking if movie has been liked by user
        if not movie in request.user.liked_movies.all():
            liked_button_message = "Like"
        else:
            liked_button_message = "Unlike"
        #checking if movie has been added to watchlist
        if not movie in request.user.watchlist_movies.all():
            watchlist_message = "Add to watchlist"
            watchlist_class = "fa fa-plus"
        else:
            watchlist_message = "Remove from watchlist"
            watchlist_class = "fa fa-minus"
        dictionary = {
            'title':movie.title,
            'overview':movie.overview,
            'rating':movie.rating,
            'releasedate':movie.releasedate,
            'genres':movie.genres,
            'posterpath':movie.posterpath,
            'movieid':movie.movieid,
            "liked_button_message": liked_button_message,
            "watchlist_message":watchlist_message,
            "watchlist_class":watchlist_class,
            "embed_url":movie.embedurl,
            "iframe_loaded": False,
            "iframe_message": "View Movie Trailer"
        }
        return JsonResponse(dictionary)
    
    if type == "tvshow":
        #filtering for tvshows with rating >7.5
        tvshows = TVShows.objects.filter(rating__gt=7.5)
        tvshow = random.choice(tvshows)

        #checking if movie has been liked by user
        if not tvshow in request.user.liked_tvshows.all():
            liked_button_message = "Like"
        else:
            liked_button_message = "Unlike"
        #checking if movie has been added to watchlist
        if not tvshow in request.user.watchlist_tvshows.all():
            watchlist_message = "Add to watchlist"
            watchlist_class = "fa fa-plus"
        else:
            watchlist_message = "Remove from watchlist"
            watchlist_class = "fa fa-minus"
        dictionary = {
            'title':tvshow.title,
            'overview':tvshow.overview,
            'rating':tvshow.rating,
            'releasedate':tvshow.releasedate,
            'genres':tvshow.genres,
            'posterpath':tvshow.posterpath,
            'movieid':tvshow.tvshowid,
            "liked_button_message": liked_button_message,
            "watchlist_message":watchlist_message,
            "watchlist_class":watchlist_class,
            "embed_url":tvshow.embedurl,
            "iframe_loaded": False,
            "iframe_message": "View Movie Trailer"
        }
        return JsonResponse(dictionary)


#rendering watchlist.html
def watchlistmovies(request):
    return render(request,"netflixpage/watchlist.html")

#rendering liked.html
def likedmovies(request):
    return render(request,"netflixpage/liked.html")

#rendering tvshows.html
def tvshows(request):
    return render(request,"netflixpage/tvshows.html")

#allow user to search for stuff
def search(request):
    searchquery = request.GET.get('searchstuff')

    # Q Object creates complex queries with multiple conditions
    # searching if searchquery is found in attributes of Movies objects
    movies = Movies.objects.filter(
        Q(title__icontains = searchquery) |
        Q(genres__icontains = searchquery) |
        Q(overview__icontains = searchquery) |
        Q(releasedate__icontains = searchquery) |
        Q(rating__icontains = searchquery)
    )

    tvshows = TVShows.objects.filter(
        Q(title__icontains = searchquery) |
        Q(genres__icontains = searchquery) |
        Q(overview__icontains = searchquery) |
        Q(releasedate__icontains = searchquery) |
        Q(rating__icontains = searchquery)
    )

    data = []
    for movie in movies:

        #checking if movie has been liked by user
        if not movie in request.user.liked_movies.all():
            liked_button_message = "Like"
        else:
            liked_button_message = "Unlike"
        #checking if movie has been added to watchlist
        if not movie in request.user.watchlist_movies.all():
            watchlist_message = "Add to watchlist"
            watchlist_class = "fa fa-plus"
        else:
            watchlist_message = "Remove from watchlist"
            watchlist_class = "fa fa-minus"
        dictionary = {
            'title':movie.title,
            'overview':movie.overview,
            'rating':movie.rating,
            'releasedate':movie.releasedate,
            'genres':movie.genres,
            'posterpath':movie.posterpath,
            'id':movie.movieid,
            "liked_button_message": liked_button_message,
            "watchlist_message":watchlist_message,
            "watchlist_class":watchlist_class,
            "embed_url":movie.embedurl,
            "iframe_loaded": False,
            "iframe_message": "View Movie Trailer"
        }
        data.append(dictionary)
    
    for tvshow in tvshows:

        #checking if movie has been liked by user
        if not tvshow in request.user.liked_tvshows.all():
            liked_button_message = "Like"
        else:
            liked_button_message = "Unlike"
        #checking if movie has been added to watchlist
        if not tvshow in request.user.watchlist_tvshows.all():
            watchlist_message = "Add to watchlist"
            watchlist_class = "fa fa-plus"
        else:
            watchlist_message = "Remove from watchlist"
            watchlist_class = "fa fa-minus"
        dictionary = {
            'title':tvshow.title,
            'overview':tvshow.overview,
            'rating':tvshow.rating,
            'releasedate':tvshow.releasedate,
            'genres':tvshow.genres,
            'posterpath':tvshow.posterpath,
            'id':tvshow.tvshowid,
            "liked_button_message": liked_button_message,
            "watchlist_message":watchlist_message,
            "watchlist_class":watchlist_class,
            "embed_url":tvshow.embedurl,
            "iframe_loaded": False,
            "iframe_message": "View Movie Trailer"
        }
        data.append(dictionary)
    return render(request,"netflixpage/searchpage.html",{
        #converts 'data' list of dictionaries into JSON-formatted string
        "movies":json.dumps(data)
    })




#retrieving movies in user's watchlist
def retrieve_watchlist(request):
    
    #response data when react components make fetch request to backend here
    movies_data=[]
    for movie in request.user.watchlist_movies.all():

        #checking if movie has been liked by user
        if not movie in request.user.liked_movies.all():
            liked_button_message = "Like"
        else:
            liked_button_message = "Unlike"
        #checking if movie has been added to watchlist
        if not movie in request.user.watchlist_movies.all():
            watchlist_message = "Add to watchlist"
            watchlist_class = "fa fa-plus"
        else:
            watchlist_message = "Remove from watchlist"
            watchlist_class = "fa fa-minus"
        dictionary = {
            'title':movie.title,
            'overview':movie.overview,
            'rating':movie.rating,
            'releasedate':movie.releasedate,
            'genres':movie.genres,
            'posterpath':movie.posterpath,
            'movieid':movie.movieid,
            "liked_button_message": liked_button_message,
            "watchlist_message":watchlist_message,
            "watchlist_class":watchlist_class,
            "embed_url":movie.embedurl,
            "iframe_loaded": False,
            "iframe_message": "View Movie Trailer"
        }
        movies_data.append(dictionary)
    
    for tvshow in request.user.watchlist_tvshows.all():

        #checking if movie has been liked by user
        if not tvshow in request.user.liked_tvshows.all():
            liked_button_message = "Like"
        else:
            liked_button_message = "Unlike"
        #checking if movie has been added to watchlist
        if not tvshow in request.user.watchlist_tvshows.all():
            watchlist_message = "Add to watchlist"
            watchlist_class = "fa fa-plus"
        else:
            watchlist_message = "Remove from watchlist"
            watchlist_class = "fa fa-minus"
        dictionary = {
            'title':tvshow.title,
            'overview':tvshow.overview,
            'rating':tvshow.rating,
            'releasedate':tvshow.releasedate,
            'genres':tvshow.genres,
            'posterpath':tvshow.posterpath,
            'movieid':tvshow.tvshowid,
            "liked_button_message": liked_button_message,
            "watchlist_message":watchlist_message,
            "watchlist_class":watchlist_class,
            "embed_url":tvshow.embedurl,
            "iframe_loaded": False,
            "iframe_message": "View Movie Trailer"
        }
        movies_data.append(dictionary)
    #JSON response to AJAX requests
    return JsonResponse(movies_data,safe=False)

#retrieving user's liked movies
def retrieve_liked(request):
    
    #response data when react components make fetch request to backend here
    movies_data=[]
    for movie in request.user.liked_movies.all():

        #checking if movie has been liked by user
        if not movie in request.user.liked_movies.all():
            liked_button_message = "Like"
        else:
            liked_button_message = "Unlike"
        #checking if movie has been added to watchlist
        if not movie in request.user.watchlist_movies.all():
            watchlist_message = "Add to watchlist"
            watchlist_class = "fa fa-plus"
        else:
            watchlist_message = "Remove from watchlist"
            watchlist_class = "fa fa-minus"
        dictionary = {
            'title':movie.title,
            'overview':movie.overview,
            'rating':movie.rating,
            'releasedate':movie.releasedate,
            'genres':movie.genres,
            'posterpath':movie.posterpath,
            'movieid':movie.movieid,
            "liked_button_message": liked_button_message,
            "watchlist_message":watchlist_message,
            "watchlist_class":watchlist_class,
            "embed_url":movie.embedurl,
            "iframe_loaded": False,
            "iframe_message": "View Movie Trailer"
        }
        movies_data.append(dictionary)
    
    for tvshow in request.user.liked_tvshows.all():

        #checking if movie has been liked by user
        if not tvshow in request.user.liked_tvshows.all():
            liked_button_message = "Like"
        else:
            liked_button_message = "Unlike"
        #checking if movie has been added to watchlist
        if not tvshow in request.user.watchlist_tvshows.all():
            watchlist_message = "Add to watchlist"
            watchlist_class = "fa fa-plus"
        else:
            watchlist_message = "Remove from watchlist"
            watchlist_class = "fa fa-minus"
        dictionary = {
            'title':tvshow.title,
            'overview':tvshow.overview,
            'rating':tvshow.rating,
            'releasedate':tvshow.releasedate,
            'genres':tvshow.genres,
            'posterpath':tvshow.posterpath,
            'movieid':tvshow.tvshowid,
            "liked_button_message": liked_button_message,
            "watchlist_message":watchlist_message,
            "watchlist_class":watchlist_class,
            "embed_url":tvshow.embedurl,
            "iframe_loaded": False,
            "iframe_message": "View Movie Trailer"
        }
        movies_data.append(dictionary)
    #JSON response to AJAX requests
    return JsonResponse(movies_data,safe=False)
    

#function to like/unlike movie for user, and to update text in like/unlike button
def like(request, id, message, movieortv):
    if message == "Like":
        user = request.user
        if movieortv == "movie":
            movie = Movies.objects.get(movieid=id)
            user.liked_movies.add(movie)
            user.save()
        
        elif movieortv == "tv":
            tv = TVShows.objects.get(tvshowid=id)
            user.liked_tvshows.add(tv)
            user.save()


        # Return JSON response to update text
        response_data = {
            "liked_message": "Unlike"
        }
        return JsonResponse(response_data)

    else:
        user = request.user
        if movieortv == "movie":
            movie = Movies.objects.get(movieid=id)
            user.liked_movies.remove(movie)
            user.save()
        
        elif movieortv == "tv":
            tv = TVShows.objects.get(tvshowid=id)
            user.liked_tvshows.remove(tv)
            user.save()

        # Return JSON response to update text
        response_data = {
            "liked_message": "Like"
        }
        return JsonResponse(response_data)


#function to add/remove movie from user's watchlist, and update text in watchlist button  
def watchlist(request, id, message, movieortv):
    if message == "Add to watchlist":
        if movieortv == "movie":
            movie = Movies.objects.get(movieid=id)
            request.user.watchlist_movies.add(movie)
            request.user.save()
        
        elif movieortv == "tv":
            tv = TVShows.objects.get(tvshowid=id)
            request.user.watchlist_tvshows.add(tv)
            request.user.save()
        

        # Return JSON response to update text
        response_data = {
            "watchlist_message": "Remove from watchlist",
            "watchlist_class":"fa fa-minus"
        }
        return JsonResponse(response_data)
    
    else:
        if movieortv == "movie":
            movie = Movies.objects.get(movieid=id)
            request.user.watchlist_movies.remove(movie)
            request.user.save()
        
        elif movieortv == "tv":
            tv = TVShows.objects.get(tvshowid=id)
            request.user.watchlist_tvshows.remove(tv)
            request.user.save()

        # Return JSON response to update text
        response_data = {
            "watchlist_message": "Add to watchlist",
            "watchlist_class":"fa fa-plus"
        }
        return JsonResponse(response_data)


def register(request):
    if request.method == "GET":
        email = request.GET.get("email")
        form = NewTaskForm(initial={"email": email})
        return render(request,"netflixpage/register.html",{
            "form":form,
        })
    
    if request.method == "POST":
        # Take in the data the user submitted in registeremail form and save it as form
        form = NewTaskForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            confirmpassword = form.cleaned_data["confirmpassword"]
            email = form.cleaned_data["email"]

            #if passwords do not match, return error message
            if password!=confirmpassword:
                error = "Passwords do not match"
                return render(request,"netflixpage/register.html",{
                "form":form,
                "message":error
                })
            
            #if passwords match, then register user
            else:
                try:
                    user = User.objects.create_user(username, email, password)
                    user.save()
                    login(request, user)
                    return redirect('/')
                except IntegrityError:
                    return render(request, "netflixpage/register.html", {
                        "message": "Username already taken.",
                        "form":form
                    })
                

        
        else:
            return render(request,"netflixpage/register.html",{
            "form":form
        })

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def login_view(request):
    if request.method=="GET":
        return render(request,"netflixpage/login.html",{
            "form":SignInForm()
        })

    #if request method is POST
    else:

        # Take in the data the user submitted in signin form and save it as form
        form = SignInForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():
            #attempt to sign user in
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            email = form.cleaned_data["email"]
            user = authenticate(request, username=username, password=password)

            # Check if authentication successful
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "netflixpage/login.html", {
                    "message": "Invalid username and/or password."
                })
        
        else:
            return render(request, "netflixpage/login.html", {
                    "form": form
                })
        
        
