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

class BookEdit(APIView):
    def get(self, request, pk):
        # Get user_id from request data (not used in this method)
        user_id = request.data.get('user_id')
        # Get book_id from request data
        book_id = request.data.get('book_id')
        # Construct URL to fetch book edit form from book microservice
        book_details_url = 'http://bookms:8000/{}/edit/'.format(book_id)
        print('book_id:', book_id)
        
        if user_id:
            # Get server IP address from environment variables
            server_ip = os.environ.get('SERVER_IP')
            # Make GET request to fetch book edit form
            response = requests.get(book_details_url)
            # Extract form data from JSON response
            books = response.json().get('form')
            # Render 'book_form.html' template with form data, book_id, and server_ip
            return render(request, 'book_form.html', {'books': books, 'book_id': book_id, 'SERVER_IP': server_ip})
        else:
            # Return error response if no user_id provided
            return JsonResponse({'error': 'No user info'}, status=402)
