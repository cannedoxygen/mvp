# backend/app/api/dependencies.py
from typing import Generator
from fastapi import Depends, HTTPException, status

from app.core.database import SessionLocal
from app.clients.sportsdataio import SportsDataIOClient
from app.clients.oddsapi import OddsAPIClient
from app.clients.weather import WeatherClient
from app.clients.openai_client import OpenAIClient
from app.services.simulation import SimulationService
from app.services.gameService import GameService
from app.services.factor_analysis import FactorAnalysisService
from app.services.ai_analysis import AIAnalysisService
from app.services.oddsService import OddsService  # Added import
from app.config import settings

def get_db() -> Generator:
    """
    Dependency for database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_sports_data_client() -> SportsDataIOClient:
    """
    Dependency for SportsData.io client
    """
    return SportsDataIOClient(api_key=settings.SPORTSDATAIO_API_KEY)

def get_odds_client() -> OddsAPIClient:
    """
    Dependency for Odds API client
    """
    return OddsAPIClient(api_key=settings.ODDS_API_KEY)

def get_weather_client() -> WeatherClient:
    """
    Dependency for Weather client
    """
    return WeatherClient(api_key=settings.WEATHER_API_KEY)

def get_openai_client() -> OpenAIClient:
    """
    Dependency for OpenAI client
    """
    return OpenAIClient(api_key=settings.OPENAI_API_KEY)

def get_game_service(
    sports_data_client: SportsDataIOClient = Depends(get_sports_data_client)
) -> GameService:
    """
    Dependency for Game service
    """
    return GameService(sports_data_client=sports_data_client)

def get_simulation_service(
    db = Depends(get_db),
    game_service: GameService = Depends(get_game_service)
) -> SimulationService:
    """
    Dependency for Simulation service
    """
    return SimulationService(db=db, game_service=game_service)

def get_factor_analysis_service(
    db = Depends(get_db),
    game_service: GameService = Depends(get_game_service)
) -> FactorAnalysisService:
    """
    Dependency for FactorAnalysis service
    """
    return FactorAnalysisService(db=db, game_service=game_service)

def get_ai_analysis_service(
    openai_client: OpenAIClient = Depends(get_openai_client),
    game_service: GameService = Depends(get_game_service)
) -> AIAnalysisService:
    """
    Dependency for AIAnalysis service
    """
    return AIAnalysisService(openai_client=openai_client, game_service=game_service)

def get_odds_service(
    sports_data_client: SportsDataIOClient = Depends(get_sports_data_client)
) -> OddsService:
    """
    Dependency for Odds service
    """
    return OddsService(sports_data_client=sports_data_client)