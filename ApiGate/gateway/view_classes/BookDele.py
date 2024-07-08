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


class BookDele(APIView):
    def get(self, request, pk):
        user_id = request.GET.get('user_id')
        book_details_url = f'http://127.0.0.1:8000/details/{pk}'
        
        response = requests.get(book_details_url)
        if response.status_code == 200:
            book = response.json()
            return render(request, 'book_delete.html', {'book': book['book'], 'user_id': user_id})
        else:
            return JsonResponse({'error': 'Failed to fetch book details'}, status=response.status_code)

    def post(self, request, pk):
        user_id = request.POST.get('user_id')
        book_dele_url = f'http://127.0.0.1:8000/book/{pk}/delete/'
        print('book_id:', pk, 'user_id:', user_id)
        
        if user_id:
            response = requests.post(book_dele_url, data={'user_id': user_id})
            if response.status_code == 200:
                return redirect('http://127.0.0.1:8001/gateway/home/')
                #return JsonResponse({'message': 'Book deleted successfully'})
            else:
                return JsonResponse({'error': 'Failed to delete book'}, status=response.status_code)
        else:
            return JsonResponse({'error': 'No user info'}, status=402)
