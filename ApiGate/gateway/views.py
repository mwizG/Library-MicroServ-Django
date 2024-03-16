from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import requests

# URL of the Users Microservice
USERS_MS_URL = 'http://127.0.0.1:8002/users/login/'

# URL of the Books Microservice
BOOKS_MS_URL = 'http://127.0.0.1:8001/books/'
# API Gateway view for user authentication

class AuthView(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        # Redirect the user to the Users Microservice login page
        return redirect(USERS_MS_URL)

    def post(self, request):
        # Assuming the Users Microservice returns a token upon successful login
        # Check if the token is present in the request
        token = request.data.get('token')
        if token:
            # Redirect to the Books Microservice with the token
            return redirect(f'{BOOKS_MS_URL}?token={token}')
        else:
            # Handle authentication failure
            return JsonResponse({'error': 'Authentication failed'}, status=status.HTTP_401_UNAUTHORIZED)
# api_gateway/views.py

class BooksView(APIView):
    def get(self, request):
        # Forward the request to the Books Microservice to retrieve all books
        response = requests.get(f'{BOOKS_MS_URL}/books')

        # Check if the request was successful
        if response.status_code == 200:
            # Return the list of books to the client
            return JsonResponse(response.json(), status=status.HTTP_200_OK)
        else:
            # Return the error message to the client
            return JsonResponse({'error': 'Failed to retrieve books'}, status=response.status_code)

    def post(self, request):
        # Forward the request to the Books Microservice to search for books
        search_term = request.data.get("query")
        response = requests.post(f'{BOOKS_MS_URL}/books/query', data={'query': search_term})

        # Check if the request was successful
        if response.status_code == 200:
            # Return the list of searched books to the client
            return JsonResponse(response.json(), status=status.HTTP_200_OK)
        else:
            # Return the error message to the client
            return JsonResponse({'error': 'Failed to search for books'}, status=response.status_code)
