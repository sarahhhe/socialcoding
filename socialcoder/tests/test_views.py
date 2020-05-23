from django.test import TestCase, Client
from django.urls import reverse
from socialcoder.models import Post, Response, Category
from users.models import User, Profile
import json

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

        self.feed_url = reverse('socialcoder-feed')
        self.leaderboard_url = reverse('socialcoder-leaderboard')

    def test_feed_GET(self):
        client = Client()
        response = self.client.get(self.feed_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'socialcoder/feed.html')

    def test_search_GET(self):
        response = self.client.get(self.leaderboard_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'socialcoder/leaderboard.html')
