from functools import wraps
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
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

# URL of the Users Microservice
USERS_MS_URL = 'http://127.0.0.1:8002/users/'

# URL of the Books Microservice
BOOKS_MS_URL = 'http://127.0.0.1:8000/books/'

# Function to decode JWT token
def decode_jwt(token):
    try:
        decoded_token = jwt.decode(token, None, None)
        return decoded_token
    except jwt.ExpiredSignatureError:
        print(1)
        return None
    except jwt.InvalidTokenError:
        return None
    except Exception as e:
        return None

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

class UserSignUp(APIView):
    """
    Endpoint for user signup.
    """
    permission_classes = []

    def get(self, request):
        """
        Render sign up form
        """
        form = AuthenticationForm()
        return render(request, 'signup.html', {'form': form})
    
    def post(self, request):
        # Extract username and password from the request data
        username = request.data.get('username')
        password = request.data.get('password')
        # Send signup details to Users Microservice for registration
        response = requests.post('http://127.0.0.1:8002/users/signup/', data={'username': username, 'password': password})
        # Return the response from Users Microservice
        if response.status_code == 200:
            return redirect('http://127.0.0.1:8001/gateway/login/')
        else:
            return JsonResponse({'error': 'Failed to signup user'}, status=response.status_code)

class UserLogin(APIView):
    """
    Endpoint for user login
    """
    def get(self, request):
        """
        Render the login form.
        """
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})
    @csrf_exempt
    def post(self, request):
        # Extract username and password from the request data
        username = request.data.get('username')
        password = request.data.get('password')
        # Send login details to Users Microservice for authentication
        response = requests.post('http://127.0.0.1:8002/users/login/', data={'username': username, 'password': password})
        # Return the response from Users Microservice
        if response.status_code == 200:
            return JsonResponse(response.json(), status=status.HTTP_200_OK)
        else:
            return JsonResponse({'error': 'Failed to login user'}, status=response.status_code)

class AuthView(APIView):
    allowed_methods = ['GET', 'POST']

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    @csrf_exempt
    def post(self, request):
        # Extract the token from the request headers
        authorization_header = request.headers.get('Authorization')
        print("Authorization: {}\n".format(authorization_header))
        if authorization_header:
            token = authorization_header.split(' ')[1]
            # Decode the token
            decoded_token = decode_jwt(token)
            print(decoded_token)
            if decoded_token:
                # Check if the token contains necessary information for authorization
                user_id = decoded_token.get('user_id')
                if user_id:
                    # Implement your authorization logic here, e.g., check user permissions
                    # For now, just return a success message
                    
                    return JsonResponse({'user_id': f'{user_id}'}, status=status.HTTP_200_OK)
                else:
                    return JsonResponse({'error': 'Invalid token format'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                # Return error response for invalid or expired token
                return JsonResponse({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            # Return error response for missing Authorization header
            return JsonResponse({'error': 'Authorization header missing'}, status=status.HTTP_401_UNAUTHORIZED)


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
        if response.status_code == 200:
            # Return the list of searched books to the client
            return JsonResponse(response.json(), status=status.HTTP_200_OK)
        else:
            # Return an error message to the client
            return JsonResponse({'error': 'Failed to search for books'}, status=response.status_code)
