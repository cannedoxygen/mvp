import React from 'react';
import { Thermometer, Wind, Droplets, Cloud } from 'lucide-react';

/**
 * WeatherInfo component
 * Displays current and forecasted weather conditions for a game
 */
const WeatherInfo = ({ weather }) => {
  // Handle missing weather data
  if (!weather) {
    return (
      <div className="text-center text-gray-500 py-4">
        Weather data not available
      </div>
    );
  }

  // Helper function to get wind direction as text
  const getWindDirectionText = (direction) => {
    // Handle numeric degrees
    if (typeof direction === 'number') {
      const directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'];
      const index = Math.round(direction / 45) % 8;
      return directions[index];
    }
    
    // Handle text direction
    if (typeof direction === 'string') {
      return direction.toUpperCase();
    }
    
    return 'Unknown';
  };

  // Helper to determine if weather conditions impact the game
  const getWeatherImpact = () => {
    const impacts = [];
    const temp = weather.temperature;
    const windSpeed = weather.windSpeed;
    const windDirection = weather.windDirection || '';
    const precipitation = weather.precipitation || 0;

    // Temperature impacts
    if (temp > 85) {
      impacts.push('Hot conditions may favor hitters');
    } else if (temp < 55) {
      impacts.push('Cool conditions may favor pitchers');
    }

    // Wind impacts
    if (windSpeed > 10) {
      const dir = windDirection.toLowerCase();
      if (dir.includes('out') || dir.includes('south')) {
        impacts.push('Wind blowing out may increase home runs');
      } else if (dir.includes('in') || dir.includes('north')) {
        impacts.push('Wind blowing in may decrease home runs');
      }
    }

    // Precipitation impacts
    if (precipitation > 0 && precipitation < 0.1) {
      impacts.push('Light rain may affect grip on ball');
    } else if (precipitation >= 0.1) {
      impacts.push('Rain may significantly affect playing conditions');
    }

    return impacts;
  };

  const weatherImpacts = getWeatherImpact();
  
  // Determine condition text
  const getConditionText = () => {
    if (weather.condition) {
      return weather.condition;
    }
    
    // Try to determine from cloudCover if condition is missing
    if (weather.cloudCover !== undefined) {
      if (weather.cloudCover < 25) return 'Clear';
      if (weather.cloudCover < 50) return 'Partly Cloudy';
      if (weather.cloudCover < 75) return 'Mostly Cloudy';
      return 'Cloudy';
    }
    
    return 'Unknown';
  };

  return (
    <div>
      <h3 className="font-medium mb-3">Weather Conditions</h3>
      
      <div className="space-y-3">
        {/* Temperature */}
        {weather.temperature !== undefined && (
          <div className="flex items-center">
            <Thermometer size={18} className="text-gray-500 mr-2" />
            <span className="text-sm">
              {weather.temperature}°F - {
                weather.temperature < 55 ? 'Cool' : 
                weather.temperature > 85 ? 'Hot' : 'Moderate'
              }
            </span>
          </div>
        )}
        
        {/* Wind */}
        {weather.windSpeed !== undefined && (
          <div className="flex items-center">
            <Wind size={18} className="text-gray-500 mr-2" />
            <span className="text-sm">
              {weather.windSpeed} mph {
                typeof weather.windDirection === 'number' 
                  ? getWindDirectionText(weather.windDirection)
                  : weather.windDirection || 'Unknown direction'
              }
            </span>
          </div>
        )}
        
        {/* Precipitation */}
        {weather.precipitation > 0 && (
          <div className="flex items-center">
            <Droplets size={18} className="text-gray-500 mr-2" />
            <span className="text-sm">
              {weather.precipitation < 0.1 ? 'Light rain' : 'Rain'} ({weather.precipitation} in)
            </span>
          </div>
        )}
        
        {/* Cloud cover */}
        <div className="flex items-center">
          <Cloud size={18} className="text-gray-500 mr-2" />
          <span className="text-sm">
            {getConditionText()}
            {weather.cloudCover !== undefined ? ` (${weather.cloudCover}%)` : ''}
          </span>
        </div>
      </div>
      
      {/* Weather impacts on game */}
      {weatherImpacts.length > 0 && (
        <div className="mt-4 pt-3 border-t border-gray-100">
          <h4 className="text-sm font-medium mb-2">Potential Game Impact</h4>
          <ul className="text-sm text-gray-600 space-y-1">
            {weatherImpacts.map((impact, index) => (
              <li key={index} className="flex items-start">
                <span className="mr-2">•</span>
                <span>{impact}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default WeatherInfo;