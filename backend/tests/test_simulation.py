import pytest
import numpy as np
from app.services.simulation import SimulationService

def test_simulation_service_initialization():
    """
    Test that SimulationService can be initialized
    """
    simulation_service = SimulationService()
    assert simulation_service is not None

@pytest.mark.asyncio
async def test_baseball_simulation_basic_flow():
    """
    Test basic flow of running a baseball game simulation
    """
    simulation_service = SimulationService()
    
    # Use a sample game ID
    game_id = "mlb-2025-03-23-lad-sf"
    
    # Run simulation
    result = await simulation_service.run_baseball_simulation(game_id)
    
    # Validate core simulation results
    assert result is not None
    assert result.gameId == game_id
    
    # Validate probabilities
    assert 0 <= result.homeWinProbability <= 1
    assert 0 <= result.awayWinProbability <= 1
    assert np.isclose(result.homeWinProbability + result.awayWinProbability, 1.0, atol=0.01)
    
    # Validate scores
    assert result.averageHomeScore >= 0
    assert result.averageAwayScore >= 0
    assert result.averageTotalRuns > 0

def test_simulation_betting_insights():
    """
    Test betting insights generation during simulation
    """
    simulation_service = SimulationService()
    
    # Sample game data
    sample_game_data = {
        "homeTeam": {
            "name": "Home Team",
            "batting_rating": 0.75,
            "pitching_rating": 0.7
        },
        "awayTeam": {
            "name": "Away Team", 
            "batting_rating": 0.8,
            "pitching_rating": 0.65
        }
    }
    
    # Simulated factors
    factors = {
        "home_batting_adjustment": 0.02,
        "away_pitching_adjustment": -0.01
    }
    
    # Validate betting insights are generated
    game_simulation = simulation_service._simulate_game(
        sample_game_data["homeTeam"],
        sample_game_data["awayTeam"],
        {"rating": 0.7},  # home pitcher
        {"rating": 0.65}  # away pitcher
    )
    
    assert "home_score" in game_simulation
    assert "away_score" in game_simulation
    assert game_simulation["home_score"] >= 0
    assert game_simulation["away_score"] >= 0

def test_probability_to_american_odds():
    """
    Test conversion of probability to American odds
    """
    simulation_service = SimulationService()
    
    # Test various probability scenarios
    test_cases = [
        0.6,  # Favorite scenario
        0.4,  # Underdog scenario
        0.5   # Near-even scenario
    ]
    
    for prob in test_cases:
        odds = simulation_service._probability_to_american_odds(prob)
        assert isinstance(odds, int)
        
        # Validate basic odds conversion rules
        if prob > 0.5:
            # Favorite has negative odds
            assert odds < 0
        elif prob < 0.5:
            # Underdog has positive odds
            assert odds > 0

def test_invalid_probability_conversion():
    """
    Test handling of invalid probability inputs
    """
    simulation_service = SimulationService()
    
    # Test out-of-range probabilities
    with pytest.raises(ValueError):
        simulation_service._probability_to_american_odds(-0.1)
    
    with pytest.raises(ValueError):
        simulation_service._probability_to_american_odds(1.1)