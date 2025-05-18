# Error Handling Guide

This document outlines a standardized approach to error handling for both backend (Django/DRF) and frontend (React) applications. Consistent error handling improves user experience, simplifies debugging, and enhances application stability.

## 1. Philosophy

*   **User-Centric:** Prioritize clear, user-friendly error messages that guide the user, avoiding technical jargon.
*   **Developer-Friendly:** Provide detailed logs and context for developers to quickly diagnose and fix issues.
*   **Consistency:** Implement a uniform error handling strategy across the application (both frontend and backend).
*   **Graceful Degradation:** Aim for the application to handle errors gracefully without crashing.
*   **Recovery:** Offer retry mechanisms or alternative actions where appropriate.
*   **Security:** Do not expose sensitive information (stack traces, internal configurations) in error messages sent to the client.

## 2. Backend Error Handling (Django & DRF)

Django Rest Framework (DRF) provides a solid foundation for API error handling.

### 2.1. Standard Error Response Format

APIs should return errors in a consistent JSON format. A common practice:

```json
// For general errors (e.g., 401, 403, 404, 500)
{
  "detail": "User-friendly error message.", // General message
  "code": "error_code_identifier" // Optional: A unique code for the error type
}

// For validation errors (typically 400)
{
  "detail": "Validation Failed.", // General message for validation errors
  "code": "validation_error",
  "errors": { // Field-specific errors
    "field_name1": ["Error message for field 1.", "Another error for field 1."],
    "field_name2": ["Error message for field 2."],
    "non_field_errors": ["A general error not specific to any field."]
  }
}
```

### 2.2. DRF Exception Handling

*   **Default Handler:** DRF's default exception handler already converts many Django exceptions (e.g., `Http404`, `PermissionDenied`) and DRF exceptions (`ValidationError`, `NotAuthenticated`) into appropriate HTTP responses with a JSON body.
*   **Custom Exception Handler:** For more control over the error response format or to handle custom exceptions, create a custom exception handler in `settings.py`:

    ```python
    # project/settings.py
    REST_FRAMEWORK = {
        'EXCEPTION_HANDLER': 'your_app.exceptions.custom_exception_handler'
        # ... other settings
    }
    ```

    ```python
    # your_app/exceptions.py
    from rest_framework.views import exception_handler
    from rest_framework.exceptions import ValidationError, NotAuthenticated, PermissionDenied, NotFound
    from django.http import Http404
    from rest_framework.response import Response
    from rest_framework import status

    def custom_exception_handler(exc, context):
        # Call DRF's default exception handler first,
        # to get the standard error response.
        response = exception_handler(exc, context)

        handlers = {
            'ValidationError': _handle_validation_error,
            'NotAuthenticated': _handle_authentication_error,
            'PermissionDenied': _handle_permission_error,
            'NotFound': _handle_not_found_error,
            'Http404': _handle_not_found_error, # Django's Http404
            # Add more custom exception types if needed
        }

        exception_class = exc.__class__.__name__

        if exception_class in handlers:
            return handlers[exception_class](exc, context, response)

        # For unhandled exceptions, return a generic 500 error
        if response is None:
            # Log the full exception here for debugging
            # import logging
            # logger = logging.getLogger(__name__)
            # logger.error(f"Unhandled exception: {exc}", exc_info=True)
            return Response(
                {"detail": "A server error occurred.", "code": "server_error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # If DRF handled it but we want to customize the format further
        if response is not None:
            if isinstance(response.data, list): # e.g. some throttle errors
                 response.data = {'detail': response.data[0]}
            elif isinstance(response.data, dict) and not ('detail' in response.data or 'errors' in response.data):
                 # Wrap simple dict responses if they don't follow our format
                 response.data = {'detail': str(response.data)}

            if 'detail' in response.data and 'code' not in response.data:
                response.data['code'] = 'generic_error' # Add a default code

        return response

    def _handle_validation_error(exc, context, response):
        response.data = {
            'detail': 'Validation Failed.',
            'code': 'validation_error',
            'errors': response.data # DRF already formats this well
        }
        return response

    def _handle_authentication_error(exc, context, response):
        response.data = {
            'detail': 'Authentication credentials were not provided or are invalid.',
            'code': 'authentication_failed'
        }
        return response

    def _handle_permission_error(exc, context, response):
        response.data = {
            'detail': 'You do not have permission to perform this action.',
            'code': 'permission_denied'
        }
        return response

    def _handle_not_found_error(exc, context, response):
        response.data = {
            'detail': 'The requested resource was not found.',
            'code': 'not_found'
        }
        # Ensure status is 404, DRF default might already do this
        response.status_code = status.HTTP_404_NOT_FOUND
        return response
    ```

