import React from 'react';

/**
 * Card component
 * Reusable container with various style options
 */
const Card = ({
  children,
  title,
  subtitle,
  footer,
  padding = 'default',
  bordered = true,
  hoverable = false,
  className = '',
  headerClassName = '',
  bodyClassName = '',
  footerClassName = '',
  ...props
}) => {
  // Padding options
  const paddingClasses = {
    none: '',
    small: 'p-3',
    default: 'p-4',
    large: 'p-6'
  };
  
  // Base classes
  const cardClasses = `
    bg-white 
    rounded-lg 
    shadow-sm 
    ${bordered ? 'border border-gray-200' : ''}
    ${hoverable ? 'transition-shadow hover:shadow-md' : ''}
    ${className}
  `.trim().replace(/\s+/g, ' ');
  
  // Header, body, and footer padding
  const headerPadding = padding !== 'none' ? paddingClasses[padding] : 'p-4';
  const bodyPadding = padding !== 'none' ? paddingClasses[padding] : 'px-4 py-3';
  const footerPadding = padding !== 'none' ? paddingClasses[padding] : 'p-4';
  
  return (
    <div className={cardClasses} {...props}>
      {/* Optional header section */}
      {(title || subtitle) && (
        <div className={`border-b border-gray-200 ${headerPadding} ${headerClassName}`}>
          {title && (
            <h3 className="text-lg font-medium text-gray-900">
              {title}
            </h3>
          )}
          {subtitle && (
            <p className="mt-1 text-sm text-gray-600">
              {subtitle}
            </p>
          )}
        </div>
      )}
      
      {/* Card body */}
      <div className={`${!title && !subtitle ? bodyPadding : paddingClasses[padding]} ${bodyClassName}`}>
        {children}
      </div>
      
      {/* Optional footer */}
      {footer && (
        <div className={`border-t border-gray-200 ${footerPadding} ${footerClassName}`}>
          {footer}
        </div>
      )}
    </div>
  );
};

export default Card;