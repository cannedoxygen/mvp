import api from './api';
import { formatApiError } from '../utils/errorUtils';

/**
 * Get betting odds for all of today's games
 * @returns {Promise<Array>} All games with odds
 */
export const getTodaysOdds = async () => {
  try {
    const response = await api.get('/odds/mlb/today');
    return response;
  } catch (error) {
    const formattedError = formatApiError(error);
    throw new Error(`Failed to fetch odds: ${formattedError.message}`);
  }
};

/**
 * Get betting odds for a specific game
 * @param {string} gameId - Game identifier
 * @returns {Promise<Object>} Game odds data
 */
export const getGameOdds = async (gameId) => {
  try {
    const response = await api.get(`/odds/mlb/games/${gameId}`);
    return response;
  } catch (error) {
    const formattedError = formatApiError(error);
    throw new Error(`Failed to fetch game odds: ${formattedError.message}`);
  }
};

/**
 * Get prop bet odds for a specific game
 * @param {string} gameId - Game identifier
 * @returns {Promise<Array>} Prop bet odds
 */
export const getGamePropBets = async (gameId) => {
  try {
    const response = await api.get(`/odds/mlb/games/${gameId}/props`);
    return response;
  } catch (error) {
    const formattedError = formatApiError(error);
    throw new Error(`Failed to fetch prop bets: ${formattedError.message}`);
  }
};

/**
 * Compare market odds to simulated odds to find value bets
 * @param {Object} marketOdds - Current market odds
 * @param {Object} simulatedOdds - Odds generated from simulation
 * @returns {Object} Value assessment
 */
export const analyzeBettingValue = (marketOdds, simulatedOdds) => {
  if (!marketOdds || !simulatedOdds) {
    return null;
  }
  
  // Convert odds to probabilities
  const marketProbs = {
    home: oddsToProb(marketOdds.homeMoneyline),
    away: oddsToProb(marketOdds.awayMoneyline),
    over: oddsToProb(marketOdds.overOdds),
    under: oddsToProb(marketOdds.underOdds)
  };
  
  const simulatedProbs = {
    home: oddsToProb(simulatedOdds.homeMoneyline),
    away: oddsToProb(simulatedOdds.awayMoneyline),
    over: oddsToProb(simulatedOdds.overOdds),
    under: oddsToProb(simulatedOdds.underOdds)
  };
  
  // Calculate edge (value)
  const edges = {
    home: simulatedProbs.home - marketProbs.home,
    away: simulatedProbs.away - marketProbs.away,
    over: simulatedProbs.over - marketProbs.over,
    under: simulatedProbs.under - marketProbs.under
  };
  
  // Analyze value and return assessment
  return {
    homeValue: determineValueType(edges.home),
    awayValue: determineValueType(edges.away),
    overValue: determineValueType(edges.over),
    underValue: determineValueType(edges.under),
    bestValue: findBestValue(edges)
  };
};

// Helper to convert American odds to probability
const oddsToProb = (americanOdds) => {
  if (americanOdds > 0) {
    return 100 / (americanOdds + 100);
  } else {
    return Math.abs(americanOdds) / (Math.abs(americanOdds) + 100);
  }
};

// Determine value type based on edge
const determineValueType = (edge) => {
  if (edge > 0.05) return 'strong_value';
  if (edge > 0.02) return 'value';
  if (edge < -0.05) return 'poor';
  if (edge < -0.02) return 'below';
  return 'fair';
};

// Find the best value bet
const findBestValue = (edges) => {
  const values = Object.entries(edges);
  values.sort((a, b) => b[1] - a[1]);
  
  const [bestType, bestEdge] = values[0];
  
  if (bestEdge <= 0.02) {
    return null;
  }
  
  const typeNames = {
    home: 'Home Moneyline',
    away: 'Away Moneyline',
    over: 'Over Total',
    under: 'Under Total'
  };
  
  return {
    type: bestType,
    typeName: typeNames[bestType],
    edge: bestEdge,
    valueType: determineValueType(bestEdge)
  };
};