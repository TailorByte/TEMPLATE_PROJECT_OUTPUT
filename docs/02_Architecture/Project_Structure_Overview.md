# Project Structure Overview

This document outlines the recommended project structure for applications built using this template. A well-defined structure promotes consistency, maintainability, and scalability.

## 1. Top-Level Directory Structure

The root of the project will typically contain:

```
[project_root]/
├── backend/                     # Opinionated Django backend application
│   ├── core_project_name/       # Main Django project configuration (renamed on init)
│   ├── common/                  # Shared utilities, BaseModel
│   ├── users_app/               # Custom user management
│   ├── main_app/                # Example application with primary business logic
│   ├── permissions_app/         # RBAC models and logic (stubs)
│   ├── manage.py
│   ├── requirements.txt
│   ├── .env.example
│   ├── .gitignore
│   └── pyproject.toml           # Linter/formatter configs
├── frontend/                    # Opinionated React frontend application
│   ├── public/
│   ├── src/
│   │   ├── components/          # Reusable UI components (ErrorDisplay, etc.)
│   │   ├── contexts/            # React Context (ErrorContext)
│   │   ├── hooks/               # Custom hooks (useErrorHandler)
│   │   ├── services/            # API service (apiService.js)
│   │   └── ...                  # Other standard React folders (pages, assets, etc.)
│   ├── package.json
│   ├── .env.example
│   ├── .gitignore
│   ├── .eslintrc.json
│   ├── .prettierrc.json
│   └── jsconfig.json
├── docs/                        # Project documentation (like this file)
├── scripts/                     # Utility and automation scripts
│   ├── initialize_new_project.py
│   ├── scaffolding/
│   ├── validation/
│   └── ...
├── .gitignore                   # Top-level .gitignore
├── README.md                    # Top-level README for the entire project
├── custom_modes.json            # Roo Code custom mode definitions
└── .env                         # Root environment variables (generated, GITIGNORED)
└── .env.example                 # Optional: Root example environment variables
```

*   **`backend/`**: Contains the Django/DRF backend application.
*   **`frontend/`**: Contains the React frontend application.
*   **`docs/`**: Contains all project-related documentation, guides, and templates.
*   **`README.md`**: Provides an overview of the entire project, setup instructions, and links to key documentation.
*   **`docker-compose.yml` (Optional)**: If using Docker, this file defines the services, networks, and volumes for local development and potentially production.
*   **`.env.example`**: An example file showing the structure of required environment variables. Actual `.env` files (containing secrets) should be in `.gitignore`.

## 2. Backend Structure (Django)

The `backend/` directory follows a standard Django project layout:

```
backend/  (Generated from backend_template)
├── manage.py                  # Django's command-line utility
├── [project_name_slug]/       # Main Django project configuration (e.g., `yournewapp_slug`)
│   ├── __init__.py
│   ├── settings.py            # Project settings (environment-aware using .env)
│   ├── urls.py                # Root URL configurations (includes API docs, JWT)
│   ├── wsgi.py
│   └── asgi.py
├── common/                    # Shared utilities and base models
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py              # Contains BaseModel (created_at, updated_at)
│   └── ...                    # admin.py, tests.py, views.py (mostly empty)
├── users_app/                 # Custom user management
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py              # Custom User model inheriting AbstractUser & BaseModel
│   ├── admin.py               # Registers custom User model
│   ├── serializers.py         # Basic UserSerializer
│   ├── views.py               # Placeholder for user-related views/API endpoints
│   ├── urls.py                # Placeholder
│   └── tests.py               # Basic model tests
├── main_app/                  # Example app for primary business logic
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py              # ExampleItem model inheriting BaseModel
│   ├── admin.py               # Registers ExampleItem
│   ├── serializers.py         # ExampleItemSerializer
│   ├── views.py               # ExampleItemViewSet
│   ├── urls.py                # Registers ExampleItemViewSet
│   └── tests.py               # Basic tests for ExampleItem model and API
├── permissions_app/           # Optional: For Role-Based Access Control (RBAC)
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py              # Stubs for Module, Role, UserRole, RolePermission, AccessLevel enum
│   ├── admin.py               # Registers RBAC models
│   ├── permissions.py         # Stub for ModulePermission class
│   ├── serializers.py         # Stubs for RBAC serializers
│   ├── views.py               # Placeholder
│   ├── urls.py                # Placeholder
│   └── tests.py               # Basic model tests for RBAC
├── static_collected/          # For `collectstatic` output (GITIGNORED by backend/.gitignore)
├── media/                     # User-uploaded media files (GITIGNORED by backend/.gitignore)
├── requirements.txt           # Python dependencies (Django, DRF, python-dotenv, etc.)
├── pyproject.toml             # Black, isort, Flake8 configurations
├── .env.example               # Example environment variables for the backend
└── .gitignore                 # Standard Django .gitignore
```

*   **`[project_name_slug]/`**: The main Django project configuration directory (name derived from user input).
    *   `settings.py`: Uses `python-dotenv` to load environment variables. Includes configurations for DRF, JWT, and `drf-spectacular`.
