from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import date

from app.models.odds import GameOdds as GameOddsModel, PropBet as PropBetModel
from app.schemas.odds import GameOdds, PropBet, PropBetsList
from app.clients.oddsapi import OddsAPIClient
from app.api.dependencies import get_db, get_odds_client

router = APIRouter()

@router.get("/mlb/today", response_model=List[GameOdds])
async def get_todays_mlb_odds(
    db = Depends(get_db),
    odds_client: OddsAPIClient = Depends(get_odds_client)
):
    """
    Get betting odds for all of today's MLB games
    """
    try:
        # Try to get cached odds first
        today = date.today()
        cached_odds = db.query(GameOddsModel).filter(
            GameOddsModel.date == today,
            GameOddsModel.sport == "baseball"
        ).all()
        
        # If odds are already cached and recent, return them
        if cached_odds:
            return [GameOdds.from_orm(odds) for odds in cached_odds]
            
        # Otherwise fetch fresh odds from the API
        odds = await odds_client.get_odds(sport="baseball", date=today)
        
        # Convert to Pydantic models
        return [GameOdds.from_orm(odds_item) for odds_item in odds]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch odds: {str(e)}"
        )

@router.get("/mlb/games/{game_id}", response_model=GameOdds)
async def get_game_odds(
    game_id: str,
    db = Depends(get_db),
    odds_client: OddsAPIClient = Depends(get_odds_client)
):
    """
    Get betting odds for a specific MLB game
    """
    try:
        # Try to get cached odds first
        cached_odds = db.query(GameOddsModel).filter(
            GameOddsModel.game_id == game_id
        ).first()
        
        # If odds are already cached and recent, return them
        if cached_odds:
            return GameOdds.from_orm(cached_odds)
            
        # Otherwise fetch fresh odds from the API
        odds = await odds_client.get_game_odds(game_id=game_id)
        
        # Convert to Pydantic model
        return GameOdds.from_orm(odds)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch game odds: {str(e)}"
        )

@router.get("/mlb/games/{game_id}/props", response_model=List[PropBet])
async def get_game_prop_bets(
    game_id: str,
    db = Depends(get_db),
    odds_client: OddsAPIClient = Depends(get_odds_client)
):
    """
    Get prop bet odds for a specific MLB game
    """
    try:
        # Try to get cached prop bets first
        cached_props = db.query(PropBetModel).filter(
            PropBetModel.game_id == game_id
        ).all()
        
        # If props are already cached and recent, return them
        if cached_props:
            return [PropBet.from_orm(prop) for prop in cached_props]
            
        # Otherwise fetch fresh prop bets from the API
        props = await odds_client.get_game_props(game_id=game_id)
        
        # Convert to Pydantic models
        return [PropBet.from_orm(prop) for prop in props]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch prop bets: {str(e)}"
        )