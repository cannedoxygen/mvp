// frontend/src/utils/configUtils.js

/**
 * Application configuration utilities
 * Handles environment-specific configuration
 */

// Safely access environment variables in browser context
const env = import.meta.env || {};

// API configuration
export const API_CONFIG = {
  // Base URL for API calls - fall back to localhost if not defined
  baseUrl: env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
  
  // API Timeouts (in milliseconds)
  timeouts: {
    default: 10000, // 10 seconds
    simulation: 30000, // 30 seconds for simulations
    weather: 15000, // 15 seconds for weather requests,
  },
  
  // Feature flags
  features: {
    // Always use mock data if the environment variable is set or API fails
    useMockData: env.VITE_ENABLE_MOCK_DATA === 'true' || true,
  },
  
  // Endpoints
  endpoints: {
    games: '/games',
    simulations: '/simulations',
    odds: '/odds',
    weather: '/weather',
    auth: '/auth',
  }
};

// Feature flags
export const FEATURES = {
  // Number of simulations to run
  simulationCount: parseInt(env.VITE_SIMULATION_COUNT || '1000', 10),
  
  // Feature to show detailed statistics
  showDetailedStats: env.VITE_SHOW_DETAILED_STATS !== 'false',
  
  // Feature to show debug information
  showDebugInfo: env.VITE_SHOW_DEBUG_INFO === 'true',
};

// Application environment
export const ENV = {
  isDevelopment: env.DEV === true,
  isProduction: env.PROD === true,
  appVersion: env.VITE_APP_VERSION || '0.1.0',
};

/**
 * Get current environment name
 * @returns {string} - Environment name (development, production)
 */
export const getEnvironment = () => {
  return ENV.isProduction ? 'production' : 'development';
};

/**
 * Check if a feature is enabled
 * @param {string} featureName - Name of the feature to check
 * @returns {boolean} - Whether the feature is enabled
 */
export const isFeatureEnabled = (featureName) => {
  if (featureName in FEATURES) {
    return FEATURES[featureName] === true;
  }
  
  // For API_CONFIG features, check in the features object
  if (featureName in API_CONFIG.features) {
    return API_CONFIG.features[featureName] === true;
  }
  
  return false;
};

/**
 * Get API URL for a specific endpoint
 * @param {string} endpoint - API endpoint path
 * @returns {string} - Full API URL
 */
export const getApiUrl = (endpoint) => {
  // Remove leading slash if present
  const path = endpoint.startsWith('/') ? endpoint.substring(1) : endpoint;
  return `${API_CONFIG.baseUrl}/${path}`;
};

/**
 * Get configuration value by path
 * @param {string} path - Dot notation path (e.g., 'API_CONFIG.timeouts.default')
 * @param {any} defaultValue - Default value if path not found
 * @returns {any} - Configuration value
 */
export const getConfigValue = (path, defaultValue = null) => {
  try {
    const parts = path.split('.');
    let current = { API_CONFIG, FEATURES, ENV };
    
    for (const part of parts) {
      if (current[part] === undefined) {
        return defaultValue;
      }
      current = current[part];
    }
    
    return current;
  } catch (error) {
    console.error(`Error accessing config path ${path}:`, error);
    return defaultValue;
  }
};