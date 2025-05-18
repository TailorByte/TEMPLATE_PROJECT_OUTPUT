#!/usr/bin/env python
import argparse
import os
import sys
import re

# --- Configuration ---
BACKEND_DIR = "backend"
COMMON_MODELS_IMPORT = "from common.models import BaseModel" # Adjust if your BaseModel is elsewhere

def to_pascal_case(snake_str):
    return "".join(word.capitalize() for word in snake_str.split('_'))

def to_camel_case(snake_str):
    parts = snake_str.split('_')
    return parts[0] + "".join(word.capitalize() for word in parts[1:])

def create_or_append_to_file(filepath, content_to_add, check_for_string=None, insert_before_marker=None):
    """Creates a file or appends content. If check_for_string is provided, appends only if not found."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    if os.path.exists(filepath):
        with open(filepath, 'r+', encoding='utf-8') as f:
            existing_content = f.read()
            if check_for_string and check_for_string in existing_content:
                print(f"Content marker '{check_for_string}' already exists in {filepath}. Skipping append for this part.")
                return
            
            if insert_before_marker and insert_before_marker in existing_content:
                parts = existing_content.split(insert_before_marker, 1)
                new_content = parts[0] + content_to_add + "\n" + insert_before_marker + parts[1]
                f.seek(0)
                f.write(new_content)
                f.truncate()
            else:
                f.seek(0, os.SEEK_END) # Go to the end of file
                if not existing_content.endswith('\\n') and existing_content: # Add newline if not present
                    f.write('\\n')
                f.write(content_to_add + '\\n')
        print(f"Appended to/Updated file: {filepath}")
    else:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content_to_add + '\\n')
        print(f"Created file: {filepath}")

def parse_field_definitions(field_str):
    """Parses a string like 'name:char,age:int' into a list of tuples."""
    fields = []
    if not field_str:
        return fields
    for part in field_str.split(','):
        name_type = part.split(':')
        if len(name_type) == 2:
            name = name_type[0].strip()
            field_type = name_type[1].strip().lower()
            if re.match(r"^[a-z_][a-z0-9_]*$", name): # Basic validation for field name
                 fields.append({'name': name, 'type': field_type})
            else:
                print(f"Warning: Invalid field name '{name}'. Skipping.")
        else:
            print(f"Warning: Could not parse field definition '{part}'. Skipping.")
    return fields

def map_simple_type_to_django_field(simple_type):
    mapping = {
        "char": "models.CharField(max_length=255)",
        "text": "models.TextField(blank=True, null=True)",
        "int": "models.IntegerField(default=0)",
        "integer": "models.IntegerField(default=0)",
        "float": "models.FloatField(default=0.0)",
        "bool": "models.BooleanField(default=False)",
        "boolean": "models.BooleanField(default=False)",
        "date": "models.DateField(null=True, blank=True)",
        "datetime": "models.DateTimeField(null=True, blank=True)",
        "uuid": "models.UUIDField(default=uuid.uuid4, editable=False, unique=True)",
        # Add more mappings as needed
    }
    return mapping.get(simple_type, "models.CharField(max_length=255) # Default, unknown type")


# --- Main Scaffolding Logic ---
def scaffold_resource(app_name, model_name_snake, fields_str):
    project_root = os.getcwd()
    app_path = os.path.join(project_root, BACKEND_DIR, app_name)

    if not os.path.isdir(app_path):
        print(f"Error: App '{app_name}' directory not found at '{app_path}'.")
        print(f"Please create the app first using 'python {BACKEND_DIR}/manage.py startapp {app_name}' or the create_django_app.py script.")
        return

    model_name_pascal = to_pascal_case(model_name_snake)
    model_name_lower = model_name_snake.lower()
    
    parsed_fields = parse_field_definitions(fields_str)

    # 1. models.py
    models_py_path = os.path.join(app_path, "models.py")
    model_fields_content = ""
    if not parsed_fields: # Add a default field if none are provided
        model_fields_content += f"    name = models.CharField(max_length=255, default='Default {model_name_pascal} Name')\n"
    else:
        for field_def in parsed_fields:
            django_field_type = map_simple_type_to_django_field(field_def['type'])
            model_fields_content += f"    {field_def['name']} = {django_field_type}\n"
            if field_def['type'] == 'uuid': # Ensure uuid is imported if used
                if "import uuid" not in open(models_py_path, 'r', encoding='utf-8').read() if os.path.exists(models_py_path) else True:
                    create_or_append_to_file(models_py_path, "import uuid\n", check_for_string="import uuid")


    model_content = f"""
class {model_name_pascal}(BaseModel): # Assumes BaseModel is imported
    # Define fields based on parsed input or defaults
{model_fields_content}
    def __str__(self):
        return str(getattr(self, '{parsed_fields[0]['name'] if parsed_fields else 'name'}', f"{model_name_pascal} object ({{self.pk}})"))

    class Meta:
        verbose_name = "{model_name_pascal.replace('_', ' ')}"
        verbose_name_plural = "{model_name_pascal.replace('_', ' ')}s"
        ordering = ['-created_at'] # Example
"""
    # Ensure BaseModel import exists or add it
    if os.path.exists(models_py_path):
        with open(models_py_path, 'r', encoding='utf-8') as f_read:
            if COMMON_MODELS_IMPORT not in f_read.read():
                 create_or_append_to_file(models_py_path, COMMON_MODELS_IMPORT + "\n", check_for_string=COMMON_MODELS_IMPORT, insert_before_marker="class ") # Try to insert before first class
    else: # File doesn't exist, create with import
        create_or_append_to_file(models_py_path, COMMON_MODELS_IMPORT + "\n")

    create_or_append_to_file(models_py_path, model_content, check_for_string=f"class {model_name_pascal}(BaseModel):")


    # 2. admin.py
    admin_py_path = os.path.join(app_path, "admin.py")
    admin_import_content = f"from .models import {model_name_pascal}"
    admin_register_content = f"""
