# Backend Template (Django)

This directory contains an opinionated Django project template designed to accelerate backend development for new projects.

## Structure

*   `core_project_name/`: Main Django project directory.
    *   `settings.py`: Project settings (environment-aware).
    *   `urls.py`: Root URL configurations.
    *   ...
*   `main_app/`: An example application with basic CRUD and API examples.
*   `users_app/`: Application for custom user model management.
*   `permissions_app/`: (Optional) Application for Role-Based Access Control.
*   `common/`: Shared utilities, base models, etc.
*   `manage.py`: Django's command-line utility.
*   `requirements.txt`: Python dependencies.
*   `.env.example`: Template for environment variables.
*   `.gitignore`: Git ignore file for Django projects.
*   `pyproject.toml`: Configuration for tools like Black, isort, Flake8.

## Getting Started (within a new project created from this template)

1.  **Navigate to this directory** (e.g., `cd backend/`).
2.  **Create and activate a Python virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    # venv\Scripts\activate    # Windows
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Copy `.env.example` to `.env` and fill in the necessary values:**
    ```bash
    cp .env.example .env
    # Open .env and edit variables
    ```
5.  **Run database migrations:**
    ```bash
    python manage.py migrate
    ```
6.  **Create a superuser (optional):**
    ```bash
    python manage.py createsuperuser
    ```
7.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

This template aims to provide a solid foundation. Customize it further to meet your project's specific needs.