import React from 'react';
import { ArrowUpRight, ArrowDownRight, Minus } from 'lucide-react';

/**
 * ValueIndicator component
 * Visual indicator for betting value assessment
 */
const ValueIndicator = ({
  value,
  type = 'auto',
  showIcon = true,
  showText = true,
  size = 'md',
  className = '',
  ...props
}) => {
  // Determine indicator type if set to auto
  const determineType = () => {
    if (type !== 'auto') return type;
    
    if (value > 0.05) return 'positive';
    if (value < -0.05) return 'negative';
    return 'neutral';
  };
  
  // Get current type
  const indicatorType = determineType();
  
  // Type-based styling and icons
  const typeConfig = {
    positive: {
      icon: ArrowUpRight,
      colorClass: 'text-green-600',
      text: value > 0.1 ? 'Strong Value' : 'Value'
    },
    negative: {
      icon: ArrowDownRight,
      colorClass: 'text-red-600',
      text: value < -0.1 ? 'Poor Value' : 'Below Value'
    },
    neutral: {
      icon: Minus,
      colorClass: 'text-gray-500',
      text: 'Fair Value'
    }
  };
  
  // Get config for current type
  const config = typeConfig[indicatorType];
  
  // Size-based classes
  const sizeClasses = {
    sm: 'text-xs',
    md: 'text-sm',
    lg: 'text-base'
  };
  
  // Icon sizes
  const iconSizes = {
    sm: 14,
    md: 16,
    lg: 18
  };
  
  return (
    <div 
      className={`inline-flex items-center ${config.colorClass} ${sizeClasses[size]} font-medium ${className}`}
      {...props}
    >
      {showIcon && (
        <config.icon size={iconSizes[size]} className="mr-1" />
      )}
      {showText && (
        <span>{config.text}</span>
      )}
    </div>
  );
};

export default ValueIndicator;