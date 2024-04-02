from functools import wraps
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.views import APIView
import jwt
import requests
import logging
# URL of the Users Microservice
USERS_MS_URL = 'http://127.0.0.1:8001/users/login/'

# URL of the Books Microservice
BOOKS_MS_URL = 'http://127.0.0.1:8002/books/'


# Custom decorator for token extraction and validation
def authenticate_request(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
       
        # Extract token from the Authorization header
        token = request.headers.get('Authorization', '').split(' ')[1]
        # Decode the token
        decoded_token = decode_jwt(token, 'My_Secret113')
        if decoded_token:
            # Add the decoded token to the request object for easy access in the view
            request.decoded_token = decoded_token
            # Call the view function
            return view_func(request, *args, **kwargs)
        else:
            # Return error response for invalid or expired token
            return JsonResponse({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
    return wrapped_view

# Function to decode JWT token
def decode_jwt(token, secret_key):
    

    try:
        decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])
        return decoded_token
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

class AuthView(APIView):
    allowed_methods = ['GET', 'POST']  
    
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
       
       return super().dispatch(*args, **kwargs)

    def get(self, request):
        # Redirect the user to the Users Microservice login page
        return redirect(USERS_MS_URL)

    def post(self, request):
        # Extract the tokens from the response data sent by the Users Microservice
        response_data = request.data
        refresh_token = response_data.get('refresh_token')
        access_token = response_data.get('access_token')

        # Assuming the response contains both refresh_token and access_token
        if refresh_token and access_token:
            # Use the tokens for further authentication and authorization
            # For now, we'll just return a success message
            return JsonResponse({'message': 'Tokens received successfully'}, status=status.HTTP_200_OK)
        else:
            # Handle the case where tokens are not present in the response
            return JsonResponse({'error': 'Tokens not received'}, status=status.HTTP_400_BAD_REQUEST)

class BooksView(APIView):
    @method_decorator(authenticate_request)
    def get(self, request):
        # Use request.decoded_token to access the decoded token
        response = requests.get(f'{BOOKS_MS_URL}')
        if response.status_code == 200:
            return JsonResponse(response.json(), status=status.HTTP_200_OK)
        else:
            return JsonResponse({'error': 'Failed to retrieve books'}, status=response.status_code)

    @method_decorator(authenticate_request)
    def post(self, request):
        # Extract the search term from the request data
        search_term = request.data.get("query")
        # Forward the request to the Books Microservice to search for books
        response = requests.post(f'{BOOKS_MS_URL}', data={'query': search_term})
        print(response,"here")
        if response.status_code == 200:
            # Return the list of searched books to the client
            return JsonResponse(response.json(), status=status.HTTP_200_OK)
        else:
            # Return an error message to the client
            return JsonResponse({'error': 'Failed to search for books'}, status=response.status_code)
