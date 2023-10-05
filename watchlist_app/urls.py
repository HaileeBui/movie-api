
from django.urls import path
from watchlist_app.api.views import *

urlpatterns = [
    path("list/", movie_list, name = "movie-list"),
    #path("<int:pk>", movie_detail, name = "movie-detail"),
]
