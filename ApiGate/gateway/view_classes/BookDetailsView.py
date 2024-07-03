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


class BookDetailView(APIView):
    def post(self, request, pk):
        user_info = request.data.get('user_id')
        
        book_id = pk  # Use the pk from the URL as the book_id
        book_details_url = f'http://127.0.0.1:8000/details/{book_id}'
        print('user id:', user_info)
        
        if user_info:
            response=requests.post(book_details_url, data={'user_id': user_info})
            print(f"Response status code: {response.status_code}")
            print(f"Response content: {response.content}")
            
            if response.status_code == 200:
                try:
                    books = response.json()
                    print("response: ", books)
                    return render(request, 'book_details.html', {'books': books, 'user_info': {'id': user_info}})
                except ValueError:
                    return JsonResponse({'error': 'Invalid JSON response'}, status=500)
            else:
                return JsonResponse({'error': 'Failed to fetch book details'}, status=response.status_code)
        else:
            return JsonResponse({'error': 'No user info'}, status=402)