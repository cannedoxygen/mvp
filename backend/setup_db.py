# Save as backend/setup_db.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create engine
DATABASE_URL = "sqlite:///./baseball_betting.db"
engine = create_engine(DATABASE_URL)

# Create tables
Base = declarative_base()

# Import only what's necessary
from app.models.team import Team

# Create tables
Base.metadata.create_all(bind=engine)
print("Database tables created successfully")