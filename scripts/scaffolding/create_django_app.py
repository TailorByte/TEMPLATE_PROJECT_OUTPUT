#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Scaffolds a new Django app and populates it with boilerplate files.
"""
import argparse
import os
import subprocess
import sys
import re

def run_command(command_args, cwd=None):
    """Runs a command and returns its output or raises an exception."""
    try:
        process = subprocess.Popen(command_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=cwd)
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            print(f"Error running command: {' '.join(command_args)}")
            print(f"Stderr: {stderr}")
            raise subprocess.CalledProcessError(process.returncode, command_args, output=stdout, stderr=stderr)
        return stdout
    except FileNotFoundError:
        print(f"Error: Command '{command_args[0]}' not found. Is it in your PATH?")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

def create_file_with_content(filepath, content):
    """Creates a file with the given content, creating parent dirs if needed."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created/Updated file: {filepath}")

# --- Boilerplate Content ---

MODELS_PY_CONTENT = """from django.db import models
# Assuming 'common' app with BaseModel exists at the same level or is in INSTALLED_APPS
# from common.models import BaseModel # Adjust import if common is structured differently relative to new apps

# TODO: If your project has a common app with a BaseModel, uncomment the import above
# and inherit from it, e.g., class YourModelName(BaseModel):

class YourModelName(models.Model): # Or YourModelName(BaseModel)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    
    # If not using a BaseModel from common, add timestamps directly:
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        verbose_name = "Your Model Name"
        verbose_name_plural = "Your Model Names"
        ordering = ['-created_at'] # Example default ordering
"""

VIEWS_PY_CONTENT = """from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import YourModelName # Placeholder, ensure this matches your model name
from .serializers import YourModelNameSerializer # Placeholder

# TODO: Define your views and viewsets here.

class YourModelNameViewSet(viewsets.ModelViewSet):
    \"\"\"
    API endpoint that allows YourModelNames to be viewed or edited.
    \"\"\"
    queryset = YourModelName.objects.all().order_by('-created_at') # Example ordering
    serializer_class = YourModelNameSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # Sensible default
    # For more specific permissions, consider creating a permissions.py in this app
    # and importing custom permissions, or using DjangoModelPermissions.

    # Example: If your model has an 'owner' field linked to the user
    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)
"""

SERIALIZERS_PY_CONTENT = """from rest_framework import serializers
from .models import YourModelName # Placeholder, ensure this matches your model name

# TODO: Define your serializers here.

class YourModelNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = YourModelName
        fields = [
            'id',
            'name',
            'description',
            # Add other fields from YourModelName here
            'created_at',
            'updated_at'
        ]
        read_only_fields = ('id', 'created_at', 'updated_at')
"""

ADMIN_PY_CONTENT = """from django.contrib import admin

# Register your models here.
# from .models import YourModel # Example import
#
# @admin.register(YourModel)
# class YourModelAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name') # Customize as needed
#     search_fields = ('name',) # Customize as needed
"""

URLS_PY_CONTENT_TEMPLATE = """from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views # Placeholder, ensure YourModelNameViewSet is in views

# TODO: Define your URL patterns here.

router = DefaultRouter()
router.register(r'yourmodelnames', views.YourModelNameViewSet, basename='yourmodelname')
# Ensure 'yourmodelnames' is a suitable URL path and 'yourmodelname' is a unique basename.

app_name = '{app_name}' # Important for namespacing

urlpatterns = [
    path('', include(router.urls)),
]
"""

TESTS_PY_CONTENT = """from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model # If you need to create users for tests
from .models import YourModelName # Placeholder

User = get_user_model() # If using users

# TODO: Write your tests here.

class YourModelNameAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a user for authentication if your views require it
        # self.user = User.objects.create_user(email='testuser@example.com', password='testpassword123')
        # self.client.force_authenticate(user=self.user)
        
        self.model_data = {{'name': 'Test Item One', 'description': 'Description for item one.'}}
        self.model_instance = YourModelName.objects.create(**self.model_data)
        
        # Ensure app_name in urls.py matches the one used here (e.g., '{{app_name}}')
        # and basename in router registration matches (e.g., 'yourmodelname')
        self.list_url = reverse('{{app_name}}:yourmodelname-list') 
        self.detail_url = reverse('{{app_name}}:yourmodelname-detail', kwargs={{'pk': self.model_instance.pk}})

    def test_get_list_unauthenticated(self): # Or authenticated if needed
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK) # Adjust if auth is strictly required
        # self.assertGreater(len(response.data['results']), 0) # If using pagination and item exists

    def test_get_detail_unauthenticated(self): # Or authenticated
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK) # Adjust if auth is strictly required
        self.assertEqual(response.data['name'], self.model_data['name'])

    # Add tests for POST, PUT, DELETE, ensuring authentication if required
    # Example POST test (assuming authentication is required):
    # def test_create_item_authenticated(self):
    #     self.client.force_authenticate(user=self.user) # Authenticate first
    #     new_item_data = {{'name': 'New API Item', 'description': 'From API test'}}
    #     response = self.client.post(self.list_url, new_item_data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(YourModelName.objects.count(), 2)
    #     self.assertEqual(response.data['name'], new_item_data['name'])
"""

