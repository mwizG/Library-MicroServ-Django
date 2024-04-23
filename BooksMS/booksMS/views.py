from urllib import request
from django.shortcuts import redirect, render
import requests
from .models import Books
from django.http import HttpResponse
import logging
from django.views.decorators.csrf import csrf_exempt
from . forms import BookForm,AuthorForm

# Create your views here.

logger = logging.getLogger(__name__)

##return all books in the db
@csrf_exempt
def books(request):
   
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
    
def book_details(request,pk):
    book=Books.objects.get(pk=pk)

    return render(request,'book_details.html',{'book':book})

def book_create(request):
    if request.method=='POST':
        form =BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/books/')
    else:
        form =BookForm()
    return render(request, 'book_form.html',{'form':form})

def book_update(request, pk):
    book = Books.objects.get(pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('/books/')
    else:
        form = BookForm(instance=book)
    return render(request, 'book_form.html', {'form': form})

def book_delete(request, pk):
    book = Books.objects.get(pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('/books/')
    return render(request, 'book_delete.html', {'book': book})