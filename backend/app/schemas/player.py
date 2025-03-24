# backend/app/schemas/player.py
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class PlayerBase(BaseModel):
    id: str
    name: str
    teamId: str
    position: str
    jerseyNumber: Optional[str] = None
    status: Optional[str] = "active"

class PlayerAttributes(BaseModel):
    bats: Optional[str] = None  # "R", "L", "S" (switch)
    throws: Optional[str] = None  # "R", "L"
    height: Optional[str] = None  # In feet/inches format (e.g. "6-2")
    weight: Optional[int] = None  # In pounds

class BattingStats(BaseModel):
    avg: Optional[float] = None
    obp: Optional[float] = None
    slg: Optional[float] = None
    ops: Optional[float] = None
    homeRuns: Optional[int] = None
    rbi: Optional[int] = None
    hits: Optional[int] = None
    atBats: Optional[int] = None

class PitchingStats(BaseModel):
    era: Optional[float] = None
    wins: Optional[int] = None
    losses: Optional[int] = None
    saves: Optional[int] = None
    inningsPitched: Optional[float] = None
    strikeouts: Optional[int] = None
    walks: Optional[int] = None
    whip: Optional[float] = None

class PlayerCreate(PlayerBase):
    attributes: Optional[PlayerAttributes] = None
    battingStats: Optional[BattingStats] = None
    pitchingStats: Optional[PitchingStats] = None

class Player(PlayerBase):
    attributes: Optional[PlayerAttributes] = None
    battingStats: Optional[BattingStats] = None
    pitchingStats: Optional[PitchingStats] = None
    lastUpdated: Optional[datetime] = None

    class Config:
        orm_mode = True

class PlayerDetail(Player):
    team: Optional[Dict[str, Any]] = None
    recentGames: Optional[list] = None
    
    class Config:
        orm_mode = True