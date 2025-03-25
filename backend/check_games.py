# backend/check_games.py
import sys
import os
from datetime import date

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.team import Team
from app.models.game import Game
from app.models.player import Player

# Now import relationships after all models are imported
from app.models.relationships import *

def check_games():
    """Check for games in the database for today's date"""
    db = SessionLocal()
    try:
        today = date.today()
        today_str = today.strftime("%Y-%m-%d")
        
        # Query teams first
        teams = db.query(Team).all()
        print(f"Found {len(teams)} teams in database:")
        for team in teams:
            print(f"- {team.id}: {team.name} ({team.abbreviation})")
        
        print("\n" + "-"*50 + "\n")
        
        # Query games for today
        games = db.query(Game).filter(Game.date == today_str).all()
        
        print(f"Found {len(games)} games for today ({today_str}):")
        for game in games:
            print(f"- {game.id}: {game.away_team_id} @ {game.home_team_id}")
            print(f"  Stadium: {game.stadium}, Start time: {game.start_time}")
            print(f"  Status: {game.status}")
            print()
            
    finally:
        db.close()

if __name__ == "__main__":
    check_games()