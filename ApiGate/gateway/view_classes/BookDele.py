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

class BookDele(APIView):
    def get(self, request, pk):
        # Get user_id from query parameters
        user_id = request.GET.get('user_id')
        # Construct URL to fetch book details from book microservice
        book_details_url = f'http://bookms:8000/details/{pk}'
        
        # Make GET request to fetch book details
        response = requests.get(book_details_url)
        if response.status_code == 200:
            # Parse book details from JSON response
            book = response.json()
            # Render 'book_delete.html' template with book details and user_id
            return render(request, 'book_delete.html', {'book': book['book'], 'user_id': user_id})
        else:
            # Return error response if failed to fetch book details
            return JsonResponse({'error': 'Failed to fetch book details'}, status=response.status_code)

    def post(self, request, pk):
        # Get user_id from POST data
        user_id = request.POST.get('user_id')
        # Construct URL to delete book using book microservice
        book_dele_url = f'http://bookms:8000/book/{pk}/delete/'
        print('book_id:', pk, 'user_id:', user_id)
        
        if user_id:
            # Make POST request to delete book with user_id
            response = requests.post(book_dele_url, data={'user_id': user_id})
            if response.status_code == 200:
                # Get server IP address from environment variables
                server_ip = os.environ.get('SERVER_IP')
                # Construct redirect URL after successful deletion
                redirect_url = f'http://{server_ip}:8001/gateway/home/'
                return redirect(redirect_url)
                # Return a success message if preferred
                # return JsonResponse({'message': 'Book deleted successfully'})
            else:
                # Return error response if failed to delete book
                return JsonResponse({'error': 'Failed to delete book'}, status=response.status_code)
        else:
            # Return error response if no user_id provided
            return JsonResponse({'error': 'No user info'}, status=402)
