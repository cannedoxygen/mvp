# backend/import_all_models.py
# Import all models first to ensure they're registered with SQLAlchemy
from app.models.team import Team
from app.models.player import Player
from app.models.game import Game
from app.models.odds import GameOdds, PropBet
from app.models.simulation import Simulation

# Import relationships after all models are defined
# This ensures that all models are loaded before establishing relationships
from app.models.relationships import *

print("All models and relationships imported successfully")