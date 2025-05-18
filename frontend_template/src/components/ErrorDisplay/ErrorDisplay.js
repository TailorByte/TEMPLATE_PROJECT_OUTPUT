import React from 'react';
import PropTypes from 'prop-types';
import styles from './ErrorDisplay.module.css'; // Using CSS Modules

const ErrorDisplay = ({ error, errorType, onClose, onRetry }) => {
  if (!error) {
    return null;
  }

  let title = 'An Error Occurred';
  let details = typeof error === 'string' ? error : 'Please try again or contact support.';

  // Customize title and details based on errorType
  switch (errorType) {
    case 'network':
      title = 'Network Error';
      details = 'Could not connect to the server. Please check your internet connection and try again.';
      break;
    case 'validation':
      title = 'Validation Error';
      // details might be an object or array from server, keep it as is or format it
      if (typeof error === 'object' && error !== null && error.message) {
        details = error.message; // If error object has a message property
      } else if (Array.isArray(error)) {
        details = error.join(' ');
      }
      break;
    case 'server':
      title = 'Server Error';
      details = 'The server encountered an issue. Please try again later. If the problem persists, contact support.';
      break;
    case 'auth':
      title = 'Authentication Error';
      details = 'There was a problem with your authentication. Please try logging in again.';
      break;
    case 'unknown':
    default:
      title = 'Unexpected Error';
      break;
  }

  // If error object has more specific details (e.g. from ApiError)
  if (typeof error === 'object' && error !== null && error.message && errorType !== 'validation') {
    details = error.message;
  }


  return (
    <div className={`${styles.errorDisplay} ${styles[errorType] || styles.unknown}`} role="alert">
      <div className={styles.errorHeader}>
        <h5 className={styles.errorTitle}>{title}</h5>
        {onClose && (
          <button onClick={onClose} className={styles.closeButton} aria-label="Close error message">
            &times;
          </button>
        )}
      </div>
      <div className={styles.errorMessage}>
        <p>{details}</p>
        {/* Example: Displaying nested errors if error.response.data.errors is an object */}
        {errorType === 'validation' && typeof error === 'object' && error?.response?.data?.errors && (
          <ul className={styles.validationList}>
            {Object.entries(error.response.data.errors).map(([field, messages]) => (
              <li key={field}>
                <strong>{field}:</strong> {Array.isArray(messages) ? messages.join(', ') : messages}
              </li>
            ))}
          </ul>
        )}
      </div>
      {onRetry && (
        <div className={styles.errorActions}>
          <button onClick={onRetry} className={styles.retryButton}>
            Retry
          </button>
        </div>
      )}
    </div>
  );
};

ErrorDisplay.propTypes = {
  error: PropTypes.oneOfType([PropTypes.string, PropTypes.object]),
  errorType: PropTypes.oneOf(['network', 'validation', 'server', 'auth', 'unknown']),
  onClose: PropTypes.func,
  onRetry: PropTypes.func,
};

ErrorDisplay.defaultProps = {
  error: null,
  errorType: 'unknown',
  onClose: null,
  onRetry: null,
};

export default ErrorDisplay;