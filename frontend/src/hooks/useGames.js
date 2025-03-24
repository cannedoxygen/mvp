import { useQuery, useMutation, useQueryClient } from 'react-query';
import { fetchTodaysGames, runGameSimulation } from '../services/gameService';

/**
 * Custom hook for fetching and managing game data
 * @param {Date} date - The date to fetch games for (defaults to today)
 * @returns {Object} - Game data and functions for managing it
 */
const useGames = (date = new Date()) => {
  const queryClient = useQueryClient();
  
  // Fetch games for the selected date
  const {
    data: games,
    isLoading,
    isError,
    error,
    refetch
  } = useQuery(
    ['games', date.toISOString().split('T')[0]],
    () => fetchTodaysGames(date),
    {
      staleTime: 5 * 60 * 1000, // 5 minutes
      refetchInterval: 10 * 60 * 1000, // Refresh every 10 minutes
    }
  );
  
  // Mutation for running simulation on a game
  const simulationMutation = useMutation(
    (gameId) => runGameSimulation(gameId),
    {
      onSuccess: (simulationResults, gameId) => {
        // Update the game in the cache with simulation results
        queryClient.setQueryData(
          ['games', date.toISOString().split('T')[0]],
          (oldData) => {
            if (!oldData) return oldData;
            
            return oldData.map(game => 
              game.id === gameId 
                ? { ...game, simulationResults } 
                : game
            );
          }
        );
        
        // Also update the individual game query if it exists
        queryClient.setQueryData(
          ['game', gameId],
          (oldData) => oldData ? { ...oldData, simulationResults } : oldData
        );
      }
    }
  );
  
  // Run simulation for a specific game
  const runSimulation = (gameId) => {
    return simulationMutation.mutate(gameId);
  };
  
  return {
    games,
    isLoading,
    isError,
    error,
    refetch,
    runSimulation,
    isSimulating: simulationMutation.isLoading,
    simulationError: simulationMutation.error
  };
};

export default useGames;