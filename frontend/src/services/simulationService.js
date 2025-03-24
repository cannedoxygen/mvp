import api from './api';
import { formatApiError } from '../utils/errorUtils';

/**
 * Service for baseball game simulations
 */
class SimulationService {
  /**
   * Run a simulation for a specific game
   * @param {string} gameId - ID of the game to simulate
   * @param {Object} options - Simulation options
   * @param {number} options.count - Number of simulations to run
   * @param {boolean} options.includeProps - Whether to include prop bet analysis
   * @returns {Promise<Object>} Simulation results
   */
  async runSimulation(gameId, options = {}) {
    try {
      const count = options.count || 1000;
      const includeProps = options.includeProps !== false;
      
      const response = await api.post(`/simulations/baseball/${gameId}`, {
        count,
        includeProps
      });
      
      return response;
    } catch (error) {
      const formattedError = formatApiError(error);
      throw new Error(`Failed to run simulation: ${formattedError.message}`);
    }
  }
  
  /**
   * Get simulation history for a game
   * @param {string} gameId - ID of the game
   * @param {number} limit - Maximum number of results to return
   * @returns {Promise<Array>} List of previous simulations
   */
  async getSimulationHistory(gameId, limit = 5) {
    try {
      const response = await api.get(`/simulations/baseball/${gameId}/history`, {
        params: { limit }
      });
      
      return response;
    } catch (error) {
      const formattedError = formatApiError(error);
      throw new Error(`Failed to get simulation history: ${formattedError.message}`);
    }
  }
  
  /**
   * Compare simulation results to market odds
   * @param {Object} simulation - Simulation results
   * @param {Object} marketOdds - Current market odds
   * @returns {Object} Value analysis
   */
  analyzeValue(simulation, marketOdds) {
    if (!simulation || !marketOdds) {
      return null;
    }
    
    // Extract simulated odds
    const simulatedOdds = simulation.bettingInsights;
    
    // Calculate value for each bet type
    const homeEdge = this._calculateEdge(
      marketOdds.homeMoneyline,
      simulatedOdds.homeMoneyline
    );
    
    const awayEdge = this._calculateEdge(
      marketOdds.awayMoneyline,
      simulatedOdds.awayMoneyline
    );
    
    const overEdge = this._calculateEdge(
      marketOdds.overOdds,
      simulatedOdds.overOdds
    );
    
    const underEdge = this._calculateEdge(
      marketOdds.underOdds,
      simulatedOdds.underOdds
    );
    
    return {
      home: {
        edge: homeEdge,
        rating: this._getValueRating(homeEdge)
      },
      away: {
        edge: awayEdge,
        rating: this._getValueRating(awayEdge)
      },
      over: {
        edge: overEdge,
        rating: this._getValueRating(overEdge)
      },
      under: {
        edge: underEdge,
        rating: this._getValueRating(underEdge)
      }
    };
  }
  
  /**
   * Calculate edge between market and simulated odds
   * @private
   */
  _calculateEdge(marketOdds, simulatedOdds) {
    // Convert to probabilities
    const marketProb = this._oddsToProb(marketOdds);
    const simulatedProb = this._oddsToProb(simulatedOdds);
    
    // Calculate edge
    return simulatedProb - marketProb;
  }
  
  /**
   * Convert American odds to probability
   * @private
   */
  _oddsToProb(americanOdds) {
    if (americanOdds > 0) {
      return 100 / (americanOdds + 100);
    } else {
      return Math.abs(americanOdds) / (Math.abs(americanOdds) + 100);
    }
  }
  
  /**
   * Get value rating based on edge
   * @private
   */
  _getValueRating(edge) {
    if (edge > 0.05) return 'strong';
    if (edge > 0.02) return 'value';
    if (edge < -0.05) return 'poor';
    if (edge < -0.02) return 'negative';
    return 'neutral';
  }
}

// Export a singleton instance
export default new SimulationService();