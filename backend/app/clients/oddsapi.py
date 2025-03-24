# backend/app/clients/oddsapi.py
import aiohttp
import asyncio
from typing import List, Dict, Any, Optional
from datetime import date, datetime
import logging

from app.config import settings
from app.models.odds import GameOdds, PropBet

logger = logging.getLogger(__name__)

class OddsAPIClient:
    """Client for fetching odds data from The Odds API"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or settings.ODDS_API_KEY
        self.base_url = "https://api.the-odds-api.com/v4"
        self.timeout = 10  # seconds
    
    async def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make a request to the Odds API"""
        url = f"{self.base_url}/{endpoint}"
        
        # Ensure API key is included
        params = params or {}
        params["apiKey"] = self.api_key
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, params=params, timeout=self.timeout) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"Odds API error: {response.status} - {error_text}")
                        response.raise_for_status()
                    
                    return await response.json()
            except aiohttp.ClientError as e:
                logger.error(f"Request to Odds API failed: {str(e)}")
                raise
    
    async def get_odds(self, sport: str = "baseball_mlb", date: Optional[date] = None) -> List[GameOdds]:
        """Get odds for all games on a specific date"""
        params = {
            "sport": sport,
            "regions": "us",
            "markets": "h2h,spreads,totals"
        }
        
        if date:
            # Format date as required by the API
            params["date"] = date.strftime("%Y-%m-%d")
        
        data = await self._make_request("sports", params)
        
        # Transform API response to our model
        odds_list = []
        for game_data in data:
            odds = self._parse_game_odds(game_data)
            odds_list.append(odds)
        
        return odds_list
    
    async def get_game_odds(self, game_id: str) -> GameOdds:
        """Get odds for a specific game"""
        # Get the game's sport type from the ID (e.g., "mlb-2025-03-23-lad-sf")
        sport = "baseball_mlb"  # Default to MLB
        if game_id.startswith("nfl"):
            sport = "football_nfl"
        elif game_id.startswith("nba"):
            sport = "basketball_nba"
        
        # Fetch all games for this sport
        games = await self.get_odds(sport=sport)
        
        # Find the specific game
        for game in games:
            if game.game_id == game_id:
                return game
        
        raise ValueError(f"Game with ID {game_id} not found")
    
    async def get_game_props(self, game_id: str) -> List[PropBet]:
        """Get prop bets for a specific game"""
        # The Odds API endpoint for props
        endpoint = f"sports/baseball_mlb/events/{game_id}/odds"
        params = {
            "markets": "player_props",
            "regions": "us"
        }
        
        data = await self._make_request(endpoint, params)
        
        # Transform API response to our model
        props = []
        for prop_data in data.get("bookmakers", []):
            for market in prop_data.get("markets", []):
                prop = self._parse_prop_bet(game_id, market)
                if prop:
                    props.append(prop)
        
        return props
    
    def _parse_game_odds(self, data: Dict[str, Any]) -> GameOdds:
        """Parse game odds from API response"""
        game_id = data.get("id")
        
        # Get home and away teams
        home_team = data.get("home_team")
        away_team = data.get("away_team")
        
        # Default values
        home_moneyline = None
        away_moneyline = None
        total_runs = None
        over_odds = None
        under_odds = None
        
        # Extract odds from bookmakers
        if "bookmakers" in data and data["bookmakers"]:
            bookmaker = data["bookmakers"][0]  # Use first bookmaker
            
            for market in bookmaker.get("markets", []):
                if market["key"] == "h2h":
                    # Moneyline odds
                    for outcome in market.get("outcomes", []):
                        if outcome["name"] == home_team:
                            home_moneyline = self._decimal_to_american(outcome["price"])
                        elif outcome["name"] == away_team:
                            away_moneyline = self._decimal_to_american(outcome["price"])
                
                elif market["key"] == "totals":
                    # Total runs over/under
                    total_runs = market.get("outcomes", [{}])[0].get("point")
                    
                    for outcome in market.get("outcomes", []):
                        if outcome["name"] == "Over":
                            over_odds = self._decimal_to_american(outcome["price"])
                        elif outcome["name"] == "Under":
                            under_odds = self._decimal_to_american(outcome["price"])
        
        # Create GameOdds object
        return GameOdds(
            game_id=game_id,
            homeTeam=home_team,
            awayTeam=away_team,
            homeMoneyline=home_moneyline,
            awayMoneyline=away_moneyline,
            totalRuns=total_runs,
            overOdds=over_odds,
            underOdds=under_odds,
            lastUpdated=datetime.now()
        )
    
    def _parse_prop_bet(self, game_id: str, data: Dict[str, Any]) -> Optional[PropBet]:
        """Parse prop bet from API response"""
        try:
            # Extract player name and bet type
            market_name = data.get("name", "")
            
            # Skip non-player props
            if not market_name.startswith("Player"):
                return None
            
            # Extract player name
            parts = market_name.split(" - ")
            if len(parts) < 2:
                return None
                
            player_name = parts[0].replace("Player ", "")
            bet_description = parts[1]
            
            # Determine bet type
            bet_type = "unknown"
            if "Strikeout" in bet_description:
                bet_type = "strikeouts"
            elif "Home Run" in bet_description:
                bet_type = "home_run"
            elif "Hit" in bet_description:
                bet_type = "hits"
            elif "RBI" in bet_description:
                bet_type = "runs_batted_in"
            elif "Total Base" in bet_description:
                bet_type = "total_bases"
            
            # Get line and odds
            line = None
            over_odds = None
            under_odds = None
            
            for outcome in data.get("outcomes", []):
                if "Over" in outcome["name"]:
                    line = outcome.get("point")
                    over_odds = self._decimal_to_american(outcome["price"])
                elif "Under" in outcome["name"]:
                    under_odds = self._decimal_to_american(outcome["price"])
            
            # Create PropBet object
            return PropBet(
                gameId=game_id,
                playerName=player_name,
                betType=bet_type,
                line=line,
                overOdds=over_odds,
                underOdds=under_odds
            )
        except Exception as e:
            logger.error(f"Error parsing prop bet: {str(e)}")
            return None
    
    @staticmethod
    def _decimal_to_american(decimal_odds: float) -> int:
        """Convert decimal odds to American format"""
        if decimal_odds >= 2.0:
            # For underdogs (positive American odds)
            return round((decimal_odds - 1) * 100)
        else:
            # For favorites (negative American odds)
            return round(-100 / (decimal_odds - 1))