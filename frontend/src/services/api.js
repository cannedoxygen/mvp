// frontend/src/services/api.js
import axios from 'axios';

// Create axios instance with default config
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 15000, // 15 second timeout for API calls
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add authorization if needed
    const apiKey = import.meta.env.VITE_API_KEY;
    if (apiKey) {
      config.headers['Ocp-Apim-Subscription-Key'] = apiKey;
    }
    
    // You could add other headers or modify the request here
    
    return config;
  },
  (error) => {
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
      if (error.response.status === 401) {
        // Handle unauthorized error (e.g., redirect to login)
        console.warn('Authentication required');
      } else if (error.response.status === 429) {
        // Handle rate limiting
        console.warn('Rate limit exceeded, please try again later');
      }
    } else if (error.request) {
      // Request made but no response received
      console.error('API Error: No response received');
    } else {
      // Error setting up the request
      console.error('API Error:', error.message);
    }
    
    return Promise.reject(error);
  }
);

export default api;