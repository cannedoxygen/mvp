import React from 'react';
import { XCircle, AlertCircle, Info } from 'lucide-react';

/**
 * ErrorMessage component
 * Displays error messages with appropriate styling
 */
const ErrorMessage = ({
  message,
  type = 'error',
  dismissible = false,
  onDismiss,
  className = '',
  ...props
}) => {
  // Type-based styling
  const typeStyles = {
    error: {
      containerClass: 'bg-red-50 border-red-200 text-red-700',
      iconColor: 'text-red-500',
      icon: XCircle
    },
    warning: {
      containerClass: 'bg-yellow-50 border-yellow-200 text-yellow-700',
      iconColor: 'text-yellow-500',
      icon: AlertCircle
    },
    info: {
      containerClass: 'bg-blue-50 border-blue-200 text-blue-700',
      iconColor: 'text-blue-500',
      icon: Info
    }
  };
  
  // Get styles for current type
  const { containerClass, iconColor, icon: Icon } = typeStyles[type] || typeStyles.error;
  
  // Return null if no message
  if (!message) return null;
  
  return (
    <div 
      className={`border rounded-md px-4 py-3 ${containerClass} ${className}`}
      role={type === 'error' ? 'alert' : 'status'}
      {...props}
    >
      <div className="flex items-start">
        <div className="flex-shrink-0">
          <Icon className={`w-5 h-5 ${iconColor}`} />
        </div>
        <div className="ml-3 flex-1">
          <p className="text-sm">
            {message}
          </p>
        </div>
        
        {dismissible && onDismiss && (
          <button
            type="button"
            className="ml-auto -mx-1.5 -my-1.5 rounded-md p-1.5 inline-flex focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
            onClick={onDismiss}
            aria-label="Dismiss"
          >
            <span className="sr-only">Dismiss</span>
            <XCircle className={`h-5 w-5 ${iconColor}`} />
          </button>
        )}
      </div>
    </div>
  );
};

export default ErrorMessage;