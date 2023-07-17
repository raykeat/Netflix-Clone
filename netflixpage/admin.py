from django.contrib import admin

from .models import User, Movies, GenresMovies, TVShows, GenresTVShows
# Register your models here.

#registers the models in admin app to allow us to use the admin app to manipulate these models/tables
admin.site.register(User)
admin.site.register(Movies)
admin.site.register(GenresMovies)
admin.site.register(TVShows)
admin.site.register(GenresTVShows)
