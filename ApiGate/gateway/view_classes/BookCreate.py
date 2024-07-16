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

class BookCreate(APIView):
    def get(self, request):
        book_create_url = 'http://bookms:8000/new/'  # URL to fetch the book creation form
        user_id = request.GET.get('user_id')  # Retrieve the user_id from the GET parameters

        if not user_id:  # Check if user_id is not provided
            return JsonResponse({'error': 'Missing user_id'}, status=400)  # Return error if user_id is missing
        
        response = requests.get(book_create_url)  # Make a GET request to fetch the form
        response.raise_for_status()  # Raise an HTTPError if the request returned an unsuccessful status code
        
        form_html = response.json().get('form')  # Extract the form HTML from the JSON response
        
        return render(request, 'book_form.html', {'form_html': form_html, 'user_id': user_id})  # Render the form HTML along with the user_id

    def post(self, request):
        book_create_url = 'http://bookms:8000/new/'  # URL to post the book creation data
        user_id = request.POST.get('user_id')  # Retrieve the user_id from the POST data
        print('userssss:', user_id)  # Print the user_id for debugging purposes

        if not user_id:  # Check if user_id is not provided
            return JsonResponse({'error': 'Missing user_id'}, status=400)  # Return error if user_id is missing
        
        data = request.POST.copy()  # Copy the POST data to modify it
        response = requests.post(book_create_url, data=data)  # Make a POST request to create the book with the form data
        response.raise_for_status()  # Raise an HTTPError if the request returned an unsuccessful status code

        if response.status_code == 200:  # Check if the book was created successfully (HTTP 200)
            #getting the docker compose exported server IP
            server_ip = os.environ.get('SERVER_IP')
            redirect_url = f'http://{server_ip}:8001/gateway/home/'
            return redirect(redirect_url)  # Redirect to the home page upon successful creation
        else:  # Handle unexpected status codes
            return JsonResponse({'error': 'Unexpected status code', 'status_code': response.status_code}, status=500)  # Return error if the status code is not 200
    