# backend/app/schemas/simulation.py
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class SimulationRequest(BaseModel):
    count: Optional[int] = Field(1000, description="Number of simulations to run")
    includeProps: Optional[bool] = Field(False, description="Whether to include prop bet analysis")
    factors: Optional[Dict[str, Any]] = Field(None, description="Custom factors to apply to simulation")

class SimulationFactors(BaseModel):
    weather: Optional[Dict[str, float]] = None
    lineups: Optional[Dict[str, Any]] = None
    injuries: Optional[List[Dict[str, Any]]] = None
    recent_form: Optional[Dict[str, float]] = None

class BettingInsight(BaseModel):
    homeMoneyline: int
    awayMoneyline: int
    overOdds: int
    underOdds: int

class PropBetInsight(BaseModel):
    playerName: str
    betType: str
    line: float
    recommendation: str
    confidence: float
    reasoning: Optional[str] = None

class SimulationResult(BaseModel):
    gameId: str
    simulationCount: int
    homeTeamName: str
    awayTeamName: str
    homeWinProbability: float
    awayWinProbability: float
    averageHomeScore: float
    averageAwayScore: float
    averageTotalRuns: float
    bettingInsights: BettingInsight
    propBetInsights: Optional[List[PropBetInsight]] = None
    impactingFactors: Optional[List[str]] = None
    createdAt: Optional[datetime] = None

    class Config:
        orm_mode = True

class SimulationHistory(BaseModel):
    gameId: str
    simulations: List[SimulationResult]
    count: int

    class Config:
        orm_mode = True