import React from 'react';
import { Clock, Activity, Check, AlertTriangle } from 'lucide-react';

/**
 * GameTimeline component
 * Displays important events and status updates for a game
 */
const GameTimeline = ({ events = [], className = '' }) => {
  // Skip rendering if no events
  if (!events || events.length === 0) {
    return (
      <div className="text-center text-gray-500 py-4">
        No timeline events available
      </div>
    );
  }
  
  // Icon mapping based on event type
  const getEventIcon = (type) => {
    switch (type) {
      case 'time':
        return <Clock size={16} className="text-gray-500" />;
      case 'status':
        return <Activity size={16} className="text-blue-500" />;
      case 'update':
        return <Check size={16} className="text-green-500" />;
      case 'alert':
        return <AlertTriangle size={16} className="text-amber-500" />;
      default:
        return <Clock size={16} className="text-gray-500" />;
    }
  };
  
  // Format timestamp
  const formatTime = (timestamp) => {
    if (!timestamp) return '';
    
    const date = new Date(timestamp);
    return date.toLocaleTimeString('en-US', {
      hour: 'numeric',
      minute: '2-digit',
      hour12: true
    });
  };
  
  return (
    <div className={className}>
      <div className="flow-root">
        <ul className="-mb-8">
          {events.map((event, eventIndex) => (
            <li key={eventIndex}>
              <div className="relative pb-8">
                {/* Connector line between events */}
                {eventIndex !== events.length - 1 && (
                  <span 
                    className="absolute top-5 left-5 -ml-px h-full w-0.5 bg-gray-200"
                    aria-hidden="true"
                  />
                )}
                
                <div className="relative flex items-start space-x-3">
                  {/* Icon */}
                  <div className="relative">
                    <div className="h-10 w-10 rounded-full bg-gray-50 flex items-center justify-center ring-4 ring-white">
                      {getEventIcon(event.type)}
                    </div>
                  </div>
                  
                  {/* Content */}
                  <div className="min-w-0 flex-1 pt-1.5">
                    <div>
                      <div className="text-sm text-gray-500">
                        {formatTime(event.timestamp)}
                      </div>
                      <p className="mt-0.5 text-sm font-medium text-gray-900">
                        {event.title}
                      </p>
                    </div>
                    {event.description && (
                      <div className="mt-1">
                        <p className="text-sm text-gray-600">
                          {event.description}
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default GameTimeline;