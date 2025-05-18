from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from .models import ExampleItem

User = get_user_model()

class ExampleItemModelTests(TestCase):
    def test_example_item_creation(self):
        item = ExampleItem.objects.create(name="Test Item", description="A test description.")
        self.assertEqual(item.name, "Test Item")
        self.assertEqual(item.description, "A test description.")
        self.assertTrue(item.is_active) # Default value

    def test_example_item_str_representation(self):
        item = ExampleItem.objects.create(name="String Test Item")
        self.assertEqual(str(item), "String Test Item")

class ExampleItemAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        # self.client.force_authenticate(user=self.user) # Authenticate if endpoints require it

        self.item1_data = {'name': 'API Item 1', 'description': 'Description 1'}
        self.item2_data = {'name': 'API Item 2', 'description': 'Description 2'}
        self.item1 = ExampleItem.objects.create(**self.item1_data)

    def test_get_example_item_list_unauthenticated(self):
        """
        Test GET list of example items (assuming IsAuthenticatedOrReadOnly or AllowAny).
        Adjust if authentication is strictly required.
        """
        url = reverse('main_app:exampleitem-list') # Ensure your app_name and basename are correct
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(len(response.data['results']), 1) # If using PageNumberPagination

    def test_get_example_item_detail_unauthenticated(self):
        """Test GET detail of an example item (assuming IsAuthenticatedOrReadOnly or AllowAny)."""
        url = reverse('main_app:exampleitem-detail', kwargs={'pk': self.item1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.item1.name)

    def test_create_example_item_authenticated(self):
        """Test POST to create an example item when authenticated."""
        self.client.force_authenticate(user=self.user)
        url = reverse('main_app:exampleitem-list')
        response = self.client.post(url, self.item2_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ExampleItem.objects.count(), 2)
        self.assertEqual(response.data['name'], self.item2_data['name'])

    def test_create_example_item_unauthenticated(self):
        """Test POST to create an example item when unauthenticated (should fail if permissions require auth)."""
        url = reverse('main_app:exampleitem-list')
        response = self.client.post(url, self.item2_data, format='json')
        # Assuming IsAuthenticatedOrReadOnly, POST requires authentication
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) # Or HTTP_403_FORBIDDEN

    def test_update_example_item_authenticated(self):
        """Test PUT to update an example item when authenticated."""
        self.client.force_authenticate(user=self.user)
        url = reverse('main_app:exampleitem-detail', kwargs={'pk': self.item1.pk})
        updated_data = {'name': 'Updated Item Name', 'description': 'Updated Description', 'is_active': False}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item1.refresh_from_db()
        self.assertEqual(self.item1.name, updated_data['name'])
        self.assertEqual(self.item1.is_active, False)

    def test_delete_example_item_authenticated(self):
        """Test DELETE an example item when authenticated."""
        self.client.force_authenticate(user=self.user)
        url = reverse('main_app:exampleitem-detail', kwargs={'pk': self.item1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ExampleItem.objects.count(), 0)

# Add more tests for edge cases, validation, permissions, custom actions, etc.