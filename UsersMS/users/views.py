from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.hashers import make_password  # Import make_password to hash passwords
from .models import CustomUser  # Import CustomUser model
from .serializers import CustomUserSerializer  # Import CustomUserSerializer
from rest_framework import serializers
import logging

logger = logging.getLogger(__name__)

# Serializer for the CustomUser model # git test
class CustomUserSerializer(serializers.ModelSerializer):
    # Define the fields and settings for the serializer
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'is_active', 'is_admin', 'password']
        # Specify additional settings for the serializer
        extra_kwargs = {
            'password': {'write_only': True},  # Password field should not be included in responses
            'is_active': {'read_only': True},  # is_active field should be read-only
            'is_admin': {'read_only': True},   # is_admin field should be read-only
        }

    # Method to create a new user instance with the validated data
    def create(self, validated_data):
        # Hash the password before creating the user
        validated_data['password'] = make_password(validated_data.get('password'))
        # Create a new user instance
        user = CustomUser.objects.create(**validated_data)
        return user

    # Method to update an existing user instance with the validated data
    def update(self, instance, validated_data):
        # Update email if provided, otherwise keep the existing email
        instance.email = validated_data.get('email', instance.email)
        # Update username if provided, otherwise keep the existing username
        instance.username = validated_data.get('username', instance.username)
        # Update password if provided, otherwise keep the existing password
        password = validated_data.get('password')
        if password:
            # Hash the new password if provided
            instance.password = make_password(password)
        # Save the updated user instance
        instance.save()
        return instance

# Custom authentication token view to generate tokens automatically upon user login.
class CustomAuthToken(ObtainAuthToken):
    """
    Custom authentication token view to generate tokens automatically upon user login.
    """
    # POST request for token generation
    def post(self, request, *args, **kwargs):
        # Deserialize request data using authentication token serializer
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        # Retrieve the authenticated user
        user = serializer.validated_data['user']
        # Generate or retrieve authentication token for the user
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

# Endpoint for user signup.
class UserSignUp(APIView):
    """
    Endpoint for user signup.
    """
    permission_classes = []

    # POST request for user signup
    def post(self, request, format=None):
        # Deserialize request data using custom user serializer
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            # Save the new user object
            user = serializer.save()
            return Response({'user': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Endpoint for user login.
class UserLogin(ObtainAuthToken):
    """
    Endpoint for user login.6666
    """
    # POST request for user login
    def post(self, request, *args, **kwargs):
        logger.debug('User login request received')
        # Deserialize request data using authentication token serializer
        serializer = self.serializer_class(data=request.data, context={'request': request})
        try:
           serializer.is_valid(raise_exception=True)
        # Retrieve the authenticated user
           user = serializer.validated_data['user']
        # Generate or retrieve authentication token for the user
           token, created = Token.objects.get_or_create(user=user)
           logger.info('User authenticated successfully')
           return Response({'token': token.key})
        except Exception as e:
            logger.error(f'Error during user login: {e}')
            return Response({'error': 'Unable to log in with provided credentials.'}, status=status.HTTP_400_BAD_REQUEST)

    

# Endpoint for listing users (admin-only).
class UserList(APIView):
    """
    Endpoint for listing users (admin-only).
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    # GET request for listing users
    def get(self, request, format=None):
        # Retrieve all user objects from the database
        users = CustomUser.objects.all()
        # Serialize user objects
        serializer = CustomUserSerializer(users, many=True)
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

    def get(self, request, pk, format=None):
        # Retrieve the user object
        user = self.get_object(pk)
        # Serialize the user object
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        # Retrieve the user object
        user = self.get_object(pk)
        # Deserialize request data using custom user serializer
        serializer = CustomUserSerializer(user, data=request.data)
        if serializer.is_valid():
            # Save the updated user object
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        # Retrieve the user object
        user = self.get_object(pk)
        # Delete the user object from the database
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
