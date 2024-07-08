# api_gateway/urls.py

from django.urls import path
from .views import AuthView, BooksView,HomeView,BorrowView
from . view_classes.UserSignUp import UserSignUp
from .view_classes.UserLogin import UserLogin
from .view_classes.BookCreate import BookCreate
from .view_classes.BookDateSend import BookDateSend
from .view_classes.BookDele import BookDele
from .view_classes.BookDetailsView import BookDetailView
from .view_classes.BookEdit import BookEdit
app_name ='gateway'
urlpatterns = [
    
    path('books/query/', BooksView.as_view(), name='books-query'),
    path('signup/', UserSignUp.as_view(), name='signup'),
    path('login/', UserLogin.as_view(), name='login'),
    path('auth/login/', AuthView.as_view(), name='auth-login'),
    path('home/', HomeView.as_view(), name='home'),
    path('borrow/', BorrowView.as_view(), name='borrow'),
    path('details/<int:pk>', BookDetailView.as_view(), name='details'),
    path('book/<int:pk>/delete/', BookDele.as_view(), name='delete'),
    path('new/', BookCreate.as_view(), name='create'),#book_form
    path('book/<int:pk>/edit/', BookEdit.as_view(), name='edit'),#book_form
    path('senddate/',BookDateSend.as_view(),name='senddate')
]
