# backend/app/services/oddsService.py
import logging
from typing import List, Dict, Any, Optional
from datetime import date, datetime

from app.clients.sportsdataio import SportsDataIOClient
from app.core.cache import cache

logger = logging.getLogger(__name__)

class OddsService:
    """Service for fetching and processing betting odds data"""
    
    def __init__(self, sports_data_client: Optional[SportsDataIOClient] = None):
        self.sports_data_client = sports_data_client or SportsDataIOClient()
    
    @cache(ttl=900)  # Cache for 15 minutes
    async def get_todays_odds(self) -> List[Dict[str, Any]]:
        """
        Get betting odds for all of today's MLB games
        
        Returns:
            List of game odds information
        """
        today = date.today()
        return await self.get_odds_by_date(today)
    
    @cache(ttl=900)  # Cache for 15 minutes
    async def get_odds_by_date(self, odds_date: date) -> List[Dict[str, Any]]:
        """
        Get betting odds for all MLB games on a specific date
        
        Args:
            odds_date: Date to fetch odds for
            
        Returns:
            List of game odds information
        """
        try:
            # Fetch odds from SportsDataIO
            odds_data = await self.sports_data_client.get_game_odds_by_date(odds_date)
            
            # Transform to our application model
            transformed_odds = []
            
            for odds in odds_data:
                transformed_odd = {
                    "gameId": odds.get("GameID"),
                    "homeTeam": odds.get("HomeTeam"),
                    "awayTeam": odds.get("AwayTeam"),
                    "homeMoneyline": odds.get("HomeMoneyLine"),
                    "awayMoneyline": odds.get("AwayMoneyLine"),
                    "totalRuns": odds.get("OverUnder"),
                    "overOdds": odds.get("OverPayout"),
                    "underOdds": odds.get("UnderPayout"),
                    "homeRunLine": odds.get("HomePointSpread"),
                    "awayRunLine": odds.get("AwayPointSpread"),
                    "homeRunLineOdds": odds.get("HomePointSpreadPayout"),
                    "awayRunLineOdds": odds.get("AwayPointSpreadPayout"),
                    "lastUpdated": odds.get("LastUpdated")
                }
                
                transformed_odds.append(transformed_odd)
            
            return transformed_odds
            
        except Exception as e:
            logger.error(f"Error fetching odds by date: {str(e)}")
            return []
    
    @cache(ttl=900)  # Cache for 15 minutes
    async def get_game_odds(self, game_id: str) -> Optional[Dict[str, Any]]:
        """
        Get betting odds for a specific game
        
        Args:
            game_id: ID of the game to fetch odds for
            
        Returns:
            Game odds information
        """
        try:
            # We need to determine the game date first
            game_date = await self._get_game_date(game_id)
            
            if not game_date:
                return None
                
            # Fetch all odds for that date
            all_odds = await self.get_odds_by_date(game_date)
            
            # Find the specific game
            for odds in all_odds:
                if odds.get("gameId") == game_id:
                    return odds
                    
            return None
            
        except Exception as e:
            logger.error(f"Error fetching game odds: {str(e)}")
            return None
    
    @cache(ttl=900)  # Cache for 15 minutes
    async def get_game_props(self, game_id: str) -> List[Dict[str, Any]]:
        """
        Get player prop bets for a specific game
        
        Args:
            game_id: ID of the game to fetch props for
            
        Returns:
            List of player prop bets
        """
        try:
            # Get the game date
            game_date = await self._get_game_date(game_id)
            
            if not game_date:
                return []
                
            # Fetch all props for that date
            all_props = await self.sports_data_client.get_player_props_by_date(game_date)
            
            # Filter to only include props for this game
            game_props = []
            for prop in all_props:
                if prop.get("GameID") == game_id:
                    transformed_prop = {
                        "gameId": game_id,
                        "playerId": prop.get("PlayerID"),
                        "playerName": prop.get("Name"),
                        "team": prop.get("Team"),
                        "position": prop.get("Position"),
                        "betType": prop.get("BetType"),
                        "description": prop.get("Description"),
                        "line": prop.get("OverUnder"),
                        "overOdds": prop.get("OverPayout"),
                        "underOdds": prop.get("UnderPayout")
                    }
                    game_props.append(transformed_prop)
            
            return game_props
            
        except Exception as e:
            logger.error(f"Error fetching game props: {str(e)}")
            return []
    
    async def _get_game_date(self, game_id: str) -> Optional[date]:
        """
        Helper method to get the date of a game from its ID
        """
        try:
            # Attempt to parse from the ID first (e.g., 'mlb-2025-03-23-lad-sf')
            if game_id.startswith('mlb-') and len(game_id) > 14:
                parts = game_id.split('-')
                if len(parts) >= 4:
                    year = int(parts[1])
                    month = int(parts[2])
                    day = int(parts[3])
                    return date(year, month, day)
            
            # If we can't parse from ID, query the game details
            from app.services.gameService import GameService
            game_service = GameService(sports_data_client=self.sports_data_client)
            game = await game_service.get_game_details(game_id)
            
            if game and 'startTime' in game:
                start_time = game['startTime']
                if isinstance(start_time, str):
                    dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                    return dt.date()
            
            # If all else fails, use today's date
            return date.today()
            
        except Exception as e:
            logger.error(f"Error determining game date: {str(e)}")
            return None