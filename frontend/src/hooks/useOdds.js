import { useQuery } from 'react-query';
import { getTodaysOdds, getGameOdds, getGamePropBets, analyzeBettingValue } from '../services/oddsService';

/**
 * Custom hook for fetching and managing betting odds
 */
const useOdds = () => {
  // Fetch all odds for today's games
  const {
    data: allOdds,
    isLoading: isLoadingAllOdds,
    isError: isAllOddsError,
    error: allOddsError,
    refetch: refetchAllOdds
  } = useQuery(
    ['odds', 'today'],
    () => getTodaysOdds(),
    {
      staleTime: 5 * 60 * 1000, // 5 minutes
      refetchInterval: 15 * 60 * 1000, // 15 minutes
    }
  );
  
  // Function to fetch odds for a specific game
  const getOddsForGame = (gameId) => {
    return useQuery(
      ['odds', 'game', gameId],
      () => getGameOdds(gameId),
      {
        staleTime: 5 * 60 * 1000, // 5 minutes
        refetchInterval: 15 * 60 * 1000, // 15 minutes
        enabled: !!gameId
      }
    );
  };
  
  // Function to fetch prop bets for a specific game
  const getPropBetsForGame = (gameId) => {
    return useQuery(
      ['odds', 'props', gameId],
      () => getGamePropBets(gameId),
      {
        staleTime: 5 * 60 * 1000, // 5 minutes
        refetchInterval: 15 * 60 * 1000, // 15 minutes
        enabled: !!gameId
      }
    );
  };
  
  /**
   * Analyze odds value compared to simulation
   * @param {Object} marketOdds - Current market odds
   * @param {Object} simulatedOdds - Odds from simulation
   * @returns {Object} Value analysis
   */
  const analyzeValue = (marketOdds, simulatedOdds) => {
    return analyzeBettingValue(marketOdds, simulatedOdds);
  };
  
  return {
    allOdds,
    isLoadingAllOdds,
    isAllOddsError,
    allOddsError,
    refetchAllOdds,
    getOddsForGame,
    getPropBetsForGame,
    analyzeValue
  };
};

export default useOdds;