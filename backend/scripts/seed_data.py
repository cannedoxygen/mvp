# backend/scripts/seed_data.py
import sys
import os
import logging
import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine

# Add parent directory to path so we can import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import Base, get_db_session
from app.config import settings
from app.models.team import Team
from app.models.player import Player
from app.models.game import Game
from app.models.odds import GameOdds, PropBet
from app.models.simulation import Simulation

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

class DataSeeder:
    """Utility for seeding the database with initial data"""
    
    def seed_all(self):
        """Seed all data"""
        with get_db_session() as db:
            # Seed in order to maintain relationships
            self.seed_teams(db)
            self.seed_players(db)
            self.seed_games(db)
            self.seed_odds(db)
            logger.info("All data seeded successfully")
    
    def seed_teams(self, db):
        """Seed baseball teams"""
        logger.info("Seeding teams data...")
        
        # Sample teams data
        teams_data = [
            {
                "id": "lad",
                "name": "Los Angeles Dodgers",
                "abbreviation": "LAD",
                "city": "Los Angeles",
                "league": "NL",
                "division": "West",
                "wins": 95,
                "losses": 67
            },
            {
                "id": "sf",
                "name": "San Francisco Giants",
                "abbreviation": "SF",
                "city": "San Francisco",
                "league": "NL",
                "division": "West",
                "wins": 82,
                "losses": 80
            },
            {
                "id": "nyy",
                "name": "New York Yankees",
                "abbreviation": "NYY",
                "city": "New York",
                "league": "AL",
                "division": "East",
                "wins": 92,
                "losses": 70
            },
            {
                "id": "bos",
                "name": "Boston Red Sox",
                "abbreviation": "BOS",
                "city": "Boston",
                "league": "AL", 
                "division": "East",
                "wins": 78,
                "losses": 84
            },
            {
                "id": "hou",
                "name": "Houston Astros",
                "abbreviation": "HOU",
                "city": "Houston",
                "league": "AL",
                "division": "West",
                "wins": 90,
                "losses": 72
            },
            {
                "id": "tex",
                "name": "Texas Rangers",
                "abbreviation": "TEX",
                "city": "Arlington",
                "league": "AL",
                "division": "West",
                "wins": 86,
                "losses": 76
            }
        ]
        
        # Check if teams already exist
        existing_count = db.query(Team).count()
        if existing_count > 0:
            logger.info(f"Teams already seeded ({existing_count} found). Skipping.")
            return
        
        # Create teams
        for team_data in teams_data:
            team = Team(
                id=team_data["id"],
                name=team_data["name"],
                abbreviation=team_data["abbreviation"],
                city=team_data["city"],
                sport_type="baseball",
                league=team_data["league"],
                division=team_data["division"],
                wins=team_data["wins"],
                losses=team_data["losses"],
                
                # Add batting stats
                team_batting_avg=round(random.uniform(0.220, 0.280), 3),
                team_obp=round(random.uniform(0.300, 0.350), 3),
                team_slg=round(random.uniform(0.380, 0.450), 3),
                team_ops=round(random.uniform(0.680, 0.800), 3),
                team_home_runs=random.randint(100, 250),
                team_runs_per_game=round(random.uniform(3.5, 5.5), 1),
                
                # Add pitching stats
                team_era=round(random.uniform(3.00, 5.00), 2),
                team_whip=round(random.uniform(1.10, 1.40), 2),
                team_strikeouts_per_nine=round(random.uniform(7.5, 10.0), 1),
                team_walks_per_nine=round(random.uniform(2.5, 4.0), 1)
            )
            db.add(team)
        
        db.commit()
        logger.info(f"Seeded {len(teams_data)} teams")
    
    def seed_players(self, db):
        """Seed baseball players"""
        logger.info("Seeding players data...")
        
        # Check if players already exist
        existing_count = db.query(Player).count()
        if existing_count > 0:
            logger.info(f"Players already seeded ({existing_count} found). Skipping.")
            return
        
        # Get all teams
        teams = {team.id: team for team in db.query(Team).all()}
        
        # Sample players data
        players_data = [
            {
                "id": "player001",
                "name": "Shohei Ohtani",
                "team_id": "lad",
                "position": "DH",
                "jersey_number": "17",
                "bats": "L",
                "throws": "R"
            },
            {
                "id": "player002",
                "name": "Mookie Betts",
                "team_id": "lad",
                "position": "RF",
                "jersey_number": "50",
                "bats": "R",
                "throws": "R"
            },
            {
                "id": "player003",
                "name": "Freddie Freeman",
                "team_id": "lad",
                "position": "1B",
                "jersey_number": "5",
                "bats": "L",
                "throws": "R"
            },
            {
                "id": "player004",
                "name": "Aaron Judge",
                "team_id": "nyy",
                "position": "RF",
                "jersey_number": "99",
                "bats": "R",
                "throws": "R"
            },
            {
                "id": "player005",
                "name": "Gerrit Cole",
                "team_id": "nyy",
                "position": "P",
                "jersey_number": "45",
                "bats": "R",
                "throws": "R"
            },
            {
                "id": "player006",
                "name": "Matt Chapman",
                "team_id": "sf",
                "position": "3B",
                "jersey_number": "26",
                "bats": "R",
                "throws": "R"
            },
            {
                "id": "player007",
                "name": "Rafael Devers",
                "team_id": "bos",
                "position": "3B",
                "jersey_number": "11",
                "bats": "L",
                "throws": "R"
            },
            {
                "id": "player008",
                "name": "Alex Verdugo",
                "team_id": "nyy",
                "position": "LF",
                "jersey_number": "24",
                "bats": "L",
                "throws": "L"
            },
            {
                "id": "player009",
                "name": "Yordan Alvarez",
                "team_id": "hou",
                "position": "DH",
                "jersey_number": "44",
                "bats": "L",
                "throws": "R"
            },
            {
                "id": "player010",
                "name": "Jose Altuve",
                "team_id": "hou",
                "position": "2B",
                "jersey_number": "27",
                "bats": "R",
                "throws": "R"
            },
            {
                "id": "player011",
                "name": "Corey Seager",
                "team_id": "tex",
                "position": "SS",
                "jersey_number": "5",
                "bats": "L",
                "throws": "R"
            },
            {
                "id": "player012",
                "name": "Marcus Semien",
                "team_id": "tex",
                "position": "2B",
                "jersey_number": "2",
                "bats": "R",
                "throws": "R"
            }
        ]
        
        # Create players
        for player_data in players_data:
            # Check if team exists
            team_id = player_data.get("team_id")
            if team_id not in teams:
                logger.warning(f"Team {team_id} not found for player {player_data.get('name')}. Skipping.")
                continue
            
            # Generate height and weight
            height = f"{random.randint(5, 6)}-{random.randint(0, 11)}"
            weight = random.randint(170, 250)
            
            # Create player
            player = Player(
                id=player_data["id"],
                name=player_data["name"],
                team_id=team_id,
                position=player_data["position"],
                jersey_number=player_data.get("jersey_number"),
                status="active",
                bats=player_data.get("bats", "R"),
                throws=player_data.get("throws", "R"),
                height=height,
                weight=weight
            )
            
            # Add statistics based on position
            if player.position == "P":
                player.era = round(random.uniform(2.50, 5.50), 2)
                player.wins = random.randint(0, 20)
                player.losses = random.randint(0, 15)
                player.saves = random.randint(0, 30) if random.random() < 0.2 else 0
                player.innings_pitched = round(random.uniform(0, 200), 1)
                player.strikeouts = random.randint(0, 300)
                player.walks = random.randint(0, 100)
                player.whip = round(random.uniform(1.00, 1.50), 2)
            else:
                player.batting_avg = round(random.uniform(0.200, 0.350), 3)
                player.obp = round(random.uniform(0.280, 0.420), 3)
                player.slg = round(random.uniform(0.350, 0.600), 3)
                player.ops = round(random.uniform(0.630, 1.020), 3)
                player.home_runs = random.randint(0, 50)
                player.rbi = random.randint(0, 120)
                player.hits = random.randint(0, 200)
                player.at_bats = random.randint(0, 600)
            
            db.add(player)
        
        db.commit()
        logger.info(f"Seeded {len(players_data)} players")
    
    def seed_games(self, db):
        """Seed baseball games"""
        logger.info("Seeding games data...")
        
        # Check if games already exist
        existing_count = db.query(Game).count()
        if existing_count > 0:
            logger.info(f"Games already seeded ({existing_count} found). Skipping.")
            return
        
        # Get all teams
        teams = {team.id: team for team in db.query(Team).all()}
        
        # Create some sample games for today and tomorrow
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)
        
        # Create games
        games_to_create = []
        
        # Today's games
        games_to_create.extend([
            Game(
                id=f"mlb-{today.strftime('%Y-%m-%d')}-lad-sf",
                sport_type="baseball",
                status="scheduled",
                start_time=datetime.combine(today, datetime.strptime("19:05", "%H:%M").time()),
                date=today.strftime("%Y-%m-%d"),
                home_team_id="sf",
                away_team_id="lad",
                stadium="Oracle Park",
                location="San Francisco, CA",
                temperature=68,
                weather_condition="Clear",
                wind_speed=12,
                wind_direction="Out to center"
            ),
            Game(
                id=f"mlb-{today.strftime('%Y-%m-%d')}-nyy-bos",
                sport_type="baseball",
                status="scheduled",
                start_time=datetime.combine(today, datetime.strptime("17:10", "%H:%M").time()),
                date=today.strftime("%Y-%m-%d"),
                home_team_id="bos",
                away_team_id="nyy",
                stadium="Fenway Park",
                location="Boston, MA",
                temperature=54,
                weather_condition="Partly Cloudy",
                wind_speed=8,
                wind_direction="In from right"
            ),
            Game(
                id=f"mlb-{today.strftime('%Y-%m-%d')}-hou-tex",
                sport_type="baseball",
                status="scheduled",
                start_time=datetime.combine(today, datetime.strptime("20:05", "%H:%M").time()),
                date=today.strftime("%Y-%m-%d"),
                home_team_id="tex",
                away_team_id="hou",
                stadium="Globe Life Field",
                location="Arlington, TX",
                temperature=72,
                weather_condition="Clear",
                wind_speed=0,
                wind_direction="None"
            )
        ])
        
        # Tomorrow's games
        games_to_create.extend([
            Game(
                id=f"mlb-{tomorrow.strftime('%Y-%m-%d')}-sf-lad",
                sport_type="baseball",
                status="scheduled",
                start_time=datetime.combine(tomorrow, datetime.strptime("19:10", "%H:%M").time()),
                date=tomorrow.strftime("%Y-%m-%d"),
                home_team_id="lad",
                away_team_id="sf",
                stadium="Dodger Stadium",
                location="Los Angeles, CA",
                temperature=72,
                weather_condition="Clear",
                wind_speed=5,
                wind_direction="Left to right"
            ),
            Game(
                id=f"mlb-{tomorrow.strftime('%Y-%m-%d')}-bos-nyy",
                sport_type="baseball",
                status="scheduled",
                start_time=datetime.combine(tomorrow, datetime.strptime("13:05", "%H:%M").time()),
                date=tomorrow.strftime("%Y-%m-%d"),
                home_team_id="nyy",
                away_team_id="bos",
                stadium="Yankee Stadium",
                location="New York, NY",
                temperature=58,
                weather_condition="Partly Cloudy",
                wind_speed=10,
                wind_direction="Out to right"
            )
        ])
        
        # Add all games
        for game in games_to_create:
            db.add(game)
        
        db.commit()
        logger.info(f"Seeded {len(games_to_create)} games")
    
    def seed_odds(self, db):
        """Seed betting odds for games"""
        logger.info("Seeding odds data...")
        
        # Check if odds already exist
        existing_count = db.query(GameOdds).count()
        if existing_count > 0:
            logger.info(f"Odds already seeded ({existing_count} found). Skipping.")
            return
        
        # Get all games
        games = db.query(Game).all()
        
        # Create odds for each game
        for game in games:
            # Create moneyline odds with home team favored more often
            home_favored = random.random() < 0.6
            if home_favored:
                home_moneyline = random.choice([-110, -120, -130, -140, -150, -160])
                away_moneyline = -home_moneyline + random.randint(-10, 10)
            else:
                away_moneyline = random.choice([-110, -120, -130, -140, -150, -160])
                home_moneyline = -away_moneyline + random.randint(-10, 10)
            
            # Create game odds
            odds = GameOdds(
                game_id=game.id,
                
                # Moneyline
                home_moneyline=home_moneyline,
                away_moneyline=away_moneyline,
                
                # Run line (spread)
                spread=1.5,
                home_spread_odds=random.choice([-110, -115, -120, -125, -130]),
                away_spread_odds=random.choice([-110, -115, -120, -125, -130]),
                
                # Total
                total_runs=random.choice([7.0, 7.5, 8.0, 8.5, 9.0, 9.5]),
                over_odds=random.choice([-110, -115, -120, -105, -100]),
                under_odds=random.choice([-110, -115, -120, -105, -100]),
                
                # Metadata
                bookmaker="Sample Sportsbook",
                last_updated=datetime.now()
            )
            db.add(odds)
            
            # Create prop bets for some players in this game
            self._create_prop_bets_for_game(db, game)
        
        db.commit()
        logger.info(f"Seeded odds for {len(games)} games")
    
    def _create_prop_bets_for_game(self, db, game):
        """Create prop bets for players in a game"""
        # Get players from home and away teams
        home_players = db.query(Player).filter_by(team_id=game.home_team_id).all()
        away_players = db.query(Player).filter_by(team_id=game.away_team_id).all()
        
        # Select players for prop bets
        players_for_props = []
        if home_players:
            players_for_props.extend(random.sample(home_players, min(3, len(home_players))))
        if away_players:
            players_for_props.extend(random.sample(away_players, min(3, len(away_players))))
        
        # Create prop bets
        for player in players_for_props:
            # Create different props based on position
            if player.position == "P":
                # Strikeout prop
                strikeout_line = 4.5 + random.uniform(0, 3)
                strikeout_prop = PropBet(
                    game_id=game.id,
                    player_id=player.id,
                    bet_type="strikeouts",
                    bet_description="Pitcher Strikeouts",
                    line=round(strikeout_line, 1),
                    over_odds=random.choice([-110, -115, -120, -125, -105]),
                    under_odds=random.choice([-110, -115, -120, -125, -105]),
                    bookmaker="Sample Sportsbook",
                    last_updated=datetime.now()
                )
                db.add(strikeout_prop)
            else:
                # Hits prop
                hits_prop = PropBet(
                    game_id=game.id,
                    player_id=player.id,
                    bet_type="hits",
                    bet_description="Player Hits",
                    line=1.5,
                    over_odds=random.choice([-110, -115, -120, -125, -105]),
                    under_odds=random.choice([-110, -115, -120, -125, -105]),
                    bookmaker="Sample Sportsbook",
                    last_updated=datetime.now()
                )
                db.add(hits_prop)
                
                # Home run prop (50% chance)
                if random.random() < 0.5:
                    hr_prop = PropBet(
                        game_id=game.id,
                        player_id=player.id,
                        bet_type="home_run",
                        bet_description="Player to Hit Home Run",
                        line=0.5,
                        over_odds=random.randint(250, 400),
                        under_odds=random.choice([-300, -350, -400, -450]),
                        bookmaker="Sample Sportsbook",
                        last_updated=datetime.now()
                    )
                    db.add(hr_prop)

def setup_database():
    """Create database tables if they don't exist"""
    from app.core.database import Base
    
    # Create engine
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}
    )
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Database seeding utility")
    parser.add_argument("--create-tables", action="store_true", help="Create database tables before seeding")
    
    args = parser.parse_args()
    
    if args.create_tables:
        setup_database()
    
    seeder = DataSeeder()
    seeder.seed_all()