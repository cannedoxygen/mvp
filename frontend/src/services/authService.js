import api from './api';
import { handleApiError } from '../utils/errorUtils';
import { toast } from 'react-toastify';

// Local storage keys
const TOKEN_KEY = 'auth_token';
const USER_KEY = 'auth_user';

/**
 * Authentication service for handling user login/logout
 */
class AuthService {
  /**
   * Login user with email and password
   * @param {string} email - User email
   * @param {string} password - User password
   * @returns {Promise<Object>} User data and token
   */
  async login(email, password) {
    try {
      const response = await api.post('/auth/login', { email, password });
      
      // Store authentication data
      this.setToken(response.token);
      this.setUser(response.user);
      
      toast.success('Logged in successfully');
      return response;
    } catch (error) {
      handleApiError(error, {
        onClientError: (err) => {
          if (err.status === 401) {
            toast.error('Invalid email or password');
          } else {
            toast.error(`Login failed: ${err.message}`);
          }
        },
        onNetworkError: () => toast.error('Network error. Please check your connection.'),
        onServerError: () => toast.error('Server error. Please try again later.')
      });
      throw error;
    }
  }
  
  /**
   * Logout the current user
   */
  logout() {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
    
    // Reload page to reset app state
    window.location.href = '/';
  }
  
  /**
   * Check if user is authenticated
   * @returns {boolean} True if authenticated
   */
  isAuthenticated() {
    return !!this.getToken();
  }
  
  /**
   * Get current authentication token
   * @returns {string|null} JWT token or null
   */
  getToken() {
    return localStorage.getItem(TOKEN_KEY);
  }
  
  /**
   * Set authentication token
   * @param {string} token - JWT token
   */
  setToken(token) {
    localStorage.setItem(TOKEN_KEY, token);
  }
  
  /**
   * Get current user data
   * @returns {Object|null} User data or null
   */
  getUser() {
    const userData = localStorage.getItem(USER_KEY);
    if (userData) {
      try {
        return JSON.parse(userData);
      } catch (e) {
        console.error('Error parsing user data:', e);
        return null;
      }
    }
    return null;
  }
  
  /**
   * Set user data
   * @param {Object} user - User data
   */
  setUser(user) {
    localStorage.setItem(USER_KEY, JSON.stringify(user));
  }
  
  /**
   * Register a new user
   * @param {Object} userData - User registration data
   * @returns {Promise<Object>} Registered user data
   */
  async register(userData) {
    try {
      const response = await api.post('/auth/register', userData);
      toast.success('Registration successful! Please log in.');
      return response;
    } catch (error) {
      handleApiError(error, {
        onClientError: (err) => {
          if (err.status === 409) {
            toast.error('Email already in use');
          } else {
            toast.error(`Registration failed: ${err.message}`);
          }
        },
        onNetworkError: () => toast.error('Network error. Please check your connection.'),
        onServerError: () => toast.error('Server error. Please try again later.')
      });
      throw error;
    }
  }
}

// Export a singleton instance
const authService = new AuthService();
export default authService;

// Also export individual methods for convenience
export const { 
  login, 
  logout, 
  isAuthenticated, 
  getToken, 
  getUser,
  register
} = authService;