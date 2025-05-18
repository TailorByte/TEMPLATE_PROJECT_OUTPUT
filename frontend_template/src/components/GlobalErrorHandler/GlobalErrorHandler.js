import React from 'react';
import { useErrorContext } from '../../contexts/ErrorContext'; // Adjusted path
import ErrorDisplay from '../ErrorDisplay/ErrorDisplay'; // Adjusted path
// import styles from './GlobalErrorHandler.module.css'; // Optional: if you need specific styles for the wrapper

const GlobalErrorHandler = () => {
  const { globalError, globalErrorType, clearGlobalError } = useErrorContext();

  if (!globalError) {
    return null;
  }

  // You could wrap this in a modal or a more prominent display
  // For now, it uses the same ErrorDisplay component
  return (
    <div /*className={styles.globalErrorWrapper}*/ style={{ position: 'fixed', top: '20px', right: '20px', zIndex: 1050 }}>
      <ErrorDisplay
        error={globalError}
        errorType={globalErrorType}
        onClose={clearGlobalError}
        // No onRetry for global errors by default, as context might be lost
      />
    </div>
  );
};

export default GlobalErrorHandler;