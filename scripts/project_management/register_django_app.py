import argparse
import os
import re

import sys

# Determine the correct project root dynamically
# Assuming the script is in scripts/project_management/
# PROJECT_ROOT should be two levels up from this script's directory.
# However, argparse default for project_root is already doing this, so we'll use that.

class AppDetails:
    def __init__(self, module_path, filesystem_path, simple_name, app_config_name):
        self.module_path = module_path
        self.filesystem_path = filesystem_path
        self.simple_name = simple_name
        self.app_config_name = app_config_name

def get_app_details(app_name_arg, project_root_path, main_project_dir_name="backend"):
    """
    Determines the various path/name formats for a Django app.
    app_name_arg can be 'users', 'backend/users', or 'backend.users'.
    main_project_dir_name is the directory containing top-level apps (e.g., 'backend').
    """
    app_name_arg = app_name_arg.strip()
    
    # Normalize path separators for consistency if app_name_arg is a path
    normalized_app_path_arg = app_name_arg.replace("/", os.sep).replace("\\", os.sep)

    simple_name = normalized_app_path_arg.split(os.sep)[-1].split('.')[-1]
    
    # Attempt to determine module_path and filesystem_path
    module_path_parts = normalized_app_path_arg.split('.')
    filesystem_path_parts = normalized_app_path_arg.split(os.sep)

    potential_module_path = ""
    potential_filesystem_path = ""

    if len(filesystem_path_parts) > 1: # e.g., backend/users
        potential_module_path = ".".join(filesystem_path_parts)
        potential_filesystem_path = os.path.join(project_root_path, *filesystem_path_parts)
    elif len(module_path_parts) > 1: # e.g., backend.users
        potential_module_path = app_name_arg
        potential_filesystem_path = os.path.join(project_root_path, *module_path_parts)
    else: # e.g., users (could be top-level or inside main_project_dir_name)
        # Check if it's a top-level app
        top_level_fs_path = os.path.join(project_root_path, simple_name)
        if os.path.isdir(top_level_fs_path) and os.path.exists(os.path.join(top_level_fs_path, 'apps.py')):
            potential_module_path = simple_name
            potential_filesystem_path = top_level_fs_path
        else:
            # Assume it's inside the main_project_dir_name (e.g., backend/users)
            potential_module_path = f"{main_project_dir_name}.{simple_name}"
            potential_filesystem_path = os.path.join(project_root_path, main_project_dir_name, simple_name)

    # Validate filesystem_path
    if not os.path.isdir(potential_filesystem_path):
        print(f"Error: Deduced app directory '{potential_filesystem_path}' does not exist or is not a directory.")
        print(f"Based on input '{app_name_arg}', project_root '{project_root_path}', main_project_dir '{main_project_dir_name}'.")
        sys.exit(1)
    if not os.path.exists(os.path.join(potential_filesystem_path, 'apps.py')):
        print(f"Warning: Deduced app directory '{potential_filesystem_path}' does not contain an apps.py file.")
        # Allow proceeding but warn, as apps.py is standard but not strictly required for basic registration.

    # Determine AppConfig name
    # Standard: module.path.apps.AppNameConfig or simple_name.apps.AppNameConfig
    app_config_name = f"{potential_module_path}.apps.{simple_name.capitalize()}Config"
    
    # Check if a more specific AppConfig is defined in apps.py (e.g. if app is nested)
    apps_py_path = os.path.join(potential_filesystem_path, 'apps.py')
    try:
        with open(apps_py_path, 'r', encoding='utf-8') as f_apps:
            content = f_apps.read()
            # Look for class YourAppNameConfig(AppConfig): name = 'your.app.module.path'
            # or default_app_config = 'your.app.module.path.apps.YourAppNameConfig'
            # This is a simplified check; a more robust check would parse the AST.
            config_match = re.search(r"class\s+(\w+Config)\(AppConfig\):", content)
            if config_match:
                actual_config_class_name = config_match.group(1)
                # Check if 'name' attribute is set in AppConfig
                name_attr_match = re.search(rf"class\s+{actual_config_class_name}\(AppConfig\):\s+name\s*=\s*['\"]({potential_module_path})['\"]", content, re.DOTALL)
                if name_attr_match:
                     app_config_name = f"{potential_module_path}.apps.{actual_config_class_name}"
                else: # Fallback if name attribute isn't explicitly the full module path
                     app_config_name = f"{potential_module_path}.apps.{actual_config_class_name}"


    except FileNotFoundError:
        print(f"Info: apps.py not found at {apps_py_path}. Using default AppConfig naming: {app_config_name}")
    except Exception as e_apps_py:
        print(f"Warning: Could not parse apps.py at {apps_py_path}. Using default AppConfig. Error: {e_apps_py}")


    return AppDetails(
        module_path=potential_module_path,
        filesystem_path=potential_filesystem_path,
        simple_name=simple_name,
        app_config_name=app_config_name
    )

