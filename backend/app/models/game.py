# backend/app/models/game.py
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Boolean, Table, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Optional, List, Dict, Any

from app.core.database import Base

class Game(Base):
    """Model for baseball games"""
    __tablename__ = "games"
    
    id = Column(String, primary_key=True, index=True)
    sport_type = Column(String, index=True, default="baseball")
    status = Column(String, index=True)  # "scheduled", "inProgress", "final", "postponed", "canceled"
    start_time = Column(DateTime, index=True)
    date = Column(String, index=True)  # YYYY-MM-DD format for easy querying
    
    # Teams
    home_team_id = Column(String, ForeignKey("teams.id"))
    away_team_id = Column(String, ForeignKey("teams.id"))
    
    # Scores
    home_score = Column(Integer, nullable=True)
    away_score = Column(Integer, nullable=True)
    
    # Game state
    inning = Column(Integer, nullable=True)
    inning_half = Column(String, nullable=True)  # "T" for top, "B" for bottom
    outs = Column(Integer, nullable=True)
    balls = Column(Integer, nullable=True)
    strikes = Column(Integer, nullable=True)
    
    # Stadium info
    stadium = Column(String)
    location = Column(String)
    
    # Weather conditions
    temperature = Column(Float, nullable=True)
    weather_condition = Column(String, nullable=True)
    wind_speed = Column(Float, nullable=True)
    wind_direction = Column(String, nullable=True)
    
    # Game details - stored as JSON
    inning_scores = Column(JSON, nullable=True)
    team_stats = Column(JSON, nullable=True)
    player_stats = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Do not include relationship definitions here to avoid circular imports
    # They will be defined in relationships.py
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "sportType": self.sport_type,
            "status": self.status,
            "startTime": self.start_time.isoformat() if self.start_time else None,
            "date": self.date,
            "homeTeam": self.home_team.to_dict() if self.home_team else None,
            "awayTeam": self.away_team.to_dict() if self.away_team else None,
            "homeScore": self.home_score,
            "awayScore": self.away_score,
            "inning": self.inning,
            "inningHalf": self.inning_half,
            "outs": self.outs,
            "balls": self.balls,
            "strikes": self.strikes,
            "stadium": self.stadium,
            "location": self.location,
            "weather": {
                "temperature": self.temperature,
                "condition": self.weather_condition,
                "windSpeed": self.wind_speed,
                "windDirection": self.wind_direction
            } if self.temperature is not None else None,
            "inningScores": self.inning_scores if self.inning_scores else [],
            "teamStats": self.team_stats if self.team_stats else {},
            "playerStats": self.player_stats if self.player_stats else []
        }