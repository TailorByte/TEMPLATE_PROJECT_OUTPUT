# Frontend Error Handling Guide

This document outlines a standardized error handling approach for React frontend applications built using this template.

## 1. Overview

A consistent error handling system aims to:
- Categorize errors effectively (e.g., network, validation, server, authentication).
- Display user-friendly and informative error messages.
- Facilitate appropriate error logging for debugging.
- Support error recovery actions where applicable.

## 2. Core Components

The error handling framework relies on the following core components, which are pre-configured in the `frontend_template/src/` directory:

### 2.1. Error Context (`contexts/ErrorContext.js`)

Provides global error state management. It exposes:
- `globalError`: The current global error message or object.
- `globalErrorType`: The category of the global error.
- `handleGlobalError(error, type)`: Function to dispatch a global error.
- `clearGlobalError()`: Function to clear the global error.
- `determineErrorType(error)`: A helper to categorize an error object.

**Usage:**
```jsx
// In a component or service that needs to trigger a global error
import { useErrorContext } from 'contexts/ErrorContext'; // Assuming jsconfig.json for absolute paths

const { handleGlobalError } = useErrorContext();

try {
  // Some critical operation
} catch (err) {
  handleGlobalError(err); // Optionally pass a specific type
}
```

### 2.2. Error Handler Hook (`hooks/useErrorHandler.js`)

Provides component-level error state and handling logic. It returns:
- `error`: The current local error message or object for the component.
- `errorType`: The category of the local error.
- `handleError(error, type)`: Function to set a local error within the component.
- `clearError()`: Function to clear the local error.

**Usage:**
```jsx
import useErrorHandler from 'hooks/useErrorHandler';

const MyComponent = () => {
  const { error, errorType, handleError, clearError } = useErrorHandler();

  const fetchData = async () => {
    clearError();
    try {
      // const data = await apiService.get('/some-data');
      // process(data);
    } catch (err) {
      handleError(err); // Optionally pass a specific type
    }
  };
  // ... render error using ErrorDisplay component ...
};
```

### 2.3. Error Display Component (`components/ErrorDisplay/ErrorDisplay.js`)

A standardized UI component for rendering error messages. It accepts props like:
- `error`: The error message or object.
- `errorType`: The category of the error (influences styling/icon).
- `onClose`: Callback function to close/dismiss the error display.
- `onRetry`: Optional callback function to trigger a retry action.

**Usage:**
```jsx
import ErrorDisplay from 'components/ErrorDisplay/ErrorDisplay';

// Inside a component's render method, using state from useErrorHandler
{error && (
  <ErrorDisplay
    error={error}
    errorType={errorType}
    onClose={clearError}
    onRetry={fetchData} // Optional
  />
)}
```

### 2.4. Global Error Handler Component (`components/GlobalErrorHandler/GlobalErrorHandler.js`)

This component is typically placed once in your main `App.js`. It consumes the `ErrorContext` and uses `ErrorDisplay` to show any global errors. It's styled to appear as an overlay or toast-like notification.

### 2.5. Error Boundary Component (`components/ErrorBoundary/ErrorBoundary.js`)

A React class component that catches JavaScript errors anywhere in its child component tree, logs those errors, and displays a fallback UI. This prevents a UI crash due to unhandled rendering errors. It should wrap major sections of your application, or the entire app.

**Usage (typically in `App.js`):**
```jsx
import ErrorBoundary from 'components/ErrorBoundary/ErrorBoundary';

<ErrorBoundary>
  <YourApplicationRoutes />
</ErrorBoundary>
```

## 3. Error Types

Errors are generally categorized into:
1.  **`network`**: Connection issues, request timeouts, server unreachable.
2.  **`validation`**: Invalid user input, form validation failures (often 400 or 422 HTTP status from API).
3.  **`server`**: Backend server errors (typically 5xx HTTP status codes).
4.  **`auth`**: Authentication failures, unauthorized access (typically 401 or 403 HTTP status).
5.  **`unknown`**: Default for uncategorized or unexpected client-side errors.

The `determineErrorType` function in `ErrorContext.js` and `useErrorHandler.js` provides a basic logic for this categorization, especially for errors originating from `apiService.js`.

## 4. API Service Error Handling (`services/apiService.js`)

The provided `apiService.js` (using Axios or a similar HTTP client) should be configured to:
- Intercept responses and errors.
- For error responses from the backend, it should parse the error and throw a custom `ApiError` object.
- This `ApiError` should include:
    - `message`: A user-friendly error message (can be from `error.response.data.detail` or a generic one).
    - `status`: The HTTP status code.
    - `type`: One of the defined error types (e.g., 'validation', 'server', 'auth').
    - `responseData`: The original error response data from the server (e.g., `error.response.data`) for more detailed debugging or specific handling.

Example `ApiError` class:
```javascript
// In apiService.js
export class ApiError extends Error {
  constructor(message, status, type = 'unknown', responseData = null) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.type = type;
    this.responseData = responseData;
  }
}
```

## 5. Best Practices

### 5.1 Handling Multiple Errors in a Component

In complex components, you might manage multiple independent operations, each of which can fail. For instance, a dashboard page might fetch data for several distinct sections, or a settings page could have multiple forms. In such cases, using a separate error handler for each operation can provide more granular error display and management.

**Example:**

