import React, { createContext, useState, useContext, useCallback } from 'react';

const ErrorContext = createContext();

export const useErrorContext = () => {
  const context = useContext(ErrorContext);
  if (!context) {
    throw new Error('useErrorContext must be used within an ErrorProvider');
  }
  return context;
};

export const ErrorProvider = ({ children }) => {
  const [globalError, setGlobalError] = useState(null);
  const [globalErrorType, setGlobalErrorType] = useState(null); // e.g., 'network', 'server', 'validation', 'auth', 'unknown'

  const determineErrorType = (error) => {
    if (error && error.type) return error.type; // If error object has a 'type' property (e.g., from ApiError)
    if (error && error.isAxiosError) { // Example for Axios errors
        if (error.response) {
            if (error.response.status === 401 || error.response.status === 403) return 'auth';
            if (error.response.status === 400 || error.response.status === 422) return 'validation';
            if (error.response.status >= 500) return 'server';
        } else if (error.request) {
            return 'network'; // No response received
        }
    }
    // Add more specific checks if needed
    return 'unknown';
  };

  const handleGlobalError = useCallback((error, type = null) => {
    console.error("Global Error Caught:", error);
    setGlobalError(error.message || 'An unexpected global error occurred.');
    setGlobalErrorType(type || determineErrorType(error));
  }, []);

  const clearGlobalError = useCallback(() => {
    setGlobalError(null);
    setGlobalErrorType(null);
  }, []);

  const value = {
    globalError,
    globalErrorType,
    handleGlobalError,
    clearGlobalError,
    determineErrorType, // Expose this if local handlers also want to use the same logic
  };

  return <ErrorContext.Provider value={value}>{children}</ErrorContext.Provider>;
};