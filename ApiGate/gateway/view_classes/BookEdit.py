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


class BookEdit(APIView):
    def get(self,request,pk):
        user_id = request.data.get('user_id')
        book_id = request.data.get('book_id')
        book_details_url = 'http://44.223.18.17:8000/{}/edit/'.format(book_id)
        print('book_id:',book_id)
        if user_id:
           response = requests.get(book_details_url)
           books = response.json().get('form')
           return render(request, 'book_form.html', {'books': books,'book_id': book_id})     
        else:
             return JsonResponse({'error': 'No user info'}, status=402)
  