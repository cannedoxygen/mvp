# backend/app/clients/weather.py
import aiohttp
import asyncio
from typing import Dict, Any, Optional
import logging

from app.config import settings

logger = logging.getLogger(__name__)

class WeatherClient:
    """Client for fetching weather data for game locations"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or settings.WEATHER_API_KEY
        self.base_url = "https://api.weatherapi.com/v1"
        self.timeout = 10  # seconds
    
    async def get_weather(self, location: str, date: Optional[str] = None) -> Dict[str, Any]:
        """
        Get weather for a location
        
        Args:
            location: City name or coordinates
            date: Optional date string (YYYY-MM-DD). If None, gets current weather.
        
        Returns:
            Dict containing weather data
        """
        if date:
            # Historical or forecast data
            endpoint = "forecast.json"
            params = {
                "key": self.api_key,
                "q": location,
                "dt": date
            }
        else:
            # Current weather
            endpoint = "current.json"
            params = {
                "key": self.api_key,
                "q": location
            }
        
        url = f"{self.base_url}/{endpoint}"
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, params=params, timeout=self.timeout) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"Weather API error: {response.status} - {error_text}")
                        response.raise_for_status()
                    
                    data = await response.json()
                    return self._format_weather_data(data)
            except aiohttp.ClientError as e:
                logger.error(f"Request to Weather API failed: {str(e)}")
                raise
    
    def _format_weather_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Format weather data into a consistent structure"""
        # Extract location info
        location = data.get("location", {})
        
        # Extract weather data from current or forecast
        if "current" in data:
            weather = data["current"]
            temp_f = weather.get("temp_f")
            condition = weather.get("condition", {}).get("text")
            wind_mph = weather.get("wind_mph")
            wind_dir = weather.get("wind_dir")
            precip_in = weather.get("precip_in")
            cloud = weather.get("cloud")
            humidity = weather.get("humidity")
        elif "forecast" in data and data.get("forecast", {}).get("forecastday"):
            day = data["forecast"]["forecastday"][0]["day"]
            temp_f = day.get("avgtemp_f")
            condition = day.get("condition", {}).get("text")
            wind_mph = day.get("maxwind_mph")
            wind_dir = None  # Not provided in forecast
            precip_in = day.get("totalprecip_in")
            cloud = None  # Not provided in forecast
            humidity = day.get("avghumidity")
        else:
            # No weather data found
            return {
                "error": "No weather data available"
            }
        
        # Return formatted data
        return {
            "location": f"{location.get('name')}, {location.get('region')}",
            "temperature": temp_f,
            "condition": condition,
            "windSpeed": wind_mph,
            "windDirection": wind_dir,
            "precipitation": precip_in,
            "cloudCover": cloud,
            "humidity": humidity,
            "timestamp": data.get("location", {}).get("localtime")
        }