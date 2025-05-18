# Frontend Template (React)

This directory contains an opinionated React project template designed to accelerate frontend development for new projects. It includes a basic structure, common utilities, and an error handling framework.

## Structure

*   `public/`: Static assets and `index.html`.
*   `src/`: Main application source code.
    *   `App.js`: Root component, routing setup.
    *   `index.js`: Entry point of the application.
    *   `assets/`: Images, fonts, etc.
    *   `components/`: Reusable UI components.
        *   `common/`: General-purpose components (buttons, inputs, modals).
        *   `layout/`: Layout components (Header, Footer, Sidebar).
        *   `ErrorDisplay/`: Standardized error display.
        *   `GlobalErrorHandler/`: Handles global errors.
        *   `ErrorBoundary/`: Catches rendering errors.
        *   `ExampleFeature/`: Example feature components.
    *   `config/`: Application configuration (e.g., API base URL).
    *   `contexts/`: React Context providers (e.g., `ErrorContext.js`, `AuthContext.js`).
    *   `hooks/`: Custom React hooks (e.g., `useErrorHandler.js`).
    *   `pages/`: Top-level page components.
    *   `services/`: API service integration (e.g., `apiService.js`).
    *   `store/`: State management (e.g., Zustand, Redux Toolkit - if used).
    *   `styles/`: Global styles, theme configurations.
    *   `utils/`: Utility functions.
*   `package.json`: Project dependencies and scripts.
*   `.env.example`: Template for environment variables (e.g., `REACT_APP_API_BASE_URL`).
*   `.gitignore`: Git ignore file for React/Node.js projects.
*   `.eslintrc.json`: ESLint configuration.
*   `.prettierrc.json`: Prettier configuration.
*   `jsconfig.json` or `tsconfig.json`: For path aliases and TypeScript configuration.

## Getting Started (within a new project created from this template)

1.  **Navigate to this directory** (e.g., `cd frontend/`).
2.  **Install dependencies:**
    ```bash
    npm install
    # or
    # yarn install
    ```
3.  **Copy `.env.example` to `.env` (or `.env.local`) and fill in necessary values:**
    ```bash
    cp .env.example .env.local
    # Open .env.local and edit variables (e.g., REACT_APP_API_BASE_URL)
    ```
4.  **Run the development server:**
    ```bash
    npm start
    # or
    # yarn start
    ```

This template aims to provide a solid foundation with best practices for error handling and project structure. Customize it further to meet your project's specific needs.