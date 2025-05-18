# Python & Django Style Guide

This document outlines the coding standards and best practices for Python and Django development in this project. Adherence to these guidelines will help maintain code quality, readability, and consistency.

## 1. General Python Conventions (PEP 8)

*   **Adherence:** Strictly follow [PEP 8 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/).
*   **Linters & Formatters:**
    *   **Linter:** Use **Flake8** for identifying PEP 8 violations, logical errors, and complexity issues.
        *   Configuration: (Define project-specific Flake8 configuration in `.flake8` or `setup.cfg` if necessary, e.g., max-line-length, excluded files/errors).
    *   **Formatter:** Use **Black** for automatic code formatting to ensure a consistent style.
        *   Run Black before committing code.
*   **Line Length:** Maximum 119 characters (if Black's default of 88 is too restrictive, otherwise stick to Black's default).
*   **Imports:**
    *   Order imports as follows:
        1.  Standard library imports (e.g., `import os`)
        2.  Related third-party imports (e.g., `import django`)
        3.  Local application/library specific imports (e.g., `from .models import MyModel`)
    *   Separate import groups with a blank line.
    *   Use absolute imports where possible.
    *   Use `isort` to automatically manage import sorting. Configure it to be compatible with Black.
*   **Naming Conventions:**
    *   `lowercase_with_underscores` for functions, methods, variables, and module names.
    *   `UPPERCASE_WITH_UNDERSCORES` for constants.
    *   `CapWords` (PascalCase) for class names.
    *   Protected members: prefix with a single underscore (e.g., `_internal_method`).
    *   Private members (name mangling): prefix with double underscores (e.g., `__private_attribute`). Use sparingly.
*   **Comments:**
    *   Write clear and concise comments for complex logic.
    *   Use docstrings for all public modules, functions, classes, and methods. Follow [PEP 257 -- Docstring Conventions](https://www.python.org/dev/peps/pep-0257/).
        *   Example (Sphinx/Google style):
            ```python
            def my_function(param1, param2):
                """Summarizes what the function does.

                Args:
                    param1 (str): Description of param1.
                    param2 (int): Description of param2.

                Returns:
                    bool: Description of the return value.

                Raises:
                    ValueError: If param1 is invalid.
                """
                # ... function logic ...
            ```
*   **Type Hinting:**
    *   Use type hints for all function signatures (arguments and return values) as per [PEP 484 -- Type Hints](https://www.python.org/dev/peps/pep-0484/).
    *   Use `mypy` for static type checking.

## 2. Django Specific Conventions

*   **Project Structure:**
    *   Follow the standard Django project and app structure.
    *   Keep apps focused and modular.
    *   Example:
        ```
        project_root/
        ├── manage.py
        ├── myproject/       # Project directory
        │   ├── __init__.py
        │   ├── settings.py
        │   ├── urls.py
        │   └── wsgi.py
        ├── app1/            # Django app
        │   ├── __init__.py
        │   ├── admin.py
        │   ├── apps.py
        │   ├── models.py
        │   ├── views.py
        │   ├── serializers.py # For DRF
        │   ├── urls.py
        │   ├── tests.py
        │   └── migrations/
        └── requirements.txt
        ```
*   **Models (`models.py`):**
    *   Use `verbose_name` and `verbose_name_plural` for model and field names.
    *   Define `__str__` methods for all models for better representation in the admin and shell.
    *   Add `created_at` and `updated_at` `DateTimeField`s to models where appropriate (e.g., `auto_now_add=True` and `auto_now=True`).
    *   Keep models focused on data representation. Business logic should primarily reside in views, services, or managers.
    *   Use custom model managers for complex queries or table-level logic.
*   **Views (`views.py`):**
    *   Prefer class-based views (CBVs) for reusability and structure, especially when using Django Rest Framework (DRF).
    *   Keep views thin. Complex business logic should be delegated to service layers or model methods/managers.
    *   Use DRF ViewSets and Serializers for API development.
*   **Serializers (`serializers.py` - DRF):**
    *   Define serializers clearly, specifying fields and any read-only/write-only attributes.
    *   Use nested serializers for related data where appropriate, but be mindful of performance (N+1 query problem).
    *   Implement custom validation logic within serializer `validate_<field>` methods or the `validate` method.
*   **URLs (`urls.py`):**
    *   Use descriptive URL names (e.g., `name='user-list'`).
    *   Group related URLs within app-specific `urls.py` files and include them in the project's main `urls.py`.
    *   Use DRF routers for ViewSets.
*   **Forms (`forms.py`):**
    *   Use Django forms for data validation and HTML form rendering if not using DRF for all interactions.
*   **Templates (if not a headless API):**
    *   Organize templates in app-specific `templates/<app_name>/` directories.
    *   Use template inheritance.
*   **Admin (`admin.py`):**
    *   Customize the Django admin interface for important models.
    *   Use `list_display`, `list_filter`, `search_fields`, etc., to improve usability.
*   **Settings (`settings.py`):**
    *   Use environment variables for sensitive information (e.g., `SECRET_KEY`, database credentials, API keys). Do not commit these to version control.
    *   Use a library like `python-decouple` or `django-environ` to manage environment variables.
    *   Split settings into base, development, testing, and production files if complexity warrants.
*   **Testing (`tests.py`):**
    *   Write unit tests for models, views, forms, serializers, and utility functions.
    *   Aim for high test coverage.
    *   Use Django's test framework and DRF's testing tools.
    *   Use factories (e.g., `factory_boy`) for creating test data.
*   **Database Migrations:**
    *   Always generate migration files (`makemigrations`) after model changes.
    *   Review migration files before applying them (`migrate`).
    *   Avoid manual editing of migration files unless absolutely necessary and you understand the implications.
    *   Keep migrations small and focused.

## 3. Security Best Practices

*   **Input Validation:** Always validate and sanitize user input (DRF serializers and Django forms help with this).
*   **SQL Injection:** Use Django's ORM; avoid raw SQL queries where possible. If raw SQL is necessary, use parameterized queries.
*   **Cross-Site Scripting (XSS):** Django templates auto-escape by default. Be cautious when using `mark_safe`.
*   **Cross-Site Request Forgery (CSRF):** Django has built-in CSRF protection; ensure it's enabled and used.
*   **Authentication & Authorization:** Use Django's built-in auth system or robust third-party packages (e.g., `django-allauth`). Implement proper permission checks (e.g., DRF permissions).
*   **Dependencies:** Keep dependencies updated to patch security vulnerabilities. Use tools like `pip-audit` or GitHub's Dependabot.

## 4. Performance Considerations

*   **Database Queries:**
    *   Use `select_related` and `prefetch_related` to optimize queries and avoid N+1 problems.
    *   Use `QuerySet.defer()` and `QuerySet.only()` to fetch only necessary fields.
    *   Use database indexes appropriately.
    *   Analyze queries using `django-debug-toolbar`.
*   **Caching:** Implement caching strategies (e.g., Django's caching framework) for frequently accessed data or computationally expensive operations.
*   **Asynchronous Tasks:** Use Celery or Django Q for long-running or background tasks.

## 5. Tooling & Workflow

*   **Virtual Environments:** Always use virtual environments (e.g., `venv`, `poetry`, `pipenv`).
*   **Version Control:** Use Git. Follow a consistent branching strategy (e.g., Gitflow).
*   **Code Reviews:** All code should be peer-reviewed before merging.
*   **Continuous Integration/Continuous Deployment (CI/CD):** Set up CI/CD pipelines (e.g., GitHub Actions, GitLab CI) to automate testing and deployment.

---
*This style guide is a living document and may be updated as the project evolves.*