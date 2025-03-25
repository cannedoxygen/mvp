# backend/app/clients/sportsdataio.py
import aiohttp
import asyncio
from typing import List, Dict, Any, Optional
from datetime import date, datetime
import logging

from app.config import settings
from app.core.database import get_db_session
from app.models.game import Game
from app.models.team import Team

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
                logger.info(f"Making API request to: {url}")
                async with session.get(url, params=params, headers=headers, timeout=self.timeout) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"SportsDataIO API error: {response.status} - {error_text}")
                        response.raise_for_status()
                    
                    data = await response.json()
                    logger.info(f"API request successful, received {len(data) if isinstance(data, list) else 'non-list'} items")
                    return data
            except aiohttp.ClientError as e:
                logger.error(f"Request to SportsDataIO API failed: {str(e)}")
                raise
    
    # === Teams Endpoints ===
    
    async def get_teams(self) -> List[Dict[str, Any]]:
        """Get all MLB teams and store them in the database"""
        try:
            logger.info("Fetching all MLB teams")
            teams_data = await self._make_request("scores", "teams")
            
            # Store teams in database
            await self._store_teams_in_database(teams_data)
            
            return teams_data
        except Exception as e:
            logger.error(f"Error fetching teams: {str(e)}")
            return []
    
    async def _store_teams_in_database(self, teams_data: List[Dict[str, Any]]):
        """Store teams data in the database"""
        with get_db_session() as db:
            try:
                stored_count = 0
                updated_count = 0
                
                for team in teams_data:
                    team_id = team.get("TeamID")
                    if not team_id:
                        continue
                        
                    # Check if team already exists
                    existing_team = db.query(Team).filter(Team.id == str(team_id)).first()
                    
                    if existing_team:
                        # Update existing team
                        existing_team.name = team.get("Name")
                        existing_team.abbreviation = team.get("Key")
                        existing_team.city = team.get("City")
                        existing_team.league = team.get("League")
                        existing_team.division = team.get("Division")
                        existing_team.wins = team.get("Wins", 0)
                        existing_team.losses = team.get("Losses", 0)
                        existing_team.team_batting_avg = team.get("BattingAvg")
                        existing_team.team_obp = team.get("OnBasePercentage")
                        existing_team.team_slg = team.get("SluggingPercentage")
                        existing_team.team_ops = team.get("OnBasePlusSlugging")
                        existing_team.team_home_runs = team.get("HomeRuns")
                        existing_team.team_runs_per_game = team.get("RunsPerGame")
                        existing_team.team_era = team.get("ERA")
                        existing_team.team_whip = team.get("WHIP")
                        existing_team.team_strikeouts_per_nine = team.get("StrikeoutsPerNineInnings")
                        existing_team.team_walks_per_nine = team.get("WalksPerNineInnings")
                        existing_team.updated_at = datetime.utcnow()
                        updated_count += 1
                    else:
                        # Create new team
                        new_team = Team(
                            id=str(team_id),
                            name=team.get("Name"),
                            abbreviation=team.get("Key"),
                            city=team.get("City"),
                            sport_type="baseball",
                            league=team.get("League"),
                            division=team.get("Division"),
                            wins=team.get("Wins", 0),
                            losses=team.get("Losses", 0),
                            team_batting_avg=team.get("BattingAvg"),
                            team_obp=team.get("OnBasePercentage"),
                            team_slg=team.get("SluggingPercentage"),
                            team_ops=team.get("OnBasePlusSlugging"),
                            team_home_runs=team.get("HomeRuns"),
                            team_runs_per_game=team.get("RunsPerGame"),
                            team_era=team.get("ERA"),
                            team_whip=team.get("WHIP"),
                            team_strikeouts_per_nine=team.get("StrikeoutsPerNineInnings"),
                            team_walks_per_nine=team.get("WalksPerNineInnings")
                        )
                        db.add(new_team)
                        stored_count += 1
                
                # Commit changes
                db.commit()
                logger.info(f"Successfully stored {stored_count} new teams and updated {updated_count} existing teams")
                
            except Exception as e:
                db.rollback()
                logger.error(f"Error storing teams in database: {str(e)}")
    
    async def get_team(self, team_id: str) -> Optional[Dict[str, Any]]:
        """Get team details by ID"""
        try:
            return await self._make_request("scores", f"team/{team_id}")
        except Exception as e:
            logger.error(f"Error fetching team {team_id}: {str(e)}")
            return None
    
    # === Schedule Endpoints ===
    
    async def get_games_by_date(self, game_date: date) -> List[Dict[str, Any]]:
        """Get all MLB games for a specific date and store them in the database"""
        try:
            # Format date as YYYY-MM-DD
            date_str = game_date.strftime("%Y-%m-%d")
            logger.info(f"Fetching games for date: {date_str}")
            
            # Make API request
            games_data = await self._make_request("scores", f"GamesByDate/{date_str}")
            
            # Log the response for debugging
            logger.info(f"Received {len(games_data)} games from SportsDataIO for date {date_str}")
            
            # Make sure we have teams data before storing games
            if not await self._ensure_teams_exist():
                logger.warning("Failed to ensure teams exist. Games may be stored with incomplete team data.")
            
            # Store games in database
            await self._store_games_in_database(games_data, game_date)
            
            return games_data
        except Exception as e:
            logger.error(f"Error fetching games for date {game_date}: {str(e)}")
            return []
    
    async def _ensure_teams_exist(self) -> bool:
        """Make sure all teams exist in the database"""
        with get_db_session() as db:
            team_count = db.query(Team).count()
            if team_count < 30:  # MLB has 30 teams
                logger.info("Less than 30 teams in database, fetching teams from API")
                teams_data = await self.get_teams()
                return len(teams_data) > 0
            return True
    
    async def _store_games_in_database(self, games_data: List[Dict[str, Any]], game_date: date):
        """Store games data in the database"""
        with get_db_session() as db:
            try:
                stored_count = 0
                updated_count = 0
                
                for game in games_data:
                    # Create game ID in our format
                    home_team_id = str(game.get("HomeTeamID"))
                    away_team_id = str(game.get("AwayTeamID"))
                    home_abbr = game.get("HomeTeam", home_team_id).lower()
                    away_abbr = game.get("AwayTeam", away_team_id).lower()
                    
                    # Format the game ID: mlb-YYYY-MM-DD-away-home
                    game_id = f"mlb-{game_date.strftime('%Y-%m-%d')}-{away_abbr}-{home_abbr}"
                    
                    # Check if game already exists
                    existing_game = db.query(Game).filter(Game.id == game_id).first()
                    
                    # Parse datetime
                    start_time = None
                    if game.get("DateTime"):
                        try:
                            start_time = datetime.fromisoformat(game.get("DateTime").replace('Z', '+00:00'))
                        except (ValueError, TypeError):
                            logger.warning(f"Failed to parse datetime: {game.get('DateTime')}")
                    
                    if existing_game:
                        # Update existing game
                        existing_game.status = self._map_game_status(game.get("Status"))
                        if start_time:
                            existing_game.start_time = start_time
                        existing_game.home_score = game.get("HomeTeamRuns")
                        existing_game.away_score = game.get("AwayTeamRuns")
                        existing_game.inning = game.get("Inning")
                        existing_game.inning_half = game.get("InningHalf")
                        existing_game.stadium = game.get("StadiumName")
                        existing_game.temperature = game.get("Temperature")
                        existing_game.weather_condition = game.get("Weather")
                        existing_game.wind_speed = game.get("WindSpeed")
                        existing_game.wind_direction = game.get("WindDirection")
                        existing_game.updated_at = datetime.utcnow()
                        updated_count += 1
                    else:
                        # Create new game
                        new_game = Game(
                            id=game_id,
                            sport_type="baseball",
                            status=self._map_game_status(game.get("Status")),
                            start_time=start_time,
                            date=game_date.strftime("%Y-%m-%d"),
                            home_team_id=home_team_id,
                            away_team_id=away_team_id,
                            home_score=game.get("HomeTeamRuns"),
                            away_score=game.get("AwayTeamRuns"),
                            inning=game.get("Inning"),
                            inning_half=game.get("InningHalf"),
                            stadium=game.get("StadiumName"),
                            temperature=game.get("Temperature"),
                            weather_condition=game.get("Weather"),
                            wind_speed=game.get("WindSpeed"),
                            wind_direction=game.get("WindDirection")
                        )
                        db.add(new_game)
                        stored_count += 1
                
                # Commit changes
                db.commit()
                logger.info(f"Successfully stored {stored_count} new games and updated {updated_count} existing games")
                
            except Exception as e:
                db.rollback()
                logger.error(f"Error storing games in database: {str(e)}")
    
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
                
            # Extract SportsDataIO game ID if our custom format is provided
            if game_id.startswith("mlb-"):
                # Try to find game in the database to get the actual SportsDataIO ID
                with get_db_session() as db:
                    game = db.query(Game).filter(Game.id == game_id).first()
                    if game:
                        # TODO: Add SportsDataIO ID to Game model if needed
                        # For now, use our ID format
                        sportsdata_id = game_id
                    else:
                        logger.warning(f"Game with ID {game_id} not found in database")
                        return None
            else:
                sportsdata_id = game_id
                
            return await self._make_request("stats", f"BoxScore/{sportsdata_id}")
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