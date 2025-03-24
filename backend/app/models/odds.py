# backend/app/models/odds.py
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Dict, Any, Optional

from app.core.database import Base

class GameOdds(Base):
    """Model for game betting odds"""
    __tablename__ = "game_odds"
    
    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(String, ForeignKey("games.id"), unique=True, index=True)
    
    # Moneyline
    home_moneyline = Column(Integer)
    away_moneyline = Column(Integer)
    
    # Spread (run line in baseball)
    spread = Column(Float, default=1.5)  # Typically 1.5 for baseball
    home_spread_odds = Column(Integer)
    away_spread_odds = Column(Integer)
    
    # Total
    total_runs = Column(Float)
    over_odds = Column(Integer)
    under_odds = Column(Integer)
    
    # Metadata
    bookmaker = Column(String, default="Consensus")
    last_updated = Column(DateTime, default=datetime.utcnow)
    
    # Additional odds in JSON format
    additional_markets = Column(JSON)  # For alternative lines, props, etc.
    
    # Relationships
    game = relationship("Game", back_populates="odds")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "gameId": self.game_id,
            "homeTeam": self.game.home_team.name if self.game and self.game.home_team else None,
            "awayTeam": self.game.away_team.name if self.game and self.game.away_team else None,
            "homeMoneyline": self.home_moneyline,
            "awayMoneyline": self.away_moneyline,
            "spread": self.spread,
            "homeSpreadOdds": self.home_spread_odds,
            "awaySpreadOdds": self.away_spread_odds,
            "totalRuns": self.total_runs,
            "overOdds": self.over_odds,
            "underOdds": self.under_odds,
            "bookmaker": self.bookmaker,
            "lastUpdated": self.last_updated.isoformat() if self.last_updated else None,
            "additionalMarkets": self.additional_markets
        }

class PropBet(Base):
    """Model for player prop bets"""
    __tablename__ = "prop_bets"
    
    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(String, ForeignKey("games.id"), index=True)
    player_id = Column(String, ForeignKey("players.id"), index=True)
    
    # Prop type and line
    bet_type = Column(String, index=True)  # "strikeouts", "home_run", "hits", etc.
    bet_description = Column(String)
    line = Column(Float)
    
    # Odds
    over_odds = Column(Integer)
    under_odds = Column(Integer)
    
    # Metadata
    bookmaker = Column(String, default="Consensus")
    last_updated = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    game = relationship("Game")
    player = relationship("Player")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "gameId": self.game_id,
            "playerId": self.player_id,
            "playerName": self.player.name if self.player else None,
            "betType": self.bet_type,
            "betDescription": self.bet_description,
            "line": self.line,
            "overOdds": self.over_odds,
            "underOdds": self.under_odds,
            "bookmaker": self.bookmaker,
            "lastUpdated": self.last_updated.isoformat() if self.last_updated else None
        }