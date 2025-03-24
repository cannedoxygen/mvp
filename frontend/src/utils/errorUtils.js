/**
 * Utility functions for error handling and display
 */

/**
 * Format API error for display
 * @param {Error} error - The error object from API call
 * @returns {Object} - Formatted error with message and status
 */
export const formatApiError = (error) => {
    // Default error message
    let message = 'An unexpected error occurred';
    let status = 500;
    let details = null;
    
    // Handle Axios error responses
    if (error.response) {
      status = error.response.status;
      
      // Use backend error message if available
      const backendMessage = error.response.data?.message || error.response.data?.error;
      if (backendMessage) {
        message = backendMessage;
        details = error.response.data?.details || null;
      } else {
        // Standard messages based on status code
        switch (status) {
          case 400:
            message = 'Invalid request data';
            break;
          case 401:
            message = 'Authentication required';
            break;
          case 403:
            message = 'You don\'t have permission to access this resource';
            break;
          case 404:
            message = 'The requested resource was not found';
            break;
          case 429:
            message = 'Too many requests. Please try again later';
            break;
          case 500:
          case 502:
          case 503:
            message = 'Server error. Please try again later';
            break;
          default:
            message = `Request failed with status ${status}`;
        }
      }
    } else if (error.request) {
      // Request was made but no response received
      message = 'No response from server. Please check your connection';
      status = 0;
    } else {
      // Error in setting up the request
      message = error.message || message;
    }
    
    return {
      message,
      status,
      details,
      isServerError: status >= 500,
      isClientError: status >= 400 && status < 500,
      isNetworkError: status === 0,
      original: error
    };
  };
  
  /**
   * Log an error for debugging
   * @param {Error} error - The error object
   * @param {string} context - Context where error occurred
   */
  export const logError = (error, context = '') => {
    // In development, log full details
    if (import.meta.env.DEV) {
      console.error(`Error ${context ? `in ${context}` : ''}:`, error);
      
      // Log additional details if available
      if (error.response) {
        console.error('Response data:', error.response.data);
      }
    } else {
      // In production, log minimal details
      console.error(`Error ${context ? `in ${context}` : ''}: ${error.message}`);
    }
  };
  
  /**
   * Check if an error is a network connectivity issue
   * @param {Error} error - The error object
   * @returns {boolean} - True if network error
   */
  export const isNetworkError = (error) => {
    return !error.response && error.request;
  };
  
  /**
   * Create a user-friendly error message
   * @param {Error} error - The error object
   * @param {string} fallbackMessage - Message to display if error can't be parsed
   * @returns {string} - User-friendly error message
   */
  export const getUserMessage = (error, fallbackMessage = 'An error occurred. Please try again.') => {
    const formattedError = formatApiError(error);
    
    // For server errors, use a generic message
    if (formattedError.isServerError) {
      return 'We\'re experiencing technical difficulties. Please try again later.';
    }
    
    // For network errors, suggest connection check
    if (formattedError.isNetworkError) {
      return 'Unable to connect to the server. Please check your internet connection.';
    }
    
    // For client errors, show the specific message
    if (formattedError.isClientError) {
      return formattedError.message;
    }
    
    // Default fallback
    return fallbackMessage;
  };
  
  /**
   * Handle API errors with common patterns
   * @param {Error} error - The error object
   * @param {Object} options - Options for handling
   * @param {Function} options.onNetworkError - Handler for network errors
   * @param {Function} options.onAuthError - Handler for authentication errors
   * @param {Function} options.onServerError - Handler for server errors
   * @param {Function} options.onClientError - Handler for client errors
   * @param {Function} options.onUnknownError - Handler for unknown errors
   */
  export const handleApiError = (error, options = {}) => {
    const formattedError = formatApiError(error);
    
    // Log the error
    logError(error);
    
    // Handle based on error type
    if (formattedError.isNetworkError && options.onNetworkError) {
      options.onNetworkError(formattedError);
    } else if (formattedError.status === 401 && options.onAuthError) {
      options.onAuthError(formattedError);
    } else if (formattedError.isServerError && options.onServerError) {
      options.onServerError(formattedError);
    } else if (formattedError.isClientError && options.onClientError) {
      options.onClientError(formattedError);
    } else if (options.onUnknownError) {
      options.onUnknownError(formattedError);
    }
    
    return formattedError;
  };