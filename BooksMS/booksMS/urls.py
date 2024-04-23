from django.urls import path

from . import views
app_name='books'
urlpatterns = [
    path('books/',views.books, name='books'),
    path('books/results',views.query_books, name='results'),
    path('details/<int:pk>',views.book_details,name='details'),
    path('new/', views.book_create, name='book_create'),
    path('book/<int:pk>/edit/', views.book_update, name='book_update'),
    path('book/<int:pk>/delete/', views.book_delete, name='delete'),

]