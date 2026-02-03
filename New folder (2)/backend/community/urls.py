from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.PostListCreateView.as_view(), name='posts'),
    path('comments/', views.CommentListCreateView.as_view(), name='comments'),
    path('like/', views.like_view, name='like'),
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),
]