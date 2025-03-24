# backend/app/api/routes/simulations.py
from fastapi import APIRouter, Depends, HTTPException, Body
from typing import Dict, Any, Optional
from datetime import date

from app.services.simulation import SimulationService
from app.services.factor_analysis import FactorAnalysisService
from app.api.dependencies import get_db, get_simulation_service, get_factor_analysis_service

router = APIRouter()

@router.post("/baseball/{game_id}")
async def run_baseball_simulation(
    game_id: str,
    request: Dict[str, Any] = Body(...),
    simulation_service: SimulationService = Depends(get_simulation_service),
    factor_service: FactorAnalysisService = Depends(get_factor_analysis_service)
):
    """
    Run a Monte Carlo simulation for a specific baseball game
    """
    try:
        # Extract simulation count from request
        count = request.get("count", 1000)
        
        # Analyze factors that might impact the game
        factors = await factor_service.analyze_game_factors(game_id)
        
        # Run Monte Carlo simulation with the analyzed factors
        simulation_results = await simulation_service.run_baseball_simulation(
            game_id=game_id,
            count=count,
            factors=factors
        )
        
        return simulation_results
    except ValueError as e:
        raise HTTPException(
            status_code=404, 
            detail=f"Game not found: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to run simulation: {str(e)}"
        )

@router.get("/baseball/{game_id}/history")
async def get_simulation_history(
    game_id: str,
    limit: int = 5,
    simulation_service: SimulationService = Depends(get_simulation_service)
):
    """
    Get history of previous simulations for a game
    """
    try:
        history = await simulation_service.get_simulation_history(
            game_id=game_id,
            limit=limit
        )
        
        return {
            "gameId": game_id,
            "simulations": history
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to retrieve simulation history: {str(e)}"
        )

@router.post("/baseball/factors/{game_id}")
async def analyze_game_factors(
    game_id: str,
    factor_service: FactorAnalysisService = Depends(get_factor_analysis_service)
):
    """
    Analyze factors that could impact a baseball game outcome
    """
    try:
        factors = await factor_service.analyze_game_factors(game_id)
        return factors
    except ValueError as e:
        raise HTTPException(
            status_code=404, 
            detail=f"Game not found: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to analyze factors: {str(e)}"
        )