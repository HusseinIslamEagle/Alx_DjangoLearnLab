from django.urls import path
from . import views

urlpatterns = [
    path('view/', views.view_article),
    path('create/', views.create_article),
    path('edit/', views.edit_article),
    path('delete/', views.delete_article),
]
