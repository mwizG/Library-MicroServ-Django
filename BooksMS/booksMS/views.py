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

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Books
from .serializers import BooksSerializer
from .forms import BookForm


class BooksView(APIView):
    permission_classes = []

    @csrf_exempt
    def get(self, request):
        # Retrieve all books from the database
        books = Books.objects.all()
        # Serialize the queryset of books
        serializer = BooksSerializer(books, many=True)
        # Return serialized data as JSON response
        return Response(serializer.data)


# Search for books in the database
@csrf_exempt
def query_books(request):
    if 'query' in request.GET and request.GET["query"]:
        search_term = request.GET.get("query")
        # Perform case-insensitive search for books by title
        searched_books = Books.objects.filter(title__icontains=search_term)
        # Render 'books.html' template with matched books
        return render(request, 'books.html', {'books': searched_books})
    else:
        # Return a plain HTTP response if no search query provided
        return HttpResponse("No books found matching %s", search_term)


@csrf_exempt
def book_details(request, pk):
    # Retrieve a specific book by primary key or return 404 error
    book = get_object_or_404(Books, pk=pk)
    # Determine if user_id is provided via POST or GET request
    user_id = request.POST.get('user_id') if request.method == 'POST' else request.GET.get('user_id')
    print("User ID from form:", user_id)
    print("Displaying the form for return date")
    
    # Prepare book data for JSON response
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
        # Initialize an empty BookForm for GET requests
        form = BookForm()
        return JsonResponse({'form': form.as_p()}, status=200)

    if request.method == 'POST':
        print("we are saving")
        # Retrieve user_id from POST data
        user_id = request.POST.get('user_id')
        print("for book create user_id:", user_id)
        # Bind BookForm with POST data
        form = BookForm(request.POST)
        if form.is_valid():
            # Save valid form data to create a new book
            form.save()
            return JsonResponse({"message": "Book saved successfully"}, status=200)
        else:
            # Return form errors if form is invalid
            return JsonResponse({'form': form.as_p(), 'errors': form.errors.as_json()}, status=400)

    else:
        # Handle unsupported HTTP methods with an empty BookForm
        form = BookForm()
        return JsonResponse({'form': form.as_p()}, status=200)


def book_update(request, pk):
    # Retrieve a specific book by primary key or return 404 error
    book = get_object_or_404(Books, pk=pk)
    if request.method == 'POST':
        # Bind BookForm with POST data and instance of the book to update
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            # Save valid form data to update the existing book
            form.save()
            # Redirect to home page after successful update (needs revision)
            return redirect('http://apigateway:8001/gateway/home/')  # needs to be updated to only send a response
    else:
        # Initialize BookForm with instance of the book for GET requests
        form = BookForm(instance=book)
    # Render 'book_form.html' template with the form for updating the book
    return JsonResponse('book_form.html', {'form': form.as_p()}, status=200)


@csrf_exempt
def book_delete(request, pk):
    # Handle only POST requests for book deletion
    if request.method == 'POST':
        # Retrieve user_id from POST data
        user_id = request.POST.get('user_id')
        # Retrieve a specific book by primary key or return 404 error
        book = get_object_or_404(Books, pk=pk)
        print("book id:", book)
        
        # Delete the specified book from the database
        book.delete()
        
        # Return a success response after successful deletion
        return JsonResponse({'message': 'Book deleted successfully'})
    
    # Return an error response for non-POST requests
    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
