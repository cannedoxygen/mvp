# backend/app/clients/sportsdataio.py
import aiohttp
import asyncio
from typing import List, Dict, Any, Optional
from datetime import date, datetime
import logging

from app.config import settings

logger = logging.getLogger(__name__)

class SportsDataIOClient:
    """Client for fetching MLB data from SportsDataIO API"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or settings.SPORTSDATAIO_API_KEY
        self.base_url = "https://api.sportsdata.io/v3/mlb"
        self.timeout = 15  # seconds
    
    async def _make_request(self, category: str, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make a request to the SportsDataIO API"""
        url = f"{self.base_url}/{category}/json/{endpoint}"
        
        # Ensure API key is included in headers
        headers = {"Ocp-Apim-Subscription-Key": self.api_key}
        
        # Filter out None values from params to prevent serialization issues
        if params:
            params = {k: v for k, v in params.items() if v is not None}
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, params=params, headers=headers, timeout=self.timeout) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"SportsDataIO API error: {response.status} - {error_text}")
                        response.raise_for_status()
                    
                    return await response.json()
            except aiohttp.ClientError as e:
                logger.error(f"Request to SportsDataIO API failed: {str(e)}")
                raise
    
    # === Teams Endpoints ===
    
    async def get_teams(self) -> List[Dict[str, Any]]:
        """Get all MLB teams"""
        try:
            return await self._make_request("scores", "teams")
        except Exception as e:
            logger.error(f"Error fetching teams: {str(e)}")
            return []
    
    async def get_team(self, team_id: str) -> Optional[Dict[str, Any]]:
        """Get team details by ID"""
        try:
            return await self._make_request("scores", f"team/{team_id}")
        except Exception as e:
            logger.error(f"Error fetching team {team_id}: {str(e)}")
            return None
    
    # === Schedule Endpoints ===
    
    async def get_games_by_date(self, game_date: date) -> List[Dict[str, Any]]:
        """Get all MLB games for a specific date"""
        try:
            date_str = game_date.strftime("%Y-%m-%d")
            return await self._make_request("scores", f"GamesByDate/{date_str}")
        except Exception as e:
            logger.error(f"Error fetching games for date {game_date}: {str(e)}")
            return []
    
    async def get_games_by_season(self, season: str = "2025") -> List[Dict[str, Any]]:
        """Get all MLB games for a specific season"""
        try:
            return await self._make_request("scores", f"Schedule/{season}")
        except Exception as e:
            logger.error(f"Error fetching schedule for season {season}: {str(e)}")
            return []
    
    # === Player Endpoints ===
    
    async def get_players(self) -> List[Dict[str, Any]]:
        """Get all MLB players"""
        try:
            return await self._make_request("scores", "Players")
        except Exception as e:
            logger.error(f"Error fetching players: {str(e)}")
            return []
    
    async def get_team_players(self, team_id: str) -> List[Dict[str, Any]]:
        """Get all players for a specific team"""
        try:
            return await self._make_request("scores", f"Players/{team_id}")
        except Exception as e:
            logger.error(f"Error fetching players for team {team_id}: {str(e)}")
            return []
    
    async def get_player(self, player_id: str) -> Optional[Dict[str, Any]]:
        """Get player details by ID"""
        try:
            return await self._make_request("scores", f"Player/{player_id}")
        except Exception as e:
            logger.error(f"Error fetching player {player_id}: {str(e)}")
            return None
    
    # === Game Stats Endpoints ===
    
    async def get_box_score(self, game_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed box score for a specific game"""
        try:
            # Check if game_id is valid before making request
            if not game_id or game_id == "today":
                logger.warning(f"Invalid game ID for box score: {game_id}")
                return None
                
            return await self._make_request("stats", f"BoxScore/{game_id}")
        except Exception as e:
            logger.error(f"Error fetching box score for game {game_id}: {str(e)}")
            return None
    
    async def get_box_scores_by_date(self, game_date: date) -> List[Dict[str, Any]]:
        """Get box scores for all games on a specific date"""
        try:
            date_str = game_date.strftime("%Y-%m-%d")
            return await self._make_request("stats", f"BoxScoresByDate/{date_str}")
        except Exception as e:
            logger.error(f"Error fetching box scores for date {game_date}: {str(e)}")
            return []
    
    async def get_play_by_play(self, game_id: str) -> Optional[Dict[str, Any]]:
        """Get play by play data for a specific game"""
        try:
            return await self._make_request("stats", f"PlayByPlay/{game_id}")
        except Exception as e:
            logger.error(f"Error fetching play by play for game {game_id}: {str(e)}")
            return None
    
    # === Standings Endpoints ===
    
    async def get_standings(self, season: str = "2025") -> List[Dict[str, Any]]:
        """Get standings for a specific season"""
        try:
            return await self._make_request("scores", f"Standings/{season}")
        except Exception as e:
            logger.error(f"Error fetching standings for season {season}: {str(e)}")
            return []
    
    # === Odds Endpoints ===
    
    async def get_game_odds_by_date(self, game_date: date) -> List[Dict[str, Any]]:
        """Get betting odds for all games on a specific date"""
        try:
            date_str = game_date.strftime("%Y-%m-%d")
            return await self._make_request("odds", f"GameOddsByDate/{date_str}")
        except Exception as e:
            logger.error(f"Error fetching game odds for date {game_date}: {str(e)}")
            return []
    
    async def get_player_props_by_date(self, game_date: date) -> List[Dict[str, Any]]:
        """Get player prop bets for all games on a specific date"""
        try:
            date_str = game_date.strftime("%Y-%m-%d")
            return await self._make_request("odds", f"PlayerPropsByDate/{date_str}")
        except Exception as e:
            logger.error(f"Error fetching player props for date {game_date}: {str(e)}")
            return []
    
    # === Projections Endpoints ===
    
    async def get_projected_player_game_stats(self, game_date: date) -> List[Dict[str, Any]]:
        """Get projected player stats for games on a specific date"""
        try:
            date_str = game_date.strftime("%Y-%m-%d")
            return await self._make_request("projections", f"PlayerGameProjectionStatsByDate/{date_str}")
        except Exception as e:
            logger.error(f"Error fetching projected player stats for date {game_date}: {str(e)}")
            return []
    
    async def get_starting_lineups_by_date(self, game_date: date) -> List[Dict[str, Any]]:
        """Get starting lineups for all games on a specific date"""
        try:
            # Note: Starting lineups are included in the projected player game stats endpoint
            return await self.get_projected_player_game_stats(game_date)
        except Exception as e:
            logger.error(f"Error fetching starting lineups for date {game_date}: {str(e)}")
            return []
    
    # === Injuries Endpoints ===
    
    async def get_injuries(self) -> List[Dict[str, Any]]:
        """Get current MLB injuries"""
        try:
            return await self._make_request("scores", "Injuries")
        except Exception as e:
            logger.error(f"Error fetching injuries: {str(e)}")
            return []
    
    # === News Endpoints ===
    
    async def get_news(self) -> List[Dict[str, Any]]:
        """Get latest MLB news"""
        try:
            return await self._make_request("scores", "News")
        except Exception as e:
            logger.error(f"Error fetching news: {str(e)}")
            return []
    
    async def get_player_news(self, player_id: str) -> List[Dict[str, Any]]:
        """Get news for a specific player"""
        try:
            return await self._make_request("scores", f"NewsByPlayerID/{player_id}")
        except Exception as e:
            logger.error(f"Error fetching news for player {player_id}: {str(e)}")
            return []
    
    # === Stadium/Weather Endpoints ===
    
    async def get_stadiums(self) -> List[Dict[str, Any]]:
        """Get all MLB stadiums"""
        try:
            return await self._make_request("scores", "Stadiums")
        except Exception as e:
            logger.error(f"Error fetching stadiums: {str(e)}")
            return []
    
    async def get_stadium_weather(self, game_date: date) -> List[Dict[str, Any]]:
        """Get weather forecasts for stadiums with games on a specific date"""
        try:
            # Weather is included in the games by date endpoint
            games = await self.get_games_by_date(game_date)
            
            weather_data = []
            for game in games:
                if "StadiumID" in game and "Weather" in game:
                    weather_data.append({
                        "GameID": game.get("GameID"),
                        "StadiumID": game.get("StadiumID"),
                        "Stadium": game.get("Stadium"),
                        "Weather": game.get("Weather"),
                        "Temperature": game.get("Temperature"),
                        "WindSpeed": game.get("WindSpeed"),
                        "WindDirection": game.get("WindDirection")
                    })
            
            return weather_data
        except Exception as e:
            logger.error(f"Error fetching stadium weather for date {game_date}: {str(e)}")
            return []