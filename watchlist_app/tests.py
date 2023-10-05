from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.urls import reverse

from watchlist_app.api.serializers import serializers
from watchlist_app import models


class StreamPlatformTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test123', email='test@example.com')
        self.user.save()

        self.token, created = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.token.key)
        
        self.stream = models.StreamPlatform.objects.create(name='Netfliz', about='Netfliz is no.1', website='http://netfliz.com')
        
    def test_streamplatform_create(self):
        data = { 
            "name": "Netfliz",
            "about": "Netfliz is no.1",
            "website": "http://netfliz.com",
        }
        
        response = self.client.post(reverse('streamplatform-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_streamplatform_list(self):
       response = self.client.get(reverse('streamplatform-list'))
       self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_streamplatform_ind(self):
        response = self.client.get(reverse('streamplatform-detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
class WatchListTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test123', email='test@example.com')
        self.user.save()

        self.token, created = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.token.key)
        
        self.stream = models.StreamPlatform.objects.create(name='Netfliz', about='Netfliz is no.1', website='http://netfliz.com')
        self.watchlist = models.WatchList.objects.create(platform = self.stream, title = "example movie", storyline = "example storyline", active = True)
        
    def test_watchlist_create(self):
        data = { 
            "platform": self.stream,
            "title": "example movie",
            "storyline": "example storyline",
            "active": True,
        }
        
        response = self.client.post(reverse('watchlist'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) #403
    
    def test_watchlist_list(self):
        response = self.client.get(reverse('watchlist'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_watchlist_detail(self):
        response = self.client.get(reverse('movie-detail', args=[self.watchlist.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        self.assertEqual(models.WatchList.objects.count(), 1) 
        self.assertEqual(models.WatchList.objects.get().title, "example movie")

class ReviewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test123', email='test@example.com')
        self.client.force_authenticate(self.user)

        #self.token = Token.objects.get(user__username=self.user)
        #self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.token.key)
        
        self.stream = models.StreamPlatform.objects.create(name='Netfliz', about='Netfliz is no.1', website='http://netfliz.com')
        self.watchlist = models.WatchList.objects.create(platform = self.stream, title = "example movie", storyline = "example storyline", active = True)
        
        self.watchlist2 = models.WatchList.objects.create(platform = self.stream, title = "example movie", storyline = "example storyline", active = True)
        
        self.review = models.Review.objects.create(review_user = self.user, rating = 5, description = "description", watchlist = self.watchlist2, active = True)
        
    def test_review_create(self):
        data = {
            "review_user": self.user,
            "rating" : 5,
            "description": "description",
            "watchlist": self.watchlist,
            "active": True,
        }
        response = self.client.post(reverse('review-create', args=[self.watchlist.id]), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Review.objects.count(), 2)
        #self.assertEqual(models.Review.objects.get().rating, 5)
        
        response = self.client.post(reverse('review-create', args=[self.watchlist.id]), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_review_create_invalid(self):
        data = {
            "review_user": self.user,
            "rating" : 5,
            "description": "description",
            "watchlist": self.watchlist,
            "active": True,
        }
        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('review-create', args=[self.watchlist.id]), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_review_update(self):
        data = {
            "review_user": self.user,
            "rating" : 4,
            "description": "description-updated",
            "watchlist": self.watchlist,
            "active": True,
        }
        response = self.client.put(reverse('review-detail', args=[self.review.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_review_list(self):
        response = self.client.get(reverse('review-list', args=[self.watchlist.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_review_list_ind(self):
        response = self.client.get(reverse('review-detail', args=[self.review.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    """def test_review_user(self):
        response = self.client.get('/watch/reviews/?username' + self.user.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)"""
   