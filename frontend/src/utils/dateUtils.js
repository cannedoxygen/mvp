/**
 * Utility functions for date formatting and manipulation
 */

/**
 * Format a date for display
 * @param {Date|string} date - Date object or ISO date string
 * @param {string} format - Format option: 'short', 'medium', 'long', 'time', 'dateTime'
 * @returns {string} - Formatted date string
 */
export const formatDate = (date, format = 'medium') => {
    if (!date) return '';
      
    // Create Date object if string
    let dateObj;
    try {
      dateObj = typeof date === 'string' ? new Date(date) : date;
      
      // Check if valid date
      if (isNaN(dateObj.getTime())) {
        return '';
      }
    } catch (e) {
      console.error('Invalid date format:', date);
      return '';
    }
      
    // Format based on requested format
    try {
      switch (format) {
        case 'short':
          return dateObj.toLocaleDateString('en-US', {
            month: 'numeric',
            day: 'numeric'
          });
          
        case 'medium':
          return dateObj.toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric',
            year: 'numeric'
          });
          
        case 'long':
          return dateObj.toLocaleDateString('en-US', {
            weekday: 'long',
            month: 'long',
            day: 'numeric',
            year: 'numeric'
          });
          
        case 'time':
          return dateObj.toLocaleTimeString('en-US', {
            hour: 'numeric',
            minute: '2-digit',
            timeZoneName: 'short'
          });
          
        case 'dateTime':
          return dateObj.toLocaleString('en-US', {
            month: 'short',
            day: 'numeric',
            hour: 'numeric',
            minute: '2-digit',
            timeZoneName: 'short'
          });
          
        default:
          return dateObj.toLocaleDateString();
      }
    } catch (e) {
      console.error('Error formatting date:', e);
      return String(date);
    }
  };
    
  /**
   * Get today's date at midnight
   * @returns {Date} - Today's date with time set to midnight
   */
  export const getToday = () => {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    return today;
  };
    
  /**
   * Get tomorrow's date at midnight
   * @returns {Date} - Tomorrow's date with time set to midnight
   */
  export const getTomorrow = () => {
    const tomorrow = getToday();
    tomorrow.setDate(tomorrow.getDate() + 1);
    return tomorrow;
  };
    
  /**
   * Format a game time including if it's today or tomorrow
   * @param {Date|string} date - Game date and time
   * @returns {string} - Formatted string like "Today, 7:05 PM ET" or "Tomorrow, 1:10 PM ET"
   */
  export const formatGameTime = (date) => {
    if (!date) return '';
    
    try {
      const gameDate = typeof date === 'string' ? new Date(date) : date;
      
      // Check if valid date
      if (isNaN(gameDate.getTime())) {
        return '';
      }
      
      const today = getToday();
      const tomorrow = getTomorrow();
      
      // Format just the time part
      const timeStr = gameDate.toLocaleTimeString('en-US', {
        hour: 'numeric',
        minute: '2-digit',
        timeZoneName: 'short'
      });
      
      // Check if game is today or tomorrow
      if (gameDate.getDate() === today.getDate() && 
          gameDate.getMonth() === today.getMonth() && 
          gameDate.getFullYear() === today.getFullYear()) {
        return `Today, ${timeStr}`;
      } else if (gameDate.getDate() === tomorrow.getDate() && 
                 gameDate.getMonth() === tomorrow.getMonth() && 
                 gameDate.getFullYear() === tomorrow.getFullYear()) {
        return `Tomorrow, ${timeStr}`;
      } else {
        // For other dates, show the date and time
        const dateStr = gameDate.toLocaleDateString('en-US', {
          weekday: 'short',
          month: 'short',
          day: 'numeric'
        });
        return `${dateStr}, ${timeStr}`;
      }
    } catch (e) {
      console.error('Error formatting game time:', e);
      return String(date);
    }
  };
  
  /**
   * Format date into YYYY-MM-DD format for API calls
   * @param {Date} date - Date to format
   * @returns {string} - Date string in YYYY-MM-DD format
   */
  export const formatDateForApi = (date) => {
    if (!date) return '';
    
    try {
      const d = typeof date === 'string' ? new Date(date) : date;
      
      // Check if valid date
      if (isNaN(d.getTime())) {
        return '';
      }
      
      return d.toISOString().split('T')[0];
    } catch (e) {
      console.error('Error formatting date for API:', e);
      return '';
    }
  };
  
  /**
   * Format a full game date and time
   * @param {Date|string} date - Game date and time
   * @returns {string} - Formatted string like "Sunday, March 21, 2025, 7:05 PM ET"
   */
  export const formatGameDateTime = (date) => {
    if (!date) return '';
    
    try {
      const gameDate = typeof date === 'string' ? new Date(date) : date;
      
      // Check if valid date
      if (isNaN(gameDate.getTime())) {
        return '';
      }
      
      return gameDate.toLocaleString('en-US', {
        weekday: 'long',
        month: 'long',
        day: 'numeric',
        year: 'numeric',
        hour: 'numeric',
        minute: '2-digit',
        timeZoneName: 'short'
      });
    } catch (e) {
      console.error('Error formatting game date and time:', e);
      return String(date);
    }
  };
  
  /**
   * Parse date string in various formats
   * @param {string} dateStr - Date string to parse
   * @returns {Date|null} - Parsed date or null if invalid
   */
  export const parseDate = (dateStr) => {
    if (!dateStr) return null;
    
    try {
      // Try standard parsing
      const date = new Date(dateStr);
      
      // Check if valid
      if (!isNaN(date.getTime())) {
        return date;
      }
      
      // Try alternative formats if needed
      // Add specialized format parsing here if the API returns non-standard formats
      
      return null;
    } catch (e) {
      console.error('Error parsing date:', e);
      return null;
    }
  };