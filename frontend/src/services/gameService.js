// frontend/src/services/gameService.js
import api from './api';
import { formatApiError } from '../utils/errorUtils';
import { API_CONFIG } from '../utils/config';

// Use mock data in development if enabled
const useMockData = API_CONFIG.useMockData;

// Import mock data if using it
let mockGames = null;
let mockGameDetails = null;
if (useMockData) {
  import('./mockData').then(module => {
    mockGames = module.todaysGames;
    mockGameDetails = module.gameDetails;
  });
}

/**
 * Fetch today's baseball games
 * @returns {Promise<Array>} List of games with basic information
 */
export const fetchTodaysGames = async () => {
  try {
    // Use mock data if enabled
    if (useMockData && mockGames) {
      return mockGames;
    }
    
    // Otherwise use real API
    const response = await api.get('/games/baseball/today');
    return response;
  } catch (error) {
    const formattedError = formatApiError(error);
    console.error('Failed to fetch today\'s games:', formattedError.message);
    throw new Error(`Failed to fetch today's games: ${formattedError.message}`);
  }
};

/**
 * Fetch games for a specific date
 * @param {Date} date - Date to fetch games for
 * @returns {Promise<Array>} List of games for the specified date
 */
export const fetchGamesByDate = async (date) => {
  try {
    // Format date as YYYY-MM-DD
    const dateStr = date.toISOString().split('T')[0];
    
    // Use mock data if enabled (with some filtering to simulate different dates)
    if (useMockData && mockGames) {
      // For mock data, just return a subset based on date to simulate different days
      const dayOfMonth = date.getDate();
      return mockGames.filter((_, index) => index % 30 === dayOfMonth % 30);
    }
    
    // Otherwise use real API
    const response = await api.get(`/games/baseball/date/${dateStr}`);
    return response;
  } catch (error) {
    const formattedError = formatApiError(error);
    console.error('Failed to fetch games by date:', formattedError.message);
    throw new Error(`Failed to fetch games by date: ${formattedError.message}`);
  }
};

/**
 * Fetch detailed game information
 * @param {string} gameId - Unique identifier for the game
 * @returns {Promise<Object>} Detailed game information
 */
export const fetchGameDetails = async (gameId) => {
  try {
    // Use mock data if enabled
    if (useMockData && mockGameDetails && mockGameDetails[gameId]) {
      return mockGameDetails[gameId];
    }
    
    // Otherwise use real API
    const response = await api.get(`/games/baseball/${gameId}`);
    return response;
  } catch (error) {
    const formattedError = formatApiError(error);
    console.error('Failed to fetch game details:', formattedError.message);
    throw new Error(`Failed to fetch game details: ${formattedError.message}`);
  }
};

/**
 * Run a game simulation
 * @param {string} gameId - Unique identifier for the game
 * @param {Object} options - Additional options for the simulation
 * @param {number} options.count - Number of simulations to run
 * @returns {Promise<Object>} Simulation results
 */
export const runGameSimulation = async (gameId, options = {}) => {
  try {
    // Default options
    const simulationOptions = {
      count: options.count || 1000,
    };
    
    // Use mock data if enabled
    if (useMockData && mockGameDetails && mockGameDetails[gameId]) {
      // Simulate a delay to mimic API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Return mock simulation results based on the game
      return {
        gameId: gameId,
        simulationCount: simulationOptions.count,
        homeTeamName: mockGameDetails[gameId].homeTeam.name,
        awayTeamName: mockGameDetails[gameId].awayTeam.name,
        homeWinProbability: 0.55 + (Math.random() * 0.3 - 0.15),
        awayWinProbability: 0.45 + (Math.random() * 0.3 - 0.15),
        averageHomeScore: 3.5 + (Math.random() * 2),
        averageAwayScore: 3.2 + (Math.random() * 2),
        averageTotalRuns: 6.7 + (Math.random() * 3),
        bettingInsights: {
          homeMoneyline: -160,
          awayMoneyline: 140,
          overOdds: -110,
          underOdds: -110
        },
        propBetInsights: _generateMockPropBets(
          mockGameDetails[gameId].homeTeam.name,
          mockGameDetails[gameId].awayTeam.name
        ),
        impactingFactors: [
          "Weather conditions favor pitchers",
          "Home team bullpen is well-rested",
          "Away team is on final game of road trip"
        ]
      };
    }
    
    // Otherwise use real API
    const response = await api.post(`/simulations/baseball/${gameId}`, simulationOptions);
    return response;
  } catch (error) {
    const formattedError = formatApiError(error);
    console.error('Failed to run simulation:', formattedError.message);
    throw new Error(`Failed to run simulation: ${formattedError.message}`);
  }
};