*   **`common/`**: App for shared code, including `BaseModel` with `created_at` and `updated_at` fields.
*   **`users_app/`**: Provides a custom `User` model (email as username, inherits `BaseModel`) and basic admin setup.
*   **`main_app/`**: An example application demonstrating a model (`ExampleItem`), serializer, `ModelViewSet`, admin registration, and URL setup.
*   **`permissions_app/`**: Contains stubs for a Role-Based Access Control system (Module, Role, UserRole, RolePermission models, AccessLevel enum, and a basic `ModulePermission` class), inspired by `GuardianRoute`.
*   **`requirements.txt`**: Lists core Python dependencies.
*   **`pyproject.toml`**: Configures Black, isort, and Flake8 for code quality.

## 3. Frontend Structure (React)

The `frontend/` directory (generated from `frontend_template`) provides an opinionated starting point for React applications:

```
frontend/
├── node_modules/              # Project dependencies (GITIGNORED)
├── public/                    # Static assets (index.html, favicon.ico, etc.)
│   ├── index.html
│   └── ...
├── src/                       # Main application source code
│   ├── App.js                 # Root React component with basic routing & ErrorBoundary
│   ├── index.js               # Entry point, wraps App with ErrorProvider
│   ├── index.css              # Basic global styles
│   ├── reportWebVitals.js
│   ├── assets/                # (Placeholder) Static assets like images, fonts
│   ├── components/            # Reusable UI components
│   │   ├── ErrorBoundary/     # ErrorBoundary.js
│   │   ├── ErrorDisplay/      # ErrorDisplay.js, ErrorDisplay.module.css
│   │   ├── GlobalErrorHandler/  # GlobalErrorHandler.js
│   │   └── ...                # (Placeholder for common, layout, feature components)
│   ├── contexts/              # React Context providers
│   │   └── ErrorContext.js    # Global error state management
│   ├── hooks/                 # Custom React Hooks
│   │   └── useErrorHandler.js # Component-level error handling
│   ├── pages/                 # (Placeholder) Top-level page components
│   ├── services/              # API interaction layer
│   │   └── apiService.js      # Configured Axios instance, ApiError class
│   ├── store/                 # (Placeholder) Global state management (e.g., Zustand, Redux)
│   ├── styles/                # (Placeholder) Global styles, theme variables
│   └── utils/                 # (Placeholder) General utility functions
├── .env.example               # Example environment variables (e.g., REACT_APP_API_BASE_URL)
├── .gitignore                 # Standard Node/React .gitignore
├── .eslintrc.json             # ESLint configuration (extends react-app, integrates Prettier)
├── .prettierrc.json           # Prettier configuration
├── jsconfig.json              # Enables absolute imports from src/
├── package.json               # Project dependencies and scripts (npm/yarn)
└── README.md                  # Frontend specific README (from frontend_template)
```

*   **Error Handling Framework**: A key feature is the pre-configured error handling system based on `GuardianRoute`'s `ErrorHandlingGuide.md`, including `ErrorContext`, `useErrorHandler` hook, `ErrorDisplay`, `GlobalErrorHandler`, and `ErrorBoundary` components.
*   **API Service**: A basic `apiService.js` is provided with an Axios instance and a custom `ApiError` class for standardized API error management.
*   **Linting & Formatting**: ESLint and Prettier are configured for code quality.
*   **Absolute Imports**: `jsconfig.json` is set up for cleaner imports from the `src/` directory.

## 4. Documentation Structure (`docs/`)

The `docs/` directory is organized to provide clear and accessible information:

```
docs/
├── 00_Project_Overview.md
├── 01_Coding_Standards/
│   ├── Python_Django_StyleGuide.md
│   └── React_StyleGuide.md
├── 02_Architecture/
│   ├── Authentication_Guide.md
│   ├── Error_Handling_Guide.md
│   └── Project_Structure_Overview.md (this file)
├── 03_Development_Guides/
│   ├── API_Design_And_Mapping_Template.md
│   ├── Database_Design_DBML_Template.md
│   ├── Model_Refactoring_Guide.md
│   └── Testing_Strategy_Guide.md
├── 04_Deployment/
│   └── Deployment_Considerations.md
└── ADR/  # Optional: Architecture Decision Records
    └── 001-use-jwt-for-authentication.md
```

*   Numbered prefixes help maintain a logical order.
*   **`ADR/` (Optional)**: Architecture Decision Records can be very useful for documenting significant architectural choices and their rationale.

## 5. Key Principles for Structuring

*   **Modularity/Separation of Concerns:** Group related code together. Django apps and React feature folders are examples of this.
*   **Discoverability:** Make it easy for developers to find the code they are looking for.
*   **Scalability:** The structure should accommodate project growth without becoming chaotic.
*   **Team Conventions:** While this guide provides a template, teams should agree on specific conventions and adapt the structure as needed.

---
*This structure is a recommendation and can be adapted based on project size, complexity, and team preferences.*