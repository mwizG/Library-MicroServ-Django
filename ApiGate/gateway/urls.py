# api_gateway/urls.py

from django.urls import path
from .views import AuthView, BooksView,UserLogin,HomeView #,BorrowView
from . view_classes.UserSignUp import UserSignUp
app_name ='gateway'
urlpatterns = [
    
    path('books/query/', BooksView.as_view(), name='books-query'),
    path('signup/', UserSignUp.as_view(), name='signup'),
    path('login/', UserLogin.as_view(), name='login'),
    path('auth/login/', AuthView.as_view(), name='auth-login'),
    path('home/', HomeView.as_view(), name='home'),
   # path('borrow/', BorrowView.as_view(), name='borrow'),
]
