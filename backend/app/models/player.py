# backend/app/models/player.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Dict, Any, List, Optional

from app.core.database import Base

class Player(Base):
    """Model for baseball players"""
    __tablename__ = "players"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    team_id = Column(String, ForeignKey("teams.id"), index=True)
    position = Column(String, index=True)  # "P", "C", "1B", "2B", "3B", "SS", "OF", etc.
    jersey_number = Column(String)
    status = Column(String)  # "active", "injured", etc.
    
    # Common player attributes
    bats = Column(String)  # "R", "L", "S" (switch)
    throws = Column(String)  # "R", "L"
    height = Column(String)  # In feet/inches format (e.g. "6-2")
    weight = Column(Integer)  # In pounds
    birth_date = Column(DateTime)
    birth_city = Column(String)
    birth_state = Column(String)
    birth_country = Column(String)
    
    # Batting statistics (season)
    batting_avg = Column(Float)
    obp = Column(Float)  # On-base percentage
    slg = Column(Float)  # Slugging percentage
    ops = Column(Float)  # On-base plus slugging
    home_runs = Column(Integer)
    rbi = Column(Integer)  # Runs batted in
    hits = Column(Integer)
    doubles = Column(Integer)
    triples = Column(Integer)
    stolen_bases = Column(Integer)
    at_bats = Column(Integer)
    runs = Column(Integer)
    
    # Pitching statistics (season)
    era = Column(Float)  # Earned run average
    wins = Column(Integer)
    losses = Column(Integer)
    saves = Column(Integer)
    innings_pitched = Column(Float)
    strikeouts = Column(Integer)
    walks = Column(Integer)
    whip = Column(Float)  # Walks plus hits per inning pitched
    complete_games = Column(Integer)
    shutouts = Column(Integer)
    
    # Fantasy data
    fanduel_salary = Column(Integer)
    draftkings_salary = Column(Integer)
    yahoo_salary = Column(Integer)
    
    # Additional data
    injury_status = Column(String)
    injury_details = Column(String)
    
    # Extended data in JSON format
    season_stats = Column(JSON)  # Current season statistics
    career_stats = Column(JSON)  # Career statistics
    recent_games = Column(JSON)  # Recent game performances
    
    # Metadata
    last_updated = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    team = relationship("Team", back_populates="players")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        player_dict = {
            "id": self.id,
            "name": self.name,
            "teamId": self.team_id,
            "position": self.position,
            "jerseyNumber": self.jersey_number,
            "status": self.status,
            "attributes": {
                "bats": self.bats,
                "throws": self.throws,
                "height": self.height,
                "weight": self.weight,
                "birthDate": self.birth_date.isoformat() if self.birth_date else None,
                "birthCity": self.birth_city,
                "birthState": self.birth_state,
                "birthCountry": self.birth_country
            }
        }
        
        # Add batting stats if this is a position player or this is a two-way player
        if self.position != "P" or self.batting_avg is not None:
            player_dict["battingStats"] = {
                "avg": self.batting_avg,
                "obp": self.obp,
                "slg": self.slg,
                "ops": self.ops,
                "homeRuns": self.home_runs,
                "rbi": self.rbi,
                "hits": self.hits,
                "doubles": self.doubles,
                "triples": self.triples,
                "stolenBases": self.stolen_bases,
                "atBats": self.at_bats,
                "runs": self.runs
            }
        
        # Add pitching stats if this is a pitcher
        if self.position == "P" or self.era is not None:
            player_dict["pitchingStats"] = {
                "era": self.era,
                "wins": self.wins,
                "losses": self.losses,
                "saves": self.saves,
                "inningsPitched": self.innings_pitched,
                "strikeouts": self.strikeouts,
                "walks": self.walks,
                "whip": self.whip,
                "completeGames": self.complete_games,
                "shutouts": self.shutouts
            }
        
        # Add fantasy data if available
        if self.fanduel_salary or self.draftkings_salary or self.yahoo_salary:
            player_dict["fantasyData"] = {
                "fanduelSalary": self.fanduel_salary,
                "draftkingsSalary": self.draftkings_salary,
                "yahooSalary": self.yahoo_salary
            }
        
        # Add injury data if available
        if self.injury_status:
            player_dict["injury"] = {
                "status": self.injury_status,
                "details": self.injury_details
            }
        
        return player_dict