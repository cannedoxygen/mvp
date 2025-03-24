# backend/app/schemas/team.py
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

class TeamBase(BaseModel):
    id: str
    name: str
    abbreviation: str
    city: Optional[str] = None
    sportType: str = "baseball"
    league: Optional[str] = None
    division: Optional[str] = None

class TeamCreate(TeamBase):
    wins: Optional[int] = 0
    losses: Optional[int] = 0
    
    # Batting stats
    teamBattingAvg: Optional[float] = None
    teamObp: Optional[float] = None
    teamSlg: Optional[float] = None
    teamOps: Optional[float] = None
    teamHomeRuns: Optional[int] = None
    teamRunsPerGame: Optional[float] = None
    
    # Pitching stats
    teamEra: Optional[float] = None
    teamWhip: Optional[float] = None
    teamStrikeoutsPerNine: Optional[float] = None
    teamWalksPerNine: Optional[float] = None

class BattingStats(BaseModel):
    average: Optional[float] = None
    obp: Optional[float] = None
    slugging: Optional[float] = None
    ops: Optional[float] = None
    homeRuns: Optional[int] = None
    runsPerGame: Optional[float] = None

class PitchingStats(BaseModel):
    era: Optional[float] = None
    whip: Optional[float] = None
    strikeoutsPerNine: Optional[float] = None
    walksPerNine: Optional[float] = None

class Team(TeamBase):
    record: Optional[str] = None
    homeRecord: Optional[str] = None
    awayRecord: Optional[str] = None
    last10: Optional[str] = None
    batting: Optional[BattingStats] = None
    pitching: Optional[PitchingStats] = None
    
    class Config:
        orm_mode = True

class TeamDetail(Team):
    upcomingGames: Optional[List[Dict[str, Any]]] = None
    recentGames: Optional[List[Dict[str, Any]]] = None
    
    class Config:
        orm_mode = True

class TeamsList(BaseModel):
    teams: List[Team]
    count: int
    
    class Config:
        orm_mode = True