def add_to_installed_apps(settings_file_path, app_config_name_to_add):
    """Adds the app_config_name to the INSTALLED_APPS list in settings.py."""
    """Adds the app_name to the INSTALLED_APPS list in settings.py."""
    try:
        with open(settings_file_path, "r+", encoding="utf-8") as f:
            content = f.read()
            
            # Find the INSTALLED_APPS list
            match = re.search(r"INSTALLED_APPS\s*=\s*\[([^\]]*)\]", content, re.DOTALL)
            if not match:
                print(f"Error: Could not find INSTALLED_APPS list in {settings_file_path}")
                return False

            installed_apps_str = match.group(1)
            
            # Check if app already exists
            # Check if app (as AppConfig or simple name) already exists
            # Simple check, might need to be more robust for variations
            if f"'{app_config_name_to_add}'" in installed_apps_str or \
               f'"{app_config_name_to_add}"' in installed_apps_str or \
               f"'{app_config_name_to_add.split('.')[0]}'" in installed_apps_str : # checks for simple app name if full config not there
                print(f"Info: App related to '{app_config_name_to_add}' likely already in INSTALLED_APPS.")
                return True

            # Add the new app, preserving indentation and commas
            lines = installed_apps_str.strip().split('\n')
            last_app_line = ""
            if lines:
                last_app_line = lines[-1].strip()
            
            new_app_entry = f"    '{app_config_name_to_add}',\n" # Standard indentation
            
            # Try to find a place to insert while maintaining some order (e.g., before 'django.contrib.admin')
            # or just append if no clear spot.
            # This is a simple append, more sophisticated logic could be added.
            
            # Find the end of the list to insert before the closing bracket
            insert_pos = match.end(1)
            
            # Ensure there's a comma if the list wasn't empty and didn't end with one
            if installed_apps_str.strip() and not installed_apps_str.strip().endswith(','):
                 # Find the last non-whitespace character before insert_pos
                last_char_index = len(installed_apps_str.rstrip()) -1
                if last_char_index >= 0:
                    # We need to insert a comma before adding the new app
                    # This requires careful manipulation of the string or re-reading and writing lines
                    # For simplicity, we'll assume a reasonably formatted list or append with a preceding comma if needed.
                    # A more robust solution would parse the list properly.
                    pass # Simplified for now

            # Add the new app entry
            # A simple approach: find the last ' or " before the closing ] and insert after it.
            # More robust: find the actual list elements.
            
            # Let's find the position of the last app entry to insert after it
            # This regex finds the last quoted string followed by an optional comma and whitespace
            last_entry_match = list(re.finditer(r"(['\"][\w.]+['\"])\s*,?\s*", installed_apps_str))
            
            if last_entry_match:
                # Insert after the last app entry
                insertion_point = match.start(1) + last_entry_match[-1].end()
                # Ensure there's a newline before the new app if the list is multi-line
                prefix = ""
                if '\n' in installed_apps_str[last_entry_match[-1].start():]: # if last entry was on its own line
                     prefix = installed_apps_str[last_entry_match[-1].end():].split('\n')[0] # get indentation
                
                new_content = content[:insertion_point] + prefix + new_app_entry + content[insertion_point:]

            else: # List is empty or only comments
                # Find the opening bracket and insert after it
                insertion_point = match.start(1)
                indentation_match = re.search(r"(\s*)", lines[0] if lines else "")
                indentation = indentation_match.group(1) if indentation_match else "    "
                new_app_entry_formatted = f"{indentation}'{app_config_name_to_add}',\n"
                new_content = content[:insertion_point] + new_app_entry_formatted + content[insertion_point:]

            f.seek(0)
            f.write(new_content)
            f.truncate()
            print(f"Successfully added '{app_config_name_to_add}' to INSTALLED_APPS in {os.path.basename(settings_file_path)}")
            return True
            
    except IOError as e:
        print(f"Error: Could not read/write {settings_file_path}. {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False


def add_to_project_urls(project_urls_path, app_module_path, app_simple_name, app_filesystem_path):
    """Adds a basic include for the app in the project's urls.py."""
    try:
        with open(project_urls_path, "r+", encoding="utf-8") as f:
            content = f.read()

            # Check if app URL is already included
            # Use app_simple_name for the URL prefix, and app_module_path for include
            url_pattern_to_check = f"path('{app_simple_name}/', include('{app_module_path}.urls'))"
            if url_pattern_to_check in content:
                print(f"Info: App '{app_module_path}' URLs already included in {os.path.basename(project_urls_path)}.")
                return True

            # Find urlpatterns list
            match = re.search(r"urlpatterns\s*=\s*\[([^\]]*)\]", content, re.DOTALL)
            if not match:
                print(f"Error: Could not find urlpatterns list in {project_urls_path}")
                return False
            
            urlpatterns_str = match.group(1)
            new_url_entry = f"    path('{app_simple_name}/', include('{app_module_path}.urls')),\n"

            # Attempt to add 'include' to imports if not present
            if "from django.urls import path, include" not in content and "from django.urls import path" in content:
                content = content.replace("from django.urls import path", "from django.urls import path, include", 1)
            elif "from django.urls import include" not in content and "from django.urls import path" in content:
                 # if only path is imported, add include
                 content = content.replace("from django.urls import path", "from django.urls import path, include")
            elif "from django.urls import path" not in content and "from django.urls import include" not in content:
                 # if neither is imported, add both (less likely for a Django project urls.py)
                 # This case might need a more specific anchor point for adding the import.
                 # For now, we'll assume 'from django.urls import path' or 'include' exists or is added manually.
                 print(f"Warning: Could not automatically add 'include' to imports in {project_urls_path}. Please ensure 'from django.urls import include' is present.")


            # Find the end of the list to insert before the closing bracket
            # Similar to INSTALLED_APPS, find the last path() entry
            last_entry_match = list(re.finditer(r"path\(.*?\)\s*,?\s*", urlpatterns_str))
            
            if last_entry_match:
                insertion_point = match.start(1) + last_entry_match[-1].end()
                prefix = ""
                if '\n' in urlpatterns_str[last_entry_match[-1].start():]:
                     prefix = urlpatterns_str[last_entry_match[-1].end():].split('\n')[0]
                
                new_content = content[:insertion_point] + prefix + new_url_entry + content[insertion_point:]
            else: # List is empty
                insertion_point = match.start(1)
                indentation_match = re.search(r"(\s*)", urlpatterns_str.strip().split('\n')[0] if urlpatterns_str.strip() else "")
                indentation = indentation_match.group(1) if indentation_match else "    "
                new_url_entry_formatted = f"{indentation}path('{app_simple_name}/', include('{app_module_path}.urls')),\n"
                new_content = content[:insertion_point] + new_url_entry_formatted + content[insertion_point:]
            
            f.seek(0)
            f.write(new_content)
            f.truncate()
            print(f"Successfully added '{app_module_path}' URLs to {os.path.basename(project_urls_path)}")
            
            # Advise to create app's urls.py
            # app_filesystem_path is the direct path to the app's directory
            app_urls_path = os.path.join(app_filesystem_path, "urls.py")
            if not os.path.exists(app_urls_path):
                print(f"Info: Please create '{os.path.join(app_simple_name, 'urls.py')}' with urlpatterns for the app.")
                try:
                    os.makedirs(os.path.dirname(app_urls_path), exist_ok=True)
                    with open(app_urls_path, "w", encoding="utf-8") as app_urls_f:
                        app_urls_f.write(
                            f"from django.urls import path\n"
                            f"from . import views\n\n"
                            f"app_name = '{app_simple_name}'\n" # Add app_name for namespacing
                            f"urlpatterns = [\n"
                            f"    # Define your app's URLs here, e.g.:\n"
                            f"    # path('', views.index, name='index'),\n"
                            f"]\n"
                        )
                    print(f"Created basic '{os.path.join(app_simple_name, 'urls.py')}'.")
                except IOError as e_app_urls:
                    print(f"Warning: Could not create '{os.path.join(app_simple_name, 'urls.py')}'. {e_app_urls}")
            return True

    except IOError as e:
        print(f"Error: Could not read/write {project_urls_path}. {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred while updating project URLs: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Register a Django app in the project.")
    parser.add_argument("app_name", help="The name of the Django app to register.")
    parser.add_argument(
        "--project_root",
        default=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")),
        help="The root directory of the ExcursionBooking project."
    )
    parser.add_argument(
        "--project_name",
        default="backend", # Default directory containing the main Django project and apps
        help="The name of the directory containing the Django project and potentially other apps (e.g., 'backend')."
    )
    parser.add_argument(
        "--django_project_name",
        default="excursionbooking", # Default ExcursionBooking project name (the one with settings.py)
        help="The name of the Django project directory itself (containing settings.py, wsgi.py)."
    )
    parser.add_argument(
        "--skip_urls",
        action="store_true",
        help="Skip adding the app to the project's urls.py."
    )

    args = parser.parse_args()

    # Validate project_root
    if not os.path.isdir(args.project_root):
        print(f"Error: Project root '{args.project_root}' does not exist or is not a directory.")
        sys.exit(1)

    # Determine app details
    # main_project_dir_name is the directory like 'backend' where apps might reside.
    app_details = get_app_details(args.app_name, args.project_root, args.project_name)

    # Construct paths to settings.py and project urls.py
    # The Django project directory (with settings.py) is inside the main_project_dir (e.g., backend/excursionbooking)
    django_project_dir_path = os.path.join(args.project_root, args.project_name, args.django_project_name)
    if not os.path.isdir(django_project_dir_path):
        print(f"Error: Django project directory '{django_project_dir_path}' does not exist.")
        print(f"Please check --project_name ('{args.project_name}') and --django_project_name ('{args.django_project_name}') arguments.")
        sys.exit(1)

    settings_file = os.path.join(django_project_dir_path, "settings.py")
    project_urls_file = os.path.join(django_project_dir_path, "urls.py")

    if not os.path.isfile(settings_file):
        print(f"Error: settings.py not found at '{settings_file}'.")
        sys.exit(1)
    if not os.path.isfile(project_urls_file):
        print(f"Error: Project urls.py not found at '{project_urls_file}'.")
        # This might be acceptable if --skip_urls is True, but usually it should exist.
        if not args.skip_urls:
            sys.exit(1)

    # The app_directory check is now handled within get_app_details
    # app_details.filesystem_path is the validated path to the app

    if add_to_installed_apps(settings_file, app_details.app_config_name): # Use AppConfig name
        if not args.skip_urls:
            add_to_project_urls(project_urls_file, app_details.module_path, app_details.simple_name, app_details.filesystem_path)
        print(f"\nApp '{app_details.module_path}' registration process complete.")
        print(f"Remember to create migrations if your app has models: python manage.py makemigrations {app_details.simple_name}")
        print("And then apply them: python manage.py migrate")
    else:
        print(f"\nFailed to fully register app '{app_details.module_path}'. Please check errors above.")