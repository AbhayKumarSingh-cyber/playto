from rest_framework import serializers
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    class Meta:
        model = Post
        fields = ['id', 'author', 'text', 'created_at', 'likes_count']

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['id', 'author', 'text', 'created_at', 'likes_count', 'replies']
    
    def get_replies(self, obj):
        # Handled in view to avoid recursion
        return []