# [Project Name] Project Template

This repository provides a standardized and opinionated template for starting new **Django (Python) and React** web application projects. It incorporates best practices and a suite of automation scripts, including foundational folder structures, pre-configured application templates, and essential documentation.

## Purpose

The goal of this template is to:
-   Drastically accelerate new project setup with ready-to-run application skeletons.
-   Ensure a high degree of consistency and standardization across projects.
-   Embed best practices for code structure, error handling, API design, and database management from the outset.
-   Provide a common, well-documented reference point for development teams.
-   Streamline development workflows with helper scripts for scaffolding, validation, and setup.

## Structure Overview

The template is organized as follows:

-   **/docs**: Contains all project documentation templates and plans.
-   **/backend_template**: A Django backend application structure (copied as `backend/`).
-   **/frontend_template**: A React frontend application structure (copied as `frontend/`).
-   **/scripts**: Utility scripts for initialization, scaffolding, etc.
-   `custom_modes.json`: Defines custom AI assistance modes.
-   `README.md`: This file (which will be customized for your new project).

---

## Getting Started with Your New Project

This guide will walk you through setting up your new project generated from this template.

### 1. Prerequisites

Before you begin, ensure you have the following software installed on your system. If not, please install them from their official websites:

*   **Python (version 3.8 or newer):**
    *   *Why?* The backend of your application is built with Python and Django.
    *   *Download:* [python.org](https://www.python.org/downloads/)
    *   *Check:* Open your terminal and type `python --version` or `python3 --version`.
*   **pip (Python Package Installer):**
    *   *Why?* Used to install Python libraries your backend needs.
    *   *Details:* Usually comes with Python. If not, see Python's installation guide.
*   **Node.js (LTS version recommended, e.g., 18.x or 20.x) and npm:**
    *   *Why?* The frontend of your application is built with React, which uses Node.js and npm (Node Package Manager) for managing packages and running scripts.
    *   *Download:* [nodejs.org](https://nodejs.org/)
    *   *Check:* Open your terminal and type `node --version` and `npm --version`.
*   **PostgreSQL (version 12 or newer recommended):**
    *   *Why?* This is the database system your application will use to store data.
    *   *Download:* [postgresql.org](https://www.postgresql.org/download/)
    *   *Note:* Ensure the PostgreSQL command-line tools (like `psql`) are added to your system's PATH during installation if you want to follow the database setup commands easily.
*   **Git:**
    *   *Why?* For version control, to track changes in your code.
    *   *Download:* [git-scm.com](https://git-scm.com/downloads/)
    *   *Check:* Open your terminal and type `git --version`.
*   **A Code Editor (e.g., Visual Studio Code):**
    *   *Why?* To write and edit your project's code.
    *   *Download (VS Code):* [code.visualstudio.com](https://code.visualstudio.com/)

### 2. Initialize Your New Project (If you haven't already)

If you are reading this in the `TEMPLATE_PROJECT_OUTPUT` directory, you first need to generate your actual project:

1.  **Clone or Copy the Template:** Obtain a local copy of the `TEMPLATE_PROJECT_OUTPUT` repository.
2.  **Run the Initialization Script:**
    *   Open your terminal (Command Prompt, PowerShell, Terminal app).
    *   Navigate to the root directory of the `TEMPLATE_PROJECT_OUTPUT` you just obtained.
    *   Execute the command:
        ```bash
        python scripts/initialize_new_project.py
        ```
    *   The script will prompt you for your new project's name (e.g., "My Awesome App").
    *   It will then create a new directory for your project (e.g., `C:\git\MyAwesomeApp` or `/users/you/git/MyAwesomeApp`), copy all template files into it, and customize them.
    *   The script will also offer to initialize a Git repository and install dependencies. It's recommended to say yes (press Enter for default) to these prompts.

### 3. Navigate to Your New Project Directory

In your terminal, change your current directory to your newly created project folder. The script will tell you this path at the end. For example:
```bash
cd C:\git\MyAwesomeApp
# or on macOS/Linux:
# cd /users/you/git/MyAwesomeApp
```
**(Replace with the actual path to *your* new project)**

**The rest of this README assumes you are in your new project's root directory.**

### 4. Post-Initialization Setup: Step-by-Step

Follow these steps carefully to get your new application running.

#### 4.1. Backend Setup

The backend is a Django application.

1.  **Navigate to the Backend Directory:**
    ```bash
    cd backend
    ```

2.  **Create and Activate a Python Virtual Environment (Highly Recommended!)**
    *   *Why do this?* A virtual environment keeps the Python packages (dependencies) for this project separate from other Python projects on your system. This prevents conflicts.
    *   **Commands:**
        ```bash
        # Make sure you are in the 'backend' directory
        python -m venv venv  # Or: python3 -m venv venv

        # To activate the virtual environment:
        # On Windows (Command Prompt/PowerShell):
        .\venv\Scripts\activate
        # On macOS/Linux (bash/zsh):
        source venv/bin/activate
        ```
    *   *Confirmation:* After activation, your terminal prompt should change to show `(venv)` at the beginning, like `(venv) C:\git\MyAwesomeApp\backend>`.

3.  **Install Python Dependencies (if not done by the script):**
    *   If the initialization script didn't install dependencies, or if you skipped it:
        ```bash
        # Make sure your virtual environment is active!
        pip install -r requirements.txt
        ```
    *   *What this does:* This command reads the `requirements.txt` file and installs all the Python libraries your backend needs to run.

#### 4.2. Database Setup (PostgreSQL)

Your application needs a PostgreSQL database to store its data.

1.  **Ensure PostgreSQL is Installed and Running:**
    *   If you haven't installed PostgreSQL, please do so from [postgresql.org](https://www.postgresql.org/download/).
    *   Make sure the PostgreSQL server is running. (How to do this depends on your operating system and installation method – consult PostgreSQL documentation if unsure).

2.  **Create a Database and User (Example using `psql`):**
    *   You'll need to create a dedicated database and a user for your application.
    *   Open a new terminal or use `psql`, the PostgreSQL command-line tool.
    *   Replace `myprojectuser`, `myprojectpass`, and `myprojectdb` with your own choices. For local development, these can be simple, but for production, use strong, unique credentials.

    1.  **Connect to `psql` as a superuser (often `postgres`):**
        ```bash
        psql -U postgres
        ```
        (You might be prompted for the `postgres` user's password if you set one during installation.)

    2.  **Create your application user:**
        ```sql
        CREATE USER myprojectuser WITH PASSWORD 'myprojectpass';
        ```
        *(Remember to replace `myprojectuser` and `myprojectpass`!)*

    3.  **Create your application database, owned by your new user:**
        ```sql
        CREATE DATABASE myprojectdb OWNER myprojectuser;
        ```
        *(Remember to replace `myprojectdb` and `myprojectuser`!)*

    4.  **Set recommended parameters for the user (optional but good for Django):**
        ```sql
        ALTER ROLE myprojectuser SET client_encoding TO 'utf8';
        ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';
        ALTER ROLE myprojectuser SET timezone TO 'UTC';
        ```

    5.  **Exit `psql`:**
        Type `\q` and press Enter.

#### 4.3. Configure the `.env` File

This file tells your application important secrets and settings, like how to connect to the database.

1.  **Locate the `.env` file:** It's in the main root folder of your new project (e.g., `C:\git\MyAwesomeApp\.env`). The initialization script created this for you.
2.  **Open `.env` in your code editor.**
3.  **Update `DATABASE_URL`:**
    *   Find the line that looks like: `DATABASE_URL=postgres://user:password@host:port/dbname_CHANGE_ME`
    *   Change it to match the database user, password, and database name you created in the previous step. For example:
        ```env
        DATABASE_URL=postgres://myprojectuser:myprojectpass@localhost:5432/myprojectdb
        ```
    *   *Note:* If your PostgreSQL server is not running on your local machine (`localhost`) or uses a different port than `5432`, you'll need to change those parts too.

4.  **Update `SECRET_KEY`:**
    *   Find the line: `SECRET_KEY='your_django_secret_key_here_CHANGE_ME'`
    *   This key is crucial for security. Replace the placeholder with a long, random string.
    *   **To generate a new secret key:**
        *   Open a Python interpreter (type `python` or `python3` in your terminal).
        *   Enter these commands:
            ```python
            import secrets
            print(secrets.token_urlsafe(50))
            ```
        *   Copy the long random string it prints.
        *   Paste it into your `.env` file as the value for `SECRET_KEY`, like this:
            ```env
            SECRET_KEY='COPIED_RANDOM_STRING_GOES_HERE_ASDFGHJKLQWERTYUIOP1234567890'
            ```

5.  **Review Other Settings (Optional for now):**
    *   `DEBUG=True`: This is fine for local development. **Change to `False` for production!**
    *   `ALLOWED_HOSTS=localhost 127.0.0.1`: This allows you to access the app from your own computer. You'll need to change this for production.
    *   The `.env` file may contain other settings (e.g., for email). You can configure these later as needed.

#### 4.4. Prepare the Database (Django Migrations)

1.  **Navigate to the `backend` directory in your terminal** (if you're not already there).
2.  **Ensure your Python virtual environment is active** (you should see `(venv)` in your prompt).
3.  **Run migrations:**
    ```bash
    python manage.py migrate
    ```
    *   *What this does:* This command applies the database schema (table structures, etc.) defined by your Django application to the PostgreSQL database you configured.

#### 4.5. Create a Superuser (Admin Account)

1.  **Ensure you are in the `backend` directory and your venv is active.**
2.  **Run the command:**
    ```bash
    python manage.py createsuperuser
    ```
3.  Follow the prompts to create a username, email address (optional), and a strong password for your admin account. This account will let you access the Django admin interface.

#### 4.6. Run the Backend Server

1.  **Ensure you are in the `backend` directory and your venv is active.**
2.  **Start the server:**
    ```bash
    python manage.py runserver
    ```
3.  You should see output indicating the server is running, typically at `http://127.0.0.1:8000/`. You can open this URL in your web browser. You might see a Django welcome page or a "Not Found" if no specific root URL is configured yet. This is normal.

#### 4.7. Frontend Setup

The frontend is a React application.

1.  **Open a new terminal window or tab.** (Leave your backend server running in the other one).
2.  **Navigate to the `frontend` directory in your new project:**
    ```bash
    # Example:
    # cd C:\git\MyAwesomeApp\frontend
    cd ../frontend  # If you were in the backend directory
    ```

3.  **Install JavaScript Dependencies (if not done by the script):**
    *   If the initialization script didn't install dependencies, or if you skipped it:
        ```bash
        npm install
        ```
        (Or `yarn install` if you prefer Yarn and have it installed).
    *   *What this does:* This command reads the `package.json` file and installs all the JavaScript libraries your frontend needs.

4.  **Review Frontend `.env` (Optional for now):**
    *   The `frontend` directory might also have an `.env.local` file (copied from `frontend_template/.env.example`).
    *   The default `REACT_APP_API_BASE_URL=http://localhost:8000/api/v1` should work if your backend is running on the default port `8000`. If your backend API is at a different URL, you'll need to update this.

5.  **Run the Frontend Server:**
    ```bash
    npm start
    ```
    (Or `yarn start`).
    *   This will usually compile the frontend application and open your default web browser to `http://localhost:3000/`. You should see your React application running.

### 5. Next Steps & Customization

Congratulations! Your basic project setup should now be complete.

*   **Version Control (if not done by script):**
    *   If a Git repository wasn't initialized by the script, navigate to your project's root directory and run:
        ```bash
        git init
        git add .
        git commit -m "Initial project setup from template"
        ```
*   **Customize Project Documentation:**
    *   Open [`docs/00_Project_Overview.md`](docs/00_Project_Overview.md:0) and fill in the details for *your* specific project.
    *   Review and update your project's main `README.md` (this file!). The script `python scripts/project_management/update_readme_todos.py` can help identify placeholders to change.
*   **Explore the Code:**
    *   Familiarize yourself with the structure in the `backend` and `frontend` directories.
    *   Review the example apps and components.
*   **`ARCHITECT_CONTEXT_GUIDE.md`:** When using Roo Code's Architect Mode for this project, provide the contents of [`ARCHITECT_CONTEXT_GUIDE.md`](ARCHITECT_CONTEXT_GUIDE.md:0) (located in the project root) as initial context to the Architect. This guide helps the Architect understand how to best leverage this template's structure, documentation, scripts, and specialized AI modes.
*   **Configure Pre-commit Hooks (Recommended):**
    *   Ensure `pre-commit` is installed: `pip install pre-commit` (ideally in a global Python environment or a shared development venv).
    *   In your project root, run: `python scripts/setup/configure_pre_commit_hooks.py`
    *   Then run: `pre-commit install`
    *   This sets up hooks that automatically check your code for style and quality before you commit it.

#### 5.1. Leveraging AI for Initial Project Planning Documents

Starting a new project involves crucial planning steps. This template provides foundational documents in the `/docs` directory to guide this process:

*   **[`docs/00_Project_Overview.md`](docs/00_Project_Overview.md:0)**: This document is vital for establishing a shared understanding of your project's purpose, goals, scope, target audience, and overall technical direction. It acts as the North Star for your development efforts, ensuring everyone is aligned.
*   **[`docs/03_Development_Guides/Database_Design_DBML_Template.md`](docs/03_Development_Guides/Database_Design_DBML_Template.md:0)**: Defines your project's data structure using DBML (Database Markup Language). A clear database design is critical for backend development, ensuring data integrity, and planning how information will be stored and related.
*   **[`docs/03_Development_Guides/API_Design_And_Mapping_Template.md`](docs/03_Development_Guides/API_Design_And_Mapping_Template.md:0)**: Outlines how different parts of your application (e.g., frontend, backend, potential external services) will communicate. A well-defined API map is essential for decoupled development, allowing teams to work independently and ensuring smooth integration.

You can significantly accelerate the process of populating these initial planning documents by using an AI chat assistant (like Roo, or other similar tools). Here's how:

**General Advice for AI-Assisted Document Creation:**

1.  **Provide the Template:** Copy the entire content of the relevant template file (e.g., [`docs/00_Project_Overview.md`](docs/00_Project_Overview.md:0)) and paste it directly into your chat with the AI. This gives the AI the structure it needs to work with.
2.  **Describe Your Project:** Give the AI a clear, concise, high-level description of your new project. Focus on its main purpose, key features, and the problem it aims to solve.
3.  **Engage in a Dialogue:** Instruct the AI to ask you clarifying questions for each section of the template. This turns the process into a collaborative effort, helping you think through the details and ensuring the AI has enough information to generate relevant content. Treat it as an interactive brainstorming session.

**Example Prompts to Get You Started:**

Here are some specific, actionable example prompts you can adapt. Remember to replace placeholders like `[Your Project Idea Name]` with your actual project details.

*   **For [`docs/00_Project_Overview.md`](docs/00_Project_Overview.md:0):**
    ```text
    I'm starting a new project called '[Your Project Idea Name]' and need help filling out the Project Overview document.
    Here's the template content from 'docs/00_Project_Overview.md':
    [Paste the full content of docs/00_Project_Overview.md here]

    My project is about [e.g., 'a web application for local artists to showcase their portfolios, connect with buyers, and manage commissions'].

    Please help me draft the content for each section of this Project Overview (Introduction, Scope, Target Audience, Technology Stack, etc.) based on my project idea. Ask me targeted questions for each section to help elicit the necessary details. Let's begin with the "1. Introduction" section.
    ```

*   **For Database Design (using [`docs/03_Development_Guides/Database_Design_DBML_Template.md`](docs/03_Development_Guides/Database_Design_DBML_Template.md:0)):**
    ```text
    I need to design the initial database schema for my project '[Your Project Idea Name]' using DBML.
    Here's the DBML template content from 'docs/03_Development_Guides/Database_Design_DBML_Template.md':
    [Paste the full content of docs/03_Development_Guides/Database_Design_DBML_Template.md here, or at least its key structural elements, conventions, and example tables]

    My project, '[Your Project Idea Name]', will primarily handle data related to [e.g., 'artists (with profiles, contact info), artworks (with details like title, medium, dimensions, price, images), buyers, and commission requests (linking artists and buyers, detailing requirements)'].

    Can you help me define the initial DBML tables for these core entities? For each table, suggest essential columns with appropriate data types (e.g., integer, varchar, text, boolean, timestamp, decimal), define primary keys (like 'id'), and establish foreign key relationships (e.g., an artwork belongs to an artist, a commission request links an artist and a buyer). Please include standard audit columns like 'created_at' and 'updated_at' in each table. Let's start by identifying the main tables: Users (for artists/buyers), Artworks, and CommissionRequests.
    ```

*   **For API Mapping (using [`docs/03_Development_Guides/API_Design_And_Mapping_Template.md`](docs/03_Development_Guides/API_Design_And_Mapping_Template.md:0)):**
    ```text
    I'm planning the API for my project '[Your Project Idea Name]' and need assistance outlining the initial RESTful endpoints.
    Here's the API Design and Mapping template:
    [Paste the full content of docs/03_Development_Guides/API_Design_And_Mapping_Template.md here, or at least its key structural elements like resource naming conventions, HTTP methods, and the example endpoint documentation format]

    The core functionalities of my project, '[Your Project Idea Name]', include [e.g., 'artist registration and login, artists uploading and managing their artworks, buyers browsing artworks, buyers initiating commission requests with artists, and users managing their profiles'].

    Based on these functionalities, please help me outline the initial API resources (e.g., /artists, /artworks, /commissions). For each resource, suggest common RESTful endpoints (like GET /artworks, POST /artworks, GET /artworks/{id}, PUT /artworks/{id}, DELETE /artworks/{id}), the corresponding HTTP methods, and a brief idea of the purpose and basic request/response data (e.g., for POST /artworks, the request might include title, description, image_url, artist_id; the response would be the newly created artwork details). Let's focus on the main CRUD operations for each core entity first.
    ```

By using these templates and AI assistance, you can create a solid foundation for your project much more efficiently. Remember to review and refine the AI's suggestions to ensure they accurately reflect your project's specific needs.

### 6. Troubleshooting Common Issues

*   **"Command not found" (e.g., `python`, `npm`, `psql`, `git`):**
    *   This usually means the software is not installed or its location is not added to your system's PATH environment variable. Revisit the "Prerequisites" section and ensure installation was completed correctly, including any options to "Add to PATH". You might need to restart your terminal or computer after installation.
*   **Python Virtual Environment Issues:**
    *   If `pip install` commands fail or you have strange Python errors, ensure your virtual environment (`venv`) is activated in the `backend` directory. You should see `(venv)` in your terminal prompt.
*   **Database Connection Errors (e.g., "could not connect to server," "password authentication failed"):**
    *   Double-check your `DATABASE_URL` in the `.env` file. Ensure the username, password, database name, host (`localhost`), and port (`5432`) exactly match what you set up in PostgreSQL.
    *   Make sure your PostgreSQL server is running.
*   **Frontend Fails to Connect to Backend (CORS errors, network errors):**
    *   Ensure your backend server is running (usually on `http://localhost:8000/`).
    *   Check the `REACT_APP_API_BASE_URL` in `frontend/.env.local` (or similar) points to the correct backend API URL.
    *   The backend template includes CORS (Cross-Origin Resource Sharing) configuration. By default, it might allow `http://localhost:3000`. If your frontend runs on a different port, you might need to adjust `CORS_ALLOWED_ORIGINS` in your root `.env` file and ensure `django-cors-headers` is correctly set up in `backend/yourprojectslug/settings.py`.

---

## Key Documents to Review First (In Your New Project)

-   [`docs/00_Project_Overview.md`](docs/00_Project_Overview.md:0) (Customize this!)
-   [`docs/02_Architecture/Project_Structure_Overview.md`](docs/02_Architecture/Project_Structure_Overview.md:0)
-   `docs/01_Coding_Standards/` (relevant style guides for Python/Django and React)

## Contributing to this Template

If you have suggestions for improving this base template itself, please refer to the [`CONTRIBUTING.md`](CONTRIBUTING.md:0) file in the original `TEMPLATE_PROJECT_OUTPUT` repository.

---

*This template is designed to be a starting point. Adapt and extend it to meet the unique requirements of your project.*