### 2.3. Custom Exceptions

Define custom application-specific exceptions if needed:

```python
# your_app/exceptions.py
from rest_framework.exceptions import APIException

class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'service_unavailable'

class ExternalIntegrationError(APIException):
    status_code = 502
    default_detail = 'Error communicating with an external service.'
    default_code = 'external_integration_error'
```
Ensure your custom exception handler can process these.

### 2.4. Logging

*   Utilize Django's built-in logging framework. Configure handlers and loggers in `settings.py`.
*   Log all unhandled exceptions (5xx errors) with full stack traces.
*   Log important business logic failures or security-related events.
*   Avoid logging sensitive data like passwords or raw API keys.
*   Include contextual information in logs (e.g., user ID, request ID).

```python
# project/settings.py (Example logging config)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        # Add file handler or external logging service handler for production
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO', # Adjust for production
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO', # Adjust as needed
            'propagate': False,
        },
        'your_app_name': { # Logger for your application
            'handlers': ['console'],
            'level': 'DEBUG', # Or INFO for production
            'propagate': False,
        },
    }
}
```

## 3. Frontend Error Handling (React)

### 3.1. Error Categories (Client-Side)

*   **Network Error:** Problems with the internet connection, server unreachable, DNS issues, CORS errors.
*   **API Error (Server Error):** The server responded with an error (4xx, 5xx).
    *   **Validation Error:** Specific type of API error (e.g., 400) indicating invalid input.
    *   **Authentication Error:** API error related to login, token expiry (e.g., 401).
    *   **Authorization Error:** API error indicating insufficient permissions (e.g., 403).
    *   **Not Found Error:** API error for a resource not found (e.g., 404).
*   **UI Error (JavaScript Error):** Errors originating from React components or client-side JavaScript logic.
*   **Unknown Error:** Any error not fitting the above categories.

### 3.2. Core Components

*   **Error Boundary (`components/ErrorBoundary.jsx`):**
    A class component that catches JavaScript errors anywhere in its child component tree, logs those errors, and displays a fallback UI.
    ```jsx
    import React, { Component } from 'react';

    class ErrorBoundary extends Component {
      constructor(props) {
        super(props);
        this.state = { hasError: false, error: null, errorInfo: null };
      }

      static getDerivedStateFromError(error) {
        return { hasError: true, error };
      }

      componentDidCatch(error, errorInfo) {
        this.setState({ errorInfo });
        // You can also log the error to an error reporting service here
        console.error("ErrorBoundary caught an error:", error, errorInfo);
      }

      render() {
        if (this.state.hasError) {
          // You can render any custom fallback UI
          return (
            <div>
              <h2>Something went wrong.</h2>
              <p>We're sorry for the inconvenience. Please try refreshing the page or contact support if the problem persists.</p>
              {process.env.NODE_ENV === 'development' && this.state.errorInfo && (
                <details style={{ whiteSpace: 'pre-wrap' }}>
                  {this.state.error && this.state.error.toString()}
                  <br />
                  {this.state.errorInfo.componentStack}
                </details>
              )}
            </div>
          );
        }
        return this.props.children;
      }
    }
    export default ErrorBoundary;
    ```
    Wrap your application or specific parts of it with `<ErrorBoundary>`.

*   **Global Error Context/State (`context/ErrorContext.jsx` or Redux/Zustand store):**
    To manage and display errors that are not caught by a local handler or need to be shown globally (e.g., a toast notification).
    ```jsx
    // Example using React Context
    import React, { createContext, useState, useContext, useCallback } from 'react';

    const ErrorContext = createContext();

    export const useGlobalError = () => useContext(ErrorContext);

    export const GlobalErrorProvider = ({ children }) => {
      const [globalError, setGlobalError] = useState(null); // { message, type, details }

      const showError = useCallback((message, type = 'unknown', details = null) => {
        console.error("Global Error:", { message, type, details });
        setGlobalError({ message, type, details });
        // Optionally, integrate with a toast notification library here
      }, []);

      const clearError = useCallback(() => {
        setGlobalError(null);
      }, []);

      return (
        <ErrorContext.Provider value={{ globalError, showError, clearError }}>
          {children}
        </ErrorContext.Provider>
      );
    };
    ```
    Wrap your `App.js` with `GlobalErrorProvider`.

