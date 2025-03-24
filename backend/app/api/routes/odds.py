# backend/app/api/routes/odds.py
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import date

from app.services.oddsService import OddsService
from app.api.dependencies import get_odds_service

router = APIRouter()

@router.get("/mlb/today")
async def get_todays_mlb_odds(
    odds_service: OddsService = Depends(get_odds_service)
):
    """
    Get betting odds for all of today's MLB games
    """
    try:
        return await odds_service.get_todays_odds()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch odds: {str(e)}"
        )

@router.get("/mlb/games/{game_id}")
async def get_game_odds(
    game_id: str,
    odds_service: OddsService = Depends(get_odds_service)
):
    """
    Get betting odds for a specific MLB game
    """
    try:
        odds = await odds_service.get_game_odds(game_id)
        
        if not odds:
            raise HTTPException(status_code=404, detail="Odds not found for this game")
            
        return odds
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch game odds: {str(e)}"
        )

@router.get("/mlb/games/{game_id}/props")
async def get_game_prop_bets(
    game_id: str,
    odds_service: OddsService = Depends(get_odds_service)
):
    """
    Get prop bet odds for a specific MLB game
    """
    try:
        props = await odds_service.get_game_props(game_id)
        return props
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch prop bets: {str(e)}"
        )