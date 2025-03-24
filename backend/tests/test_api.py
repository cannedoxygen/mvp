from fastapi.testclient import TestClient
from datetime import date, datetime

def test_get_todays_games(test_app, db):
    """
    Test retrieving today's baseball games
    """
    client = TestClient(test_app)
    
    # Make request to get today's games
    response = client.get("/api/v1/games/baseball/today")
    
    # Check response
    assert response.status_code == 200
    
    # Verify response structure
    games = response.json()
    assert isinstance(games, list)

def test_get_game_details(test_app, db):
    """
    Test retrieving details for a specific game
    """
    client = TestClient(test_app)
    
    # Assuming we have a way to get a sample game ID
    # This might need to be adjusted based on your actual data seeding strategy
    sample_game_id = "mlb-2025-03-23-lad-sf"
    
    # Make request to get game details
    response = client.get(f"/api/v1/games/baseball/{sample_game_id}")
    
    # Check response
    assert response.status_code == 200
    
    # Verify response structure
    game = response.json()
    assert "id" in game
    assert "homeTeam" in game
    assert "awayTeam" in game
    assert "startTime" in game

def test_run_simulation(test_app, db):
    """
    Test running a game simulation
    """
    client = TestClient(test_app)
    
    # Assuming we have a way to get a sample game ID
    sample_game_id = "mlb-2025-03-23-lad-sf"
    
    # Make request to run simulation
    response = client.post(f"/api/v1/simulations/baseball/{sample_game_id}", json={
        "count": 1000
    })
    
    # Check response
    assert response.status_code == 200
    
    # Verify simulation result structure
    simulation = response.json()
    assert "gameId" in simulation
    assert "homeWinProbability" in simulation
    assert "awayWinProbability" in simulation
    assert 0 <= simulation["homeWinProbability"] <= 1
    assert 0 <= simulation["awayWinProbability"] <= 1