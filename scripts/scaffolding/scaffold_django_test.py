import argparse
import os
import re

def scaffold_django_test(app_name, target_name, project_root_dir, test_type):
    """
    Generates a boilerplate test file for a Django model, view, or serializer.
    """
    app_path = os.path.join(project_root_dir, app_name)
    if not os.path.isdir(app_path):
        print(f"Error: App directory '{app_path}' does not exist.")
        return

    # Sanitize target_name to be a valid Python module name component
    sanitized_target_name = re.sub(r'\W|^(?=\d)', '_', target_name.lower())
    
    test_file_name = f"test_{test_type}_{sanitized_target_name}.py"
    test_file_path = os.path.join(app_path, "tests", test_file_name) # Store in app/tests/ directory

    os.makedirs(os.path.join(app_path, "tests"), exist_ok=True) # Ensure tests directory exists

    if os.path.exists(test_file_path):
        print(f"Info: Test file '{test_file_path}' already exists.")
        return

    class_name_suffix = ""
    imports = "from django.test import TestCase\n"

    if test_type == "model":
        imports += f"from {app_name}.models import {target_name}\n"
        class_name_suffix = f"{target_name}Model"
    elif test_type == "view":
        # Assuming views are in views.py or a views module.
        # For simplicity, we'll assume target_name is the view function/class name.
        # More complex parsing might be needed if views are in submodules.
        imports += f"# from {app_name}.views import {target_name} # Adjust if your view is in a different module\n"
        imports += "from django.urls import reverse\n"
        class_name_suffix = f"{target_name}View"
    elif test_type == "serializer":
        imports += f"from {app_name}.serializers import {target_name}\n"
        # Potentially add model import if serializer is ModelSerializer
        # imports += f"# from {app_name}.models import YourModelForSerializer\n"
        class_name_suffix = f"{target_name}Serializer"
    else:
        print(f"Error: Unknown test type '{test_type}'. Supported types are 'model', 'view', 'serializer'.")
        return

    test_class_name = f"Test{class_name_suffix}"

    content = (
        f"{imports}\n"
        f"class {test_class_name}(TestCase):\n"
        f"    def setUp(self):\n"
        f"        \"\"\"Set up test data for the {test_type}.\"\"\"\n"
        f"        # Example: self.my_instance = {target_name}.objects.create(field='value') if model\n"
        f"        pass\n\n"
        f"    def test_{sanitized_target_name}_basic_functionality(self):\n"
        f"        \"\"\"Test basic functionality of the {target_name} {test_type}.\"\"\"\n"
        f"        # Example for model: self.assertIsNotNone(self.my_instance)\n"
        f"        # Example for view: response = self.client.get(reverse('your_url_name'))\n"
        f"        # Example for view: self.assertEqual(response.status_code, 200)\n"
        f"        # Example for serializer: serializer = {target_name}(data={{...}})\n"
        f"        # Example for serializer: self.assertTrue(serializer.is_valid())\n"
        f"        self.assertTrue(True) # Replace with actual assertions\n\n"
        f"    # Add more test methods here\n"
    )

    try:
        with open(test_file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Successfully created boilerplate test file: {test_file_path}")
        print(f"Remember to add specific test logic and adjust imports as needed.")
    except IOError as e:
        print(f"Error: Could not write to {test_file_path}. {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scaffold a Django test file for a model, view, or serializer.")
    parser.add_argument("app_name", help="The name of the Django app.")
    parser.add_argument("target_name", help="The name of the Model, View class/function, or Serializer class.")
    parser.add_argument(
        "--type",
        required=True,
        choices=["model", "view", "serializer"],
        help="The type of Django component to test."
    )
    parser.add_argument(
        "--project_root",
        default=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")),
        help="The root directory of the GuardianRoute project."
    )

    args = parser.parse_args()
    scaffold_django_test(args.app_name, args.target_name, args.project_root, args.type)