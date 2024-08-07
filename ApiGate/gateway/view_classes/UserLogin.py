
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
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
import os
# userlogin_gateway.py


def decode_jwt(token):
    try:
        # Decode the JWT token
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        return decoded_token
    except jwt.ExpiredSignatureError:
        print("Token has expired")
        return None
    except jwt.InvalidTokenError:
        print("Invalid token")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

class UserLogin(APIView):
    """
    Endpoint for user login
    """
    def get(self, request):
        """
        Render the login form.
        """
        form = AuthenticationForm()
        server_ip = os.environ.get('SERVER_IP')
        return render(request, 'login.html', {'form': form, 'SERVER_IP': server_ip})

        

    @csrf_exempt
    def post(self, request):
        # Extract username and password from the request data
        username = request.data.get('username')
        password = request.data.get('password')

        # Send login details to usersms API for authentication
        auth_response = requests.post('http://usersms:8002/users/login/', data={'username': username, 'password': password})

        if auth_response.status_code == 200:
            auth_data = auth_response.json()
            access_token = auth_data.get('access_token')
            user_id = auth_data.get('user_id')
            print('access: ',access_token)
            if access_token and user_id:
                # Decode the token
                decoded_token = decode_jwt(access_token)
                print('decoded token: ',decoded_token)
                if decoded_token:
                    # Retrieve user info from Auth API using the user_id
                    user_info_response = requests.get(f'http://usersms:8002/users/users/{user_id}')
                    if user_info_response.status_code == 200:
                        user_info = user_info_response.json()
                        print('user data HERE: ', user_info)
                        # Store user_info in session or use it as needed
                        request.session['user_info'] = user_info
                        print("requeSSST: ",request)
                        server_ip = os.environ.get('SERVER_IP')
                        print("server ip: ",server_ip)
                        redirect_url = f'http://{server_ip}:8001/gateway/home/'
                        print('Redirect URL: ', redirect_url)
                        return redirect(redirect_url)
                    else:
                        return JsonResponse({'error': 'Failed to fetch user info'}, status=401)
                else:
                    return JsonResponse({'error': 'Invalid token'}, status=401)
            else:
                return JsonResponse({'error': 'Failed to login user'}, status=401)
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=auth_response.status_code)
