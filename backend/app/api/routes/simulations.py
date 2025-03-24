# backend/app/api/routes/simulations.py
from fastapi import APIRouter, Depends, HTTPException, Body
from typing import Dict, Any, Optional
from datetime import date

from app.models.simulation import SimulationResult, SimulationRequest
from app.services.simulation import SimulationService
from app.services.factor_analysis import FactorAnalysisService
from app.api.dependencies import get_db, get_simulation_service, get_factor_analysis_service

router = APIRouter()

@router.post("/baseball/{game_id}", response_model=SimulationResult)
async def run_baseball_simulation(
    game_id: str,
    request: SimulationRequest = Body(...),
    simulation_service: SimulationService = Depends(get_simulation_service),
    factor_service: FactorAnalysisService = Depends(get_factor_analysis_service)
):
    """
    Run a Monte Carlo simulation for a specific baseball game
    """
    try:
        # Analyze factors that might impact the game
        factors = await factor_service.analyze_game_factors(game_id)
        
        # Run Monte Carlo simulation with the analyzed factors
        simulation_results = await simulation_service.run_baseball_simulation(
            game_id=game_id,
            count=request.count,
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

@router.get("/baseball/{game_id}/history", response_model=Dict[str, Any])
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
            "game_id": game_id,
            "simulations": history
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to retrieve simulation history: {str(e)}"
        )

@router.post("/baseball/factors/{game_id}", response_model=Dict[str, Any])
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