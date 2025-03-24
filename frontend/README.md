# Baseball Betting Simulator - Frontend

This is the React frontend for the Baseball Betting Simulator application.

## Features

- View today's MLB games
- Run Monte Carlo simulations for game predictions
- Compare market odds to simulation results
- View prop bet recommendations
- Analyze key factors impacting games

## Tech Stack

- React 18
- React Router
- React Query
- Tailwind CSS
- Vite

## Getting Started

### Prerequisites

- Node.js 16+
- npm or yarn

### Installation

1. Install dependencies:
npm install
Copy
2. Configure environment:
cp .env.example .env
Copy
3. Start development server:
npm run dev
Copy
4. Access the application at http://localhost:3000

## Build for Production
npm run build
Copy
The build files will be in the `dist` directory.

## Project Structure

- `/src` - Main source code
  - `/components` - Reusable React components
  - `/pages` - Top-level page components
  - `/services` - API and data services
  - `/utils` - Utility functions
  - `/hooks` - Custom React hooks
  - `/context` - React context providers
  - `/styles` - CSS and styling files

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build locally
- `npm run lint` - Run ESLint

## Environment Variables

Key environment variables include:

- `VITE_API_BASE_URL` - Backend API URL
- `VITE_ENABLE_MOCK_DATA` - Use mock data for development
- `VITE_SIMULATION_COUNT` - Number of simulations to run