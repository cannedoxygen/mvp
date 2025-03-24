# backend/app/api/routes/games.py
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict, Any
from datetime import date, datetime

from app.services.gameService import GameService
from app.core.database import get_db
from app.api.dependencies import get_game_service
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/baseball/date/{game_date}", response_model=List[Dict[str, Any]])
async def get_baseball_games_by_date(
    game_date: date,
    game_service: GameService = Depends(get_game_service)
):
    """
    Get all MLB games scheduled for a specific date
    """
    # Query games for the specific date
    games = await game_service.get_games_by_date(game_date)
    
    # Return empty list if no games found
    if not games:
        return []
        
    return games

@router.get("/baseball/{game_id}", response_model=Dict[str, Any])
async def get_baseball_game_details(
    game_id: str,
    game_service: GameService = Depends(get_game_service)
):
    """
    Get detailed information for a specific MLB game
    """
    # Find the game by ID
    game = await game_service.get_game_details(game_id)
    
    # Raise 404 if game not found
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    return game

@router.get("/baseball/today", response_model=List[Dict[str, Any]])
async def get_todays_baseball_games(
    game_service: GameService = Depends(get_game_service)
):
    """
    Get all MLB games scheduled for today
    """
    # Get today's games
    games = await game_service.get_todays_games()
    
    return games

@router.get("/baseball/teams", response_model=List[Dict[str, Any]])
async def get_baseball_teams(
    game_service: GameService = Depends(get_game_service)
):
    """
    Get all MLB teams
    """
    teams = await game_service.get_all_teams()
    return teams

@router.get("/baseball/teams/{team_id}", response_model=Dict[str, Any])
async def get_baseball_team(
    team_id: str,
    game_service: GameService = Depends(get_game_service)
):
    """
    Get information about a specific MLB team
    """
    team = await game_service.get_team_stats(team_id)
    
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
        
    return team

@router.get("/baseball/odds/{game_id}", response_model=Dict[str, Any])
async def get_game_odds(
    game_id: str,
    game_service: GameService = Depends(get_game_service)
):
    """
    Get betting odds for a specific MLB game
    """
    odds = await game_service.get_game_odds(game_id)
    
    if not odds:
        raise HTTPException(status_code=404, detail="Odds not found for this game")
        
    return odds

@router.get("/baseball/props/{game_id}", response_model=List[Dict[str, Any]])
async def get_player_props(
    game_id: str,
    game_service: GameService = Depends(get_game_service)
):
    """
    Get player prop bets for a specific MLB game
    """
    props = await game_service.get_player_props(game_id)
    
    return props

@router.get("/baseball/projections/date/{game_date}", response_model=List[Dict[str, Any]])
async def get_player_projections_by_date(
    game_date: date,
    game_service: GameService = Depends(get_game_service)
):
    """
    Get projected player statistics for games on a specific date
    """
    projections = await game_service.get_projected_player_stats(game_date)
    
    return projections

@router.get("/baseball/weather/{game_id}", response_model=Dict[str, Any])
async def get_game_weather(
    game_id: str,
    game_service: GameService = Depends(get_game_service)
):
    """
    Get weather conditions for a specific MLB game
    """
    game = await game_service.get_game_details(game_id)
    
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
        
    weather = game.get("weather")
    
    if not weather:
        raise HTTPException(status_code=404, detail="Weather data not available for this game")
        
    return weather