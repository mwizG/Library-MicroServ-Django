from rest_framework import serializers
from django.contrib.auth.hashers import make_password  # Import make_password to hash passwords
from .models import CustomUser

# Serializer for the CustomUser model
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
            instance.password = password
        # Save the updated user instance
        instance.save()
        return instance
