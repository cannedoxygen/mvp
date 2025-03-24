# backend/app/clients/openai_client.py
import os
import json
import logging
from typing import Dict, Any, List, Optional
from openai import AsyncOpenAI

from app.config import settings

logger = logging.getLogger(__name__)

class OpenAIClient:
    """Client for OpenAI API to provide AI analysis of games and betting insights"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or settings.OPENAI_API_KEY
        self.client = AsyncOpenAI(api_key=self.api_key)
        self.model = settings.OPENAI_MODEL or "gpt-4"
    
    async def analyze_game(self, game_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a baseball game and provide betting insights
        
        Args:
            game_data: Dictionary containing game, team, player, and odds information
            
        Returns:
            Dict containing AI analysis with betting insights
        """
        # Construct prompt for the AI model
        prompt = self._construct_game_analysis_prompt(game_data)
        
        try:
            # Make API request to OpenAI
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a baseball analytics expert specializing in predicting game outcomes and identifying betting value."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.2,
                max_tokens=1000
            )
            
            # Extract and parse JSON response
            analysis_text = response.choices[0].message.content
            return json.loads(analysis_text)
            
        except Exception as e:
            logger.error(f"OpenAI API request failed: {str(e)}")
            # Return basic error response
            return {
                "error": str(e),
                "summary": "Unable to complete game analysis due to an error."
            }
    
    async def analyze_prop_bets(self, game_data: Dict[str, Any], player_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Analyze player prop bets and provide recommendations
        
        Args:
            game_data: Dictionary containing game and team information
            player_data: List of dictionaries with player stats and prop bet odds
            
        Returns:
            List of recommended prop bets with confidence levels
        """
        # Construct prompt for the AI model
        prompt = self._construct_prop_bet_prompt(game_data, player_data)
        
        try:
            # Make API request to OpenAI
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a sports analytics expert specializing in player performance prediction and prop bet analysis."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.2,
                max_tokens=1500
            )
            
            # Extract and parse JSON response
            analysis_text = response.choices[0].message.content
            result = json.loads(analysis_text)
            
            return result.get("propBets", [])
            
        except Exception as e:
            logger.error(f"OpenAI API request failed: {str(e)}")
            return []
    
    def _construct_game_analysis_prompt(self, game_data: Dict[str, Any]) -> str:
        """Construct a prompt for game analysis"""
        # Extract key information
        home_team = game_data.get("homeTeam", {})
        away_team = game_data.get("awayTeam", {})
        odds = game_data.get("odds", {})
        weather = game_data.get("weather", {})
        
        # Create the prompt
        prompt = f"""
Please analyze this baseball game and provide betting insights in JSON format.

GAME INFORMATION:
{game_data.get('homeTeam', {}).get('name')} vs {game_data.get('awayTeam', {}).get('name')}
Stadium: {game_data.get('stadium')}
Date: {game_data.get('startTime')}

TEAM STATS:
Home Team ({home_team.get('name')}):
- Record: {home_team.get('record', 'N/A')}
- Home Record: {home_team.get('homeRecord', 'N/A')}
- Last 10 Games: {home_team.get('last10', 'N/A')}
- Team Batting Average: {home_team.get('batting', {}).get('average', 'N/A')}
- Team ERA: {home_team.get('pitching', {}).get('era', 'N/A')}

Away Team ({away_team.get('name')}):
- Record: {away_team.get('record', 'N/A')}
- Away Record: {away_team.get('awayRecord', 'N/A')}
- Last 10 Games: {away_team.get('last10', 'N/A')}
- Team Batting Average: {away_team.get('batting', {}).get('average', 'N/A')}
- Team ERA: {away_team.get('pitching', {}).get('era', 'N/A')}

STARTING PITCHERS:
Home: {game_data.get('homePitcher', {}).get('name', 'N/A')} - ERA: {game_data.get('homePitcher', {}).get('era', 'N/A')}
Away: {game_data.get('awayPitcher', {}).get('name', 'N/A')} - ERA: {game_data.get('awayPitcher', {}).get('era', 'N/A')}

BETTING ODDS:
Home Moneyline: {odds.get('homeMoneyline', 'N/A')}
Away Moneyline: {odds.get('awayMoneyline', 'N/A')}
Over/Under: {odds.get('totalRuns', 'N/A')}
Over Odds: {odds.get('overOdds', 'N/A')}
Under Odds: {odds.get('underOdds', 'N/A')}

WEATHER CONDITIONS:
Temperature: {weather.get('temperature', 'N/A')}°F
Wind: {weather.get('windSpeed', 'N/A')} mph, Direction: {weather.get('windDirection', 'N/A')}
Conditions: {weather.get('condition', 'N/A')}

Please analyze this game and provide:
1. Win probability for each team
2. Projected score
3. Betting recommendation for moneyline and over/under
4. Key factors that could impact this game
5. Confidence level in your prediction (0-1 scale)

Return your analysis in the following JSON format:
{{
  "homeWinProbability": 0.XX,
  "awayWinProbability": 0.XX,
  "projectedScore": {{
    "home": X.X,
    "away": X.X,
    "total": X.X
  }},
  "bettingInsights": {{
    "recommendation": "Home/Away/Over/Under",
    "value": "Strong/Moderate/Slight",
    "explanation": "Brief explanation"
  }},
  "keyFactors": [
    "Factor 1",
    "Factor 2",
    "Factor 3"
  ],
  "confidence": 0.XX
}}
"""
        return prompt
    
    def _construct_prop_bet_prompt(self, game_data: Dict[str, Any], player_data: List[Dict[str, Any]]) -> str:
        """Construct a prompt for prop bet analysis"""
        # Extract key information
        home_team = game_data.get("homeTeam", {}).get("name", "Home Team")
        away_team = game_data.get("awayTeam", {}).get("name", "Away Team")
        
        # Create player props section
        player_props_text = ""
        for player in player_data:
            player_name = player.get("name", "Unknown Player")
            team = player.get("team", "Unknown Team")
            position = player.get("position", "Unknown Position")
            
            player_props_text += f"""
Player: {player_name}
Team: {team}
Position: {position}
Recent Stats: {json.dumps(player.get('recentStats', {}), indent=2)}
Season Stats: {json.dumps(player.get('seasonStats', {}), indent=2)}
Prop Bets:
"""
            for prop in player.get("propBets", []):
                player_props_text += f"- {prop.get('betType', 'Unknown')}: {prop.get('line', 'N/A')} (Over: {prop.get('overOdds', 'N/A')}, Under: {prop.get('underOdds', 'N/A')})\n"
            
            player_props_text += "\n"
        
        # Create the prompt
        prompt = f"""
Analyze the following player prop bets for the baseball game between {home_team} and {away_team}.

GAME INFORMATION:
Stadium: {game_data.get('stadium', 'Unknown Stadium')}
Weather: {game_data.get('weather', {}).get('condition', 'Unknown')}
Temperature: {game_data.get('weather', {}).get('temperature', 'N/A')}°F
Wind: {game_data.get('weather', {}).get('windSpeed', 'N/A')} mph, Direction: {game_data.get('weather', {}).get('windDirection', 'N/A')}

PLAYER PROP BETS:
{player_props_text}

Based on the matchup, recent performance, weather conditions, and other relevant factors, analyze the value of these prop bets.

Return your analysis in the following JSON format:
{{
  "propBets": [
    {{
      "playerName": "Player Name",
      "betType": "bet_type",
      "line": X.X,
      "recommendation": "over/under",
      "confidence": 0.XX,
      "reasoning": "Brief explanation"
    }},
    ...
  ]
}}

Only include prop bets where you have at least 60% confidence in the recommendation.
"""
        return prompt