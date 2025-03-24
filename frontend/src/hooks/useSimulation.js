import { useMutation, useQuery, useQueryClient } from 'react-query';
import simulationService from '../services/simulationService';
import { SIMULATION_DEFAULTS } from '../utils/constants';

/**
 * Custom hook for managing game simulations
 * @param {string} gameId - ID of the game to simulate (optional)
 * @param {Object} options - Optional configuration
 * @param {number} options.simulationCount - Number of simulations to run
 * @param {boolean} options.autoRun - Whether to run simulation automatically
 * @returns {Object} - Simulation data and functions
 */
const useSimulation = (gameId = null, options = {}) => {
  const queryClient = useQueryClient();
  const { 
    simulationCount = SIMULATION_DEFAULTS.COUNT,
    autoRun = false 
  } = options;
  
  // Query for simulation results if gameId is provided
  const {
    data: simulationResults,
    isLoading: isLoadingResults,
    isError: isResultsError,
    error: resultsError,
    refetch: refetchResults
  } = useQuery(
    ['simulation', gameId],
    () => simulationService.runSimulation(gameId, { count: simulationCount }),
    {
      // Only run if gameId is provided and autoRun is true
      enabled: !!gameId && autoRun,
      // Don't refetch automatically
      refetchOnWindowFocus: false,
      staleTime: Infinity
    }
  );
  
  // Mutation for running simulation on demand
  const {
    mutate: runSimulation,
    isLoading: isRunningSimulation,
    error: simulationError,
    reset: resetSimulation
  } = useMutation(
    (id) => simulationService.runSimulation(id || gameId, { count: simulationCount }),
    {
      onSuccess: (data, id) => {
        // Update simulation results in cache
        queryClient.setQueryData(['simulation', id || gameId], data);
        
        // Update game data in cache if it exists
        queryClient.setQueryData(['game', id || gameId], (oldData) => {
          if (!oldData) return oldData;
          return { ...oldData, simulationResults: data };
        });
      }
    }
  );
  
  // Combined loading state
  const isLoading = isLoadingResults || isRunningSimulation;
  
  // Combined error state
  const error = resultsError || simulationError;
  const isError = isResultsError || !!simulationError;
  
  return {
    simulationResults,
    isLoading,
    isError,
    error,
    runSimulation,
    resetSimulation,
    refetchResults
  };
};

export default useSimulation;