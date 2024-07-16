from functools import wraps
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.views import APIView
import jwt
import requests
import logging
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
logger = logging.getLogger(__name__)
import os

# URL of the Users Microservice
USERS_MS_URL = 'http://usersms:8002/users/'

# URL of the Books Microservice
BOOKS_MS_URL = 'http://bookms:8000/books/'

class HomeView(APIView):
    print('IM RUNNING')  # Debugging print statement to indicate class initialization

    def get(self, request):
        # Get user_info from session data
        user_info = request.session.get('user_info')
        print('here boy:', user_info)  # Debugging print statement
        
        if user_info:
            # Make GET request to fetch books from book microservice
            response = requests.get('http://bookms:8000/books/')
            # Get server IP address from environment variables
            server_ip = os.environ.get('SERVER_IP')
            # Parse books from JSON response
            books = response.json()
            # Render 'home.html' template with books, user_info, and server_ip
            return render(request, 'home.html', {'books': books, 'user_info': user_info, 'SERVER_IP': server_ip})
        else:
            # Return error response if no user_info found in session
            return JsonResponse({'error': 'No user info'}, status=402)


class MyBooksView(APIView):
    def post(self, request):
        # Get user_id from request data
        user_id = request.data.get('user_id')
        print('IM RUNNING my books')  # Debugging print statement
        print('User ID:', user_id)  # Debugging print statement
        
        if user_id:
            try:
                # Make POST request to loans microservice to fetch user's books
                response = requests.post('http://loansms:8003/loans/mybookapi/', data={'user_id': user_id})
                print(f"Response status code:", response)  # Debugging print statement
                
                if response.status_code == 200:
                    try:
                        # Parse books from JSON response
                        books = response.json()
                        print("The books: ", books)  # Debugging print statement
                        # Get server IP address from environment variables
                        server_ip = os.environ.get('SERVER_IP')
                        # Render 'mybooks.html' template with books, user_id, and server_ip
                        return render(request, 'mybooks.html', {'books': books, 'user_id': user_id, 'SERVER_IP': server_ip})
                    except ValueError:
                        # Return error response if JSON parsing fails
                        return JsonResponse({'error': 'Invalid JSON response'}, status=500)
                else:
                    # Return error response if failed to fetch books
                    return JsonResponse({'error': 'Failed to fetch books from the API'}, status=response.status_code)
            except requests.RequestException as e:
                # Return error response if request to loans microservice fails
                print(f'Error fetching books: {e}')  # Debugging print statement
                return JsonResponse({'error': 'Failed to fetch books from the API'}, status=500)
        else:
            # Return error response if no user_id provided
            return JsonResponse({'error': 'No user info'}, status=402)


class BorrowAndDateSendView(APIView):
    def borrow_book(self, request):
        # Get user_id, book_id, and book_title from request data
        user_id = request.data.get('user_id')
        book_id = request.data.get('book_id')
        book_title = request.data.get('book_title')  # Receive book title from request data
        
        # Send borrow request to loans microservice
        borrow_data = {'user_id': user_id, 'book_id': book_id, 'book_title': book_title}  # Include book_title in borrow data
        response = requests.post('http://loansms:8003/loans/borrow/', data=borrow_data)
        
        if response.status_code == 200:
            # Get server IP address from environment variables
            server_ip = os.environ.get('SERVER_IP')
            # Parse form HTML from JSON response
            form_html = response.json().get('form')
            # Render 'borrow.html' template with form HTML, user_id, book_id, book_title, and server_ip
            return render(request, 'borrow.html', {
                'form': form_html,
                'user_id': user_id,
                'book_id': book_id,
                'book_title': book_title,
                'SERVER_IP': server_ip,
            })
        else:
            # Return error response if failed to borrow the book
            return JsonResponse({'error': 'Failed to borrow the book.'}, status=response.status_code)

    def send_date(self, request):
        # Get return_date, user_id, book_id, and book_title from request data
        return_date = request.data.get('return_date')
        user_id = request.data.get('user_id')
        book_id = request.data.get('book_id')
        book_title = request.data.get('book_title')  # Receive book title from request data
        
        if not return_date:
            # Return error response if return_date is missing
            return JsonResponse({'error': 'Missing date'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Send request to loans microservice to create loan with return_date and book_title
        loan_data = {
            'user_id': user_id,
            'book_id': book_id,
            'return_date': return_date,
            'book_title': book_title  # Include book title in loan creation data
        }
        response = requests.post('http://loansms:8003/loans/create/', data=loan_data)
        
        if response.status_code == 201:
            # Return success message if loan creation was successful
            return JsonResponse({'message': 'Book return date set successfully.'}, status=status.HTTP_201_CREATED)
        else:
            # Return error response if failed to set return date
            return JsonResponse({'error': 'Failed to set return date.'}, status=response.status_code)

    def post(self, request):
        # Check if 'return_date' exists in request data to determine action
        if 'return_date' in request.data:
            return self.send_date(request)
        else:
            return self.borrow_book(request)
