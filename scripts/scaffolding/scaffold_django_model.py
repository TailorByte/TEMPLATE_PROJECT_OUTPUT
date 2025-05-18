#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Scaffolds a new Django model and optionally its related DRF components
within an existing Django app.
"""
import argparse
import os
import re
import sys

def to_snake_case(name):
    """Converts PascalCase to snake_case."""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def to_pascal_case(name):
    """Converts snake_case to PascalCase."""
    return "".join(word.capitalize() for word in name.split('_'))

def append_to_file(filepath, content_to_append):
    """Appends content to a file, adding a newline if needed."""
    if not os.path.exists(filepath):
        print(f"Warning: File {filepath} does not exist. Creating it.")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content_to_append + "\n")
    else:
        with open(filepath, 'r+', encoding='utf-8') as f:
            existing_content = f.read()
            f.seek(0, os.SEEK_END) # Go to the end of file
            if existing_content and not existing_content.endswith('\n'):
                f.write('\n') # Add a newline if file doesn't end with one
            if not existing_content.endswith('\n\n') and existing_content.endswith('\n'): # ensure separation
                 f.write('\n')
            f.write(content_to_append + "\n")
    print(f"Appended to/Updated file: {filepath}")

def add_import_if_not_exists(filepath, import_statement):
    """Adds an import statement to a Python file if it doesn't already exist."""
    if not os.path.exists(filepath):
        print(f"Warning: Cannot add import to non-existent file: {filepath}")
        return

    with open(filepath, 'r+', encoding='utf-8') as f:
        content = f.read()
        # Simple check to avoid duplicate imports
        if import_statement.strip() not in content:
            # Try to add after other imports, or at the top
            lines = content.splitlines()
            insert_pos = 0
            for i, line in enumerate(lines):
                if line.startswith("from ") or line.startswith("import "):
                    insert_pos = i + 1
                elif line.strip() == "" and insert_pos > 0: # After a block of imports
                    break 
                elif line.strip() != "" and not (line.startswith("from ") or line.startswith("import ")): # First non-import line
                    break
            
            lines.insert(insert_pos, import_statement.strip())
            new_content = "\n".join(lines)
            if not new_content.endswith("\n"): # Ensure a newline at the end
                new_content += "\n"

            f.seek(0)
            f.write(new_content)
            f.truncate()
            print(f"Added import '{import_statement.strip()}' to {filepath}")

# --- Boilerplate Content Templates ---

MODEL_TEMPLATE = """
class {ModelName}(models.Model): # Or your BaseModel if you have one
    # TODO: Define fields for {ModelName}
    name = models.CharField(max_length=255, blank=True, null=True) # Example field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self: '{ModelName}') -> str:
        # Consider a more descriptive string representation
        return f"{{self.name or '{ModelName} object (' + str(self.pk) + ')'}}"

    class Meta:
        verbose_name = "{model_verbose_name}"
        verbose_name_plural = "{model_verbose_name_plural}"
        # ordering = ['-created_at'] # Example
"""

SERIALIZER_TEMPLATE = """
class {ModelName}Serializer(serializers.ModelSerializer):
    class Meta:
        model = {ModelName}
        fields = '__all__' # Or specify: ['id', 'name', 'created_at', 'updated_at']
        # read_only_fields = ('id', 'created_at', 'updated_at') # Example
"""

VIEWSET_TEMPLATE = """
class {ModelName}ViewSet(viewsets.ModelViewSet):
    queryset = {ModelName}.objects.all()
    serializer_class = {ModelName}Serializer
    # permission_classes = [permissions.IsAuthenticated] # Example
    # filterset_fields = ['name'] # Example for django-filter
    # search_fields = ['name'] # Example for DRF search
    # ordering_fields = ['name', 'created_at'] # Example for DRF ordering
"""

ADMIN_TEMPLATE = """
@admin.register({ModelName})
class {ModelName}Admin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at') # Customize as needed
    search_fields = ('name',) # Customize
    # list_filter = ('created_at', 'updated_at') # Customize
    # readonly_fields = ('created_at', 'updated_at') # Example
"""

URL_REGISTRATION_TEMPLATE = "router.register(r'{model_name_url_safe}', views.{ModelName}ViewSet, basename='{model_name_url_safe_singular}')"


