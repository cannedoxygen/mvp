# backend/app/models/simulation.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Dict, Any, List, Optional

from app.core.database import Base
from app.models.game import Game  # Import Game model

class Simulation(Base):
    """Model for game simulations"""
    __tablename__ = "simulations"
    
    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(String, ForeignKey("games.id"), index=True)
    
    # Simulation parameters
    simulation_count = Column(Integer, default=1000)
    
    # Simulation results
    home_win_probability = Column(Float)
    away_win_probability = Column(Float)
    average_home_score = Column(Float)
    average_away_score = Column(Float)
    average_total_runs = Column(Float)
    
    # Betting insights
    betting_insights = Column(JSON)  # JSON field for storing calculated odds
    prop_bet_insights = Column(JSON)  # JSON field for storing prop bet recommendations
    
    # Factors that impacted the simulation
    impacting_factors = Column(JSON)  # JSON field for storing impact factors
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    game = relationship("Game", backref="simulations")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "gameId": self.game_id,
            "simulationCount": self.simulation_count,
            "homeTeamName": self.game.home_team.name if self.game and self.game.home_team else None,
            "awayTeamName": self.game.away_team.name if self.game and self.game.away_team else None,
            "homeWinProbability": self.home_win_probability,
            "awayWinProbability": self.away_win_probability,
            "averageHomeScore": self.average_home_score,
            "averageAwayScore": self.average_away_score,
            "averageTotalRuns": self.average_total_runs,
            "bettingInsights": self.betting_insights,
            "propBetInsights": self.prop_bet_insights,
            "impactingFactors": self.impacting_factors,
            "createdAt": self.created_at.isoformat() if self.created_at else None
        }

class SimulationRequest:
    """Schema for simulation request"""
    def __init__(self, count: int = 1000):
        self.count = count

class SimulationResult:
    """Schema for simulation result"""
    def __init__(
        self,
        gameId: str,
        simulationCount: int,
        homeTeamName: str,
        awayTeamName: str,
        homeWinProbability: float,
        awayWinProbability: float,
        averageHomeScore: float,
        averageAwayScore: float,
        averageTotalRuns: float,
        bettingInsights: Dict[str, Any],
        propBetInsights: Optional[List[Dict[str, Any]]] = None,
        impactingFactors: Optional[List[str]] = None
    ):
        self.gameId = gameId
        self.simulationCount = simulationCount
        self.homeTeamName = homeTeamName
        self.awayTeamName = awayTeamName
        self.homeWinProbability = homeWinProbability
        self.awayWinProbability = awayWinProbability
        self.averageHomeScore = averageHomeScore
        self.averageAwayScore = averageAwayScore
        self.averageTotalRuns = averageTotalRuns
        self.bettingInsights = bettingInsights
        self.propBetInsights = propBetInsights or []
        self.impactingFactors = impactingFactors or []