/**
 * Fetch betting odds for a game
 * @param {string} gameId - Unique identifier for the game
 * @returns {Promise<Object>} Betting odds information
 */
export const fetchGameOdds = async (gameId) => {
  try {
    // Use mock data if enabled
    if (useMockData && mockGameDetails && mockGameDetails[gameId]) {
      return mockGameDetails[gameId].bettingOdds;
    }
    
    // Otherwise use real API
    const response = await api.get(`/games/baseball/odds/${gameId}`);
    return response;
  } catch (error) {
    const formattedError = formatApiError(error);
    console.error('Failed to fetch game odds:', formattedError.message);
    throw new Error(`Failed to fetch game odds: ${formattedError.message}`);
  }
};

/**
 * Fetch player prop bets for a game
 * @param {string} gameId - Unique identifier for the game
 * @returns {Promise<Array>} List of player prop bets
 */
export const fetchPlayerProps = async (gameId) => {
  try {
    // Use mock data if enabled
    if (useMockData && mockGameDetails && mockGameDetails[gameId]) {
      // Generate some mock props
      return _generateMockPropBets(
        mockGameDetails[gameId].homeTeam.name,
        mockGameDetails[gameId].awayTeam.name
      );
    }
    
    // Otherwise use real API
    const response = await api.get(`/games/baseball/props/${gameId}`);
    return response;
  } catch (error) {
    const formattedError = formatApiError(error);
    console.error('Failed to fetch player props:', formattedError.message);
    throw new Error(`Failed to fetch player props: ${formattedError.message}`);
  }
};

/**
 * Generate mock prop bets for testing
 * @private
 */
function _generateMockPropBets(homeTeam, awayTeam) {
  const propTypes = ['strikeouts', 'home_run', 'hits', 'runs_batted_in', 'total_bases'];
  const players = [
    { name: "Player 1", team: homeTeam },
    { name: "Player 2", team: homeTeam },
    { name: "Player 3", team: awayTeam },
    { name: "Player 4", team: awayTeam }
  ];
  
  const props = [];
  
  players.forEach(player => {
    // Add 1-2 random prop types for each player
    const propsToAdd = Math.floor(Math.random() * 2) + 1;
    
    for (let i = 0; i < propsToAdd; i++) {
      const propType = propTypes[Math.floor(Math.random() * propTypes.length)];
      const line = propType === 'strikeouts' ? 
        (4.5 + Math.random() * 3) : 
        (propType === 'home_run' ? 0.5 : (1.5 + Math.random()));
      
      const overConfidence = 0.4 + Math.random() * 0.4;
      const rec = overConfidence > 0.6 ? 'over' : 
                 overConfidence < 0.4 ? 'under' : 
                 (Math.random() > 0.5 ? 'over' : 'under');
      
      props.push({
        playerName: player.name,
        betType: propType,
        line: parseFloat(line.toFixed(1)),
        recommendation: rec,
        confidence: rec === 'over' ? overConfidence : (1 - overConfidence),
        reasoning: `Based on matchup and recent performance trends`
      });
    }
  });
  
  // Sort by confidence
  props.sort((a, b) => b.confidence - a.confidence);
  
  return props;
}