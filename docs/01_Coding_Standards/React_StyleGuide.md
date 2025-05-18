# React & JavaScript Style Guide

This document outlines coding standards and best practices for React and JavaScript development in this project. Consistency in coding style improves readability, maintainability, and collaboration.

## 1. General JavaScript Conventions

*   **ECMAScript Version:** Use modern JavaScript (ES6+ features).
*   **Linters & Formatters:**
    *   **Linter:** Use **ESLint** to identify problematic patterns and enforce coding standards.
        *   Configuration: A base ESLint configuration (e.g., `eslint-config-react-app`, `eslint-config-airbnb`) should be established in `.eslintrc.js` or `package.json`. Customize rules as needed.
    *   **Formatter:** Use **Prettier** for automatic code formatting.
        *   Integrate Prettier with ESLint (`eslint-plugin-prettier`, `eslint-config-prettier`) to avoid conflicts.
        *   Run Prettier before committing code.
*   **Variables:**
    *   Prefer `const` by default.
    *   Use `let` for variables that need to be reassigned.
    *   Avoid `var`.
*   **Naming Conventions:**
    *   `camelCase` for variables, functions, and instance methods.
    *   `PascalCase` (CapWords) for classes and React components.
    *   `UPPERCASE_WITH_UNDERSCORES` for constants (e.g., action types in Redux).
*   **Modules:**
    *   Use ES6 modules (`import`/`export`).
    *   Prefer named exports over default exports for better clarity and refactorability, unless a module truly has one primary export (like a main component).
    *   Order imports:
        1.  React and core library imports (e.g., `import React from 'react';`)
        2.  Third-party library imports (e.g., `import axios from 'axios';`)
        3.  Absolute imports from within the project (e.g., `import MyComponent from 'src/components/MyComponent';`)
        4.  Relative imports (e.g., `import utils from './utils';`)
        5.  CSS or asset imports (e.g., `import './styles.css';`)
    *   Separate import groups with a blank line.
*   **Functions:**
    *   Prefer arrow functions for anonymous functions and when `this` context is important (e.g., callbacks in class components, though functional components with hooks are preferred).
    *   Use regular functions for top-level function declarations or object methods where `this` binding is intentional.
*   **Comments:**
    *   Write clear JSDoc-style comments for functions and complex logic.
        ```javascript
        /**
         * Calculates the sum of two numbers.
         * @param {number} a - The first number.
         * @param {number} b - The second number.
         * @returns {number} The sum of a and b.
         */
        const sum = (a, b) => a + b;
        ```
*   **Type Checking (Optional but Recommended):**
    *   Consider using **TypeScript** for larger projects to add static typing.
    *   If not using TypeScript, use **PropTypes** for runtime type checking of React component props.

## 2. React Specific Conventions

*   **Component Structure:**
    *   **Functional Components with Hooks:** Prefer functional components with Hooks over class components for new development.
    *   **File Naming:** Use PascalCase for component file names (e.g., `UserProfile.js`, `Button.jsx`).
    *   **Folder Structure:**
        *   Group components by feature or domain in a `src/components/` or `src/features/` directory.
        *   Consider co-locating styles, tests, and stories with their components:
            ```
            src/components/Button/
            ├── Button.jsx
            ├── Button.module.css  (or Button.scss)
            ├── Button.test.js
            └── Button.stories.js
            ```
*   **JSX:**
    *   Use parentheses for multi-line JSX.
    *   Always include `key` props when rendering lists of elements.
    *   Use camelCase for HTML attributes (e.g., `className` instead of `class`, `onClick` instead of `onclick`).
    *   Self-close tags with no children: `<MyComponent />`.
*   **Props:**
    *   Destructure props at the beginning of the component.
    *   Define `propTypes` (or use TypeScript interfaces) for all components to specify expected prop types and whether they are required.
    *   Define `defaultProps` for non-required props.
        ```javascript
        import React from 'react';
        import PropTypes from 'prop-types';

        const Greeting = ({ name, enthusiasmLevel }) => {
          return <p>Hello, {name}{'!'.repeat(enthusiasmLevel)}</p>;
        };

        Greeting.propTypes = {
          name: PropTypes.string.isRequired,
          enthusiasmLevel: PropTypes.number,
        };

        Greeting.defaultProps = {
          enthusiasmLevel: 1,
        };

        export default Greeting;
        ```
