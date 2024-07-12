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

# URL of the Users Microservice
USERS_MS_URL = 'http://127.0.0.1:8002/users/'

# URL of the Books Microservice
BOOKS_MS_URL = 'http://127.0.0.1:8000/books/'



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
      
class BorrowView(APIView):
    def post(self, request):  
        user_id = request.data.get('user_id')
        print("user_idsss",user_id)
        book_id = request.data.get('book_id')
        print("book_idsss",book_id)
        

        response = requests.post('http://127.0.0.1:8003/loans/borrow/', data={'user_id': user_id, 'book_id': book_id})   

        if response.status_code == 200:
            form_html = response.json().get('form')
            return render(request, 'borrow.html', {
                'form': form_html,
                'user_id': user_id,
                'book_id': book_id
            })
        
        else:
            return JsonResponse({'error': 'Failed to borrow the book.'}, status=response.status_code)

class BooksView(APIView):
    def dummy(self,requests):
    
       return render(requests,f"{BOOKS_MS_URL}")
    

