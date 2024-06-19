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

class BookEdit(APIView):
    def get(self,request,pk):
        user_id = request.data.get('user_id')
        book_id = request.data.get('book_id')
        book_details_url = 'http://127.0.0.1:8000/{}/edit/'.format(book_id)
        print('book_id:',book_id)
        if user_id:
           response = requests.get(book_details_url)
           books = response.json().get('form')
           return render(request, 'book_form.html', {'books': books,'book_id': book_id})     
        else:
             return JsonResponse({'error': 'No user info'}, status=402)
        
class BookCreate(APIView):
    print('we are running')
    def get(self,request):
        user_id = request.data.get('user_id')
        book_create_url = 'http://127.0.0.1:8000/new/'
        print('here boy:',user_id)
        if user_id:
           response = requests.get(book_create_url)
           #books = response.json().get('form')
           return render(request, 'book_form.html', {'form': response.json().get('form'),'user_info': user_id})     
        else:
             return JsonResponse({'error': 'No user info'}, status=402)

class BorrowView(APIView):
    def post(self,request):  
        #extract userinfo
        user_id = request.data.get('user_id')
        book_id = request.data.get('book_id')
         # Send borrow details to the borrow_book function
        response = requests.post('http://127.0.0.1:8003/loans/borrow/', data={'user_id': user_id, 'book_id': book_id})   
        
        #rendering the borrow form which is just the dates
        if response.status_code == 200:
            print("success")
            return render(request, 'borrow.html', {
                'form': response.json().get('form'),
                'user_id': user_id,
                'book_id': book_id
            })
        else:
            return JsonResponse({'error': 'Failed to borrow the book.'}, status=response.status_code)

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
    