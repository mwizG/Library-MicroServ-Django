from django.shortcuts import render
from .models import Books
from django.http import HttpResponse
import logging
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

logger = logging.getLogger(__name__)

##return all books in the db
@csrf_exempt
def books(request):
    print("here123")
    books = Books.objects.all()
    return render(request, 'books.html', {'books': books})

##search for books in the db
@csrf_exempt
def query_books(request):
    if 'query' in request.GET and request.GET["query"]:
        search_term = request.GET.get("query")
        searched_books = Books.objects.filter(title__icontains=search_term)
        return render(request, 'books.html', {'books': searched_books })
    else:
        return HttpResponse("No books foudn matching %s", search_term)