from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import viewsets
from rest_framework import mixins , generics
from rest_framework.views import APIView
from watchlist_app.models import StreamPlatform, WatchList, Review
from watchlist_app.api.serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer
from watchlist_app.api.permissions import IsAdminOrReadOnly, ReviewUserOrReadOnly
from watchlist_app.api.paginations import WatchlistPagination, WatchlistLOPagination, WatchlistCPagination
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from watchlist_app.api.throttling import ReviewCreateThrottle, ReviewListThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class UserReview(generics.ListAPIView):
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        # username = self.kwargs['username']
        username = self.request.query_params.get('username', None)
        return Review.objects.filter(review_user__username = username)

class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self,serializer): 
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)
        review_user = self.request.user 
        review_queryset = Review.objects.filter(watchlist = watchlist, review_user = review_user)
        
        if review_queryset.exists():
            raise ValidationError('You have already reviewed this movie!')
        
        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating'])/2
            
        watchlist.number_rating += 1
        watchlist.save()
        serializer.save(watchlist=watchlist, review_user=review_user)

class ReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly]
    throttle_classes = [ReviewListThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']
    
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Review.objects.filter(watchlist = pk)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'
    
class StreamPlatformVS(viewsets.ModelViewSet): 
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
        
    
class StreamPlatformListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request):
        list = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(list, many=True, context = {'request': request})
        return Response(serializer.data)
    
    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class StreamPlatformDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request, pk):
        try:
            watchlist = StreamPlatform.objects.get(pk = pk)
        except StreamPlatform.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(watchlist, context = {'request': request})
        return Response(serializer.data)
    
    def put(self, request, pk):
        watchlist = StreamPlatform.objects.get(pk = pk)
        serializer = StreamPlatformSerializer(watchlist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        watchlist = WatchList.objects.get(pk = pk)
        watchlist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
       
       
class WatchListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request):
        list = WatchList.objects.all()
        serializer = WatchListSerializer(list, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class WatchListGV(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    pagination_class = WatchlistCPagination
    
    #filter_backends = [filters.SearchFilter]
    #search_fields = ['=title', 'platform__name']
    
    #filter_backends = [filters.OrderingFilter]
    #ordering_fields = ['avg_rating']
     

class WatchListDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self, request, pk):
        try:
            watchlist = WatchList.objects.get(pk = pk)
        except WatchList.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(watchlist)
        return Response(serializer.data)
    
    def put(self, request, pk):
        watchlist = WatchList.objects.get(pk = pk)
        serializer = WatchListSerializer(watchlist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        watchlist = WatchList.objects.get(pk = pk)
        watchlist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
"""
@api_view(["GET", "POST"])
def movie_list(request):
    if request.method == "GET": 
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    
    if request.method == "POST": 
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
def movie_details(request, pk):
    if request.method == "GET": 
        try:
            movie = Movie.objects.get(pk = pk)
        except Movie.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    
    if request.method == "PUT": 
        movie = Movie.objects.get(pk = pk)
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == "DELETE":
        movie = Movie.objects.get(pk = pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""