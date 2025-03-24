# Baseball Betting Simulator

An AI-powered baseball betting simulator that provides data-driven predictions and betting insights based on Monte Carlo simulations.

## Features

- Daily MLB matchups and analysis
- AI-generated game predictions and betting odds comparison
- Player prop bet recommendations
- Key impacting factors (injuries, weather, etc.)

## Tech Stack

- **Frontend**: React, Tailwind CSS
- **Backend**: Python (FastAPI)
- **AI Integration**: OpenAI GPT-4
- **Data Sources**: SportsDataIO API, The Odds API

## Getting Started

### Prerequisites

- Node.js (v16+)
- Python (v3.9+)
- Docker and Docker Compose (optional)

### Quick Start with Docker

1. Clone the repository
git clone https://github.com/yourusername/baseball-betting-simulator.git
cd baseball-betting-simulator
Copy
2. Create environment files
cp .env.example .env
Copy
3. Start the application using Docker Compose
docker-compose -f infra/docker-compose.yml up -d
Copy
4. Access the application at http://localhost:3000

### Manual Setup

#### Frontend
1. Navigate to frontend directory and install dependencies
cd frontend
npm install
Copy
2. Start the development server
npm run dev
Copy
#### Backend
1. Navigate to backend directory
cd backend
Copy
2. Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Copy
3. Install dependencies
pip install -r requirements.txt
Copy
4. Set up the database
python scripts/db_setup.py
python scripts/seed_data.py
Copy
5. Start the server
uvicorn app.main --reload
Copy
## Project Structure

- `/frontend` - React application
- `/backend` - FastAPI application
- `/infra` - Docker and deployment configurations
- `/data` - Data storage directories
- `/docs` - Documentation

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This application is for entertainment purposes only. The predictions and insights provided should not be used for actual gambling.