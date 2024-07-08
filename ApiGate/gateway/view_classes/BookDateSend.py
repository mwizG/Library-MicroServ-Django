
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


class BookDateSend(APIView):
    def post(self, request):
        return_date=request.POST.get('return_date')
        user_id=request.POST.get('user_id')
        book_id=request.POST.get('book_id')
        home = 'http://44.223.18.17:8001/gateway/home/'
        print("daatteee",return_date)
        if not return_date:
            return JsonResponse({'error':'missing date'})
        response = requests.post('http://44.223.18.17:8003/loans/create/', data={'user_id': user_id, 'book_id': book_id,'return_date':return_date})
        if response.status_code == 201:
            return redirect(home)
        else:
            return JsonResponse({'error': 'Failed to borrow the book.'}, status=response.status_code)
