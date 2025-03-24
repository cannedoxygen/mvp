# backend/reset_database.py
import os
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.config import settings
from sqlalchemy import create_engine
from app.core.database import Base

# Import all models to ensure they're registered with SQLAlchemy
from app.models.team import Team
from app.models.player import Player
from app.models.game import Game
from app.models.odds import GameOdds, PropBet
from app.models.simulation import Simulation

def reset_database():
    """Reset the database by dropping and recreating all tables"""
    # Get database path for SQLite
    if settings.DATABASE_URL.startswith('sqlite:///'):
        db_path = settings.DATABASE_URL.replace('sqlite:///', '')
        
        # Confirm with user before proceeding
        logger.info(f"About to reset database at {db_path}")
        confirm = input("This will delete all data in the database. Type 'yes' to confirm: ")
        
        if confirm.lower() != 'yes':
            logger.info("Operation cancelled")
            return
        
        # Delete the file if it exists (for SQLite)
        if os.path.exists(db_path) and db_path != '/':  # Safety check
            try:
                os.remove(db_path)
                logger.info(f"Deleted database file at {db_path}")
            except Exception as e:
                logger.error(f"Failed to delete database file: {str(e)}")
                return
    
    # Create engine
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}
    )
    
    # Create all tables
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Successfully created all database tables")
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")
        return
    
    logger.info("Database reset complete. You can now run the seeder script to populate it.")

if __name__ == "__main__":
    reset_database()