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
    
    async def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make a request to the SportsDataIO API"""
        url = f"{self.base_url}/{endpoint}"
        
        # Ensure API key is included
        params = params or {}
        
        # Add API key to headers
        headers = {"Ocp-Apim-Subscription-Key": self.api_key}
        
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
        endpoint = "json/teams"
        return await self._make_request(endpoint)
    
    async def get_team(self, team_id: str) -> Dict[str, Any]:
        """Get team details by ID"""
        teams = await self.get_teams()
        for team in teams:
            if team.get("TeamID") == team_id:
                return team
        return None
    
    # === Schedule Endpoints ===
    
    async def get_games_by_date(self, game_date: date) -> List[Dict[str, Any]]:
        """Get all MLB games for a specific date"""
        date_str = game_date.strftime("%Y-%b-%d")
        endpoint = f"json/GamesByDate/{date_str}"
        return await self._make_request(endpoint)
    
    async def get_games_by_season(self, season: str = "2025") -> List[Dict[str, Any]]:
        """Get all MLB games for a specific season"""
        endpoint = f"json/Games/{season}"
        return await self._make_request(endpoint)
    
    # === Player Endpoints ===
    
    async def get_players(self) -> List[Dict[str, Any]]:
        """Get all MLB players"""
        endpoint = "json/Players"
        return await self._make_request(endpoint)
    
    async def get_player(self, player_id: str) -> Dict[str, Any]:
        """Get player details by ID"""
        players = await self.get_players()
        for player in players:
            if player.get("PlayerID") == player_id:
                return player
        return None
    
    async def get_team_players(self, team_id: str) -> List[Dict[str, Any]]:
        """Get all players for a specific team"""
        players = await self.get_players()
        team_players = [p for p in players if p.get("TeamID") == team_id]
        return team_players
    
    # === Game Stats Endpoints ===
    
    async def get_box_score(self, game_id: str) -> Dict[str, Any]:
        """Get detailed box score for a specific game"""
        endpoint = f"json/BoxScore/{game_id}"
        return await self._make_request(endpoint)
    
    async def get_box_scores_by_date(self, game_date: date) -> List[Dict[str, Any]]:
        """Get box scores for all games on a specific date"""
        date_str = game_date.strftime("%Y-%b-%d")
        endpoint = f"json/BoxScoresByDate/{date_str}"
        return await self._make_request(endpoint)
    
    async def get_play_by_play(self, game_id: str) -> Dict[str, Any]:
        """Get play by play data for a specific game"""
        endpoint = f"json/PlayByPlay/{game_id}"
        return await self._make_request(endpoint)
    
    # === Projections Endpoints ===
    
    async def get_projected_player_game_stats(self, game_date: date) -> List[Dict[str, Any]]:
        """Get projected player stats for games on a specific date"""
        date_str = game_date.strftime("%Y-%b-%d")
        endpoint = f"json/PlayerGameProjectionStatsByDate/{date_str}"
        return await self._make_request(endpoint)
    
    async def get_starting_lineups_by_date(self, game_date: date) -> List[Dict[str, Any]]:
        """Get starting lineups for all games on a specific date"""
        # Note: Starting lineups are included in the projected player game stats endpoint
        projected_stats = await self.get_projected_player_game_stats(game_date)
        
        # Process the data to extract lineups by game
        lineups = {}
        for player in projected_stats:
            game_id = player.get("GameID")
            if not game_id:
                continue
                
            team_id = player.get("TeamID")
            batting_order = player.get("BattingOrder")
            
            if not batting_order or int(batting_order or 0) <= 0:
                continue
                
            if game_id not in lineups:
                lineups[game_id] = {"home": [], "away": []}
            
            # Determine if home or away team based on game info
            is_home = player.get("HomeOrAway") == "HOME"
            lineup_key = "home" if is_home else "away"
            
            lineups[game_id][lineup_key].append({
                "player_id": player.get("PlayerID"),
                "name": player.get("Name"),
                "position": player.get("Position"),
                "batting_order": int(batting_order),
                "confirmed": player.get("BattingOrderConfirmed", False)
            })
            
            # Sort by batting order
            lineups[game_id][lineup_key].sort(key=lambda x: x["batting_order"])
        
        # Convert to list format
        result = []
        for game_id, lineup in lineups.items():
            result.append({
                "GameID": game_id,
                "HomeLineup": lineup["home"],
                "AwayLineup": lineup["away"],
                "HomeLineupConfirmed": all(p.get("confirmed", False) for p in lineup["home"]),
                "AwayLineupConfirmed": all(p.get("confirmed", False) for p in lineup["away"])
            })
            
        return result
    
    # === Odds Endpoints ===
    
    async def get_game_odds_by_date(self, game_date: date) -> List[Dict[str, Any]]:
        """Get betting odds for all games on a specific date"""
        date_str = game_date.strftime("%Y-%b-%d")
        endpoint = f"json/GameOddsByDate/{date_str}"
        return await self._make_request(endpoint)
    
    async def get_player_props_by_date(self, game_date: date) -> List[Dict[str, Any]]:
        """Get player prop bets for all games on a specific date"""
        date_str = game_date.strftime("%Y-%b-%d")
        endpoint = f"json/PlayerPropsByDate/{date_str}"
        return await self._make_request(endpoint)
    
    # === Standings Endpoints ===
    
    async def get_standings(self, season: str = "2025") -> Dict[str, Any]:
        """Get standings for a specific season"""
        endpoint = f"json/Standings/{season}"
        return await self._make_request(endpoint)
    
    # === Weather Endpoints ===
    
    async def get_stadium_weather(self, game_date: date) -> List[Dict[str, Any]]:
        """Get weather forecasts for stadiums with games on a specific date"""
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