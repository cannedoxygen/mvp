import React, { useState } from 'react';

/**
 * TabPanel component
 * Displays content in organized, switchable tabs
 */
const TabPanel = ({
  tabs = [],
  defaultActiveTab = 0,
  onChange,
  variant = 'default',
  className = '',
  tabsClassName = '',
  panelClassName = '',
  ...props
}) => {
  // Active tab state
  const [activeTab, setActiveTab] = useState(defaultActiveTab);
  
  // Handle tab click
  const handleTabClick = (index) => {
    setActiveTab(index);
    if (onChange) {
      onChange(index);
    }
  };
  
  // Variant styling
  const variantStyles = {
    default: {
      container: 'border-b border-gray-200',
      tabs: 'flex -mb-px',
      tab: {
        active: 'border-b-2 border-primary-500 text-primary-600 font-medium',
        inactive: 'text-gray-500 hover:text-gray-700 hover:border-gray-300'
      }
    },
    pills: {
      container: 'mb-4',
      tabs: 'flex space-x-2',
      tab: {
        active: 'bg-primary-100 text-primary-700 font-medium',
        inactive: 'bg-gray-100 text-gray-600 hover:bg-gray-200'
      }
    },
    bordered: {
      container: 'border-b border-gray-200',
      tabs: 'flex -mb-px',
      tab: {
        active: 'bg-white border-l border-t border-r border-gray-200 rounded-t text-primary-600 font-medium',
        inactive: 'text-gray-500 hover:text-gray-700'
      }
    }
  };
  
  // Get current variant style
  const style = variantStyles[variant] || variantStyles.default;
  
  // Base tab classes
  const baseTabClasses = 'px-4 py-2 text-sm cursor-pointer transition-colors';
  
  // If no tabs, return empty div
  if (!tabs.length) return <div className={className} {...props} />;
  
  return (
    <div className={className} {...props}>
      {/* Tab navigation */}
      <div className={`${style.container} ${tabsClassName}`.trim()}>
        <div className={style.tabs}>
          {tabs.map((tab, index) => (
            <div
              key={index}
              className={`
                ${baseTabClasses}
                ${index === activeTab ? style.tab.active : style.tab.inactive}
                ${index === 0 ? 'rounded-tl' : ''}
                ${index === tabs.length - 1 ? 'rounded-tr' : ''}
              `}
              onClick={() => handleTabClick(index)}
              role="tab"
              aria-selected={index === activeTab}
              tabIndex={index === activeTab ? 0 : -1}
            >
              {tab.label}
            </div>
          ))}
        </div>
      </div>
      
      {/* Active tab content */}
      <div className={`pt-4 ${panelClassName}`.trim()}>
        {tabs[activeTab]?.content}
      </div>
    </div>
  );
};

export default TabPanel;