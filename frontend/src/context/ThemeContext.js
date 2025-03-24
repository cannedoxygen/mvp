import React, { createContext, useState, useContext, useEffect } from 'react';

// Create theme context
const ThemeContext = createContext();

/**
 * Theme Provider component
 * Manages application theme (light/dark)
 */
export const ThemeProvider = ({ children }) => {
  // Check if user already has a theme preference stored
  const getInitialTheme = () => {
    if (typeof window !== 'undefined' && window.localStorage) {
      const storedPrefs = window.localStorage.getItem('color-theme');
      if (typeof storedPrefs === 'string') {
        return storedPrefs;
      }

      // Check for system preference
      if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
        return 'dark';
      }
    }

    // Default to light theme
    return 'light';
  };

  const [theme, setTheme] = useState(getInitialTheme);

  // Update theme attribute on document and store preference
  const rawSetTheme = (rawTheme) => {
    const root = window.document.documentElement;
    const isDark = rawTheme === 'dark';

    // Remove old class and add new class
    root.classList.remove(isDark ? 'light' : 'dark');
    root.classList.add(rawTheme);

    // Store preference
    localStorage.setItem('color-theme', rawTheme);
  };

  // Set theme when it changes
  useEffect(() => {
    rawSetTheme(theme);
  }, [theme]);

  // Context value
  const value = {
    theme,
    setTheme: (newTheme) => setTheme(newTheme),
    toggleTheme: () => setTheme(theme === 'dark' ? 'light' : 'dark'),
    isDarkMode: theme === 'dark'
  };

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
};

/**
 * Custom hook to use theme context
 */
export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};