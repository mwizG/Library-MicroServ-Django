from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username=None, password=None, **extra_fields):
        """
        Creates and saves a custom user with the given email, username, and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        
        # Normalize the email address to ensure consistency
        email = self.normalize_email(email)
        
        # Create a new user instance with the provided email, username, and any additional fields
        user = self.model(email=email, username=username, **extra_fields)
        
        # Set the password for the user
        user.set_password(password)
        
        # Save the user in the database using the default database
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username=None, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email, username, and password.
        """
        # Set is_staff and is_superuser flags to True by default
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        # Create a new superuser using the create_user method
        return self.create_user(email, username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model representing a user of the system.
    """
    # Choices for membership status field
    MEMBERSHIP_STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    
    is_admin = models.BooleanField(default=False)
    # Email field for the user (unique)
    email = models.EmailField()
    
    # Username field (optional, can be left blank)
    username = models.CharField(max_length=150, blank=True,unique=True)
    
    # Membership status field with choices
    membership_status = models.CharField(max_length=10, choices=MEMBERSHIP_STATUS_CHOICES, default='active')
    
    # Boolean field indicating if the user is active
    is_active = models.BooleanField(default=True)
    
    # Boolean field indicating if the user is a staff member
    is_staff = models.BooleanField(default=False)
    
    # Date when the user joined
    date_joined = models.DateTimeField(auto_now_add=True)

    # Custom user manager for managing user creation
    objects = CustomUserManager()

    # Field used for authentication (email)
    USERNAME_FIELD = 'username'
    
    # Additional fields required in createsuperuser command
    REQUIRED_FIELDS = ['email']  # Email is required for createsuperuser command

    def get_email(self):
        return self.email

    def __str__(self):
        """
        String representation of the user object (email).
        """
        return 'email: ' + self.email + '\n username: ' + self.username + '\n password:'+ self.password
