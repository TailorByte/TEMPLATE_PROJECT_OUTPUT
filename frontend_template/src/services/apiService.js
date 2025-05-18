import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api/v1';

// Create an Axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
    // You can add other default headers here
  },
});

// Add a request interceptor to include the auth token
apiClient.interceptors.request.use(
  (config) => {
    // const token = localStorage.getItem('accessToken'); // Or get from AuthContext
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`;
    // }
    // Log request details (excluding sensitive data)
    const logConfig = { ...config };
    if (logConfig.data && config.url && config.url.includes('/auth/')) {
      logConfig.data = '[REDACTED_AUTH_BODY]';
    }
    if (logConfig.headers && logConfig.headers.Authorization) {
        logConfig.headers = {...logConfig.headers, Authorization: 'Bearer [REDACTED_TOKEN]'};
    }
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`, logConfig);
    return config;
  },
  (error) => {
    console.error('API Request Interceptor Error:', error);
    return Promise.reject(error);
  }
);


// Custom Error class for API errors
export class ApiError extends Error {
  constructor(message, status, type = 'unknown', responseData = null) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.type = type; // 'network', 'validation', 'server', 'auth', 'unknown'
    this.responseData = responseData; // Original error response data from server
    
    // Maintains proper stack trace in V8
    if (Error.captureStackTrace) {
      Error.captureStackTrace(this, ApiError);
    }
  }
}

const handleApiResponse = (response) => {
  console.log(`API Response: ${response.config.method?.toUpperCase()} ${response.config.url} - ${response.status}`, {
    status: response.status,
    data: response.config.url && response.config.url.includes('/auth/') ? '[REDACTED_AUTH_RESPONSE]' : response.data,
  });
  return response.data;
};

const handleApiError = (error) => {
  console.error(`API Error: ${error.config?.method?.toUpperCase()} ${error.config?.url}`, error);

  if (error.response) {
    // The request was made and the server responded with a status code
    // that falls out of the range of 2xx
    const { status, data } = error.response;
    let type = 'server';
    if (status === 400 || status === 422) type = 'validation';
    if (status === 401 || status === 403) type = 'auth';
    
    const message = data?.detail || data?.message || error.message || `Request failed with status code ${status}`;
    throw new ApiError(message, status, type, data);
  } else if (error.request) {
    // The request was made but no response was received
    throw new ApiError('Network error: No response received from server.', null, 'network', null);
  } else {
    // Something happened in setting up the request that triggered an Error
    throw new ApiError(error.message || 'An unexpected error occurred.', null, 'unknown', null);
  }
};

/**
 * Generic API request function
 * @param {string} endpoint - The API endpoint (e.g., '/users')
 * @param {object} options - Axios request options (method, body, params, etc.)
 * @returns {Promise<any>} - The response data
 * @throws {ApiError} - Custom error object for API failures
 */
export const apiRequest = async (endpoint, options = {}) => {
  try {
    const response = await apiClient({
      url: endpoint,
      method: options.method || 'GET',
      data: options.body, // For POST, PUT, PATCH
      params: options.params, // For GET requests
      ...options, // Allow overriding other axios options
    });
    return handleApiResponse(response);
  } catch (error) {
    return handleApiError(error); // Re-throw our custom ApiError
  }
};

// Example usage:
//
// const fetchUsers = async () => {
//   try {
//     const users = await apiRequest('/users');
//     console.log(users);
//   } catch (error) {
//     // handleError(error); // Using useErrorHandler hook
//     console.error("Failed to fetch users:", error.message, error.status, error.type, error.responseData);
//   }
// };
//
// const createUser = async (userData) => {
//   try {
//     const newUser = await apiRequest('/users', { method: 'POST', body: userData });
//     console.log('User created:', newUser);
//   } catch (error) {
//     // handleError(error);
//     console.error("Failed to create user:", error.message, error.status, error.type, error.responseData);
//   }
// };