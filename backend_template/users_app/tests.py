from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserModelTests(TestCase):

    def test_create_user(self):
        """Test creating a new user with an email is successful."""
        email = 'test@example.com'
        password = 'testpassword123'
        user = User.objects.create_user(email=email, password=password, first_name='Test', last_name='User')
        
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active) # Default from UserManager

    def test_create_superuser(self):
        """Test creating a new superuser is successful."""
        email = 'super@example.com'
        password = 'superpassword123'
        admin_user = User.objects.create_superuser(email=email, password=password, first_name='Super', last_name='User')
        
        self.assertEqual(admin_user.email, email)
        self.assertTrue(admin_user.check_password(password))
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_active)

    def test_create_user_without_email(self):
        """Test creating user without an email raises ValueError."""
        with self.assertRaises(ValueError):
            User.objects.create_user(email=None, password="foo")

    def test_create_superuser_not_staff(self):
        """Test creating superuser with is_staff=False raises ValueError."""
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='super2@example.com', password='foo', is_staff=False)

    def test_create_superuser_not_superuser(self):
        """Test creating superuser with is_superuser=False raises ValueError."""
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='super3@example.com', password='foo', is_superuser=False)

    def test_user_str_representation(self):
        """Test the string representation of the user model."""
        email = 'teststr@example.com'
        user = User.objects.create_user(email=email, password='password')
        self.assertEqual(str(user), email)

    def test_activation_token_methods(self):
        """Test activation token generation and clearing."""
        user = User.objects.create_user(email='activate@example.com', password='password')
        self.assertIsNone(user.activation_token)
        self.assertIsNone(user.activation_expiry)

        user.set_activation_token()
        self.assertIsNotNone(user.activation_token)
        self.assertIsNotNone(user.activation_expiry)

        user.clear_activation_token()
        self.assertIsNone(user.activation_token)
        self.assertIsNone(user.activation_expiry)

    def test_password_reset_token_methods(self):
        """Test password reset token generation and clearing."""
        user = User.objects.create_user(email='reset@example.com', password='password')
        self.assertIsNone(user.password_reset_token)
        self.assertIsNone(user.password_reset_expiry)

        user.set_password_reset_token()
        self.assertIsNotNone(user.password_reset_token)
        self.assertIsNotNone(user.password_reset_expiry)

        user.clear_password_reset_token()
        self.assertIsNone(user.password_reset_token)
        self.assertIsNone(user.password_reset_expiry)

# Add more tests for user-related views, serializers, etc.