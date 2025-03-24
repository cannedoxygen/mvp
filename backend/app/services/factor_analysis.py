# backend/app/services/factor_analysis.py
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class FactorAnalysisService:
    """Service for analyzing factors that impact baseball game outcomes"""
    
    def __init__(self, db=None, game_service=None):
        self.db = db
        self.game_service = game_service
        
    async def analyze_game_factors(self, game_id: str) -> Dict[str, Any]:
        """
        Analyze factors that could impact a baseball game
        
        Args:
            game_id: Identifier for the game
            
        Returns:
            Dictionary of impact factors and their effects
        """
        # Get game data
        game = await self.game_service.get_game_details(game_id)
        
        if not game:
            raise ValueError(f"Game with ID {game_id} not found")
        
        # Analyze different factor categories
        weather_factors = await self._analyze_weather_factors(game)
        lineup_factors = await self._analyze_lineup_factors(game)
        fatigue_factors = await self._analyze_team_fatigue(game)
        ballpark_factors = await self._analyze_ballpark_factors(game)
        
        # Combine all factors
        all_factors = {
            **weather_factors,
            **lineup_factors,
            **fatigue_factors,
            **ballpark_factors
        }
        
        # Generate descriptions for significant factors
        impact_descriptions = self._generate_factor_descriptions(all_factors)
        
        # Add descriptions to the factors dictionary
        all_factors["impact_descriptions"] = impact_descriptions
        
        return all_factors
    
    async def _analyze_weather_factors(self, game: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze weather impacts on the game"""
        factors = {}
        weather = game.get("weather", {})
        
        if not weather:
            return factors
        
        # Temperature effects
        temp = weather.get("temperature")
        if temp is not None:
            if temp > 85:
                # Hot weather tends to favor hitters
                factors["home_batting_adjustment"] = 0.03
                factors["away_batting_adjustment"] = 0.03
                factors["home_pitching_adjustment"] = -0.02
                factors["away_pitching_adjustment"] = -0.02
                factors["weather_temp_factor"] = "hot"
            elif temp < 55:
                # Cold weather tends to favor pitchers
                factors["home_batting_adjustment"] = -0.02
                factors["away_batting_adjustment"] = -0.02
                factors["home_pitching_adjustment"] = 0.03
                factors["away_pitching_adjustment"] = 0.03
                factors["weather_temp_factor"] = "cold"
        
        # Wind effects
        wind_speed = weather.get("windSpeed")
        wind_direction = str(weather.get("windDirection", "")).lower()
        
        if wind_speed and wind_speed > 10:
            # Check for keywords indicating wind direction
            out_indicators = ["out", "outfield", "center", "south", "southeast", "southwest"]
            in_indicators = ["in", "infield", "home", "north", "northeast", "northwest"]
            
            wind_blowing_out = any(indicator in wind_direction for indicator in out_indicators)
            wind_blowing_in = any(indicator in wind_direction for indicator in in_indicators)
            
            if wind_blowing_out:
                # Wind blowing out favors hitters
                factors["home_batting_adjustment"] = factors.get("home_batting_adjustment", 0) + 0.05
                factors["away_batting_adjustment"] = factors.get("away_batting_adjustment", 0) + 0.05
                factors["weather_wind_factor"] = "out"
            elif wind_blowing_in:
                # Wind blowing in favors pitchers
                factors["home_pitching_adjustment"] = factors.get("home_pitching_adjustment", 0) + 0.04
                factors["away_pitching_adjustment"] = factors.get("away_pitching_adjustment", 0) + 0.04
                factors["weather_wind_factor"] = "in"
        
        return factors
    
    async def _analyze_lineup_factors(self, game: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze lineup impacts (injuries, changes, etc.)"""
        factors = {}
        
        # Get projected lineups if available
        game_date_str = game.get("startTime")
        if not game_date_str:
            return factors
            
        # Parse game date
        try:
            game_datetime = datetime.fromisoformat(game_date_str.replace('Z', '+00:00'))
            game_date = game_datetime.date()
        except (ValueError, TypeError):
            return factors
        
        # Get player projections for the date
        projections = await self.game_service.get_projected_player_stats(game_date)
        
        # Filter projections for this game
        game_projections = [p for p in projections if p.get("gameId") == game.get("id")]
        
        if not game_projections:
            return factors
            
        # Analyze home team lineup
        home_team_id = game.get("homeTeam", {}).get("id")
        home_team_players = [p for p in game_projections if p.get("team") == home_team_id]
        
        # Check if key players are missing from lineup
        home_team_lineup_strength = self._calculate_lineup_strength(home_team_players)
        if home_team_lineup_strength < 0.7:
            factors["home_batting_adjustment"] = factors.get("home_batting_adjustment", 0) - 0.05
            factors["home_lineup_factor"] = "weak"
        elif home_team_lineup_strength > 0.9:
            factors["home_batting_adjustment"] = factors.get("home_batting_adjustment", 0) + 0.03
            factors["home_lineup_factor"] = "strong"
            
        # Analyze away team lineup
        away_team_id = game.get("awayTeam", {}).get("id")
        away_team_players = [p for p in game_projections if p.get("team") == away_team_id]
        
        # Check if key players are missing from lineup
        away_team_lineup_strength = self._calculate_lineup_strength(away_team_players)
        if away_team_lineup_strength < 0.7:
            factors["away_batting_adjustment"] = factors.get("away_batting_adjustment", 0) - 0.05
            factors["away_lineup_factor"] = "weak"
        elif away_team_lineup_strength > 0.9:
            factors["away_batting_adjustment"] = factors.get("away_batting_adjustment", 0) + 0.03
            factors["away_lineup_factor"] = "strong"
            
        return factors
    
    def _calculate_lineup_strength(self, players: List[Dict[str, Any]]) -> float:
        """Calculate lineup strength based on available players"""
        if not players:
            return 0.5  # Default neutral value
            
        # In a real implementation, we would use more sophisticated metrics
        # For now, just check if there's a full lineup with expected players
        
        # For baseball, check if we have 9 players in the batting order
        batting_order_players = [p for p in players if p.get("battingOrder") and int(p.get("battingOrder") or 0) > 0]
        
        if len(batting_order_players) < 9:
            return 0.5 + (len(batting_order_players) / 18)  # Scale from 0.5 to 1.0
            
        return 0.9  # Strong lineup
    
    async def _analyze_team_fatigue(self, game: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze team fatigue (based on recent games, travel, etc.)"""
        factors = {}
        
        # In a real implementation, this would check recent schedules
        # and travel patterns to determine team fatigue
        # For this simplified version, we'll use random factors
        
        # Example of potential factors:
        # - Team played yesterday (especially if it was a night game)
        # - Team is on an extended road trip
        # - Team has played many games in a row without a day off
        
        return factors
    
    async def _analyze_ballpark_factors(self, game: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the impact of the ballpark on the game"""
        factors = {}
        
        stadium = game.get("stadium")
        if not stadium:
            return factors
            
        # In a real implementation, this would use a database of
        # ballpark factors for different stadiums
        # For this simplified version, we'll use a few well-known examples
        
        hitter_friendly_parks = [
            "Coors Field",         # Colorado Rockies
            "Great American",      # Cincinnati Reds
            "Fenway Park",         # Boston Red Sox
            "Yankee Stadium"       # New York Yankees
        ]
        
        pitcher_friendly_parks = [
            "Oracle Park",         # San Francisco Giants
            "T-Mobile Park",       # Seattle Mariners
            "Busch Stadium",       # St. Louis Cardinals
            "Citi Field"           # New York Mets
        ]
        
        if any(park in stadium for park in hitter_friendly_parks):
            factors["home_batting_adjustment"] = factors.get("home_batting_adjustment", 0) + 0.04
            factors["away_batting_adjustment"] = factors.get("away_batting_adjustment", 0) + 0.04
            factors["ballpark_factor"] = "hitter_friendly"
            
        elif any(park in stadium for park in pitcher_friendly_parks):
            factors["home_pitching_adjustment"] = factors.get("home_pitching_adjustment", 0) + 0.04
            factors["away_pitching_adjustment"] = factors.get("away_pitching_adjustment", 0) + 0.04
            factors["ballpark_factor"] = "pitcher_friendly"
            
        return factors
    
    def _generate_factor_descriptions(self, factors: Dict[str, Any]) -> List[str]:
        """Generate human-readable descriptions of significant factors"""
        descriptions = []
        
        # Weather factors
        if "weather_temp_factor" in factors:
            if factors["weather_temp_factor"] == "hot":
                descriptions.append("Hot temperatures favor hitters (higher scoring game likely)")
            elif factors["weather_temp_factor"] == "cold":
                descriptions.append("Cold temperatures favor pitchers (lower scoring game likely)")
                
        if "weather_wind_factor" in factors:
            if factors["weather_wind_factor"] == "out":
                descriptions.append("Strong winds blowing out will likely increase home runs and scoring")
            elif factors["weather_wind_factor"] == "in":
                descriptions.append("Strong winds blowing in will likely suppress home runs and scoring")
        
        # Lineup factors
        if "home_lineup_factor" in factors:
            home_team_name = "Home team"  # In a real implementation, get the actual name
            if factors["home_lineup_factor"] == "weak":
                descriptions.append(f"{home_team_name} lineup missing key players (weakened offense)")
            elif factors["home_lineup_factor"] == "strong":
                descriptions.append(f"{home_team_name} has full-strength lineup (strong offense)")
                
        if "away_lineup_factor" in factors:
            away_team_name = "Away team"  # In a real implementation, get the actual name
            if factors["away_lineup_factor"] == "weak":
                descriptions.append(f"{away_team_name} lineup missing key players (weakened offense)")
            elif factors["away_lineup_factor"] == "strong":
                descriptions.append(f"{away_team_name} has full-strength lineup (strong offense)")
        
        # Ballpark factors
        if "ballpark_factor" in factors:
            if factors["ballpark_factor"] == "hitter_friendly":
                descriptions.append("Ballpark favors hitters (higher run-scoring environment)")
            elif factors["ballpark_factor"] == "pitcher_friendly":
                descriptions.append("Ballpark favors pitchers (lower run-scoring environment)")
        
        return descriptions