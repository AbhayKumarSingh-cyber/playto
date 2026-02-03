from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from community.models import User, Post, Comment, Like
from community.views import leaderboard_view
from rest_framework.test import APIRequestFactory

class LeaderboardTest(TestCase):
    def test_leaderboard_calculation(self):
        user1 = User.objects.create_user(username='user1')
        user2 = User.objects.create_user(username='user2')
        post = Post.objects.create(author=user1, text='Test')
        comment = Comment.objects.create(author=user1, post=post, text='Test')
        now = timezone.now()
        Like.objects.create(user=user2, post=post, created_at=now)
        Like.objects.create(user=user2, comment=comment, created_at=now)
        factory = APIRequestFactory()
        request = factory.get('/api/leaderboard/')
        response = leaderboard_view(request)
        self.assertEqual(response.data[0]['user'], 'user1')
        self.assertEqual(response.data[0]['karma'], 6)