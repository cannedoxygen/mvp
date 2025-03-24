import { useQuery } from 'react-query';
import api from '../services/api';
import { formatApiError } from '../utils/errorUtils';

/**
 * Custom hook for fetching weather data for game locations
 */
const useWeather = () => {
  /**
   * Fetch weather for a specific stadium location
   * @param {Object} location - Stadium location data
   * @param {string} location.city - City name
   * @param {string} location.state - State code (for US locations)
   * @param {string} location.country - Country code
   * @returns {Object} Query result with weather data
   */
  const getWeatherForLocation = (location) => {
    // Skip query if location data is missing
    if (!location || !location.city) {
      return {
        data: null,
        isLoading: false,
        isError: false,
        error: null
      };
    }
    
    // Format location for query
    let locationString = location.city;
    if (location.state) {
      locationString += `,${location.state}`;
    }
    if (location.country) {
      locationString += `,${location.country}`;
    }
    
    // Return query for real weather data
    return useQuery(
      ['weather', locationString],
      () => fetchWeatherData(locationString),
      {
        staleTime: 30 * 60 * 1000, // 30 minutes
        refetchInterval: 60 * 60 * 1000, // 60 minutes
        retry: 2
      }
    );
  };
  
  /**
   * Fetch weather data from API
   * @param {string} location - Formatted location string
   * @returns {Promise<Object>} Weather data
   */
  const fetchWeatherData = async (location) => {
    try {
      const response = await api.get(`/weather?location=${encodeURIComponent(location)}`);
      return response;
    } catch (error) {
      const formattedError = formatApiError(error);
      throw new Error(`Failed to fetch weather data: ${formattedError.message}`);
    }
  };
  
  /**
   * Calculate weather impact on game
   * @param {Object} weather - Weather data
   * @returns {Object} Impact assessment
   */
  const analyzeWeatherImpact = (weather) => {
    if (!weather) return null;
    
    const impacts = [];
    
    // Temperature impacts
    if (weather.temperature > 85) {
      impacts.push({
        factor: 'temperature',
        description: 'Hot conditions may favor hitters',
        impact: 'hitting'
      });
    } else if (weather.temperature < 55) {
      impacts.push({
        factor: 'temperature',
        description: 'Cool conditions may favor pitchers',
        impact: 'pitching'
      });
    }
    
    // Wind effects
    if (weather.windSpeed && weather.windSpeed > 10) {
      const windDir = (weather.windDirection || '').toUpperCase();
      
      if (['OUT', 'S', 'SW', 'SE'].includes(windDir)) {
        // Wind blowing out favors hitters
        impacts.push({
          factor: 'wind',
          description: 'Wind blowing out may increase home runs',
          impact: 'hitting'
        });
      } else if (['IN', 'N', 'NW', 'NE'].includes(windDir)) {
        // Wind blowing in favors pitchers
        impacts.push({
          factor: 'wind',
          description: 'Wind blowing in may decrease home runs',
          impact: 'pitching'
        });
      }
    }
    
    // Precipitation impacts
    if (weather.precipitation && weather.precipitation > 0) {
      impacts.push({
        factor: 'precipitation',
        description: 'Precipitation may affect ball grip and field conditions',
        impact: 'pitching'
      });
    }
    
    return {
      impacts,
      overallImpact: impacts.length > 0 ? 
        (impacts.filter(i => i.impact === 'hitting').length > 
         impacts.filter(i => i.impact === 'pitching').length ? 
         'hitting' : 'pitching') : 
        'neutral'
    };
  };
  
  return {
    getWeatherForLocation,
    analyzeWeatherImpact
  };
};

export default useWeather;