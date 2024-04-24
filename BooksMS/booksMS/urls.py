from django.urls import path
from . views import BooksView
from . import views
app_name='books'
urlpatterns = [
    path('books/', BooksView.as_view(), name='books'),
    path('books/results',views.query_books, name='results'),
    path('details/<int:pk>',views.book_details,name='details'),
    path('new/', views.book_create, name='book_create'),
    path('book/<int:pk>/edit/', views.book_update, name='book_update'),
    path('book/<int:pk>/delete/', views.book_delete, name='delete'),

]