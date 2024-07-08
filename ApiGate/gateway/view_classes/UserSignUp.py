from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm
import requests
from rest_framework.views import APIView


class UserSignUp(APIView):
    """
    Endpoint for user signup.
    """
    permission_classes = []

    def get(self, request):
        """
        Render sign up form
        """
        form = AuthenticationForm()
        return render(request, 'signup.html', {'form': form})
    
    def post(self, request):
        # Extract username and password from the request data
        username = request.data.get('username')
        password = request.data.get('password')
        # Send signup details to Users Microservice for registration
        response = requests.post('http://127.0.0.1:8002/users/signup/', data={'username': username, 'password': password})
        # Return the response from Users Microservice
        if response.status_code == 200:
            return redirect('http://127.0.0.1:8001/gateway/login/')
        else:
            return JsonResponse({'error': 'Failed to signup user'}, status=response.status_code)