```jsx
// Example for handling multiple independent errors
import useErrorHandler from 'hooks/useErrorHandler'; // Assuming jsconfig.json for absolute paths
import ErrorDisplay from 'components/ErrorDisplay/ErrorDisplay'; // Assuming jsconfig.json

const ComplexDashboardSection = () => {
  const { error: userProfileError, handleError: handleUserProfileError, clearError: clearUserProfileError } = useErrorHandler();
  const { error: recentActivityError, handleError: handleRecentActivityError, clearError: clearRecentActivityError } = useErrorHandler();

  // useEffect to fetch user profile, calling handleUserProfileError on failure
  // useEffect to fetch recent activity, calling handleRecentActivityError on failure

  return (
    <div>
      <section className="user-profile-section">
        <h2>User Profile</h2>
        {userProfileError && (
          <ErrorDisplay
            error={userProfileError}
            onClose={clearUserProfileError}
            // onRetry={fetchUserProfile} // Optional
          />
        )}
        {/* ... display user profile data ... */}
      </section>

      <section className="recent-activity-section">
        <h2>Recent Activity</h2>
        {recentActivityError && (
          <ErrorDisplay
            error={recentActivityError}
            onClose={clearRecentActivityError}
            // onRetry={fetchRecentActivity} // Optional
          />
        )}
        {/* ... display recent activity data ... */}
      </section>
    </div>
  );
};
```

### 5.2 Naming Conventions for Error Handlers

When using multiple instances of `useErrorHandler` in a single component, adopt consistent naming conventions to maintain clarity:

*   **Single Handler:** If a component only has one primary operation that can fail, the default names are clear:
    ```jsx
    const { error, errorType, handleError, clearError } = useErrorHandler();
    ```
*   **Multiple Handlers:** Prefix the error state and functions with a descriptive name related to the operation they handle.
    ```jsx
    // For a user profile editing form
    const { error: profileFormError, handleError: handleProfileFormError, clearError: clearProfileFormError } = useErrorHandler();

    // For a data list fetching operation
    const { error: itemListError, handleError: handleItemListError, clearError: clearItemListError } = useErrorHandler();
    ```
*   Always destructure all four properties (`error`, `errorType`, `handleError`, `clearError`) from each `useErrorHandler()` call, even if `errorType` is not immediately used, for consistency and future-proofing.

### 5.3 Logging

Effective logging is crucial for debugging and monitoring application health.

*   **Development Logging:** All errors caught by `handleError` (from `useErrorHandler`) and `handleGlobalError` (from `ErrorContext`) should be logged to the console during development. This provides immediate feedback to developers.
    ```javascript
    // Example within useErrorHandler or ErrorContext
    console.error('Error handled:', {
      message: err.message,
      type: determinedType,
      originalError: err
    });
    ```
*   **Production Logging:** In production environments, integrate with a dedicated error reporting service (e.g., Sentry, LogRocket, Azure Application Insights). The `handleError` and `handleGlobalError` functions can be extended to send detailed error information, including stack traces and context, to these services.
    ```javascript
    // Example extension for production logging
    // if (process.env.NODE_ENV === 'production') {
    //   monitoringService.captureException(err, { extra: { type: determinedType, componentStack: ... } });
    // }
    ```
*   **API Request/Response Logging (Development):** For easier debugging of API interactions during development, consider logging details of API requests and responses in your `apiService.js` or equivalent.
    *   **Request Logging:** Log method, URL, headers, and body.
    *   **Response Logging:** Log status code, headers, and response data.
    *   **CRITICAL: Redact Sensitive Information:** When logging, **always ensure sensitive data is redacted**. This includes:
        *   Authentication tokens (e.g., `Authorization` headers).
        *   Passwords or other credentials in request bodies.
        *   Personally Identifiable Information (PII) in request or response data.
    *   This detailed logging should typically be disabled in production builds or managed via environment variables to avoid leaking sensitive data and excessive log volume.
*   **Contextual Information:** When logging errors, include as much relevant context as possible, such as the component where the error occurred, user ID (if available and appropriate), and any relevant state variables.

### 5.4 Specific Considerations for Authentication Errors

Authentication errors are critical as they often dictate user flow (e.g., redirecting to a login page) and have security implications.

*   **Refer to Authentication Guide:** For detailed authentication mechanisms, token management, and specific backend error responses related to authentication, always refer to the project's primary `Authentication_Guide.md` (or its equivalent as defined in your project documentation).
*   **User Feedback:** Provide clear, non-technical messages for common authentication failures:
    *   "Invalid username or password. Please try again."
    *   "Your session has expired. Please log in again."
    *   "You do not have permission to access this page." (For authorization issues post-login)
*   **Client-Side Input Validation:** Before submitting authentication requests, perform basic client-side validation (e.g., ensuring email and password fields are not empty).
*   **Secure Error Messaging:** Avoid revealing specific reasons for authentication failure that could aid attackers (e.g., "User not found" vs. "Invalid password"). The backend should typically return a generic "Authentication failed" message for incorrect credentials, and the frontend should relay this.
*   **Handling Token Expiry:** Implement logic to gracefully handle expired access tokens, typically by attempting a token refresh or redirecting the user to log in again.

---
**General Best Practices (Continued):**

-   **Local vs. Global:** Use `useErrorHandler` for errors specific to a component's operation (e.g., form submission). Use `handleGlobalError` from `ErrorContext` for critical, application-wide errors that need immediate user attention or might affect overall stability.
-   **Clear Messages:** Provide clear, concise, and user-friendly error messages. Avoid exposing raw stack traces or overly technical details to the end-user in production.
-   **Retry Mechanisms:** For transient errors (like network issues), provide an `onRetry` option in `ErrorDisplay`.
-   **Graceful Degradation:** Design components to handle error states gracefully, preventing the entire UI from breaking.
-   **Security:** Be cautious not to reveal sensitive system information in error messages displayed to users.

By adhering to this guide, development teams can ensure a consistent and robust error handling experience across the frontend application.