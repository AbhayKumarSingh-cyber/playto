from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.request.query_params.get('post_id')
        return Comment.objects.filter(post_id=post_id).select_related('author', 'parent')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        # Build tree in Python to avoid N+1
        comments = list(queryset)
        comment_dict = {c.id: CommentSerializer(c).data for c in comments}
        for comment in comments:
            if comment.parent_id:
                if 'replies' not in comment_dict[comment.parent_id]:
                    comment_dict[comment.parent_id]['replies'] = []
                comment_dict[comment.parent_id]['replies'].append(comment_dict[comment.id])
        # Return top-level comments only
        top_level = [comment_dict[c.id] for c in comments if not c.parent_id]
        return Response(top_level)

@api_view(['POST'])
def like_view(request):
    user = request.user
    post_id = request.data.get('post_id')
    comment_id = request.data.get('comment_id')
    if post_id:
        obj = Post.objects.get(id=post_id)
        like, created = Like.objects.get_or_create(user=user, post=obj, defaults={'created_at': timezone.now()})
        if created:
            obj.likes_count += 1
            obj.save()
            return Response({'message': 'Liked post'}, status=status.HTTP_201_CREATED)
    elif comment_id:
        obj = Comment.objects.get(id=comment_id)
        like, created = Like.objects.get_or_create(user=user, comment=obj, defaults={'created_at': timezone.now()})
        if created:
            obj.likes_count += 1
            obj.save()
            return Response({'message': 'Liked comment'}, status=status.HTTP_201_CREATED)
    return Response({'message': 'Already liked'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def leaderboard_view(request):
    now = timezone.now()
    cutoff = now - timedelta(hours=24)
    
    # Karma from post likes: 5 per like
    post_karma = Like.objects.filter(post__isnull=False, created_at__gte=cutoff).values('post__author').annotate(
        karma=Count('id') * 5
    ).values('post__author', 'karma')
    
    # Karma from comment likes: 1 per like
    comment_karma = Like.objects.filter(comment__isnull=False, created_at__gte=cutoff).values('comment__author').annotate(
        karma=Count('id')
    ).values('comment__author', 'karma')
    
    # Aggregate in Python
    karma_dict = {}
    for item in post_karma:
        karma_dict[item['post__author']] = karma_dict.get(item['post__author'], 0) + item['karma']
    for item in comment_karma:
        karma_dict[item['comment__author']] = karma_dict.get(item['comment__author'], 0) + item['karma']
    
    # Get top 5 with usernames
    from django.contrib.auth.models import User
    top_users = sorted(karma_dict.items(), key=lambda x: x[1], reverse=True)[:5]
    leaderboard = [{'user': User.objects.get(id=uid).username, 'karma': karma} for uid, karma in top_users]
    return Response(leaderboard)