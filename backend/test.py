# test_sportsdataio.py
import asyncio
import sys
import logging
from datetime import date

# Configure logging to see detailed output
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Import the client directly
sys.path.append(".")  # Add the current directory to the path
from app.clients.sportsdataio import SportsDataIOClient
from app.config import settings

async def test_get_games():
    """Test fetching games directly from the API"""
    logger.info("Starting API test")
    
    # Print API key status (don't print the actual key)
    api_key = settings.SPORTSDATAIO_API_KEY
    logger.info(f"API key status: {'AVAILABLE' if api_key else 'MISSING'}")
    
    # Create client
    client = SportsDataIOClient(api_key=api_key)
    
    # Try to fetch today's games
    today = date.today()
    logger.info(f"Fetching games for {today}")
    
    try:
        games = await client.get_games_by_date(today)
        
        if games:
            logger.info(f"Success! Found {len(games)} games for today")
            for i, game in enumerate(games):
                home_team = game.get("HomeTeam", "Unknown")
                away_team = game.get("AwayTeam", "Unknown")
                logger.info(f"Game {i+1}: {away_team} @ {home_team}")
        else:
            logger.warning(f"No games found for {today}")
            
            # Try tomorrow as a fallback
            tomorrow = date(today.year, today.month, today.day + 1)
            logger.info(f"Trying tomorrow: {tomorrow}")
            
            games = await client.get_games_by_date(tomorrow)
            if games:
                logger.info(f"Found {len(games)} games for tomorrow")
            else:
                logger.warning(f"No games found for tomorrow either")
                
                # Try a known MLB regular season month (e.g., July)
                test_date = date(today.year, 7, 15)
                logger.info(f"Trying test date: {test_date}")
                
                games = await client.get_games_by_date(test_date)
                if games:
                    logger.info(f"Found {len(games)} games for test date")
                else:
                    logger.error("Could not find any games for any date")
    
    except Exception as e:
        logger.error(f"Error during test: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())

# Run the test
if __name__ == "__main__":
    asyncio.run(test_get_games())