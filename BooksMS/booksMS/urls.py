from django.urls import path

from . import views

urlpatterns = [
    path('books/',views.books, name='books'),
    path('books/results',views.query_books, name='results')

]