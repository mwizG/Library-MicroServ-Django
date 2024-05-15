import json
from urllib import request
from django.shortcuts import redirect, render
from django.views import View
import requests
from .models import Books
from django.http import HttpResponse, JsonResponse
import logging
from django.views.decorators.csrf import csrf_exempt
from . forms import BookForm,AuthorForm
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from . serializers import BooksSerializer
# Create your views here.

logger = logging.getLogger(__name__)

##return all books in the db

class BooksView(APIView):
    permission_classes = []
    @csrf_exempt
    def get(self, request):
        books = Books.objects.all()
        serializer = BooksSerializer(books, many=True)
        return Response(serializer.data)

    

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
            return redirect('http://127.0.0.1:8001/gateway/home/')
    else:
        form =BookForm()
    return render(request, 'book_form.html',{'form':form})

def book_update(request, pk):
    book = Books.objects.get(pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('http://127.0.0.1:8001/gateway/home/')
    else:
        form = BookForm(instance=book)
    return render(request, 'book_form.html', {'form': form})

def book_delete(request, pk):
    book = Books.objects.get(pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('http://127.0.0.1:8001/gateway/home/')
    return render(request, 'book_delete.html', {'book': book})