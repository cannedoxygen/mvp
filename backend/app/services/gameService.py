# backend/app/services/gameService.py
import logging
from typing import List, Dict, Any, Optional
from datetime import date, datetime, timedelta

from app.clients.sportsdataio import SportsDataIOClient
from app.core.database import get_db_session
from app.models.game import Game
from app.models.team import Team
from app.core.cache import cache, remove_from_cache

logger = logging.getLogger(__name__)

class GameService:
    """Service for fetching and processing game data"""
    
    def __init__(self, sports_data_client: Optional[SportsDataIOClient] = None):
        """
        Initialize the GameService
        
        Args:
            sports_data_client: Optional client for SportsDataIO API
        """
        if sports_data_client:
            self.sports_data_client = sports_data_client
        else:
            # Make sure to use the API key from settings
            from app.config import settings
            self.sports_data_client = SportsDataIOClient(api_key=settings.SPORTSDATAIO_API_KEY)
        
        logger.info(f"GameService initialized with {'provided' if sports_data_client else 'new'} SportsDataIOClient")
        
        # Log API key status (without revealing the key)
        api_key_status = "AVAILABLE" if self.sports_data_client.api_key else "MISSING"
        logger.info(f"API key status on initialization: {api_key_status}")
    
    @cache(ttl=3600)  # Cache for 1 hour
    async def get_todays_games(self, force_refresh=False) -> List[Dict[str, Any]]:
        """
        Get all MLB games scheduled for today
        
        Args:
            force_refresh: If True, bypass cache and force data refresh
            
        Returns:
            List of games with essential information
        """
        today = date.today()
        
        # Add debug logging
        logger.info(f"Getting today's games for {today}, force_refresh={force_refresh}")
        
        # Call get_games_by_date with the force_refresh flag
        return await self.get_games_by_date(today, force_refresh=force_refresh)
    
    @cache(ttl=3600)  # Cache for 1 hour
    async def get_games_by_date(self, game_date: date, force_refresh=False) -> List[Dict[str, Any]]:
        """
        Get all MLB games scheduled for a specific date
        Fetches from external API and stores in database
        
        Args:
            game_date: Date to fetch games for
            force_refresh: If True, bypass cache and force data refresh
            
        Returns:
            List of games with essential information
        """
        try:
            logger.info(f"Fetching games for date: {game_date}, force_refresh: {force_refresh}")
            
            # If force refresh, clear the cache for this function call
            if force_refresh:
                cache_key = f"get_games_by_date:{game_date.isoformat()}"
                remove_from_cache(cache_key)
                logger.info(f"Cleared cache for {cache_key}")
            
            # Step 1: Always try to fetch from API first
            api_games_data = None
            
            # Make sure client is initialized
            if not self.sports_data_client:
                logger.error("Sports data client is not initialized")
                self.sports_data_client = SportsDataIOClient()
            
            # Attempt API call - log the API key status (without revealing the key)
            api_key_status = "AVAILABLE" if self.sports_data_client.api_key else "MISSING"
            logger.info(f"Attempting API call with API key status: {api_key_status}")
            
            api_games_data = await self.sports_data_client.get_games_by_date(game_date)
            
            logger.info(f"API returned {len(api_games_data) if api_games_data else 0} games")
            
            # Step 2: If API returned data, transform and store in database
            if api_games_data:
                transformed_games = []
                
                for game in api_games_data:
                    # Format the game ID in our standard format
                    home_team_id = str(game.get("HomeTeamID"))
                    away_team_id = str(game.get("AwayTeamID"))
                    home_abbr = game.get("HomeTeam", home_team_id).lower()
                    away_abbr = game.get("AwayTeam", away_team_id).lower()
                    game_id = f"mlb-{game_date.strftime('%Y-%m-%d')}-{away_abbr}-{home_abbr}"
                    
                    # Transform to our application model
                    transformed_game = {
                        "id": game_id,
                        "status": self._map_game_status(game.get("Status")),
                        "startTime": game.get("DateTime"),
                        "stadium": game.get("StadiumName"),
                        "homeTeam": {
                            "id": home_team_id,
                            "name": game.get("HomeTeam"),
                            "abbreviation": home_abbr.upper()
                        },
                        "awayTeam": {
                            "id": away_team_id,
                            "name": game.get("AwayTeam"),
                            "abbreviation": away_abbr.upper()
                        },
                        "weather": {
                            "temperature": game.get("Temperature"),
                            "condition": game.get("Weather"),
                            "windSpeed": game.get("WindSpeed"),
                            "windDirection": game.get("WindDirection")
                        } if game.get("Weather") else None
                    }
                    
                    # Store the game in database
                    await self._store_game_in_database(transformed_game)
                    
                    transformed_games.append(transformed_game)
                
                logger.info(f"Returning {len(transformed_games)} games from API")
                return transformed_games
            
            # Step 3: If API returned no data, fall back to database
            logger.info(f"No data from API, checking database for date {game_date}")
            
            with get_db_session() as db:
                # Query database for games on this date
                date_str = game_date.strftime("%Y-%m-%d")
                db_games = db.query(Game).filter(Game.date == date_str).all()
                
                if not db_games:
                    logger.warning(f"No games found in database for date {date_str}")
                    return []
                
                # Transform database games to API format
                transformed_games = []
                for game in db_games:
                    # Get team data
                    home_team = db.query(Team).filter(Team.id == game.home_team_id).first()
                    away_team = db.query(Team).filter(Team.id == game.away_team_id).first()
                    
                    transformed_game = {
                        "id": game.id,
                        "status": game.status,
                        "startTime": game.start_time.isoformat() if game.start_time else None,
                        "stadium": game.stadium,
                        "homeTeam": {
                            "id": game.home_team_id,
                            "name": home_team.name if home_team else "Unknown",
                            "abbreviation": home_team.abbreviation if home_team else game.home_team_id.upper()
                        },
                        "awayTeam": {
                            "id": game.away_team_id,
                            "name": away_team.name if away_team else "Unknown",
                            "abbreviation": away_team.abbreviation if away_team else game.away_team_id.upper()
                        },
                        "weather": {
                            "temperature": game.temperature,
                            "condition": game.weather_condition,
                            "windSpeed": game.wind_speed,
                            "windDirection": game.wind_direction
                        } if game.temperature is not None else None
                    }
                    transformed_games.append(transformed_game)
                
                logger.info(f"Returning {len(transformed_games)} games from database")
                return transformed_games
                
        except Exception as e:
            logger.error(f"Error fetching games by date: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            # Return empty list if all methods fail
            return []
    
    @cache(ttl=1800)  # Cache for 30 minutes
    async def get_game_details(self, game_id: str, force_refresh=False) -> Optional[Dict[str, Any]]:
        """
        Get detailed information for a specific game
        
        Args:
            game_id: ID of the game to fetch
            force_refresh: If True, bypass cache and force data refresh
            
        Returns:
            Game details including play-by-play, box score, etc.
        """
        try:
            # If force refresh, clear the cache for this function call
            if force_refresh:
                cache_key = f"get_game_details:{game_id}"
                remove_from_cache(cache_key)
                logger.info(f"Cleared cache for {cache_key}")
            
            # Validate game_id
            if not game_id or game_id == "today":
                logger.warning(f"Invalid game ID: {game_id}")
                return None
                
            # Step 1: First check our database
            with get_db_session() as db:
                db_game = db.query(Game).filter(Game.id == game_id).first()
                
                if db_game:
                    logger.info(f"Found game {game_id} in database")
                    
                    # Step 2: Get teams from database
                    home_team = db.query(Team).filter(Team.id == db_game.home_team_id).first()
                    away_team = db.query(Team).filter(Team.id == db_game.away_team_id).first()
                    
                    # Step 3: Try to get box score from API for most up-to-date data
                    box_score = await self.sports_data_client.get_box_score(game_id)
                    
                    # Step 4: Transform to our application model
                    game_details = {
                        "id": db_game.id,
                        "status": db_game.status,
                        "startTime": db_game.start_time.isoformat() if db_game.start_time else None,
                        "stadium": db_game.stadium,
                        "homeTeam": home_team.to_dict() if home_team else {
                            "id": db_game.home_team_id,
                            "name": "Unknown",
                            "abbreviation": db_game.home_team_id.upper()
                        },
                        "awayTeam": away_team.to_dict() if away_team else {
                            "id": db_game.away_team_id,
                            "name": "Unknown",
                            "abbreviation": db_game.away_team_id.upper()
                        },
                        "homeScore": db_game.home_score,
                        "awayScore": db_game.away_score,
                        "inning": db_game.inning,
                        "inningHalf": db_game.inning_half,
                        "weather": {
                            "temperature": db_game.temperature,
                            "condition": db_game.weather_condition,
                            "windSpeed": db_game.wind_speed,
                            "windDirection": db_game.wind_direction
                        } if db_game.temperature is not None else None
                    }
                    
                    # Add box score data if available
                    if box_score:
                        # Update with latest data from box score
                        game_details["homeStats"] = box_score.get("HomeTeamStats")
                        game_details["awayStats"] = box_score.get("AwayTeamStats")
                        game_details["inningScores"] = box_score.get("Innings", [])
                        
                        # Update database with latest score
                        if box_score.get("Game"):
                            game_data = box_score.get("Game")
                            db_game.home_score = game_data.get("HomeTeamRuns")
                            db_game.away_score = game_data.get("AwayTeamRuns")
                            db_game.status = self._map_game_status(game_data.get("Status"))
                            db_game.inning = game_data.get("Inning")
                            db_game.inning_half = game_data.get("InningHalf")
                            db_game.updated_at = datetime.utcnow()
                            
                            # Update game details with latest data
                            game_details["homeScore"] = game_data.get("HomeTeamRuns")
                            game_details["awayScore"] = game_data.get("AwayTeamRuns")
                            game_details["status"] = self._map_game_status(game_data.get("Status"))
                            game_details["inning"] = game_data.get("Inning")
                            game_details["inningHalf"] = game_data.get("InningHalf")
                            
                            # Commit changes
                            db.commit()
                    
                    return game_details
                
                # Step 5: If not in database, try to fetch from API
                logger.warning(f"Game {game_id} not found in database, attempting to fetch from API")
                
                # Check if game_id follows our format (mlb-YYYY-MM-DD-away-home)
                if game_id.startswith("mlb-") and len(game_id.split("-")) >= 5:
                    parts = game_id.split("-")
                    date_str = f"{parts[1]}-{parts[2]}-{parts[3]}"
                    
                    try:
                        # Parse date string
                        game_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                        
                        # Fetch games for this date
                        games = await self.get_games_by_date(game_date, force_refresh=force_refresh)
                        
                        # Find the specific game
                        for game in games:
                            if game.get("id") == game_id:
                                logger.info(f"Found game {game_id} in API results")
                                return game
                    except ValueError:
                        logger.error(f"Invalid date format in game ID: {game_id}")
            
            # Game not found in database or API
            logger.error(f"Game {game_id} not found in database or API")
            return None
            
        except Exception as e:
            logger.error(f"Error fetching game details: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return None
    
    @cache(ttl=900)  # Cache for 15 minutes
    async def get_team_stats(self, team_id: str, force_refresh=False) -> Optional[Dict[str, Any]]:
        """
        Get team statistics and information
        
        Args:
            team_id: ID of the team to fetch
            force_refresh: If True, bypass cache and force data refresh
            
        Returns:
            Team details including players and stats
        """
        try:
            # If force refresh, clear the cache for this function call
            if force_refresh:
                cache_key = f"get_team_stats:{team_id}"
                remove_from_cache(cache_key)
                logger.info(f"Cleared cache for {cache_key}")
            
            # Step 1: Check database first
            with get_db_session() as db:
                team = db.query(Team).filter(Team.id == team_id).first()
                
                if team:
                    # Step 2: Call API to get latest data and update database
                    api_team = await self.sports_data_client.get_team(team_id)
                    
                    if api_team:
                        # Update team with latest data
                        team.wins = api_team.get("Wins", team.wins)
                        team.losses = api_team.get("Losses", team.losses)
                        team.team_batting_avg = api_team.get("BattingAvg", team.team_batting_avg)
                        team.team_obp = api_team.get("OnBasePercentage", team.team_obp)
                        team.team_slg = api_team.get("SluggingPercentage", team.team_slg)
                        team.team_ops = api_team.get("OnBasePlusSlugging", team.team_ops)
                        team.team_home_runs = api_team.get("HomeRuns", team.team_home_runs)
                        team.team_runs_per_game = api_team.get("RunsPerGame", team.team_runs_per_game)
                        team.team_era = api_team.get("ERA", team.team_era)
                        team.team_whip = api_team.get("WHIP", team.team_whip)
                        team.team_strikeouts_per_nine = api_team.get("StrikeoutsPerNineInnings", team.team_strikeouts_per_nine)
                        team.team_walks_per_nine = api_team.get("WalksPerNineInnings", team.team_walks_per_nine)
                        team.updated_at = datetime.utcnow()
                        db.commit()
                    
                    # Step 3: Fetch team players
                    players = await self.sports_data_client.get_team_players(team_id)
                    
                    # Step 4: Transform to our application model
                    team_stats = team.to_dict()
                    
                    # Add players to response if available
                    if players:
                        team_stats["players"] = [
                            {
                                "id": p.get("PlayerID"),
                                "name": f"{p.get('FirstName')} {p.get('LastName')}",
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
                        ]
                    
                    return team_stats
                
                # Step 5: If not in database, fetch from API
                logger.info(f"Team {team_id} not found in database, fetching from API")
                api_team = await self.sports_data_client.get_team(team_id)
                
                if api_team:
                    # Create new team and store in database
                    new_team = Team(
                        id=str(api_team.get("TeamID")),
                        name=api_team.get("Name"),
                        abbreviation=api_team.get("Key"),
                        city=api_team.get("City"),
                        sport_type="baseball",
                        league=api_team.get("League"),
                        division=api_team.get("Division"),
                        wins=api_team.get("Wins", 0),
                        losses=api_team.get("Losses", 0),
                        team_batting_avg=api_team.get("BattingAvg"),
                        team_obp=api_team.get("OnBasePercentage"),
                        team_slg=api_team.get("SluggingPercentage"),
                        team_ops=api_team.get("OnBasePlusSlugging"),
                        team_home_runs=api_team.get("HomeRuns"),
                        team_runs_per_game=api_team.get("RunsPerGame"),
                        team_era=api_team.get("ERA"),
                        team_whip=api_team.get("WHIP"),
                        team_strikeouts_per_nine=api_team.get("StrikeoutsPerNineInnings"),
                        team_walks_per_nine=api_team.get("WalksPerNineInnings")
                    )
                    db.add(new_team)
                    db.commit()
                    
                    # Transform API response to our model
                    return new_team.to_dict()
            
            logger.error(f"Team {team_id} not found in database or API")
            return None
                
        except Exception as e:
            logger.error(f"Error fetching team stats: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return None
    
    @cache(ttl=900)  # Cache for 15 minutes
    async def get_all_teams(self, force_refresh=False) -> List[Dict[str, Any]]:
        """
        Get all MLB teams
        
        Args:
            force_refresh: If True, bypass cache and force data refresh
            
        Returns:
            List of teams with basic information
        """
        try:
            # If force refresh, clear the cache for this function call
            if force_refresh:
                cache_key = "get_all_teams"
                remove_from_cache(cache_key)
                logger.info(f"Cleared cache for {cache_key}")
            
            # Step 1: First check database
            with get_db_session() as db:
                db_teams = db.query(Team).all()
                
                # If we have teams in the database, return them
                if db_teams and len(db_teams) >= 30:  # MLB has 30 teams
                    logger.info(f"Found {len(db_teams)} teams in database")
                    return [team.to_dict() for team in db_teams]
            
            # Step 2: If not enough teams in database, fetch from API
            logger.info("Fetching teams from API")
            teams_data = await self.sports_data_client.get_teams()
            
            if teams_data:
                # Store teams in database
                with get_db_session() as db:
                    for team in teams_data:
                        team_id = str(team.get("TeamID"))
                        # Check if team already exists
                        existing_team = db.query(Team).filter(Team.id == team_id).first()
                        
                        if not existing_team:
                            # Create new team
                            new_team = Team(
                                id=team_id,
                                name=team.get("Name"),
                                abbreviation=team.get("Key"),
                                city=team.get("City"),
                                sport_type="baseball",
                                league=team.get("League"),
                                division=team.get("Division")
                            )
                            db.add(new_team)
                    
                    db.commit()
                
                # Transform API data to our model
                transformed_teams = []
                for team in teams_data:
                    team_id = str(team.get("TeamID"))
                    transformed_team = {
                        "id": team_id,
                        "name": team.get("Name"),
                        "city": team.get("City"),
                        "abbreviation": team.get("Key"),
                        "league": team.get("League"),
                        "division": team.get("Division"),
                        "stadium": team.get("StadiumName"),
                        "logo": team.get("WikipediaLogoUrl")
                    }
                    transformed_teams.append(transformed_team)
                
                logger.info(f"Fetched {len(transformed_teams)} teams from API")
                return transformed_teams
            
            # Step 3: Fall back to database regardless of count if API fails
            with get_db_session() as db:
                db_teams = db.query(Team).all()
                logger.warning(f"API fetch failed, falling back to {len(db_teams)} teams in database")
                return [team.to_dict() for team in db_teams]
                
        except Exception as e:
            logger.error(f"Error fetching all teams: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return []
    
    @cache(ttl=600)  # Cache for 10 minutes
    async def get_projected_player_stats(self, date_obj: date, force_refresh=False) -> List[Dict[str, Any]]:
        """
        Get projected player statistics for games on a specific date
        
        Args:
            date_obj: Date to fetch projections for
            force_refresh: If True, bypass cache and force data refresh
            
        Returns:
            List of player projections with stats
        """
        try:
            # If force refresh, clear the cache for this function call
            if force_refresh:
                cache_key = f"get_projected_player_stats:{date_obj.isoformat()}"
                remove_from_cache(cache_key)
                logger.info(f"Cleared cache for {cache_key}")
            
            # Fetch projections from API
            projections = await self.sports_data_client.get_projected_player_game_stats(date_obj)
            
            if not projections:
                logger.warning(f"No player projections found for date {date_obj}")
                return []
            
            # Transform to our application model
            transformed_projections = []
            
            for proj in projections:
                transformed_proj = {
                    "playerId": str(proj.get("PlayerID")),
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
            import traceback
            logger.error(traceback.format_exc())
            return []
    
    @cache(ttl=1800)  # Cache for 30 minutes
    async def get_game_odds(self, game_id: str, force_refresh=False) -> Optional[Dict[str, Any]]:
        """
        Get betting odds for a specific game
        
        Args:
            game_id: ID of the game to fetch odds for
            force_refresh: If True, bypass cache and force data refresh
            
        Returns:
            Game odds including moneyline, runline, and totals
        """
        try:
            # If force refresh, clear the cache for this function call
            if force_refresh:
                cache_key = f"get_game_odds:{game_id}"
                remove_from_cache(cache_key)
                logger.info(f"Cleared cache for {cache_key}")
            
            # Step 1: First get the game details to determine the date
            game_details = await self.get_game_details(game_id)
            if not game_details:
                logger.error(f"Cannot fetch odds: Game {game_id} not found")
                return None
                
            # Step 2: Parse game date from startTime
            game_datetime_str = game_details.get("startTime")
            if not game_datetime_str:
                logger.error(f"Cannot fetch odds: Game {game_id} has no start time")
                return None
                
            # Parse the datetime string
            game_datetime = datetime.fromisoformat(game_datetime_str.replace('Z', '+00:00'))
            game_date = game_datetime.date()
            
            # Step 3: Fetch odds for the game date
            all_odds = await self.sports_data_client.get_game_odds_by_date(game_date)
            
            if not all_odds:
                logger.warning(f"No odds found for date {game_date}")
                return None
            
            # Step 4: Find the odds for this specific game
            # This requires mapping between our game ID and the API's game ID
            # For now, use team names to match
            home_team_name = game_details.get("homeTeam", {}).get("name")
            away_team_name = game_details.get("awayTeam", {}).get("name")
            
            game_odds = None
            for odds in all_odds:
                if (odds.get("HomeTeam") == home_team_name and 
                    odds.get("AwayTeam") == away_team_name):
                    game_odds = odds
                    break
            
            if not game_odds:
                logger.warning(f"No odds found for game {game_id}")
                return None
                
            # Step 5: Transform to our application model
            transformed_odds = {
                "gameId": game_id,
                "homeTeam": home_team_name,
                "awayTeam": away_team_name,
                "homeMoneyline": game_odds.get("HomeMoneyLine"),
                "awayMoneyline": game_odds.get("AwayMoneyLine"),
                "totalRuns": game_odds.get("OverUnder"),
                "overOdds": game_odds.get("OverPayout"),
                "underOdds": game_odds.get("UnderPayout"),
                "homeRunLine": game_odds.get("HomePointSpread"),
                "awayRunLine": game_odds.get("AwayPointSpread"),
                "homeRunLineOdds": game_odds.get("HomePointSpreadPayout"),
                "awayRunLineOdds": game_odds.get("AwayPointSpreadPayout"),
                "lastUpdated": game_odds.get("LastUpdated")
            }
            
            return transformed_odds
            
        except Exception as e:
            logger.error(f"Error fetching game odds: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return None
    
    @cache(ttl=1800)  # Cache for 30 minutes
    async def get_player_props(self, game_id: str, force_refresh=False) -> List[Dict[str, Any]]:
        """
        Get player prop bets for a specific game
        
        Args:
            game_id: ID of the game to fetch props for
            force_refresh: If True, bypass cache and force data refresh
            
        Returns:
            List of player props for the game
        """
        try:
            # If force refresh, clear the cache for this function call
            if force_refresh:
                cache_key = f"get_player_props:{game_id}"
                remove_from_cache(cache_key)
                logger.info(f"Cleared cache for {cache_key}")
            
            # Special handling for invalid game IDs
            if not game_id or game_id == "today":
                logger.warning(f"Invalid game ID for player props: {game_id}")
                return []
                
            # Step 1: Get game details to determine date
            game_details = await self.get_game_details(game_id)
            if not game_details:
                logger.error(f"Cannot fetch props: Game {game_id} not found")
                return []
                
            # Step 2: Parse game date
            game_datetime_str = game_details.get("startTime")
            if not game_datetime_str:
                logger.error(f"Cannot fetch props: Game {game_id} has no start time")
                return []
                
            # Parse the datetime string
            game_datetime = datetime.fromisoformat(game_datetime_str.replace('Z', '+00:00'))
            game_date = game_datetime.date()
            
            # Step 3: Fetch all props for the date
            all_props = await self.sports_data_client.get_player_props_by_date(game_date)
            
            if not all_props:
                logger.warning(f"No props found for date {game_date}")
                return []
            
            # Step 4: Match props to our game
            # Since game IDs may differ, match by team names
            home_team_name = game_details.get("homeTeam", {}).get("name")
            away_team_name = game_details.get("awayTeam", {}).get("name")
            
            # Filter props for this specific game
            game_props = []
            for prop in all_props:
                if ((prop.get("HomeTeam") == home_team_name and 
                     prop.get("AwayTeam") == away_team_name) or
                    (prop.get("HomeTeam") == away_team_name and 
                     prop.get("AwayTeam") == home_team_name)):
                    game_props.append(prop)
            
            # Step 5: Transform to our application model
            transformed_props = []
            
            for prop in game_props:
                transformed_prop = {
                    "gameId": game_id,
                    "playerId": str(prop.get("PlayerID")),
                    "playerName": prop.get("Name"),
                    "team": prop.get("Team"),
                    "position": prop.get("Position"),
                    "betType": prop.get("BetType"),
                    "betDescription": prop.get("Description"),
                    "line": prop.get("OverUnder"),
                    "overOdds": prop.get("OverPayout"),
                    "underOdds": prop.get("UnderPayout")
                }
                
                transformed_props.append(transformed_prop)
            
            return transformed_props
            
        except Exception as e:
            logger.error(f"Error fetching player props: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return []
    
    async def get_injuries(self) -> List[Dict[str, Any]]:
        """
        Get current MLB injuries
        
        Returns:
            List of player injuries
        """
        try:
            injuries_data = await self.sports_data_client.get_injuries()
            
            if not injuries_data:
                logger.warning("No injury data found")
                return []
            
            transformed_injuries = []
            for injury in injuries_data:
                transformed_injury = {
                    "playerId": str(injury.get("PlayerID")),
                    "playerName": injury.get("Name"),
                    "team": injury.get("Team"),
                    "position": injury.get("Position"),
                    "status": injury.get("Status"),
                    "injuryType": injury.get("InjuryType"),
                    "injuryNotes": injury.get("InjuryNotes"),
                    "expectedReturn": injury.get("ExpectedReturn")
                }
                transformed_injuries.append(transformed_injury)
                
            return transformed_injuries
        except Exception as e:
            logger.error(f"Error fetching injuries: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return []
    
    async def get_standings(self) -> Dict[str, Any]:
        """
        Get current MLB standings
        
        Returns:
            Dictionary containing standings by league and division
        """
        try:
            standings_data = await self.sports_data_client.get_standings()
            
            if not standings_data:
                logger.warning("No standings data found")
                return {}
            
            # Organize standings by league and division
            leagues = {}
            
            for team in standings_data:
                league = team.get("League")
                division = team.get("Division")
                
                if not league or not division:
                    continue
                    
                if league not in leagues:
                    leagues[league] = {}
                    
                if division not in leagues[league]:
                    leagues[league][division] = []
                    
                team_standing = {
                    "id": str(team.get("TeamID")),
                    "name": team.get("Name"),
                    "abbreviation": team.get("Key"),
                    "wins": team.get("Wins"),
                    "losses": team.get("Losses"),
                    "winPercentage": team.get("Percentage"),
                    "gamesBehind": team.get("GamesBehind"),
                    "homeRecord": f"{team.get('HomeWins')}-{team.get('HomeLosses')}",
                    "awayRecord": f"{team.get('AwayWins')}-{team.get('AwayLosses')}",
                    "lastTen": self._format_last_ten(team),
                    "streak": self._format_streak(team)
                }
                
                leagues[league][division].append(team_standing)
                
            return leagues
        except Exception as e:
            logger.error(f"Error fetching standings: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return {}
    
    async def refresh_games(self, game_date: Optional[date] = None) -> List[Dict[str, Any]]:
        """
        Force refresh of games data from API
        
        Args:
            game_date: Date to fetch games for (defaults to today)
            
        Returns:
            List of games with fresh data
        """
        # Use today if no date provided
        if game_date is None:
            game_date = date.today()
        
        logger.info(f"Forcing refresh of games for {game_date}")
        
        # Clear the cache for this specific function and arguments
        cache_key = f"get_games_by_date:{game_date.isoformat()}"
        remove_from_cache(cache_key)
        
        # Fetch fresh data with force_refresh flag
        return await self.get_games_by_date(game_date, force_refresh=True)
    
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
    
    def _format_last_ten(self, team: Dict[str, Any]) -> str:
        """Format team's last 10 games record"""
        if "Last10Wins" in team and "Last10Losses" in team:
            return f"{team.get('Last10Wins')}-{team.get('Last10Losses')}"
        return "0-0"
    
    def _format_streak(self, team: Dict[str, Any]) -> str:
        """Format team's winning/losing streak"""
        if "StreakType" in team and "StreakCount" in team:
            streak_type = "W" if team.get("StreakType") == "Win" else "L"
            return f"{streak_type}{team.get('StreakCount')}"
        return "N/A"
    
    async def _store_game_in_database(self, game_data: Dict[str, Any]) -> None:
        """Store game data in the database"""
        try:
            with get_db_session() as db:
                # Check if game already exists
                game_id = game_data.get("id")
                existing_game = db.query(Game).filter(Game.id == game_id).first()
                
                if existing_game:
                    # Update existing game
                    existing_game.status = game_data.get("status", existing_game.status)
                    existing_game.home_score = game_data.get("homeScore", existing_game.home_score)
                    existing_game.away_score = game_data.get("awayScore", existing_game.away_score)
                    existing_game.inning = game_data.get("inning", existing_game.inning)
                    existing_game.inning_half = game_data.get("inningHalf", existing_game.inning_half)
                    existing_game.updated_at = datetime.utcnow()
                else:
                    # Create new game
                    game_datetime_str = game_data.get("startTime")
                    if not game_datetime_str:
                        logger.error(f"Cannot create game: Game {game_id} has no start time")
                        return
                        
                    # Parse the datetime string
                    game_datetime = datetime.fromisoformat(game_datetime_str.replace('Z', '+00:00'))
                    game_date = game_datetime.date()
                    
                    new_game = Game(
                        id=game_id,
                        sport_type="baseball",
                        status=game_data.get("status", "scheduled"),
                        start_time=game_datetime,
                        date=game_date.strftime("%Y-%m-%d"),
                        home_team_id=game_data.get("homeTeam", {}).get("id"),
                        away_team_id=game_data.get("awayTeam", {}).get("id"),
                        stadium=game_data.get("stadium"),
                        location=game_data.get("location"),
                        home_score=game_data.get("homeScore"),
                        away_score=game_data.get("awayScore"),
                        inning=game_data.get("inning"),
                        inning_half=game_data.get("inningHalf")
                    )
                    
                    # Add weather information if available
                    if game_data.get("weather"):
                        new_game.temperature = game_data["weather"].get("temperature")
                        new_game.weather_condition = game_data["weather"].get("condition")
                        new_game.wind_speed = game_data["weather"].get("windSpeed")
                        new_game.wind_direction = game_data["weather"].get("windDirection")
                    
                    db.add(new_game)
                
                db.commit()
                logger.info(f"Successfully stored/updated game {game_id} in database")
                
        except Exception as e:
            logger.error(f"Error storing game in database: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())