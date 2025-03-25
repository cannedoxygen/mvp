# backend/app/api/routes/games.py
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict, Any
from datetime import date, datetime
import logging

from app.services.gameService import GameService
from app.api.dependencies import get_game_service

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/baseball/date/{game_date}")
async def get_baseball_games_by_date(
    game_date: date,
    game_service: GameService = Depends(get_game_service)
):
    """
    Get all MLB games scheduled for a specific date
    """
    try:
        # Query games for the specific date
        games = await game_service.get_games_by_date(game_date)
        
        # Return empty list if no games found
        return games or []
    except Exception as e:
        logger.error(f"Error fetching games by date: {str(e)}")
        return []

@router.get("/baseball/{game_id}")
async def get_baseball_game_details(
    game_id: str,
    game_service: GameService = Depends(get_game_service)
):
    """
    Get detailed information for a specific MLB game
    """
    try:
        # Validate game_id
        if not game_id or game_id == "today":
            raise HTTPException(status_code=400, detail="Invalid game ID")
            
        # Find the game by ID
        game = await game_service.get_game_details(game_id)
        
        # Raise 404 if game not found
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
        
        return game
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching game details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching game details: {str(e)}")

@router.get("/baseball/today")
async def get_todays_baseball_games(
    game_service: GameService = Depends(get_game_service)
):
    """
    Get all MLB games scheduled for today
    """
    try:
        # Get today's games
        games = await game_service.get_todays_games()
        
        # Return games or empty list if none
        return games or []
    except Exception as e:
        logger.error(f"Error fetching today's games: {str(e)}")
        # Return empty list instead of error for better frontend experience
        return []

@router.get("/baseball/teams")
async def get_baseball_teams(
    game_service: GameService = Depends(get_game_service)
):
    """
    Get all MLB teams
    """
    try:
        teams = await game_service.get_all_teams()
        return teams or []
    except Exception as e:
        logger.error(f"Error fetching teams: {str(e)}")
        return []

@router.get("/baseball/teams/{team_id}")
async def get_baseball_team(
    team_id: str,
    game_service: GameService = Depends(get_game_service)
):
    """
    Get information about a specific MLB team
    """
    try:
        if not team_id:
            raise HTTPException(status_code=400, detail="Invalid team ID")
            
        team = await game_service.get_team_stats(team_id)
        
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")
            
        return team
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching team stats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching team stats: {str(e)}")

@router.get("/baseball/odds/{game_id}")
async def get_game_odds(
    game_id: str,
    game_service: GameService = Depends(get_game_service)
):
    """
    Get betting odds for a specific MLB game
    """
    try:
        # Validate game_id
        if not game_id or game_id == "today":
            raise HTTPException(status_code=400, detail="Invalid game ID")
            
        odds = await game_service.get_game_odds(game_id)
        
        if not odds:
            raise HTTPException(status_code=404, detail="Odds not found for this game")
            
        return odds
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching game odds: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching game odds: {str(e)}")

@router.get("/baseball/props/{game_id}")
async def get_player_props(
    game_id: str,
    game_service: GameService = Depends(get_game_service)
):
    """
    Get player prop bets for a specific MLB game
    """
    try:
        # Validate game_id
        if not game_id or game_id == "today":
            raise HTTPException(status_code=400, detail="Invalid game ID")
            
        props = await game_service.get_player_props(game_id)
        
        # Return empty list if no props found (instead of 404)
        return props or []
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching player props: {str(e)}")
        return []

@router.get("/baseball/projections/date/{game_date}")
async def get_player_projections_by_date(
    game_date: date,
    game_service: GameService = Depends(get_game_service)
):
    """
    Get projected player statistics for games on a specific date
    """
    try:
        projections = await game_service.get_projected_player_stats(game_date)
        return projections or []
    except Exception as e:
        logger.error(f"Error fetching player projections: {str(e)}")
        return []

@router.get("/baseball/weather/{game_id}")
async def get_game_weather(
    game_id: str,
    game_service: GameService = Depends(get_game_service)
):
    """
    Get weather conditions for a specific MLB game
    """
    try:
        # Validate game_id
        if not game_id or game_id == "today":
            raise HTTPException(status_code=400, detail="Invalid game ID")
            
        game = await game_service.get_game_details(game_id)
        
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
            
        weather = game.get("weather")
        
        if not weather:
            raise HTTPException(status_code=404, detail="Weather data not available for this game")
            
        return weather
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching game weather: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching game weather: {str(e)}")