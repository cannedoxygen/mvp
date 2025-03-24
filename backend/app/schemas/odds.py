# backend/app/schemas/odds.py
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class OddsBase(BaseModel):
    gameId: str
    homeTeam: Optional[str] = None
    awayTeam: Optional[str] = None
    
    # Moneyline
    homeMoneyline: int
    awayMoneyline: int
    
    # Total
    totalRuns: float
    overOdds: int
    underOdds: int
    
    # Spread (run line in baseball)
    spread: Optional[float] = Field(1.5, description="Run line (typically 1.5 for baseball)")
    homeSpreadOdds: Optional[int] = None
    awaySpreadOdds: Optional[int] = None
    
    # Metadata
    bookmaker: Optional[str] = "Consensus"
    lastUpdated: datetime

class GameOddsCreate(OddsBase):
    pass

class GameOdds(OddsBase):
    id: int
    
    class Config:
        orm_mode = True

class PropBetBase(BaseModel):
    gameId: str
    playerId: str
    playerName: Optional[str] = None
    betType: str  # "strikeouts", "home_run", "hits", etc.
    line: float
    overOdds: int
    underOdds: int

class PropBetCreate(PropBetBase):
    bookmaker: Optional[str] = "Consensus"

class PropBet(PropBetBase):
    id: int
    bookmaker: str
    lastUpdated: datetime
    
    class Config:
        orm_mode = True

class PropBetsList(BaseModel):
    propBets: List[PropBet]
    total: int
    
    class Config:
        orm_mode = True