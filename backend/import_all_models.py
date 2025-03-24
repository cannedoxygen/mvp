# Create this as backend/import_all_models.py
# Import all models to ensure they're registered with SQLAlchemy
from app.models.team import Team
from app.models.player import Player
from app.models.game import Game
from app.models.odds import GameOdds, PropBet
from app.models.simulation import Simulation

print("All models imported successfully")