def scaffold_django_app(app_name, target_project_dir="backend"):
    """
    Scaffolds a new Django app within the specified target project directory (e.g., 'backend').
    """
    script_execution_root = os.getcwd() # Where this script is run from (e.g., ExcursionBooking)
    django_project_root = os.path.join(script_execution_root, target_project_dir)
    
    if not os.path.isdir(django_project_root) or not os.path.exists(os.path.join(django_project_root, "manage.py")):
        print(f"Error: Django project directory '{django_project_root}' or 'manage.py' not found.")
        print(f"Please ensure you are in the main project template root and '{target_project_dir}/manage.py' exists.")
        sys.exit(1)

    app_path = os.path.join(django_project_root, app_name)

    if os.path.exists(app_path):
        print(f"Error: App directory '{app_path}' already exists. Cannot create app.")
        return

    print(f"Creating Django app '{app_name}' in '{django_project_root}' using manage.py startapp...")
    try:
        python_executable = sys.executable
        run_command([python_executable, "manage.py", "startapp", app_name], cwd=django_project_root)
    except subprocess.CalledProcessError:
        print(f"Failed to create app '{app_name}' using manage.py. Aborting.")
        return
    # FileNotFoundError for manage.py should be caught by the check above

    print(f"\nPopulating boilerplate files for app '{app_name}' in '{app_path}':")
    
    create_file_with_content(os.path.join(app_path, "models.py"), MODELS_PY_CONTENT)
    create_file_with_content(os.path.join(app_path, "views.py"), VIEWS_PY_CONTENT)
    create_file_with_content(os.path.join(app_path, "serializers.py"), SERIALIZERS_PY_CONTENT)
    create_file_with_content(os.path.join(app_path, "admin.py"), ADMIN_PY_CONTENT)
    create_file_with_content(os.path.join(app_path, "urls.py"), URLS_PY_CONTENT_TEMPLATE.format(app_name=app_name))
    # Corrected f-string usage for TESTS_PY_CONTENT
    create_file_with_content(os.path.join(app_path, "tests.py"), TESTS_PY_CONTENT.replace('{app_name}', app_name))


    # apps.py is created by startapp, just ensure name is correct (it should be)
    # And potentially set a more descriptive verbose_name
    apps_py_path = os.path.join(app_path, "apps.py")
    if os.path.exists(apps_py_path):
        with open(apps_py_path, 'r+', encoding='utf-8') as f:
            content = f.read()
            # Ensure the name field is correct, startapp usually gets this right
            expected_name_line = f"    name = '{app_name}'"
            # app_class_name = "".join(word.capitalize() for word in app_name.split('_')) + "Config" # Already created by startapp
            # expected_class_line = f"class {app_class_name}(AppConfig):"
            
            modified = False
            if expected_name_line not in content: # Check if name = 'app_name' is present
                # If not, try to replace the existing name = '...' line
                content = re.sub(r"(name\s*=\s*)'.*?'", rf"\1'{app_name}'", content)
                modified = True
            
            # Add verbose_name if not present
            if "verbose_name =" not in content:
                # Try to insert it after the name line
                # This regex looks for "name = '...'" and inserts verbose_name after it
                content = re.sub(r"(^\s*name\s*=\s*'.*?'\s*$)", 
                                 rf"\1\n    verbose_name = '{app_name.replace('_', ' ').title()}'", 
                                 content, flags=re.MULTILINE)
                if "verbose_name =" not in content: # Fallback if the above regex didn't match (e.g. no name line)
                    # This case should ideally not happen if startapp worked.
                    # As a fallback, try to add it after "class ...Config(AppConfig):"
                    class_name_pattern = r"(class\s+\w+Config\(AppConfig\):)"
                    if re.search(class_name_pattern, content):
                        content = re.sub(class_name_pattern,
                                         rf"\1\n    name = '{app_name}'\n    verbose_name = '{app_name.replace('_', ' ').title()}'",
                                         content, count=1) # Apply only once
                    else: # Absolute fallback, append to file (less ideal)
                        content += f"\n    name = '{app_name}'\n    verbose_name = '{app_name.replace('_', ' ').title()}'\n"
                modified = True

            if modified:
                f.seek(0)
                f.write(content)
                f.truncate()
                print(f"Updated: {apps_py_path}")
    
    print(f"\nSuccessfully scaffolded Django app '{app_name}' in '{target_project_dir}'.")
    print("Next steps:")
    print(f"1. Add '{target_project_dir}.{app_name}' (or just '{app_name}' if '{target_project_dir}' is in sys.path via settings) to INSTALLED_APPS in your project's settings.py.")
    print(f"2. Include '{app_name}.urls' in your '{target_project_dir}/[excursionbooking]/urls.py' (e.g., path('api/v1/{app_name}/', include('{app_name}.urls'))).")
    print(f"3. Define your models in '{target_project_dir}/{app_name}/models.py'.")
    print(f"4. Run 'python {target_project_dir}/manage.py makemigrations {app_name}'.")
    print(f"5. Run 'python {target_project_dir}/manage.py migrate'.")

def main():
    parser = argparse.ArgumentParser(description="Scaffold a new Django app with boilerplate files.")
    parser.add_argument(
        "app_name",
        help="The name of the Django app to create (e.g., 'inventory', 'notifications'). Should be lowercase_with_underscores if multiple words."
    )
    args = parser.parse_args()

    if not re.match(r"^[a-z_][a-z0-9_]*$", args.app_name):
        print("Error: App name should be lowercase_with_underscores and a valid Python module name.")
        sys.exit(1)
    
    # Assuming the default target project directory is 'backend' as per our template structure
    scaffold_django_app(args.app_name, target_project_dir="backend")

if __name__ == "__main__":
    main()