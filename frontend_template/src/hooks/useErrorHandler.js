import { useState, useCallback } from 'react';
// Import useErrorContext if you want to use its determineErrorType logic
// import { useErrorContext } from '../contexts/ErrorContext'; 

const useErrorHandler = (defaultErrorType = 'unknown') => {
  const [error, setError] = useState(null);
  const [errorType, setErrorType] = useState(null);
  // const { determineErrorType } = useErrorContext(); // Or define a local version

  // Local version of determineErrorType if not using from context
  const determineLocalErrorType = (err) => {
    if (err && err.type) return err.type;
    if (err && err.isAxiosError) {
        if (err.response) {
            if (err.response.status === 401 || err.response.status === 403) return 'auth';
            if (err.response.status === 400 || err.response.status === 422) return 'validation';
            if (err.response.status >= 500) return 'server';
        } else if (err.request) {
            return 'network';
        }
    }
    return defaultErrorType;
  };

  const handleError = useCallback((err, type = null) => {
    console.error("Local Error Caught:", err);
    setError(err.message || 'An unexpected error occurred.');
    setErrorType(type || determineLocalErrorType(err));
    // setErrorType(type || determineErrorType(err)); // If using context's version
  }, [determineLocalErrorType, defaultErrorType]);
  // }, [determineErrorType, defaultErrorType]); // If using context's version

  const clearError = useCallback(() => {
    setError(null);
    setErrorType(null);
  }, []);

  return {
    error,
    errorType,
    handleError,
    clearError,
  };
};

export default useErrorHandler;