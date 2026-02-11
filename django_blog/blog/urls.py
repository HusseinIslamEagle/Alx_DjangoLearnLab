from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    register_view,
    login_view,
    profile_view,
    add_comment,
    PostByTagListView,
    SearchResultsView,
)

urlpatterns = [

    # Posts
    path('', PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),

    # Comments
    path('post/<int:pk>/comments/new/', add_comment, name='add-comment'),

    # Authentication
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('profile/', profile_view, name='profile'),

    # Tag filtering
    path('tags/<slug:tag_slug>/', PostByTagListView.as_view(), name='posts-by-tag'),

    # Search
    path('search/', SearchResultsView.as_view(), name='search'),
]
