# TEMPLATE_PROJECT_OUTPUT Enhancement Plan (v2)

## 1. Introduction

This document outlines a comprehensive, multi-phase plan to enhance the `TEMPLATE_PROJECT_OUTPUT` project. The goal is to create a more robust, opinionated, and standardized starting point for new projects, incorporating best practices observed from the `GuardianRoute` project and introducing new automation scripts to support development and ensure consistency. This plan aims to accelerate project setup, promote best practices, and reduce manual effort, including for AI-assisted development using custom modes.

## 2. Overall Phased Approach

The enhancement will be carried out in the following phases:

```mermaid
graph TD
    A[Start Enhancement Process] --> P1[Phase 1: Create Opinionated Application Templates];
    P1 --> T1_1[Task 1.1: Define & Create backend_template (Django)];
    P1 --> T1_2[Task 1.2: Define & Create frontend_template (React)];

    A --> P2[Phase 2: Enhance Initialization Script];
    P2 --> T2_1[Task 2.1: Modify initialize_new_project.py for New Templates];
    P2 --> T2_2[Task 2.2: Add Config File Generation (.env)];
    P2 --> T2_3[Task 2.3 (Optional): Add Automated Setup Steps (git init, etc.)];

    A --> P3[Phase 3: Develop/Enhance Standardization Scripts];
    P3 --> T3_1[Task 3.1: Review & Enhance Existing Validation Scripts];
    P3 --> T3_2[Task 3.2: Create New Generation Scripts];
    P3 --> T3_3[Task 3.3: Create New Validation Scripts];
    P3 --> T3_4[Task 3.4: Enhance Existing Scaffolding Scripts];
    P3 --> T3_5[Task 3.5: Create New Scaffolding Scripts];
    P3 --> T3_6[Task 3.6: Create New Setup/Management Scripts];

    A --> P4[Phase 4: Update & Augment Documentation];
    P4 --> T4_1[Task 4.1: Update Core Project Docs (README, Structure Overview)];
    P4 --> T4_2[Task 4.2: Update/Create Development Guides];
    P4 --> T4_3[Task 4.3: Add Template Project Meta-Docs (CONTRIBUTING, CHANGELOG)];
    P4 --> T4_4[Task 4.4: Add SECURITY.md Template for New Projects];

    A --> P5[Phase 5: Standardize Tooling & Configuration];
    P5 --> T5_1[Task 5.1: Add/Verify Linter/Formatter Configs];
    P5 --> T5_2[Task 5.2: Add .pre-commit-config.yaml Template];
    P5 --> T5_3[Task 5.3: Review/Enhance Root .gitignore];
    
    P1 & P2 & P3 & P4 & P5 --> Z[End: Enhanced Template Project Ready];
```

## 3. Detailed Plan by Phase

### Phase 1: Create Opinionated Application Templates

*   **Task 1.1: Define & Create `backend_template/` (Opinionated Django)**
    *   **Objective:** Provide a feature-rich starting point for Django backends, incorporating `GuardianRoute` best practices.
    *   **Key Contents & `GuardianRoute` Learnings:**
        *   **Project Structure:**
            *   `core_project_name/` (Django project dir) with environment-aware `settings.py` (using `python-dotenv`), root `urls.py` (with `/api/v1/` namespace as seen in `GuardianRoute.API_Mapping.txt`).
            *   `main_app/` (Example app) with:
                *   Example model adhering to `GuardianRoute.DBML.txt` naming conventions (PascalCase table, snake_case fields) and including `created_at`, `updated_at` (potentially via a base model).
                *   DRF `APIView` & `ModelViewSet` (following `GuardianRoute.API_Mapping.txt` structure).
                *   `ModelSerializer` (following `GuardianRoute.API_Mapping.txt` structure).
                *   App-specific `urls.py` registered with `DefaultRouter`.
                *   Admin registration for the model.
                *   Basic tests.
            *   `users_app/` (Common app for custom user model) with `AbstractUser` model (including `is_staff`, `is_superuser` as in `GuardianRoute.DBML.txt`), admin, serializer.
            *   `permissions_app/` (Optional, for RBAC): Stubs for `Module`, `Role`, `RolePermission` models and `AccessLevel` enum based on `GuardianRoute.DBML.txt`, and an example `ModulePermission` class for DRF.
            *   `common/` (Utility app/directory) for shared utilities (e.g., base model with audit fields).
        *   **Configuration:**
            *   `requirements.txt`: `Django`, `djangorestframework`, `psycopg2-binary`, `python-dotenv`, `gunicorn`, `drf-spectacular` (for API docs, as `GuardianRoute` has detailed API mapping).
            *   `.env.example`: Placeholders for `SECRET_KEY`, `DEBUG`, `DATABASE_URL`, etc.
            *   Comprehensive Django `.gitignore`.
            *   `pyproject.toml` (for Black, isort) and/or `.flake8`, `.editorconfig`.
        *   **Features:**
            *   Basic API documentation setup with `drf-spectacular`.
            *   JWT Authentication setup using `rest_framework_simplejwt` (as per `GuardianRoute.API_Mapping.txt`).
            *   A brief README within `backend_template`.

