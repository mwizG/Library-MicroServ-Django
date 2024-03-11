from django.shortcuts import render
from .models import Books
from django.http import HttpResponse

# Create your views here.

##return all books in the db
def books(request):
    books = Books.objects.all()
    return render(request, 'books.html', {'books': books})

##search for books in the db
def query_books(request):
    if 'query' in request.GET and request.GET["query"]:
        search_term = request.GET.get("query")
        searched_books = Books.objects.filter(title__icontains=search_term)
        return render(request, 'books.html', {'books': searched_books })
    else:
        return HttpResponse("No books foudn matching %s", search_term)