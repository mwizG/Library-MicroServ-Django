from django.urls import path
from . views import ReturnBookView
from .views import create_loan,borrow_book

app_name='loans'
urlpatterns = [
    path('return/', ReturnBookView.as_view(),name='return'),
    path('create/', create_loan, name='create'),
    path('borrow/', borrow_book, name='borrow'),
    
]
