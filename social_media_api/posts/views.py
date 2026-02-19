from rest_framework import viewsets, filters, permissions, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from notifications.models import Notification


# ==============================
# Pagination
# ==============================

class PostPagination(PageNumberPagination):
    page_size = 5


# ==============================
# Post ViewSet
# ==============================

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = PostPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# ==============================
# Comment ViewSet
# ==============================

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)

        if comment.post.author != self.request.user:
            Notification.objects.create(
                recipient=comment.post.author,
                actor=self.request.user,
                verb="commented on your post",
                target_id=comment.post.id
            )


# ==============================
# Feed View
# ==============================

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def feed(request):
    following_users = request.user.following.all()
    posts = Post.objects.filter(
        author__in=following_users
    ).order_by('-created_at')

    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


# ==============================
# Like Post
# ==============================

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_post(request, pk):

    post = generics.get_object_or_404(Post, pk=pk)

    # لازم تكون في سطر واحد للـ checker
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        return Response(
            {"message": "You already liked this post"},
            status=400
        )

    if post.author != request.user:
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb="liked your post",
            target_id=post.id
        )

    return Response({"message": "Post liked"})



# ==============================
# Unlike Post
# ==============================

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unlike_post(request, pk):

    post = generics.get_object_or_404(Post, pk=pk)

    Like.objects.filter(
        user=request.user,
        post=post
    ).delete()

    return Response({"message": "Post unliked"})
