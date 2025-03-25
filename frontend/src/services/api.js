// frontend/src/services/api.js
import axios from 'axios';
import { API_CONFIG } from '../utils/configUtils';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_CONFIG.baseUrl,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: API_CONFIG.timeouts.default, // Default timeout
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add authorization if needed
    const apiKey = import.meta.env.VITE_API_KEY;
    if (apiKey) {
      config.headers['Ocp-Apim-Subscription-Key'] = apiKey;
    }
    
    // Customize timeout for specific endpoints
    if (config.url.includes('/simulations/')) {
      config.timeout = API_CONFIG.timeouts.simulation;
    } else if (config.url.includes('/weather/')) {
      config.timeout = API_CONFIG.timeouts.weather;
    }
    
    return config;
  },
  (error) => {
    console.error('Request setup error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    // Just return the data part of the response
    return response.data;
  },
  (error) => {
    // Handle common errors
    if (error.response) {
      // Server responded with error status
      console.error('API Error:', error.response.status, error.response.data);
      
      // Add additional handling for specific status codes
      if (error.response.status === 400 || error.response.status === 404) {
        // For 400/404 errors, return empty data instead of failing
        console.warn('Resource not found or invalid request, returning empty data');
        
        // Return empty array or object based on the expected response type
        const url = error.config.url;
        if (url.includes('/games/baseball/today') || 
            url.includes('/games/baseball/date/') ||
            url.includes('/props/') ||
            url.includes('/projections/')) {
          return [];
        } else if (url.includes('/odds/') || 
                  url.includes('/games/baseball/') && !url.includes('/today')) {
          return {};
        } else {
          return null;
        }
      } else if (error.response.status === 401) {
        // Handle unauthorized error (e.g., redirect to login)
        console.warn('Authentication required');
      } else if (error.response.status === 429) {
        // Handle rate limiting
        console.warn('Rate limit exceeded, please try again later');
      } else if (error.response.status >= 500) {
        // Server errors
        console.error('Server error:', error.response.status, error.response.data);
        
        // For server errors with list endpoints, return empty array
        const url = error.config.url;
        if (url.includes('/games/baseball/today') || 
            url.includes('/games/baseball/date/') ||
            url.includes('/props/') ||
            url.includes('/projections/')) {
          return [];
        }
      }
    } else if (error.request) {
      // Request made but no response received (network error)
      console.error('API Error: No response received', error.request);
      
      // For network errors with games endpoints, return empty data
      const url = error.config.url;
      if (url.includes('/games/baseball/today') || 
          url.includes('/games/baseball/date/') ||
          url.includes('/props/') ||
          url.includes('/projections/')) {
        return [];
      } else if (url.includes('/odds/') || 
                url.includes('/games/baseball/') && !url.includes('/today')) {
        return {};
      }
    } else {
      // Error setting up the request
      console.error('API Error:', error.message);
    }
    
    // Add extra information to the error for better debugging
    const enhancedError = new Error(
      `Failed to ${error.config.method} ${error.config.url}: ${error.message}`
    );
    enhancedError.originalError = error;
    enhancedError.config = error.config;
    enhancedError.request = error.request;
    enhancedError.response = error.response;
    
    return Promise.reject(enhancedError);
  }
);

/**
 * Custom method to handle failed requests with mock data fallback
 * @param {Function} apiFn - API function to call
 * @param {Function} mockFn - Fallback mock data function 
 * @param {Array} args - Arguments to pass to both functions
 * @returns {Promise<Any>} - API or mock data
 */
export const withMockFallback = async (apiFn, mockFn, ...args) => {
  try {
    if (API_CONFIG.features.useMockData) {
      return await mockFn(...args);
    }
    return await apiFn(...args);
  } catch (error) {
    console.warn('API call failed, using mock data fallback', error);
    return mockFn(...args);
  }
};

export default api;