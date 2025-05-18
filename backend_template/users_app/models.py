import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
from common.models import BaseModel # Assuming BaseModel is in common/models.py

class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser, BaseModel):
    """
    Custom User model.
    Inherits from BaseModel for created_at and updated_at fields.
    Uses email as the username field.
    """
    # Override username to be None as we use email for login
    username = None
    email = models.EmailField(unique=True, verbose_name='Email Address')

    # Additional fields based on GuardianRoute.DBML.txt insights
    # first_name and last_name are already in AbstractUser
    # is_active, is_staff, is_superuser, last_login are in AbstractUser/AbstractBaseUser

    activation_token = models.UUIDField(default=uuid.uuid4, editable=False, null=True, blank=True, unique=True)
    activation_expiry = models.DateTimeField(null=True, blank=True)
    
    password_reset_token = models.UUIDField(null=True, blank=True, unique=True)
    password_reset_expiry = models.DateTimeField(null=True, blank=True)

    # Add any other custom fields for your user model here
    # Example: phone_number = models.CharField(max_length=20, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name'] # Add other fields required during createsuperuser

    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['email']

    def __str__(self):
        return self.email

    def set_activation_token(self, expiry_minutes=1440): # 24 hours
        """Generates a new activation token and expiry."""
        self.activation_token = uuid.uuid4()
        self.activation_expiry = timezone.now() + timezone.timedelta(minutes=expiry_minutes)
        self.save(update_fields=['activation_token', 'activation_expiry'])

    def clear_activation_token(self):
        """Clears the activation token and expiry."""
        self.activation_token = None
        self.activation_expiry = None
        self.save(update_fields=['activation_token', 'activation_expiry'])

    def set_password_reset_token(self, expiry_minutes=60): # 1 hour
        """Generates a new password reset token and expiry."""
        self.password_reset_token = uuid.uuid4()
        self.password_reset_expiry = timezone.now() + timezone.timedelta(minutes=expiry_minutes)
        self.save(update_fields=['password_reset_token', 'password_reset_expiry'])

    def clear_password_reset_token(self):
        """Clears the password reset token and expiry."""
        self.password_reset_token = None
        self.password_reset_expiry = None
        self.save(update_fields=['password_reset_token', 'password_reset_expiry'])

# Consider adding Role and UserRole models here or in a separate 'permissions_app'
# if you plan to implement the RBAC system seen in GuardianRoute.
# For now, keeping User model focused.