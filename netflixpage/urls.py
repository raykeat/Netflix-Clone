from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("/<str:type>/", views.index2, name="index2"),
    path("register/",views.register,name="register"),
    path("logout/",views.logout_view,name="logout"),
    path("login/",views.login_view,name="login"),

    #Django API Endpoint to retrieve movie data
    path("retrievemovie/homepage/<int:genreid>/<str:genrename>/",views.retrieve,name="retrieve"),
    path("retrievemovie/watchlist/",views.retrieve_watchlist,name="retrieve_watchlist"),
    path("retrievemovie/liked/",views.retrieve_liked,name="retrieve_liked"),
    path("retrievemovie/tvshows/<int:genreid>/<str:genrename>/",views.retrieve_tvshows,name="retrieve_tvshows"),

    #to display main iframe at top of page, similar to netflix
    path("mainmovie/<str:type>/",views.mainmovie,name="mainmovie"),

    #to like and add to watchlist
    path("like/<int:id>/<str:message>/<str:movieortv>/",views.like,name="like"),
    path("watchlist/<int:id>/<str:message>/<str:movieortv>/",views.watchlist,name="watchlist"),

    #to allow users to search for movies, titles, genres etc
    path("search/",views.search,name="search"),

    #to render watchlist page
    path("watchlistmovies/",views.watchlistmovies,name="watchlistmovies"),
    #to render TV shows page
    path("tvshows/",views.tvshows,name="tvshows"),
    #to render liked movies
    path("likedmovies/",views.likedmovies,name="likedmovies"),

    #check if user is logged in
    path("isloggedin/",views.isloggedin,name="isloggedin"),


    
]