*   **API Client Error Handling (e.g., `services/apiClient.js`):**
    Your API client (e.g., using Axios or Fetch) should intercept responses, parse backend error formats, and throw structured errors.
    ```javascript
    // Example with Axios
    import axios from 'axios';

    const apiClient = axios.create({ baseURL: '/api/v1' /* Your API base */ });

    apiClient.interceptors.response.use(
      response => response,
      error => {
        let customError = {
          message: 'An unexpected error occurred.',
          type: 'unknown',
          status: null,
          originalError: error,
          errors: null, // For field-specific validation errors
        };

        if (error.response) {
          // Server responded with a status code out of 2xx range
          customError.status = error.response.status;
          const data = error.response.data;

          if (data && data.detail) {
            customError.message = data.detail;
          } else if (typeof data === 'string') {
            customError.message = data;
          }

          if (data && data.code) {
            customError.type = data.code; // Use backend error code as type
          } else { // Infer type from status
            if (customError.status === 400) customError.type = 'validation_error';
            else if (customError.status === 401) customError.type = 'authentication_error';
            else if (customError.status === 403) customError.type = 'permission_denied';
            else if (customError.status === 404) customError.type = 'not_found';
            else if (customError.status >= 500) customError.type = 'server_error';
          }

          if (data && data.errors) { // For DRF-style validation errors
            customError.errors = data.errors;
          }

        } else if (error.request) {
          // Request was made but no response received (network error)
          customError.message = 'Network error. Please check your connection.';
          customError.type = 'network_error';
        } else {
          // Something happened in setting up the request
          customError.message = error.message || 'Error setting up request.';
        }
        // Log the error here or in a dedicated logging service
        console.error('API Client Error:', customError);
        return Promise.reject(customError);
      }
    );
    export default apiClient;
    ```

### 3.3. Handling Errors in Components

*   **Local State for Errors:** Use `useState` for errors specific to a component's operation (e.g., form submission).
    ```jsx
    import React, { useState } from 'react';
    import apiClient from '../services/apiClient'; // Your API client

    function MyForm() {
      const [formData, setFormData] = useState({ email: '' });
      const [error, setError] = useState(null); // { message, errors: { field: [...] } }
      const [loading, setLoading] = useState(false);
      const { showError: showGlobalError } = useGlobalError(); // Optional global error display

      const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        try {
          await apiClient.post('/submit-data', formData);
          // Handle success
        } catch (err) {
          // err is the structured error from apiClient
          if (err.type === 'validation_error') {
            setError({ message: err.message, errors: err.errors });
          } else {
            // For other errors, you might show them locally or globally
            setError({ message: err.message });
            // OR showGlobalError(err.message, err.type);
          }
          console.error("Form submission error:", err);
        } finally {
          setLoading(false);
        }
      };

      return (
        <form onSubmit={handleSubmit}>
          {/* Display general error */}
          {error && !error.errors && <p style={{color: 'red'}}>{error.message}</p>}

          <div>
            <label htmlFor="email">Email:</label>
            <input type="email" id="email" value={formData.email}
                   onChange={e => setFormData({...formData, email: e.target.value})} />
            {/* Display field-specific error */}
            {error && error.errors && error.errors.email &&
              <p style={{color: 'red'}}>{error.errors.email.join(', ')}</p>
            }
          </div>
          <button type="submit" disabled={loading}>
            {loading ? 'Submitting...' : 'Submit'}
          </button>
        </form>
      );
    }
    ```

### 3.4. Displaying Errors

*   **Inline Errors:** For form validation, display errors next to the respective fields.
*   **Component-Level Banners/Alerts:** For errors related to a specific component's operation.
*   **Global Toasts/Notifications:** For application-wide errors or non-critical issues (using the `GlobalErrorContext` and a toast library like `react-toastify`).
*   **Dedicated Error Pages:** For critical errors like 404 Not Found or 500 Server Error, if a full page redirect is desired.

### 3.5. Logging

*   Log all caught errors to the console during development.
*   In production, integrate with a client-side error monitoring service (e.g., Sentry, LogRocket, Datadog).
    ```javascript
    // Example: in ErrorBoundary or global error handler
    if (process.env.NODE_ENV === 'production' && typeof Sentry !== 'undefined') {
      Sentry.captureException(error, { extra: errorInfo });
    }
    ```

## 4. General Best Practices

*   **Retry Mechanisms:** For transient errors (e.g., network issues), implement retry logic with exponential backoff, especially for critical operations.
*   **Error Codes:** Use unique error codes (backend) to allow for easier identification and specific handling on the frontend if needed.
*   **Testing:** Write tests for error scenarios:
    *   Backend: Test that your API returns correct error responses and status codes.
    *   Frontend: Test that your components display errors correctly and that ErrorBoundaries catch UI errors.
*   **Documentation:** Document common error codes and their meanings.

---
*This guide provides a template. Adapt it to your project's specific needs and technologies.*