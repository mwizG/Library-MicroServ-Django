from django.http import Http404, HttpResponseRedirect
import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.hashers import make_password  # Import make_password to hash passwords
from .models import CustomUser  # Import CustomUser model
from .serializers import CustomUserSerializer  # Import CustomUserSerializer
import logging

from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView, TokenBlacklistView


logger = logging.getLogger(__name__)

"""
# Custom authentication token view to generate tokens automatically upon user login.
class CustomAuthToken(ObtainJSONWebToken):
    permission_classes =[]
    def post(self,request, *args, **kwargs):
         # Call the parent class method to generate the token
        response = super(CustomAuthToken, self).post(request, *args, **kwargs)
        return response        
"""     

# Endpoint for user signup.
class UserSignUp(TokenObtainPairView):
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

    # POST request for user signup
    def post(self, request):
        # Extract username and password from the request data
        username = request.data.get('username')
        password = request.data.get('password')
        # Check if the user already exists
        exists = CustomUser.objects.filter(username=username).exists()
        if(exists):
            # Return an error response if the user already exists
            return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Hash the password
            hashed_password = make_password(password)
            # Create a new user with the hashed password
            user = CustomUser.objects.create(username=username, password=hashed_password)
            try:
                # Generate tokens for the new user
                refresh = RefreshToken.for_user(user)
                # Return the tokens in the response
                return Response({
                    'refresh_token': str(refresh),
                    'access_token': str(refresh.access_token),
                })
            except Exception as e:
                # Return an error response if token generation fails
                return Response({'error': e})

# Endpoint for user login.
class UserLogin(TokenObtainPairView):
    """
    Endpoint for user login
    """
    def get(self, request):
        """
        Render the login form.
        """
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

    # POST request for user login
    def post(self, request):
        """
        Handle login in request
        """
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            response = requests.post('http://127.0.0.1:8001/gateway/books/', data={
                'refresh_token': str(refresh),
                'access_token': str(refresh.access_token),
            })
            if response.status_code == 200:
                # Redirect to the Books Microservice
                return HttpResponseRedirect('http://books-ms-url/books/')
            else:
                return Response({'error': 'Failed to authenticate with API Gateway'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
#work in progress
class UserLogout(TokenBlacklistView):
    """
    Endpoint for logging out
    """
    def get(self, request):
        
        return

# Endpoint for listing users (admin-only).
class UserList(APIView):
    """
    Endpoint for listing users (admin-only).
    """
    
    permission_classes = [IsAdminUser]
    
    # GET request for listing users
    def get(self, request):
        # Retrieve all user objects from the database
        users = CustomUser.objects.all()
        # Serialize user objects
        serializer = CustomUserSerializer(users, many=True)
        #context = list(users.values())
        return Response(serializer.data)

# Endpoint for retrieving, updating, or deleting a user.
class UserDetail(APIView):
    """
    Endpoint for retrieving, updating, or deleting a user.
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            # Retrieve a specific user object based on the provided primary key (pk)
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            # Raise Http404 exception if the user does not exist
            raise Http404

    def get(self, request, pk):
        # Retrieve the user object
        user = self.get_object(pk)
        # Serialize the user object
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        # Retrieve the user object
        user = self.get_object(pk)
        # Deserialize request data using custom user serializer
        serializer = CustomUserSerializer(user, data=request.data)
        if serializer.is_valid():
            # Save the updated user object
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # Retrieve the user object
        user = self.get_object(pk)
        # Delete the user object from the database
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
