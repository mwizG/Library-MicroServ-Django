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
            accesstoken=response.json()['access_token']
            print('here acc: ',accesstoken)
            user_id=response.json()['user_id']
            print("user id in gate:",user_id)
            if user_id:
                # Implement your authorization logic here, e.g., check user permissions
                # For now, just return a success message
                user_info_url= f'http://127.0.0.1:8002/users/users/{user_id}'
                user_info_response = requests.get(user_info_url)
                if user_info_response.status_code == 200:
                    user_info = user_info_response.json()
                    # Store user_info in session
                    request.session['user_info'] = user_info
                    return redirect('http://127.0.0.1:8001/gateway/home/')

                else:
                    return JsonResponse({'error': 'Failed to fetch user info'}, status=401)
           
            else:
                return JsonResponse({'error': 'No user id'}, status=402)
        else:
            return JsonResponse({'error': 'Failed to login user'}, status=response.status_code)
class HomeView(APIView):
    def get(self,request):
        user_info=request.session.get('user_info')
        print('here boy:',user_info)
        if user_info:
           response = requests.get('http://127.0.0.1:8000/books/')
           books = response.json()
           return render(request, 'home.html', {'books': books,'user_info': user_info})     
        else:
             return JsonResponse({'error': 'No user info'}, status=402)
    
        
    

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
    def dummy(self,requests):
    
       return render(requests,f"{BOOKS_MS_URL}")
    