@admin.register({model_name_pascal})
class {model_name_pascal}Admin(admin.ModelAdmin):
    list_display = ('id', {' + '.join([f"'{f['name']}'" for f in parsed_fields[:2]]) + ", " if parsed_fields else "'name', "} 'created_at', 'updated_at')
    search_fields = ({' + '.join([f"'{f['name']}'" for f in parsed_fields if 'char' in f['type'] or 'text' in f['type']][:2]) + "," if parsed_fields else "'name',"})
    readonly_fields = ('id', 'created_at', 'updated_at')
"""
    create_or_append_to_file(admin_py_path, admin_import_content, check_for_string=admin_import_content)
    create_or_append_to_file(admin_py_path, admin_register_content, check_for_string=f"@admin.register({model_name_pascal})")


    # 3. serializers.py
    serializers_py_path = os.path.join(app_path, "serializers.py")
    serializer_import_content = f"from .models import {model_name_pascal}"
    serializer_fields_list = "['id'] + " + str([f['name'] for f in parsed_fields]) + " + ['created_at', 'updated_at']" if parsed_fields else "['id', 'name', 'created_at', 'updated_at']"

    serializer_content = f"""
class {model_name_pascal}Serializer(serializers.ModelSerializer):
    class Meta:
        model = {model_name_pascal}
        fields = {serializer_fields_list}
        read_only_fields = ('id', 'created_at', 'updated_at')
"""
    create_or_append_to_file(serializers_py_path, "from rest_framework import serializers", check_for_string="from rest_framework import serializers")
    create_or_append_to_file(serializers_py_path, serializer_import_content, check_for_string=serializer_import_content)
    create_or_append_to_file(serializers_py_path, serializer_content, check_for_string=f"class {model_name_pascal}Serializer(serializers.ModelSerializer):")


    # 4. views.py
    views_py_path = os.path.join(app_path, "views.py")
    view_imports_content = f"from .models import {model_name_pascal}\\nfrom .serializers import {model_name_pascal}Serializer"
    viewset_content = f"""
class {model_name_pascal}ViewSet(viewsets.ModelViewSet):
    queryset = {model_name_pascal}.objects.all().order_by('-created_at')
    serializer_class = {model_name_pascal}Serializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # Default permission
"""
    create_or_append_to_file(views_py_path, "from rest_framework import viewsets, permissions", check_for_string="from rest_framework import viewsets")
    create_or_append_to_file(views_py_path, view_imports_content, check_for_string=f"from .models import {model_name_pascal}")
    create_or_append_to_file(views_py_path, viewset_content, check_for_string=f"class {model_name_pascal}ViewSet(viewsets.ModelViewSet):")


    # 5. urls.py
    urls_py_path = os.path.join(app_path, "urls.py")
    router_import_line = "from rest_framework.routers import DefaultRouter"
    router_instantiation_line = "router = DefaultRouter()"
    router_registration_line = f"router.register(r'{model_name_lower}s', views.{model_name_pascal}ViewSet, basename='{model_name_lower}')"
    
    # Ensure basic structure exists
    if not os.path.exists(urls_py_path):
        base_urls_content = f"""from django.urls import path, include
{router_import_line}
from . import views

{router_instantiation_line}
# {router_registration_line} # Will be added by subsequent call

app_name = '{app_name}'

urlpatterns = [
    path('', include(router.urls)),
]
"""
        create_file_with_content(urls_py_path, base_urls_content)

    # Add imports and router registration
    create_or_append_to_file(urls_py_path, f"from .views import {model_name_pascal}ViewSet", check_for_string=f"from .views import {model_name_pascal}ViewSet", insert_before_marker="router = DefaultRouter()")
    create_or_append_to_file(urls_py_path, router_registration_line, check_for_string=router_registration_line, insert_before_marker="app_name = ")
    
    print(f"Successfully scaffolded DRF resource for '{model_name_pascal}' in app '{app_name}'.")
    print(f"Remember to run 'python {BACKEND_DIR}/manage.py makemigrations {app_name}' and 'python {BACKEND_DIR}/manage.py migrate'.")

def main():
    parser = argparse.ArgumentParser(description="Scaffold a new DRF resource (Model, Serializer, ViewSet, Admin, URL).")
    parser.add_argument("app_name", help="Name of the Django app (e.g., 'products').")
    parser.add_argument("model_name", help="Name of the model in snake_case (e.g., 'product_item').")
    parser.add_argument(
        "--fields",
        default="",
        help="Comma-separated list of field definitions (e.g., 'name:char,price:float,is_available:bool'). Supported types: char, text, int, float, bool, date, datetime, uuid."
    )
    args = parser.parse_args()

    if not re.match(r"^[a-z_][a-z0-9_]*$", args.app_name):
        print("Error: App name should be lowercase_with_underscores.")
        sys.exit(1)
    if not re.match(r"^[a-z_][a-z0-9_]*$", args.model_name):
        print("Error: Model name should be lowercase_with_underscores.")
        sys.exit(1)

    scaffold_resource(args.app_name, args.model_name, args.fields)

if __name__ == "__main__":
    # Example usage from project root:
    # python scripts/scaffolding/scaffold_drf_resource.py my_app new_item --fields name:char,quantity:int
    main()