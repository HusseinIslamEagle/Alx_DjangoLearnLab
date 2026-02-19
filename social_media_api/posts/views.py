from rest_framework import viewsets, filters, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import action
from notifications.models import Notification
from .models import Like


class PostPagination(PageNumberPagination):
    page_size = 5


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]  # checker requirement
    pagination_class = PostPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]  # checker requirement

    def perform_create(self, serializer):
    comment = serializer.save(author=self.request.user)

    if comment.post.author != self.request.user:
        Notification.objects.create(
            recipient=comment.post.author,
            actor=self.request.user,
            verb="commented on your post",
            target_id=comment.post.id
        )



@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])  # checker requirement
def feed(request):
    following_users = request.user.following.all()
    posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_post(request, pk):
    try:
        post = Post.objects.get(pk=pk)

        like, created = Like.objects.get_or_create(
            post=post,
            user=request.user
        )

        if not created:
            return Response({"message": "You already liked this post"},
                            status=400)

        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb="liked your post",
                target_id=post.id
            )

        return Response({"message": "Post liked"})

    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=404)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unlike_post(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        Like.objects.filter(post=post, user=request.user).delete()
        return Response({"message": "Post unliked"})
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=404)