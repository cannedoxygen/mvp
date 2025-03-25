// frontend/src/services/api.js
import axios from 'axios';
import { formatApiError } from '../utils/errorUtils';
import { API_CONFIG } from '../utils/configUtils';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_CONFIG.baseUrl,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: API_CONFIG.timeouts.default,
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add authorization if needed (e.g., from local storage)
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    
    // Optional: Add API key if required
    const apiKey = import.meta.env.VITE_API_KEY;
    if (apiKey) {
      config.headers['Ocp-Apim-Subscription-Key'] = apiKey;
    }
    
    // Log request details in development
    if (import.meta.env.DEV) {
      console.log('API Request:', {
        url: config.url,
        method: config.method,
        baseURL: config.baseURL,
        headers: config.headers
      });
    }
    
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    // Log response details in development
    if (import.meta.env.DEV) {
      console.log('API Response:', {
        url: response.config.url,
        method: response.config.method,
        status: response.status,
        data: response.data
      });
    }
    
    // Return only the data part of the response
    return response.data;
  },
  (error) => {
    // Format and log the error
    const formattedError = formatApiError(error);
    
    // Handle specific error scenarios
    if (formattedError.status === 401) {
      // Unauthorized - clear token and redirect to login
      localStorage.removeItem('auth_token');
      window.location.href = '/login';
    } else if (formattedError.status === 403) {
      // Forbidden - show access denied message
      console.warn('Access denied');
    } else if (formattedError.status >= 500) {
      // Server errors
      console.error('Server error:', formattedError.message);
    }
    
    return Promise.reject(formattedError);
  }
);

// Utility methods to handle common API operations
api.get = async (url, config = {}) => {
  try {
    return await axios.get(url, {
      ...config,
      baseURL: API_CONFIG.baseUrl
    });
  } catch (error) {
    throw formatApiError(error);
  }
};

api.post = async (url, data = {}, config = {}) => {
  try {
    return await axios.post(url, data, {
      ...config,
      baseURL: API_CONFIG.baseUrl
    });
  } catch (error) {
    throw formatApiError(error);
  }
};

api.put = async (url, data = {}, config = {}) => {
  try {
    return await axios.put(url, data, {
      ...config,
      baseURL: API_CONFIG.baseUrl
    });
  } catch (error) {
    throw formatApiError(error);
  }
};

api.delete = async (url, config = {}) => {
  try {
    return await axios.delete(url, {
      ...config,
      baseURL: API_CONFIG.baseUrl
    });
  } catch (error) {
    throw formatApiError(error);
  }
};

// Ping endpoint for connection testing
api.ping = async () => {
  try {
    const response = await api.get('/games/ping');
    console.log('API Connection Successful:', response);
    return response;
  } catch (error) {
    console.error('API Connection Failed:', error);
    throw error;
  }
};

export default api;