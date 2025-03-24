# backend/app/services/simulation.py
import random
import statistics
import numpy as np
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime

from app.models.simulation import SimulationResult
from app.services.factor_analysis import FactorAnalysisService

logger = logging.getLogger(__name__)

class SimulationService:
    """Service for running baseball game simulations"""
    
    def __init__(self, db=None, game_service=None):
        self.db = db
        self.game_service = game_service
    
    async def run_baseball_simulation(
        self, 
        game_id: str, 
        count: int = 1000,
        factors: Optional[Dict[str, Any]] = None
    ) -> SimulationResult:
        """
        Run a Monte Carlo simulation for a baseball game
        
        Args:
            game_id: Identifier for the game
            count: Number of simulations to run
            factors: Dictionary of factors that might impact the game
            
        Returns:
            SimulationResult object with simulation outcomes
        """
        # Get game data
        game = await self.game_service.get_game_details(game_id)
        
        if not game:
            raise ValueError(f"Game with ID {game_id} not found")
        
        # Get team and pitcher data
        home_team = game.get("homeTeam", {})
        away_team = game.get("awayTeam", {})
        
        # Create basic rating models for teams
        home_team_rating = {"batting_rating": 0.65, "pitching_rating": 0.7, "defense_rating": 0.6}
        away_team_rating = {"batting_rating": 0.6, "pitching_rating": 0.75, "defense_rating": 0.65}
        
        # Placeholder for pitcher data
        home_pitcher = {"rating": 0.7}
        away_pitcher = {"rating": 0.65}
        
        # Apply impact factors if provided
        adjusted_factors = self._apply_impact_factors(
            home_team_rating, 
            away_team_rating, 
            home_pitcher, 
            away_pitcher, 
            factors
        )
        
        # Run simulations
        results = []
        for _ in range(count):
            result = self._simulate_game(
                adjusted_factors["home_team"],
                adjusted_factors["away_team"],
                adjusted_factors["home_pitcher"],
                adjusted_factors["away_pitcher"]
            )
            results.append(result)
        
        # Calculate statistics
        home_wins = sum(1 for r in results if r["home_score"] > r["away_score"])
        home_win_probability = home_wins / count
        away_win_probability = 1 - home_win_probability
        
        avg_home_score = statistics.mean(r["home_score"] for r in results)
        avg_away_score = statistics.mean(r["away_score"] for r in results)
        avg_total_runs = avg_home_score + avg_away_score
        
        # Convert average implied probabilities to American odds
        home_ml_odds = self._probability_to_american_odds(home_win_probability)
        away_ml_odds = self._probability_to_american_odds(away_win_probability)
        
        # Determine over/under odds based on total runs distribution
        total_runs = [r["home_score"] + r["away_score"] for r in results]
        market_total = 8.5  # Default to common MLB total
        
        over_probability = sum(1 for r in total_runs if r > market_total) / count
        under_probability = 1 - over_probability
        over_odds = self._probability_to_american_odds(over_probability)
        under_odds = self._probability_to_american_odds(under_probability)
        
        # Create betting insights
        betting_insights = {
            "homeMoneyline": home_ml_odds,
            "awayMoneyline": away_ml_odds,
            "overOdds": over_odds,
            "underOdds": under_odds
        }
        
        # In a real implementation, generate prop bet insights
        prop_bet_insights = self._generate_sample_prop_insights(home_team.get("name"), away_team.get("name"))
        
        # Store simulation result
        simulation_result = SimulationResult(
            gameId=game_id,
            simulationCount=count,
            homeTeamName=home_team.get("name"),
            awayTeamName=away_team.get("name"),
            homeWinProbability=home_win_probability,
            awayWinProbability=away_win_probability,
            averageHomeScore=avg_home_score,
            averageAwayScore=avg_away_score,
            averageTotalRuns=avg_total_runs,
            bettingInsights=betting_insights,
            propBetInsights=prop_bet_insights,
            impactingFactors=factors.get("impact_descriptions") if factors else []
        )
        
        return simulation_result
    
    def _apply_impact_factors(
        self, 
        home_team: Dict[str, Any], 
        away_team: Dict[str, Any],
        home_pitcher: Dict[str, Any],
        away_pitcher: Dict[str, Any],
        factors: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Apply impact factors to team and pitcher ratings"""
        # Default adjusted factors are the original values
        adjusted_home_team = home_team.copy()
        adjusted_away_team = away_team.copy()
        adjusted_home_pitcher = home_pitcher.copy()
        adjusted_away_pitcher = away_pitcher.copy()
        
        # Apply adjustments based on impact factors
        if factors:
            # Batting adjustments
            if "home_batting_adjustment" in factors:
                adjusted_home_team["batting_rating"] = max(0, min(1, 
                    home_team.get("batting_rating", 0.5) + factors["home_batting_adjustment"]
                ))
            
            if "away_batting_adjustment" in factors:
                adjusted_away_team["batting_rating"] = max(0, min(1, 
                    away_team.get("batting_rating", 0.5) + factors["away_batting_adjustment"]
                ))
            
            # Pitching adjustments
            if "home_pitching_adjustment" in factors:
                adjusted_home_team["pitching_rating"] = max(0, min(1, 
                    home_team.get("pitching_rating", 0.5) + factors["home_pitching_adjustment"]
                ))
                
                adjusted_home_pitcher["rating"] = max(0, min(1, 
                    home_pitcher.get("rating", 0.5) + factors["home_pitching_adjustment"]
                ))
            
            if "away_pitching_adjustment" in factors:
                adjusted_away_team["pitching_rating"] = max(0, min(1, 
                    away_team.get("pitching_rating", 0.5) + factors["away_pitching_adjustment"]
                ))
                
                adjusted_away_pitcher["rating"] = max(0, min(1, 
                    away_pitcher.get("rating", 0.5) + factors["away_pitching_adjustment"]
                ))
            
            # Defense adjustments
            if "home_defense_adjustment" in factors:
                adjusted_home_team["defense_rating"] = max(0, min(1, 
                    home_team.get("defense_rating", 0.5) + factors["home_defense_adjustment"]
                ))
            
            if "away_defense_adjustment" in factors:
                adjusted_away_team["defense_rating"] = max(0, min(1, 
                    away_team.get("defense_rating", 0.5) + factors["away_defense_adjustment"]
                ))
        
        return {
            "home_team": adjusted_home_team,
            "away_team": adjusted_away_team,
            "home_pitcher": adjusted_home_pitcher,
            "away_pitcher": adjusted_away_pitcher
        }
    
    def _simulate_game(
        self,
        home_team: Dict[str, Any],
        away_team: Dict[str, Any],
        home_pitcher: Dict[str, Any],
        away_pitcher: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Simulate a single baseball game
        
        Uses a simplified model based on team and pitcher ratings
        to generate realistic scores
        """
        # Base expected runs for a team (league average)
        base_runs = 4.5
        
        # Calculate expected runs for each team
        home_expected_runs = base_runs * (
            0.6 * home_team.get("batting_rating", 0.5) + 
            0.4 * (1 - away_pitcher.get("rating", 0.5))
        )
        
        away_expected_runs = base_runs * (
            0.6 * away_team.get("batting_rating", 0.5) + 
            0.4 * (1 - home_pitcher.get("rating", 0.5))
        )
        
        # Apply home field advantage
        home_expected_runs *= 1.05
        
        # Apply defensive impact
        home_expected_runs *= (1 - 0.2 * away_team.get("defense_rating", 0.5))
        away_expected_runs *= (1 - 0.2 * home_team.get("defense_rating", 0.5))
        
        # Simulate actual runs scored (using Poisson distribution)
        home_score = np.random.poisson(home_expected_runs)
        away_score = np.random.poisson(away_expected_runs)
        
        return {
            "home_score": home_score,
            "away_score": away_score
        }
    
    def _probability_to_american_odds(self, probability: float) -> int:
        """Convert win probability to American odds"""
        if probability <= 0 or probability >= 1:
            raise ValueError("Probability must be between 0 and 1")
            
        if probability > 0.5:
            # Favorite (negative odds)
            odds = -100 * probability / (1 - probability)
        else:
            # Underdog (positive odds)
            odds = 100 * (1 - probability) / probability
            
        # Round to nearest 5
        return int(round(odds / 5) * 5)
    
    def _generate_sample_prop_insights(self, home_team_name: str, away_team_name: str) -> List[Dict[str, Any]]:
        """Generate sample player prop bet insights for demonstration"""
        # This is mock data - in a real implementation, this would be based on simulations
        return [
            {
                "playerName": "Player 1",
                "betType": "strikeouts",
                "line": 5.5,
                "recommendation": "over",
                "confidence": 0.75,
                "reasoning": "Strong matchup against a team with high strikeout rate"
            },
            {
                "playerName": "Player 2",
                "betType": "home_run",
                "line": 0.5,
                "recommendation": "over",
                "confidence": 0.68,
                "reasoning": "Power hitter facing a pitcher who gives up home runs frequently"
            },
            {
                "playerName": "Player 3",
                "betType": "hits",
                "line": 1.5,
                "recommendation": "under",
                "confidence": 0.62,
                "reasoning": "Facing a pitcher who has been dominant in recent starts"
            }
        ]
    
    async def get_simulation_history(self, game_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Get history of previous simulations for a game"""
        # In a real implementation, this would query the database
        # For now, return empty list
        return []