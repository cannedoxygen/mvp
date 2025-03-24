/**
 * Utility functions for formatting data for display
 */

/**
 * Format a currency value
 * @param {number} value - Value to format
 * @param {string} currency - Currency code (default: USD)
 * @returns {string} - Formatted currency string
 */
export const formatCurrency = (value, currency = 'USD') => {
    if (value === undefined || value === null) {
      return '-';
    }
    
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency,
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(value);
  };
  
  /**
   * Format a number with specified decimal places
   * @param {number} value - Number to format
   * @param {number} decimals - Number of decimal places
   * @returns {string} - Formatted number string
   */
  export const formatNumber = (value, decimals = 1) => {
    if (value === undefined || value === null) {
      return '-';
    }
    
    return new Intl.NumberFormat('en-US', {
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals
    }).format(value);
  };
  
  /**
   * Format a percentage value
   * @param {number} value - Value to format (0-1)
   * @param {number} decimals - Number of decimal places
   * @returns {string} - Formatted percentage string
   */
  export const formatPercent = (value, decimals = 0) => {
    if (value === undefined || value === null) {
      return '-';
    }
    
    return new Intl.NumberFormat('en-US', {
      style: 'percent',
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals
    }).format(value);
  };
  
  /**
   * Format team name with abbreviation
   * @param {Object} team - Team object with name and abbreviation
   * @returns {string} - Formatted team name
   */
  export const formatTeamName = (team) => {
    if (!team) return '';
    
    if (typeof team === 'string') {
      return team;
    }
    
    return team.abbreviation ? `${team.name} (${team.abbreviation})` : team.name;
  };
  
  /**
   * Format a player name with position
   * @param {Object} player - Player object with name and position
   * @returns {string} - Formatted player name
   */
  export const formatPlayerName = (player) => {
    if (!player) return '';
    
    if (typeof player === 'string') {
      return player;
    }
    
    return player.position ? `${player.name}, ${player.position}` : player.name;
  };
  
  /**
   * Format a decimal odds value to American odds
   * @param {number} decimal - Decimal odds (e.g., 1.91)
   * @returns {string} - American odds with + or - sign
   */
  export const formatAmericanOdds = (decimal) => {
    if (decimal === undefined || decimal === null) {
      return '-';
    }
    
    // If it's already in American format, just ensure it has the sign
    if (typeof decimal === 'number' && (decimal > 100 || decimal < -100)) {
      return decimal > 0 ? `+${decimal}` : `${decimal}`;
    }
    
    try {
      if (decimal >= 2.0) {
        // Plus odds (underdog)
        return `+${Math.round((decimal - 1) * 100)}`;
      } else {
        // Minus odds (favorite)
        return `-${Math.round(100 / (decimal - 1))}`;
      }
    } catch (e) {
      console.error('Error formatting odds:', e);
      return '-';
    }
  };
  
  /**
   * Format string to title case
   * @param {string} str - String to format
   * @returns {string} - Title case string
   */
  export const toTitleCase = (str) => {
    if (!str) return '';
    
    return str
      .toLowerCase()
      .split(' ')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  };
  
  /**
   * Format a confidence level with appropriate label
   * @param {number} confidence - Confidence value (0-1)
   * @returns {Object} - Label and color class
   */
  export const formatConfidence = (confidence) => {
    if (confidence === undefined || confidence === null) {
      return { label: 'Unknown', colorClass: 'text-gray-500' };
    }
    
    if (confidence >= 0.75) {
      return { label: 'Very High', colorClass: 'text-green-600' };
    } else if (confidence >= 0.65) {
      return { label: 'High', colorClass: 'text-green-500' };
    } else if (confidence >= 0.55) {
      return { label: 'Moderate', colorClass: 'text-blue-500' };
    } else if (confidence >= 0.45) {
      return { label: 'Uncertain', colorClass: 'text-gray-500' };
    } else {
      return { label: 'Low', colorClass: 'text-red-500' };
    }
  };
  
  /**
   * Truncate text with ellipsis if it exceeds max length
   * @param {string} text - Text to truncate
   * @param {number} maxLength - Maximum length
   * @returns {string} - Truncated text
   */
  export const truncateText = (text, maxLength = 100) => {
    if (!text) return '';
    if (text.length <= maxLength) return text;
    return `${text.substring(0, maxLength - 3)}...`;
  };
  
  /**
   * Format a date in a standard way
   * @param {Date|string} date - Date to format
   * @param {string} format - Format type (short, medium, long)
   * @returns {string} - Formatted date string
   */
  export const formatDate = (date, format = 'medium') => {
    if (!date) return '';
    
    const dateObj = typeof date === 'string' ? new Date(date) : date;
    
    if (isNaN(dateObj.getTime())) {
      return '';
    }
    
    const options = {
      short: { month: 'numeric', day: 'numeric' },
      medium: { month: 'short', day: 'numeric', year: 'numeric' },
      long: { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' }
    };
    
    return dateObj.toLocaleDateString('en-US', options[format] || options.medium);
  };