def scaffold_django_model(app_name, ModelName, with_serializer, with_viewset, register_admin, register_url):
    project_root = os.getcwd()
    app_path = os.path.join(project_root, app_name)

    if not os.path.isdir(app_path):
        print(f"Error: App directory '{app_path}' does not exist.")
        sys.exit(1)

    model_verbose_name = re.sub(r'(?<!^)(?=[A-Z])', ' ', ModelName).strip() # Model Name
    model_verbose_name_plural = model_verbose_name + "s" # Simple plural
    if model_verbose_name.endswith('y') and not model_verbose_name.endswith(('ay','ey','iy','oy','uy')):
        model_verbose_name_plural = model_verbose_name[:-1] + "ies"


    # 1. Scaffold Model
    models_py_path = os.path.join(app_path, "models.py")
    add_import_if_not_exists(models_py_path, "from django.db import models")
    model_content = MODEL_TEMPLATE.format(
        ModelName=ModelName,
        model_verbose_name=model_verbose_name,
        model_verbose_name_plural=model_verbose_name_plural
    )
    append_to_file(models_py_path, model_content)

    # 2. Scaffold Serializer
    if with_serializer:
        serializers_py_path = os.path.join(app_path, "serializers.py")
        add_import_if_not_exists(serializers_py_path, "from rest_framework import serializers")
        add_import_if_not_exists(serializers_py_path, f"from .models import {ModelName}")
        serializer_content = SERIALIZER_TEMPLATE.format(ModelName=ModelName)
        append_to_file(serializers_py_path, serializer_content)

    # 3. Scaffold ViewSet
    if with_viewset:
        views_py_path = os.path.join(app_path, "views.py")
        add_import_if_not_exists(views_py_path, "from rest_framework import viewsets #, permissions")
        add_import_if_not_exists(views_py_path, f"from .models import {ModelName}")
        if with_serializer: # Only add serializer import if it's being created
            add_import_if_not_exists(views_py_path, f"from .serializers import {ModelName}Serializer")
        else: # Add a placeholder comment if serializer is not created by this script
            add_import_if_not_exists(views_py_path, f"# from .serializers import {ModelName}Serializer # Ensure this is created/imported")

        viewset_content = VIEWSET_TEMPLATE.format(ModelName=ModelName)
        append_to_file(views_py_path, viewset_content)

    # 4. Register in Admin
    if register_admin:
        admin_py_path = os.path.join(app_path, "admin.py")
        add_import_if_not_exists(admin_py_path, "from django.contrib import admin")
        add_import_if_not_exists(admin_py_path, f"from .models import {ModelName}")
        admin_content = ADMIN_TEMPLATE.format(ModelName=ModelName)
        append_to_file(admin_py_path, admin_content)

    # 5. Register URL (for ViewSet)
    if register_url and with_viewset:
        urls_py_path = os.path.join(app_path, "urls.py")
        model_name_url_safe = to_snake_case(ModelName).replace('_', '') + "s" # productitems
        model_name_url_safe_singular = to_snake_case(ModelName).replace('_', '') # productitem

        add_import_if_not_exists(urls_py_path, "from rest_framework.routers import DefaultRouter")
        add_import_if_not_exists(urls_py_path, f"from . import views")
        
        # Ensure router object exists
        with open(urls_py_path, 'r+', encoding='utf-8') as f:
            content = f.read()
            if "router = DefaultRouter()" not in content:
                # Add it near the top, after imports
                lines = content.splitlines()
                insert_pos = 0
                for i, line in enumerate(lines):
                    if line.startswith("from ") or line.startswith("import "):
                        insert_pos = i + 1
                    elif line.strip() == "" and insert_pos > 0: break
                    elif line.strip() != "" and not (line.startswith("from ") or line.startswith("import ")): break
                lines.insert(insert_pos, "\nrouter = DefaultRouter()")
                content = "\n".join(lines)
            
            # Ensure router.urls is in urlpatterns
            if "path('', include(router.urls))" not in content and "include(router.urls)" not in content :
                 content = content.replace("urlpatterns = [", "urlpatterns = [\n    path('', include(router.urls)),")


            f.seek(0)
            f.write(content)
            f.truncate()
        
        url_registration_content = URL_REGISTRATION_TEMPLATE.format(
            model_name_url_safe=model_name_url_safe,
            ModelName=ModelName,
            model_name_url_safe_singular=model_name_url_safe_singular
        )
        # Append the registration before the urlpatterns list
        with open(urls_py_path, 'r+', encoding='utf-8') as f:
            lines = f.read().splitlines()
            try:
                urlpatterns_index = lines.index("urlpatterns = [")
                lines.insert(urlpatterns_index -1 if urlpatterns_index > 0 else 0, url_registration_content)
            except ValueError: # urlpatterns not found or not in expected format
                lines.append(url_registration_content) # Append at the end as a fallback
            
            new_content = "\n".join(lines)
            if not new_content.endswith("\n"): new_content += "\n"
            f.seek(0)
            f.write(new_content)
            f.truncate()

        print(f"Added URL registration for {ModelName}ViewSet to {urls_py_path}")

    print(f"\nSuccessfully scaffolded components for model '{ModelName}' in app '{app_name}'.")
    print("Next steps:")
    print(f"1. Review and customize the generated files in '{app_name}/'.")
    print(f"2. Run 'python manage.py makemigrations {app_name}' and 'python manage.py migrate'.")


def main():
    parser = argparse.ArgumentParser(description="Scaffold a Django model and related DRF components.")
    parser.add_argument("app_name", help="Name of the existing Django app.")
    parser.add_argument("ModelName", help="Name of the model in PascalCase (e.g., ProductItem).")
    parser.add_argument("--with-serializer", action="store_true", help="Scaffold a DRF serializer.")
    parser.add_argument("--with-viewset", action="store_true", help="Scaffold a DRF ModelViewSet.")
    parser.add_argument("--register-admin", action="store_true", help="Register the model with Django admin.")
    parser.add_argument("--register-url", action="store_true", help="Register ViewSet URL with DRF router (implies --with-viewset).")
    
    args = parser.parse_args()

    if args.register_url and not args.with_viewset:
        print("Warning: --register-url implies --with-viewset. Enabling ViewSet scaffolding.")
        args.with_viewset = True
    if args.with_viewset and not args.with_serializer:
        print("Warning: --with-viewset typically requires a serializer. Enabling Serializer scaffolding.")
        args.with_serializer = True


    if not re.match(r"^[a-z_][a-z0-9_]*$", args.app_name):
        print("Error: App name should be lowercase_with_underscores.")
        sys.exit(1)
    if not re.match(r"^[A-Z][a-zA-Z0-9]*$", args.ModelName):
        print("Error: ModelName should be PascalCase.")
        sys.exit(1)

    scaffold_django_model(
        args.app_name, 
        args.ModelName,
        args.with_serializer,
        args.with_viewset,
        args.register_admin,
        args.register_url
    )

if __name__ == "__main__":
    main()