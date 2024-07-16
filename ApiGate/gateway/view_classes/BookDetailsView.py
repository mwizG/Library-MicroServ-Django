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

class BookDetailView(APIView):
    def post(self, request, pk):
        # Get user_id from request data
        user_info = request.data.get('user_id')
        
        # Use the pk from the URL as the book_id
        book_id = pk
        # Construct URL to fetch book details from book microservice
        book_details_url = f'http://bookms:8000/details/{book_id}'
        print('user id:', user_info)
        
        if user_info:
            # Make POST request to fetch book details with user_id
            response = requests.post(book_details_url, data={'user_id': user_info})
            print(f"Response status code: {response.status_code}")
            print(f"Response content: {response.content}")
            
            if response.status_code == 200:
                try:
                    # Parse book details from JSON response
                    books = response.json()
                    print("response: ", books)
                    # Get server IP address from environment variables
                    server_ip = os.environ.get('SERVER_IP')
                    # Render 'book_details.html' template with book details and user_info
                    return render(request, 'book_details.html', {'books': books, 'user_info': {'id': user_info}, 'SERVER_IP': server_ip})
                except ValueError:
                    # Return error response if JSON parsing fails
                    return JsonResponse({'error': 'Invalid JSON response'}, status=500)
            else:
                # Return error response if failed to fetch book details
                return JsonResponse({'error': 'Failed to fetch book details'}, status=response.status_code)
        else:
            # Return error response if no user_id provided
            return JsonResponse({'error': 'No user info'}, status=402)
