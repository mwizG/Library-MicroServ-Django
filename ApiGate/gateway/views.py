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

# URL of the Users Microservice
USERS_MS_URL = 'http://usersms:8002/users/'

# URL of the Books Microservice
BOOKS_MS_URL = 'http://bookms:8000/books/'



class HomeView(APIView):
    print('IM RUNNING')
    def get(self,request):
        user_info=request.session.get('user_info')
        print('here boy:',user_info)
        if user_info:
           response = requests.get('http://bookms:8000/books/')
           server_ip = os.environ.get('SERVER_IP')
           books = response.json()
           return render(request, 'home.html', {'books': books,'user_info': user_info,'SERVER_IP': server_ip})     
        else:
             return JsonResponse({'error': 'No user info'}, status=402)
      
class BorrowAndDateSendView(APIView):
    def post(self, request):
        if 'return_date' in request.data:
            # This is the send date action
            return self.send_date(request)
        else:
            # This is the borrow book action
            return self.borrow_book(request)
    
    def borrow_book(self, request):
        user_id = request.data.get('user_id')
        print("user_idsss", user_id)
        book_id = request.data.get('book_id')
        print("book_idsss", book_id)
        
        response = requests.post('http://loansms:8003/loans/borrow/', data={'user_id': user_id, 'book_id': book_id})
        print('we are back here to allow send render borrow.html')
        
        if response.status_code == 200:
            server_ip = os.environ.get('SERVER_IP')
            form_html = response.json().get('form')
            return render(request, 'borrow.html', {
                'form': form_html,
                'user_id': user_id,
                'book_id': book_id,
                'SERVER_IP': server_ip,
            })
        else:
            return JsonResponse({'error': 'Failed to borrow the book.'}, status=response.status_code)

    def send_date(self, request):
        print('send date code running')
        return_date = request.POST.get('return_date')
        user_id = request.POST.get('user_id')
        book_id = request.POST.get('book_id')
        
        server_ip = os.environ.get('SERVER_IP')
        home = f'http://{server_ip}:8001/gateway/home/'

        print("daatteee", return_date)
        if not return_date:
            return JsonResponse({'error': 'missing date'})
        
        response = requests.post('http://loansms:8003/loans/create/', data={'user_id': user_id, 'book_id': book_id, 'return_date': return_date})
        
        if response.status_code == 201:
            return redirect(home)
        else:
            return JsonResponse({'error': 'Failed to borrow the book.'}, status=response.status_code)

class BooksView(APIView):
    def dummy(self,requests):
    
       return render(requests,f"{BOOKS_MS_URL}")
    
    