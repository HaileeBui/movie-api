
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from watchlist_app.api.views import *

router = DefaultRouter()
router.register('stream', StreamPlatformVS, basename='streamplatform')

urlpatterns = [
    path("list/", WatchListAV.as_view(), name = "watchlist"),
    path("<int:pk>/", WatchListDetailAV.as_view(), name = "movie-detail"),
    path("newlist/", WatchListGV.as_view(), name = "movie-list"),
    
    path('', include(router.urls)),
    #path("stream/", StreamPlatformListAV.as_view(), name = "stream-list"),
    #path("stream/<int:pk>", StreamPlatformDetailAV.as_view(), name = "streamplatform-detail"),
    
    path('<int:pk>/review/', ReviewList.as_view(), name='review-list'),
    path('<int:pk>/review-create/', ReviewCreate.as_view(), name='review-create'),
    path('review/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
    
    #path('review/<str:username>/', UserReview.as_view(), name='user-review-detail'),
    path('review/', UserReview.as_view(), name='user-review-detail'),
]
