# backend/scripts/db_setup.py
import sys
import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add parent directory to path so we can import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import Base
from app.config import settings

# Import all models to ensure they're registered with SQLAlchemy
from app.models.game import Game
from app.models.team import Team
from app.models.player import Player
from app.models.odds import GameOdds, PropBet
from app.models.simulation import Simulation

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

def setup_database():
    """
    Create database tables based on SQLAlchemy models
    """
    logger.info(f"Setting up database at {settings.DATABASE_URL}")
    
    # Create engine
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}
    )
    
    # Create all tables
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")
        sys.exit(1)
    
    return engine

def drop_database():
    """
    Drop all database tables (use with caution!)
    """
    logger.warning(f"Dropping all tables from {settings.DATABASE_URL}")
    
    # Ask for confirmation
    confirm = input("This will delete all data in the database. Type 'YES' to confirm: ")
    if confirm != "YES":
        logger.info("Operation cancelled")
        return
    
    # Create engine
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}
    )
    
    # Drop all tables
    try:
        Base.metadata.drop_all(bind=engine)
        logger.info("Database tables dropped successfully")
    except Exception as e:
        logger.error(f"Error dropping database tables: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Database setup utility")
    parser.add_argument("--action", choices=["setup", "drop"], default="setup", 
                      help="Action to perform (setup or drop)")
    
    args = parser.parse_args()
    
    if args.action == "setup":
        setup_database()
    elif args.action == "drop":
        drop_database()