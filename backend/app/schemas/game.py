# backend/app/schemas/game.py
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class TeamBase(BaseModel):
    id: str
    name: str
    abbreviation: str

    class Config:
        orm_mode = True

class TeamDetail(TeamBase):
    city: Optional[str] = None
    league: Optional[str] = None
    division: Optional[str] = None
    record: Optional[str] = None
    batting: Optional[Dict[str, Any]] = None
    pitching: Optional[Dict[str, Any]] = None

class WeatherInfo(BaseModel):
    temperature: Optional[float] = None
    condition: Optional[str] = None
    windSpeed: Optional[float] = None
    windDirection: Optional[str] = None

class GameBase(BaseModel):
    id: str
    sportType: str = "baseball"
    status: str
    startTime: datetime
    stadium: Optional[str] = None

class GameCreate(GameBase):
    homeTeamId: str
    awayTeamId: str
    date: str  # YYYY-MM-DD format
    location: Optional[str] = None
    temperature: Optional[float] = None
    weatherCondition: Optional[str] = None
    windSpeed: Optional[float] = None
    windDirection: Optional[str] = None

class Game(GameBase):
    homeTeam: TeamBase
    awayTeam: TeamBase
    weather: Optional[WeatherInfo] = None

    class Config:
        orm_mode = True

class GameDetail(Game):
    bettingOdds: Optional[Dict[str, Any]] = None
    simulationResults: Optional[Dict[str, Any]] = None

    class Config:
        orm_mode = True

class GameList(BaseModel):
    games: List[Game]
    total: int
    page: int
    pageSize: int

    class Config:
        orm_mode = True