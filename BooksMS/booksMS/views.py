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
from django.shortcuts import render, get_object_or_404
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
    
@csrf_exempt    
def book_details(request, pk):
    book = get_object_or_404(Books, pk=pk)
    user_id = request.POST.get('user_id') if request.method == 'POST' else request.GET.get('user_id')
    print("User ID from form:", user_id)
    print("Displaying the form for return date")
    
    book_data = {
        'id': book.id,
        'title': book.title,
        'author': book.author_name if book.author else 'Unknown Author',
        'published_date': book.pub_year,
        'coverimg': book.coverimg,
        'rating': book.rating,
        'genre': book.genre,
    }
    
    return JsonResponse({'book': book_data}, status=200)


@csrf_exempt
def book_create(request):
    if request.method == 'GET':
        form = BookForm()
        return JsonResponse({'form': form.as_p()}, status=200)

    if request.method == 'POST':
        print("we are saving")
        user_id = request.POST.get('user_id')
        print("for book cre user_id:", user_id)
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"message": "Book saved successfully"}, status=200)
        else:
            return JsonResponse({'form': form.as_p(), 'errors': form.errors.as_json()}, status=400)

    else:
        form = BookForm()
        return JsonResponse({'form': form.as_p()}, status=200)
    
def book_update(request, pk):
    book = get_object_or_404(Books, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('http://127.0.0.1:8001/gateway/home/')
    else:
        form = BookForm(instance=book)
    return JsonResponse('book_form.html',{'form':form.as_p()}, status=200)

@csrf_exempt
def book_delete(request, pk):
    # Only handle POST requests
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        book = get_object_or_404(Books, pk=pk)
        print("book id:", book)
        
        # Delete the book
        book.delete()
        
        # Return a success response
        return JsonResponse({'message': 'Book deleted successfully'})
    
    # Return an error response for non-POST requests
    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)