*   **Task 1.2: Define & Create `frontend_template/` (Opinionated React)**
    *   **Objective:** Provide a feature-rich starting point for React frontends, incorporating `GuardianRoute` error handling.
    *   **Key Contents & `GuardianRoute` Learnings:**
        *   **Project Structure (e.g., based on Create React App, then customized):**
            *   `src/` with `App.js` (routing, global providers), `index.js`.
            *   Subdirectories: `assets/`, `components/` (with `common/`, `layout/`, `ExampleFeature/`, `ErrorDisplay/`, `GlobalErrorHandler/`, `ErrorBoundary/`), `config/`, `contexts/` (with `ErrorContext.js`), `hooks/` (with `useErrorHandler.js`), `pages/`, `services/` (with `apiService.js` demonstrating `ApiError`), `styles/`, `utils/`.
        *   **Configuration:**
            *   `package.json`: `react`, `react-router-dom`, `axios`, state management library (e.g., Zustand or Redux Toolkit). Dev: `eslint`, `prettier`, testing libraries.
            *   `.env.example`: `REACT_APP_API_BASE_URL`.
            *   Comprehensive React/Node `.gitignore`.
            *   `.eslintrc.json`, `.prettierrc.json`, `jsconfig.json` (for absolute paths), `.editorconfig`.
        *   **Features:**
            *   Pre-configured error handling framework based on `GuardianRoute.ErrorHandlingGuide.md`.
            *   Example page demonstrating data fetching, form handling, routing, state management, and usage of the error handling framework.
            *   A brief README within `frontend_template`.

### Phase 2: Enhance Initialization Script (`scripts/initialize_new_project.py`)

*   **Task 2.1: Modify `initialize_new_project.py` for New Templates**
    *   Rename `backend_template` to `backend` (or `[project_name]_backend`) and `frontend_template` to `frontend` (or `[project_name]_frontend`) in the new project.
    *   Implement placeholder replacement within the new `backend` and `frontend` directories (e.g., Django project name in `settings.py`, React app name in `package.json`, update internal project name references in example code).

*   **Task 2.2: Add Configuration File Generation**
    *   The script should create a root `.env` file in the new project by copying/merging from `.env.example` files found in root, `backend_template`, and `frontend_template`.

*   **Task 2.3 (Optional): Add Automated Setup Steps**
    *   Add optional flags/prompts to:
        *   Initialize a Git repository (`git init`).
        *   Run `pip install -r requirements.txt` (backend).
        *   Run `npm install` (frontend).

### Phase 3: Develop/Enhance Standardization Scripts

*   **Task 3.1: Review & Potentially Enhance Existing Validation Scripts**
    *   **`scripts/validation/validate_api_mapping.py`**: Review and enhance to cover all conventions observed in `GuardianRoute.API_Mapping.txt` (required sections, path/link formatting, terminology, HTTP methods).
    *   **`scripts/validation/validate_dbml.py`**: Review and enhance to cover all conventions from `GuardianRoute.DBML.txt` (naming, audit columns, PKs, enums, relationships, versioning header).

