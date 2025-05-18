import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import ErrorBoundary from './components/ErrorBoundary/ErrorBoundary'; // Import ErrorBoundary
import GlobalErrorHandler from './components/GlobalErrorHandler/GlobalErrorHandler'; // Import GlobalErrorHandler
// import { useErrorContext } from './contexts/ErrorContext'; // Not needed directly in App.js if GlobalErrorHandler handles it

// Placeholder Pages
const HomePage = () => <h2>Home Page</h2>;
const AboutPage = () => <h2>About Page</h2>;

// Example component that might throw an error for ErrorBoundary testing
const ProblematicComponent = () => {
  // To test ErrorBoundary, uncomment the line below:
  // throw new Error("Test error from ProblematicComponent!");
  return <h3>Example Feature Page (Potentially Problematic)</h3>;
};


function App() {
  // GlobalErrorHandler now gets its state from ErrorContext directly
  return (
    <ErrorBoundary>
      <Router>
        <div>
          <nav>
            <ul>
              <li><Link to="/">Home</Link></li>
              <li><Link to="/about">About</Link></li>
              <li><Link to="/feature">Example Feature</Link></li>
            </ul>
          </nav>

          <GlobalErrorHandler /> {/* Displays global errors from ErrorContext */}
          
          <hr />

          <Routes>
            <Route path="/about" element={<AboutPage />} />
            <Route path="/feature" element={<ProblematicComponent />} />
            <Route path="/" element={<HomePage />} />
          </Routes>
        </div>
      </Router>
    </ErrorBoundary>
  );
}

export default App;