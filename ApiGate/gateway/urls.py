# api_gateway/urls.py

from django.urls import path
from .views import MyBooksView,HomeView,BorrowAndDateSendView
from . view_classes.UserSignUp import UserSignUp
from .view_classes.UserLogin import UserLogin
from .view_classes.BookCreate import BookCreate

from .view_classes.BookDele import BookDele
from .view_classes.BookDetailsView import BookDetailView
from .view_classes.BookEdit import BookEdit
app_name ='gateway'
urlpatterns = [
    
    path('mybooks/<int:user_id>/', MyBooksView.as_view(), name='mybooks'),
    path('signup/', UserSignUp.as_view(), name='signup'),
    path('login/', UserLogin.as_view(), name='login'),
    path('borrow/', BorrowAndDateSendView.as_view(), name='borrow'),
    path('home/', HomeView.as_view(), name='home'),
    
    path('details/<int:pk>', BookDetailView.as_view(), name='details'),
    path('book/<int:pk>/delete/', BookDele.as_view(), name='delete'),
    path('new/', BookCreate.as_view(), name='create'),#book_form
    path('book/<int:pk>/edit/', BookEdit.as_view(), name='edit'),#book_form
   
]
