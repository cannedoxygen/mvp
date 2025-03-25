# backend/app/models/relationships.py
from sqlalchemy.orm import relationship
from app.models.game import Game
from app.models.team import Team
from app.models.player import Player
from app.models.odds import GameOdds, PropBet
from app.models.simulation import Simulation

# Define relationships after all models are imported
Game.home_team = relationship("Team", foreign_keys=[Game.home_team_id], backref="home_games")
Game.away_team = relationship("Team", foreign_keys=[Game.away_team_id], backref="away_games")
Game.odds = relationship("GameOdds", back_populates="game", uselist=False)
Game.simulations = relationship("Simulation", back_populates="game")

# Player relationships
Player.team = relationship("Team", back_populates="players")
Team.players = relationship("Player", back_populates="team")

# Simulation relationships
Simulation.game = relationship("Game", back_populates="simulations")