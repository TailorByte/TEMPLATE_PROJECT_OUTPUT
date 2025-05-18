import React from 'react';
import PropTypes from 'prop-types';
// import styles from './ErrorBoundary.module.css'; // Optional: if you need specific styles

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    // Update state so the next render will show the fallback UI.
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    // You can also log the error to an error reporting service
    console.error("Uncaught error:", error, errorInfo);
    this.setState({ errorInfo });
    // Example: logErrorToMyService(error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      // You can render any custom fallback UI
      return (
        <div /*className={styles.errorBoundaryContainer}*/>
          <h2>Something went wrong.</h2>
          <p>We're sorry for the inconvenience. Please try refreshing the page, or contact support if the problem persists.</p>
          {process.env.NODE_ENV === 'development' && this.state.error && (
            <details style={{ whiteSpace: 'pre-wrap', marginTop: '1rem', padding: '1rem', border: '1px solid #ccc', borderRadius: '4px' }}>
              <summary>Error Details (Development Mode)</summary>
              {this.state.error.toString()}
              <br />
              {this.state.errorInfo && this.state.errorInfo.componentStack}
            </details>
          )}
        </div>
      );
    }

    return this.props.children;
  }
}

ErrorBoundary.propTypes = {
  children: PropTypes.node.isRequired,
};

export default ErrorBoundary;