*   **Task 3.2: Create New Generation Scripts**
    *   **`scripts/generation/generate_dbml_from_django_models.py`**: To introspect Django models and generate/update DBML, aiding consistency.

*   **Task 3.3: Create New Validation Scripts**
    *   **`scripts/validation/check_error_handling_patterns_react.js`** (or Python equivalent): To scan React components for adherence to error handling patterns from `GuardianRoute.ErrorHandlingGuide.md`.

*   **Task 3.4: Enhance Existing Scaffolding Scripts**
    *   **`scripts/scaffolding/create_django_app.py`**: Enhance to create more opinionated app structures (basic models with audit fields, views, serializers, URLs, admin).
    *   **`scripts/scaffolding/create_react_component.js`**: Enhance to scaffold components aligned with error handling boilerplate and opinionated directory structure.

*   **Task 3.5: Create New Scaffolding Scripts**
    *   **`scripts/scaffolding/scaffold_drf_resource.py`**: For comprehensive DRF resource scaffolding (model, serializer, ModelViewSet, URL registration, basic tests).

*   **Task 3.6: Create New Setup/Management Scripts**
    *   **`scripts/setup/configure_pre_commit_hooks.py`** (or shell script): To automate pre-commit setup.
    *   **`scripts/project_management/update_readme_todos.py`**: To help customize the `README.md` in new projects by replacing placeholders or prompting for input.

### Phase 4: Update & Augment Documentation

*   **Task 4.1: Update Core Project Docs**
    *   Revise `TEMPLATE_PROJECT_OUTPUT/README.md` and `TEMPLATE_PROJECT_OUTPUT/docs/02_Architecture/Project_Structure_Overview.md` to reflect the new `backend` and `frontend` application structures and the enhanced initialization script.
    *   Update the "Getting Started" section in `README.md`.

*   **Task 4.2: Update/Create Development Guides**
    *   Create `TEMPLATE_PROJECT_OUTPUT/docs/03_Development_Guides/Frontend_Error_Handling_Guide.md` adapted from `GuardianRoute.ErrorHandlingGuide.md` (generic paths/examples).
    *   Review and update `TEMPLATE_PROJECT_OUTPUT/docs/03_Development_Guides/Database_Design_DBML_Template.md` to align with `GuardianRoute.DBML.txt` best practices (e.g., versioning/changelog within DBML).
    *   Review and update `TEMPLATE_PROJECT_OUTPUT/docs/03_Development_Guides/API_Design_And_Mapping_Template.md` based on `GuardianRoute.API_Mapping.txt`.
