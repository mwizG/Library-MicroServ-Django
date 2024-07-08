from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm
import requests
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt


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
           # else:
                #response = requests.get('http://127.0.0.1:8000/books/')
               # books = response.json()
               # return render(request, 'books.html', {'books': books,'user_info': user_info})  
            else:
                return JsonResponse({'error': 'No user id'}, status=402)
        else:
            return JsonResponse({'error': 'Failed to login user'}, status=response.status_code)