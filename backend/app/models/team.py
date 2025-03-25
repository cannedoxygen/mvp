# backend/app/models/team.py
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, JSON
from sqlalchemy.orm import relationship
from typing import Dict, Any, List, Optional
from datetime import datetime

from app.core.database import Base

class Team(Base):
    """Model for sports teams"""
    __tablename__ = "teams"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    abbreviation = Column(String, index=True)
    city = Column(String)
    sport_type = Column(String, index=True, default="baseball")
    league = Column(String)  # "AL", "NL" for baseball
    division = Column(String)  # "East", "Central", "West"
    
    # Team statistics (baseball-specific)
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    
    # Team rating components
    team_batting_avg = Column(Float)
    team_obp = Column(Float)  # On-base percentage
    team_slg = Column(Float)  # Slugging percentage
    team_ops = Column(Float)  # On-base plus slugging
    team_home_runs = Column(Integer)
    team_runs_per_game = Column(Float)
    
    # Pitching metrics
    team_era = Column(Float)  # Earned run average
    team_whip = Column(Float)  # Walks plus hits per inning pitched
    team_strikeouts_per_nine = Column(Float)
    team_walks_per_nine = Column(Float)
    
    # Extended data in JSON format
    team_stats = Column(JSON) # For additional statistics
    
    # Timestamps
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Do not include relationship definitions here to avoid circular imports
    # They will be defined in relationships.py
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "abbreviation": self.abbreviation,
            "city": self.city,
            "league": self.league,
            "division": self.division,
            "record": f"{self.wins}-{self.losses}" if self.wins is not None and self.losses is not None else None,
            "batting": {
                "average": self.team_batting_avg,
                "obp": self.team_obp,
                "slugging": self.team_slg,
                "ops": self.team_ops,
                "homeRuns": self.team_home_runs,
                "runsPerGame": self.team_runs_per_game
            } if self.team_batting_avg is not None else None,
            "pitching": {
                "era": self.team_era,
                "whip": self.team_whip,
                "strikeoutsPerNine": self.team_strikeouts_per_nine,
                "walksPerNine": self.team_walks_per_nine
            } if self.team_era is not None else None,
            "stadium": {
                "name": None,
                "location": None,
                "type": None
            }
        }