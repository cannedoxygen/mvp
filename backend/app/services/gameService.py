# backend/app/services/gameService.py
import logging
from typing import List, Dict, Any, Optional
from datetime import date, datetime, timedelta

from app.clients.sportsdataio import SportsDataIOClient
from app.models.game import Game
from app.schemas.game import GameDetail  # If it exists in schemas
from app.core.cache import cache

logger = logging.getLogger(__name__)

class GameService:
    """Service for fetching and processing game data"""
    
    def __init__(self, sports_data_client: Optional[SportsDataIOClient] = None):
        self.sports_data_client = sports_data_client or SportsDataIOClient()
    
    @cache(ttl=3600)  # Cache for 1 hour
    async def get_todays_games(self) -> List[Dict[str, Any]]:
        """
        Get all MLB games scheduled for today
        
        Returns:
            List of games with essential information
        """
        today = date.today()
        return await self.get_games_by_date(today)
    
    @cache(ttl=3600)  # Cache for 1 hour
    async def get_games_by_date(self, game_date: date) -> List[Dict[str, Any]]:
        """
        Get all MLB games scheduled for a specific date
        
        Args:
            game_date: Date to fetch games for
            
        Returns:
            List of games with essential information
        """
        try:
            # Fetch games from SportsDataIO
            games_data = await self.sports_data_client.get_games_by_date(game_date)
            
            # Transform to our application model
            transformed_games = []
            
            for game in games_data:
                transformed_game = {
                    "id": game.get("GameID"),
                    "status": self._map_game_status(game.get("Status")),
                    "startTime": game.get("DateTime"),
                    "stadium": game.get("Stadium"),
                    "homeTeam": {
                        "id": game.get("HomeTeamID"),
                        "name": game.get("HomeTeam"),
                        "abbreviation": game.get("HomeTeamID")
                    },
                    "awayTeam": {
                        "id": game.get("AwayTeamID"),
                        "name": game.get("AwayTeam"),
                        "abbreviation": game.get("AwayTeamID")
                    },
                    "weather": {
                        "temperature": game.get("Temperature"),
                        "condition": game.get("Weather"),
                        "windSpeed": game.get("WindSpeed"),
                        "windDirection": game.get("WindDirection")
                    } if game.get("Weather") else None
                }
                
                transformed_games.append(transformed_game)
            
            return transformed_games
            
        except Exception as e:
            logger.error(f"Error fetching games by date: {str(e)}")
            return []
    
    @cache(ttl=1800)  # Cache for 30 minutes
    async def get_game_details(self, game_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information for a specific game
        
        Args:
            game_id: ID of the game to fetch
            
        Returns:
            Game details including play-by-play, box score, etc.
        """
        try:
            # Fetch box score for the game
            box_score = await self.sports_data_client.get_box_score(game_id)
            
            # The box score contains the core game info
            game = box_score.get("Game", {})
            
            # Transform to our application model
            game_details = {
                "id": game.get("GameID"),
                "status": self._map_game_status(game.get("Status")),
                "startTime": game.get("DateTime"),
                "stadium": game.get("Stadium"),
                "homeTeam": {
                    "id": game.get("HomeTeamID"),
                    "name": game.get("HomeTeam"),
                    "abbreviation": game.get("HomeTeamID")
                },
                "awayTeam": {
                    "id": game.get("AwayTeamID"),
                    "name": game.get("AwayTeam"),
                    "abbreviation": game.get("AwayTeamID")
                },
                "homeScore": game.get("HomeTeamRuns"),
                "awayScore": game.get("AwayTeamRuns"),
                "inning": game.get("Inning"),
                "isTopInning": game.get("InningHalf") == "T",
                "weather": {
                    "temperature": game.get("Temperature"),
                    "condition": game.get("Weather"),
                    "windSpeed": game.get("WindSpeed"),
                    "windDirection": game.get("WindDirection")
                } if game.get("Weather") else None,
                "homeStats": box_score.get("HomeTeamStats"),
                "awayStats": box_score.get("AwayTeamStats"),
                "inningScores": box_score.get("Innings", [])
            }
            
            return game_details
            
        except Exception as e:
            logger.error(f"Error fetching game details: {str(e)}")
            return None
    
    @cache(ttl=900)  # Cache for 15 minutes
    async def get_team_stats(self, team_id: str) -> Optional[Dict[str, Any]]:
        """
        Get team statistics and information
        
        Args:
            team_id: ID of the team to fetch
            
        Returns:
            Team details including players and stats
        """
        try:
            # Fetch team details
            team = await self.sports_data_client.get_team(team_id)
            
            # Fetch team players
            players = await self.sports_data_client.get_team_players(team_id)
            
            # Transform to our application model
            team_stats = {
                "id": team.get("TeamID"),
                "name": team.get("Name"),
                "city": team.get("City"),
                "abbreviation": team.get("Key"),
                "league": team.get("League"),
                "division": team.get("Division"),
                "stadium": team.get("StadiumName"),
                "players": [
                    {
                        "id": p.get("PlayerID"),
                        "name": p.get("FanDuelName") or p.get("DraftKingsName") or f"{p.get('FirstName')} {p.get('LastName')}",
                        "position": p.get("Position"),
                        "jerseyNumber": p.get("Jersey"),
                        "stats": {
                            "battingAverage": p.get("BattingAverage"),
                            "homeRuns": p.get("HomeRuns"),
                            "runsBattedIn": p.get("RunsBattedIn"),
                            "stolenBases": p.get("StolenBases"),
                            "earnedRunAverage": p.get("EarnedRunAverage"),
                            "wins": p.get("Wins"),
                            "losses": p.get("Losses"),
                            "saves": p.get("Saves"),
                            "strikeouts": p.get("PitchingStrikeouts")
                        }
                    } for p in players
                ] if players else []
            }
            
            return team_stats
            
        except Exception as e:
            logger.error(f"Error fetching team stats: {str(e)}")
            return None
    
    @cache(ttl=600)  # Cache for 10 minutes
    async def get_projected_player_stats(self, date_obj: date) -> List[Dict[str, Any]]:
        """
        Get projected player statistics for games on a specific date
        
        Args:
            date_obj: Date to fetch projections for
            
        Returns:
            List of player projections with stats
        """
        try:
            # Fetch projections
            projections = await self.sports_data_client.get_projected_player_game_stats(date_obj)
            
            # Transform to our application model
            transformed_projections = []
            
            for proj in projections:
                transformed_proj = {
                    "playerId": proj.get("PlayerID"),
                    "name": proj.get("Name"),
                    "team": proj.get("Team"),
                    "position": proj.get("Position"),
                    "gameId": proj.get("GameID"),
                    "opponent": proj.get("Opponent"),
                    "isHome": proj.get("HomeOrAway") == "HOME",
                    "battingOrder": proj.get("BattingOrder"),
                    "battingOrderConfirmed": proj.get("BattingOrderConfirmed"),
                    "projections": {
                        "atBats": proj.get("AtBats"),
                        "hits": proj.get("Hits"),
                        "singles": proj.get("Singles"),
                        "doubles": proj.get("Doubles"),
                        "triples": proj.get("Triples"),
                        "homeRuns": proj.get("HomeRuns"),
                        "runs": proj.get("Runs"),
                        "runsBattedIn": proj.get("RunsBattedIn"),
                        "battingAverage": proj.get("BattingAverage"),
                        "outs": proj.get("Outs"),
                        "strikeouts": proj.get("Strikeouts"),
                        "walks": proj.get("Walks"),
                        "stolenBases": proj.get("StolenBases"),
                        "inningsPitched": proj.get("InningsPitched"),
                        "pitchingHits": proj.get("PitchingHits"),
                        "pitchingRuns": proj.get("PitchingRuns"),
                        "earnedRuns": proj.get("EarnedRuns"),
                        "pitchingWalks": proj.get("PitchingWalks"),
                        "pitchingStrikeouts": proj.get("PitchingStrikeouts"),
                        "pitchingHomeRuns": proj.get("PitchingHomeRuns"),
                        "wins": proj.get("Wins"),
                        "losses": proj.get("Losses"),
                        "earnedRunAverage": proj.get("EarnedRunAverage")
                    }
                }
                
                transformed_projections.append(transformed_proj)
            
            return transformed_projections
            
        except Exception as e:
            logger.error(f"Error fetching projected player stats: {str(e)}")
            return []
    
    @cache(ttl=1800)  # Cache for 30 minutes
    async def get_game_odds(self, game_id: str) -> Optional[Dict[str, Any]]:
        """
        Get betting odds for a specific game
        
        Args:
            game_id: ID of the game to fetch odds for
            
        Returns:
            Game odds including moneyline, runline, and totals
        """
        try:
            # We need to get all odds by date and then filter
            # First, we need to determine what date the game is on
            game_details = await self.get_game_details(game_id)
            if not game_details:
                return None
                
            game_datetime_str = game_details.get("startTime")
            if not game_datetime_str:
                return None
                
            # Parse the datetime string
            game_datetime = datetime.fromisoformat(game_datetime_str.replace('Z', '+00:00'))
            game_date = game_datetime.date()
            
            # Fetch odds for the game date
            all_odds = await self.sports_data_client.get_game_odds_by_date(game_date)
            
            # Find the odds for this specific game
            game_odds = next((odds for odds in all_odds if odds.get("GameID") == game_id), None)
            
            if not game_odds:
                return None
                
            # Transform to our application model
            transformed_odds = {
                "gameId": game_id,
                "homeTeam": game_details.get("homeTeam", {}).get("name"),
                "awayTeam": game_details.get("awayTeam", {}).get("name"),
                "homeMoneyline": game_odds.get("HomeMoneyLine"),
                "awayMoneyline": game_odds.get("AwayMoneyLine"),
                "homeRunLine": game_odds.get("HomePointSpread"),
                "awayRunLine": game_odds.get("AwayPointSpread"),
                "homeRunLineOdds": game_odds.get("HomePointSpreadPayout"),
                "awayRunLineOdds": game_odds.get("AwayPointSpreadPayout"),
                "overUnder": game_odds.get("OverUnder"),
                "overOdds": game_odds.get("OverPayout"),
                "underOdds": game_odds.get("UnderPayout"),
                "lastUpdated": game_odds.get("LastUpdated")
            }
            
            return transformed_odds
            
        except Exception as e:
            logger.error(f"Error fetching game odds: {str(e)}")
            return None
    
    @cache(ttl=1800)  # Cache for 30 minutes
    async def get_player_props(self, game_id: str) -> List[Dict[str, Any]]:
        """
        Get player prop bets for a specific game
        
        Args:
            game_id: ID of the game to fetch props for
            
        Returns:
            List of player props for the game
        """
        try:
            # Similar to odds, we need to filter from all props on a date
            game_details = await self.get_game_details(game_id)
            if not game_details:
                return []
                
            game_datetime_str = game_details.get("startTime")
            if not game_datetime_str:
                return []
                
            # Parse the datetime string
            game_datetime = datetime.fromisoformat(game_datetime_str.replace('Z', '+00:00'))
            game_date = game_datetime.date()
            
            # Fetch all props for the date
            all_props = await self.sports_data_client.get_player_props_by_date(game_date)
            
            # Filter props for this specific game
            game_props = [prop for prop in all_props if prop.get("GameID") == game_id]
            
            # Transform to our application model
            transformed_props = []
            
            for prop in game_props:
                transformed_prop = {
                    "gameId": game_id,
                    "playerId": prop.get("PlayerID"),
                    "playerName": prop.get("Name"),
                    "team": prop.get("Team"),
                    "position": prop.get("Position"),
                    "betType": prop.get("BetType"),
                    "betDescription": prop.get("Description"),
                    "overUnder": prop.get("OverUnder"),
                    "overOdds": prop.get("OverPayout"),
                    "underOdds": prop.get("UnderPayout")
                }
                
                transformed_props.append(transformed_prop)
            
            return transformed_props
            
        except Exception as e:
            logger.error(f"Error fetching player props: {str(e)}")
            return []
    
    def _map_game_status(self, status_code: str) -> str:
        """Map SportsDataIO status codes to our application status"""
        status_map = {
            "Scheduled": "scheduled",
            "InProgress": "inProgress",
            "Final": "final",
            "F/OT": "final",
            "Suspended": "suspended",
            "Postponed": "postponed",
            "Delayed": "delayed",
            "Canceled": "canceled",
            "Forfeit": "forfeit"
        }
        
        return status_map.get(status_code, "unknown")