*   **Detailed Plan for Task 4.2 Updates (Approved):**
        *   **Objective:** To refine the development guide templates based on `GuardianRoute` project best practices, ensuring they are comprehensive and actionable.
        *   **Reference Documents Used:**
            *   `GuardianRoute.ErrorHandlingGuide.md`
            *   `GuardianRoute.DBML.txt`
            *   `GuardianRoute.API_Mapping.txt`
        *   **Planned Updates for `docs/03_Development_Guides/Frontend_Error_Handling_Guide.md`:**
            *   No changes to Sections 1-4 (Overview, Core Components, Error Types, API Service Error Handling).
            *   Enhancements to Section 5 "Best Practices":
                *   Add new subsection: "5.1 Handling Multiple Errors in a Component" with examples.
                *   Add new subsection: "5.2 Naming Conventions for Error Handlers" with examples.
                *   Expand subsection "Logging" to include notes on "Enhanced API Request/Response Logging," emphasizing redaction of sensitive data.
                *   Add new subsection: "Specific Considerations for Authentication Errors," including advice on user feedback, client-side validation, and secure error messaging.
        *   **Planned Updates for `docs/03_Development_Guides/Database_Design_DBML_Template.md`:**
            *   Add a new section: "1.1 Versioning and Changelog" at the beginning of the document, with an example.
            *   Refine "General Conventions" (Section 1.2 or merged): Reinforce PascalCase for tables, PK conventions (`[table_singular_name]_id` or `id`), inclusion of `created_at`/`updated_at` audit columns, and clarify usage of DBML notes/comments.
            *   Enhance "Enum Definitions": Add a note encouraging domain-specific enums, inspired by `GuardianRoute`.
            *   Update "Table Definitions" examples:
                *   Make the `Users` table example more Django-centric (e.g., `id integer [pk, increment]`, standard Django user model fields).
                *   Ensure consistent use of `created_at` and `updated_at` in all examples.
                *   Add a note and example illustrating polymorphic-like ownership using separate nullable Foreign Keys (similar to `GuardianRoute`'s `Document` table).
            *   Refine "Notes on Django Integration": Explicitly state that the DBML `Users` table should mirror Django's `User` model fields if the default is used, and reiterate that `ManyToManyField` implies explicitly defined junction tables in DBML.
        *   **Planned Updates for `docs/03_Development_Guides/API_Design_And_Mapping_Template.md`:**
            *   Section 1 "General Principles": Add a note that permissions are often handled by a combination of `IsAuthenticated` and a more granular system (e.g., `ModulePermission`), and that template examples will use placeholders like `[CustomPermission (ViewResource)]`.
            *   Section 6 "API Endpoint Documentation Template":
                *   Resource Block: Add a "Module (for Permissions):" field (e.g., `Module (for Permissions): [e.g., Locations Management, Users Management]`).
                *   Endpoint Details (for List, Create, Retrieve, Update, Patch, Delete, Custom Action):
                    *   Permissions: Update placeholders to be more specific (e.g., `Permissions: IsAuthenticated, [CustomPermission (ViewResourceName)]`).
                    *   Request Body (for POST/PUT/PATCH): Add a note to refer to the associated Serializer for detailed field validation rules.
                    *   Error Responses:
                        *   Ensure `401 Unauthorized`, `403 Forbidden`, and `404 Not Found` are consistently listed.
                        *   Clarify the `400 Bad Request` validation error response format, including a structure for field-specific errors.
                        *   Add `409 Conflict` as a potential error for `POST` if creating a duplicate resource with unique constraints.
                    *   Custom Actions: Emphasize clear documentation for request body and success response structure. Note that custom actions often have specific permission requirements.
            *   General Formatting/Consistency: Review all endpoint examples for consistent placeholder usage. Ensure "Base Path" is clearly defined.

*   **Task 4.3: Add Template Project Meta-Docs**
    *   Create `TEMPLATE_PROJECT_OUTPUT/CONTRIBUTING.md`: Guidelines for contributing to the template project itself.
    *   Create `TEMPLATE_PROJECT_OUTPUT/CHANGELOG.md`: To track versions and changes to the template.

*   **Task 4.4: Add `SECURITY.md` Template**
    *   Include a `TEMPLATE_PROJECT_OUTPUT/docs/SECURITY.md` template for new projects to fill out.

### Phase 5: Standardize Tooling & Configuration

*   **Task 5.1: Add/Verify Linter/Formatter Configurations**
    *   Ensure `.flake8`, `pyproject.toml` (for Black/isort), `.editorconfig`, `.eslintrc.json`, `.prettierrc.json` are present at the root of `TEMPLATE_PROJECT_OUTPUT` and/or within the `backend_template` and `frontend_template` as appropriate.

*   **Task 5.2: Add `.pre-commit-config.yaml` Template**
    *   Include a template `.pre-commit-config.yaml` with common hooks (linters, formatters).
    *   Add documentation on setting up pre-commit hooks.

*   **Task 5.3: Review/Enhance Root `.gitignore`**
    *   Ensure the root `.gitignore` in `TEMPLATE_PROJECT_OUTPUT` is comprehensive.

## 4. Conclusion

This enhanced plan provides a detailed roadmap for evolving `TEMPLATE_PROJECT_OUTPUT` into a highly effective and standardized foundation for new projects. Implementation will be iterative, and feedback will be incorporated throughout the process.