from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class GenresMovies(models.Model):
    genreid = models.IntegerField(default=0)
    genre = models.CharField(max_length=100)
    movie_data_retrieved = models.BooleanField(default=False)


class Movies(models.Model):
    movieid = models.IntegerField(default=0)
    title = models.CharField(max_length=300)
    genres = models.CharField(max_length=300)
    overview = models.TextField(max_length=300)
    releasedate = models.CharField(max_length=300)
    rating = models.FloatField(default=0)
    posterpath = models.TextField(max_length=300)
    embedurl = models.CharField(max_length=300)

    cast = models.TextField(max_length=300,null=True)
    duration = models.IntegerField(default=100,null=True)
    descriptiveadjectives = models.TextField(max_length=300,null=True)

class GenresTVShows(models.Model):
    genreid = models.IntegerField(default=0)
    genre = models.CharField(max_length=100)
    tvshow_data_retrieved = models.BooleanField(default=False)

class TVShows(models.Model):
    tvshowid = models.IntegerField(default=0)
    title = models.CharField(max_length=300)
    genres = models.CharField(max_length=300)
    overview = models.TextField(max_length=300)
    releasedate = models.CharField(max_length=300)
    rating = models.FloatField(default=0)
    posterpath = models.TextField(max_length=300)
    embedurl = models.CharField(max_length=300,blank=True)

class User(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,
        verbose_name=('groups'),
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_query_name='custom_user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
        verbose_name=('user permissions'),
        help_text=('Specific permissions for this user.'),
        related_query_name='custom_user'
    )
    liked_movies = models.ManyToManyField(Movies,related_name="likedusermovie")
    watchlist_movies = models.ManyToManyField(Movies,related_name="watchlistusermovie")

    liked_tvshows = models.ManyToManyField(TVShows,related_name="likedusertvshow")
    watchlist_tvshows = models.ManyToManyField(TVShows,related_name="watchlistusertvshow")








