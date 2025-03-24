# Baseball Betting Simulator - Backend

## Overview
Python-based FastAPI backend for the Baseball Betting Simulator, providing data-driven game predictions and betting insights.

## Technology Stack
- Python 3.9+
- FastAPI
- SQLAlchemy
- Alembic (Database Migrations)
- OpenAI GPT Integration

## Key Features
- MLB Game Predictions
- Monte Carlo Simulation Engine
- Betting Odds Analysis
- Player Prop Bet Recommendations
- External API Integrations

## Setup Instructions
1. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Set up database
```bash
python scripts/db_setup.py
python scripts/seed_data.py
```

4. Run the application
```bash
uvicorn app.main:app --reload
```

## Environment Variables
- `DATABASE_URL`: Database connection string
- `SPORTSDATAIO_API_KEY`: Sports data API key
- `ODDS_API_KEY`: Betting odds API key
- `OPENAI_API_KEY`: OpenAI API key

## Testing
```bash
pytest
```

## License
MIT License