*   **State Management:**
    *   Use the `useState` hook for simple component-level state.
    *   For more complex global state, consider:
        *   React Context API (for moderately complex state or theming).
        *   Libraries like Redux, Zustand, or Recoil for large-scale applications.
    *   If using Redux:
        *   Follow a structured approach (e.g., Redux Toolkit, Ducks pattern).
        *   Keep reducers pure.
        *   Use selectors to derive data from the state.
*   **Side Effects:**
    *   Use the `useEffect` hook for side effects like data fetching, subscriptions, or manually changing the DOM.
    *   Provide a dependency array to `useEffect` to control when it runs.
    *   Clean up side effects (e.g., unsubscribe from subscriptions, clear timers) in the return function of `useEffect`.
*   **Event Handling:**
    *   Name event handlers `handleEventName` (e.g., `handleClick`, `handleSubmit`).
    *   Pass event handlers as props (e.g., `onClick={handleClick}`).
*   **Conditional Rendering:**
    *   Use clear and concise methods for conditional rendering:
        *   Ternary operators for simple conditions: `{isLoggedIn ? <UserProfile /> : <LoginForm />}`
        *   Logical `&&` operator for short-circuiting: `{showWarning && <WarningMessage />}`
        *   Explicit `if` statements or helper functions for more complex logic.
*   **Styling:**
    *   Choose a consistent styling approach:
        *   **CSS Modules:** (Recommended for component-scoped styles) `styles.module.css`
        *   **Styled-components / Emotion:** (CSS-in-JS)
        *   **Global CSS:** Use sparingly, typically for base styles and resets.
        *   **Utility CSS Frameworks:** (e.g., Tailwind CSS)
    *   Avoid inline styles for anything beyond trivial dynamic styling.
*   **Accessibility (a11y):**
    *   Write semantic HTML.
    *   Use ARIA attributes where necessary.
    *   Ensure keyboard navigability and focus management.
    *   Test with accessibility tools (e.g., Axe).
*   **Performance:**
    *   Use `React.memo` for functional components or `shouldComponentUpdate` / `PureComponent` for class components to prevent unnecessary re-renders.
    *   Use `useCallback` and `useMemo` to memoize functions and values.
    *   Virtualize long lists (e.g., using `react-window` or `react-virtualized`).
    *   Code-split using `React.lazy` and `Suspense`.

## 3. Testing

*   **Tools:**
    *   **Jest:** As the test runner.
    *   **React Testing Library (RTL):** For component testing, focusing on user interactions and accessibility.
    *   **Cypress / Playwright:** For end-to-end testing.
*   **What to Test:**
    *   Component rendering based on props and state.
    *   User interactions (e.g., button clicks, form submissions).
    *   State changes and side effects.
    *   Utility functions.
*   **Best Practices:**
    *   Write tests that reflect how users interact with the application.
    *   Avoid testing implementation details.
    *   Ensure tests are independent and repeatable.
    *   Aim for good test coverage.

## 4. Project Structure (Example)

```
src/
├── App.js                     # Main application component
├── index.js                   # Entry point
├── components/                # Shared, reusable UI components
│   ├── Button/
│   │   ├── Button.jsx
│   │   └── Button.module.css
│   └── ...
├── features/                  # Feature-specific modules/components
│   ├── UserAuthentication/
│   │   ├── LoginPage.jsx
│   │   ├── RegistrationForm.jsx
│   │   └── authAPI.js
│   └── ...
├── hooks/                     # Custom React hooks
│   └── useAuth.js
├── services/                  # API service layers, utility functions
│   └── apiClient.js
├── store/                     # State management (e.g., Redux, Zustand)
│   ├── index.js
│   ├── reducers/
│   └── actions/
├── contexts/                  # React Context providers
│   └── ThemeContext.js
├── pages/                     # Top-level route components (if using a page-based structure)
│   ├── HomePage.jsx
│   └── ProfilePage.jsx
├── styles/                    # Global styles, theme variables
│   └── global.css
└── utils/                     # General utility functions
```

---
*This style guide is a living document and should be adapted to the specific needs and decisions of the project team.*