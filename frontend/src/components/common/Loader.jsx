import React from 'react';

/**
 * Loader component
 * Displays a loading spinner with optional text
 */
const Loader = ({
  size = 'md',
  text = 'Loading...',
  showText = true,
  fullPage = false,
  className = '',
  ...props
}) => {
  // Size variations for the spinner
  const spinnerSizes = {
    sm: 'w-4 h-4',
    md: 'w-6 h-6',
    lg: 'w-8 h-8',
    xl: 'w-12 h-12'
  };
  
  // Text size based on spinner size
  const textSizes = {
    sm: 'text-xs',
    md: 'text-sm',
    lg: 'text-base',
    xl: 'text-lg'
  };
  
  // Base classes for different layouts
  const baseClasses = fullPage
    ? 'fixed inset-0 flex items-center justify-center bg-white bg-opacity-75 z-50'
    : 'flex items-center justify-center';
    
  const containerClasses = `${baseClasses} ${className}`.trim();
  
  return (
    <div className={containerClasses} role="status" {...props}>
      {/* Spinner */}
      <svg 
        className={`animate-spin text-primary-600 ${spinnerSizes[size]}`} 
        xmlns="http://www.w3.org/2000/svg" 
        fill="none" 
        viewBox="0 0 24 24"
      >
        <circle 
          className="opacity-25" 
          cx="12" 
          cy="12" 
          r="10" 
          stroke="currentColor" 
          strokeWidth="4"
        />
        <path 
          className="opacity-75" 
          fill="currentColor" 
          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
        />
      </svg>
      
      {/* Loading text */}
      {showText && (
        <span className={`ml-3 ${textSizes[size]} text-gray-700`}>
          {text}
        </span>
      )}
      
      {/* Screen reader text */}
      <span className="sr-only">Loading</span>
    </div>
  );
};

export default Loader;