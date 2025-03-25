# backend/setup_db.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create engine
DATABASE_URL = "sqlite:///./baseball_betting.db"
engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(bind=engine)

# Create base class
Base = declarative_base()

def setup_database():
    """Create database tables if they don't exist"""
    # Import all models
    from app.models.team import Team
    from app.models.player import Player
    from app.models.game import Game
    from app.models.odds import GameOdds, PropBet
    from app.models.simulation import Simulation
    
    # Import relationships after all models are defined
    from app.models.relationships import *
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")

if __name__ == "__main__":
    setup_database()