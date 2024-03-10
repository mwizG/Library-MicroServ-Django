# api_gateway/urls.py

from django.urls import path
from .views import AuthView, BooksView

urlpatterns = [
    path('auth/login/', AuthView.as_view(), name='auth-login'),
    path('books/', BooksView.as_view(), name='books'),
    path('books/query/', BooksView.as_view(), name='books-query'),
]
