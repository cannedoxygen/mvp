# backend/app/services/ai_analysis.py
import logging
from typing import Dict, Any, List, Optional
import json

from app.clients.openai_client import OpenAIClient

logger = logging.getLogger(__name__)

class AIAnalysisService:
    """Service for AI-powered analysis of baseball games and betting value"""
    
    def __init__(self, openai_client: Optional[OpenAIClient] = None):
        self.openai_client = openai_client or OpenAIClient()
    
    async def analyze_game(self, game_id: str) -> Dict[str, Any]:
        """
        Perform AI analysis on a baseball game
        
        Args:
            game_id: Identifier for the game
            
        Returns:
            Dictionary with AI analysis insights
        """
        # Get complete game data
        game_data = await self._get_complete_game_data(game_id)
        
        if not game_data:
            raise ValueError(f"Game with ID {game_id} not found")
        
        # Use OpenAI client to analyze the game
        analysis = await self.openai_client.analyze_game(game_data)
        
        return analysis
    
    async def analyze_prop_bets(self, game_id: str) -> List[Dict[str, Any]]:
        """
        Analyze player prop bets for a game
        
        Args:
            game_id: Identifier for the game
            
        Returns:
            List of prop bet recommendations with confidence levels
        """
        # Get game data
        game_data = await self._get_complete_game_data(game_id)
        
        if not game_data:
            raise ValueError(f"Game with ID {game_id} not found")
        
        # Get player data with prop bet odds
        player_data = await self._get_player_prop_data(game_id)
        
        # Use OpenAI client to analyze prop bets
        prop_analysis = await self.openai_client.analyze_prop_bets(game_data, player_data)
        
        return prop_analysis
    
    async def generate_insights_summary(self, analysis: Dict[str, Any]) -> str:
        """
        Generate a human-readable summary of the analysis insights
        
        Args:
            analysis: Full analysis dictionary
            
        Returns:
            String with formatted summary
        """
        try:
            # Extract key information
            home_win_prob = analysis.get("homeWinProbability", 0.5) * 100
            away_win_prob = analysis.get("awayWinProbability", 0.5) * 100
            
            projected_score = analysis.get("projectedScore", {})
            home_score = projected_score.get("home", 0)
            away_score = projected_score.get("away", 0)
            
            betting = analysis.get("bettingInsights", {})
            recommendation = betting.get("recommendation", "N/A")
            value = betting.get("value", "N/A")
            
            factors = analysis.get("keyFactors", [])
            factors_text = "\n".join([f"- {factor}" for factor in factors])
            
            # Format the summary
            summary = f"""
Game Analysis Summary:
---------------------
Win Probability: {home_win_prob:.1f}% vs {away_win_prob:.1f}%
Projected Score: {home_score:.1f} - {away_score:.1f}

Betting Recommendation: {recommendation} ({value} value)

Key Factors:
{factors_text}
"""
            return summary.strip()
            
        except Exception as e:
            logger.error(f"Error generating insights summary: {str(e)}")
            return "Unable to generate insights summary due to an error."
    
    async def _get_complete_game_data(self, game_id: str) -> Dict[str, Any]:
        """
        Get complete game data including teams, players, odds, and weather
        
        In a real implementation, this would query multiple data sources
        """
        # This would be replaced with actual data fetching logic
        # For now, return mock data
        return {
            "id": game_id,
            "homeTeam": {
                "name": "Los Angeles Dodgers",
                "record": "50-30",
                "homeRecord": "27-15"
            },
            "awayTeam": {
                "name": "San Francisco Giants",
                "record": "45-35",
                "awayRecord": "22-18" 
            },
            "startTime": "2025-03-23T19:05:00Z",
            "stadium": "Dodger Stadium",
            "weather": {
                "temperature": 72,
                "condition": "Clear",
                "windSpeed": 8,
                "windDirection": "Out to center"
            },
            "odds": {
                "homeMoneyline": -150,
                "awayMoneyline": 130,
                "totalRuns": 8.5,
                "overOdds": -110,
                "underOdds": -110
            }
        }
    
    async def _get_player_prop_data(self, game_id: str) -> List[Dict[str, Any]]:
        """
        Get player data with prop bet odds
        
        In a real implementation, this would query multiple data sources
        """
        # This would be replaced with actual data fetching logic
        # For now, return mock data
        return []