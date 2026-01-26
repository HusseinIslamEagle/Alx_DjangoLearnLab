from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import list_books, LibraryDetailView
from . import views

urlpatterns = [
    # Function-based view
    path('books/', list_books, name='list_books'),

    # Class-based view
    path('libraries/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # Home
    path('', views.home, name='home'),

    # Authentication
    path(
        'login/',
        LoginView.as_view(template_name='relationship_app/login.html'),
        name='login'
    ),
    path(
        'logout/',
        LogoutView.as_view(template_name='relationship_app/logout.html'),
        name='logout'
    ),
    path('register/', views.register, name='register'),

    # Book permissions
    path('add_book/', views.add_book, name='add_book'),
    path('edit_book/<int:book_id>/', views.edit_book, name='edit_book'),
    path('delete_book/<int:book_id>/', views.delete_book, name='delete_book'),
]
