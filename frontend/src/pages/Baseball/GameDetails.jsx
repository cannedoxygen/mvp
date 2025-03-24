import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { useQuery } from 'react-query';
import { ArrowLeft } from 'lucide-react';

// Import our custom hooks
import useSimulation from '../../hooks/useSimulation';
import { formatGameDateTime } from '../../utils/dateUtils';

// Components
import SimulationResult from '../../components/baseball/SimulationResult';
import OddsComparison from '../../components/baseball/OddsComparison';
import PropBetsList from '../../components/baseball/PropBetsList';
import ImpactingFactors from '../../components/baseball/ImpactingFactors';
import Loader from '../../components/common/Loader';
import ErrorMessage from '../../components/common/ErrorMessage';
import Button from '../../components/common/Button';

// API functions
import { fetchGameDetails } from '../../services/gameService';
import { getGameOdds } from '../../services/oddsService';

/**
 * Game details page showing in-depth analysis for a specific game
 */
const GameDetails = () => {
  const { gameId } = useParams();
  
  // Fetch game details
  const { 
    data: game, 
    isLoading: isLoadingGame, 
    error: gameError 
  } = useQuery(['game', gameId], () => fetchGameDetails(gameId));
  
  // Fetch game odds
  const {
    data: odds,
    isLoading: isLoadingOdds,
    error: oddsError
  } = useQuery(['odds', gameId], () => getGameOdds(gameId), {
    enabled: !!game
  });

  // Use our simulation hook
  const {
    simulationResults,
    isLoading: isSimulating,
    error: simulationError,
    runSimulation
  } = useSimulation(gameId, { autoRun: false });
  
  // Determine if we have any loading or error states
  const isLoading = isLoadingGame || isLoadingOdds;
  const error = gameError || oddsError || simulationError;

  return (
    <div>
      {/* Back link */}
      <Link to="/baseball" className="inline-flex items-center text-primary-600 hover:text-primary-700 mb-6">
        <ArrowLeft size={16} className="mr-1" />
        <span>Back to all games</span>
      </Link>
      
      {/* Loading state */}
      {isLoading && (
        <div className="text-center py-12">
          <Loader text="Loading game details..." />
        </div>
      )}
      
      {/* Error state */}
      {error && (
        <ErrorMessage
          message="Unable to load game details. Please try again later."
          type="error"
        />
      )}
      
      {/* Game content */}
      {game && (
        <div>
          {/* Game header */}
          <div className="mb-8">
            <h1 className="text-2xl font-bold text-gray-900 mb-2">
              {game.awayTeam.name} @ {game.homeTeam.name}
            </h1>
            <p className="text-gray-600">
              {formatGameDateTime(game.startTime)} • {game.stadium}
            </p>
          </div>
          
          {/* Main content grid */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Main simulation column */}
            <div className="lg:col-span-2">
              {/* Simulation results */}
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 mb-6">
                <h2 className="text-lg font-medium p-4 border-b border-gray-200">
                  Simulation Results
                </h2>
                <div className="p-4">
                  {isSimulating ? (
                    <div className="text-center py-4">
                      <Loader text="Running simulation..." size="sm" />
                    </div>
                  ) : simulationResults ? (
                    <SimulationResult results={simulationResults} />
                  ) : (
                    <div className="text-center py-4">
                      <Button 
                        variant="primary" 
                        onClick={() => runSimulation(gameId)}
                      >
                        Run Simulation
                      </Button>
                    </div>
                  )}
                </div>
              </div>
              
              {/* Betting odds comparison */}
              {simulationResults && odds && (
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 mb-6">
                  <h2 className="text-lg font-medium p-4 border-b border-gray-200">
                    Betting Odds Analysis
                  </h2>
                  <div className="p-4">
                    <OddsComparison 
                      marketOdds={odds} 
                      simulatedOdds={simulationResults.bettingInsights} 
                    />
                  </div>
                </div>
              )}
              
              {/* Player prop bets */}
              {simulationResults && simulationResults.propBetInsights && (
                <div className="bg-white rounded-lg shadow-sm border border-gray-200">
                  <h2 className="text-lg font-medium p-4 border-b border-gray-200">
                    Player Prop Bet Recommendations
                  </h2>
                  <div className="p-4">
                    <PropBetsList propBets={simulationResults.propBetInsights} />
                  </div>
                </div>
              )}
            </div>
            
            {/* Sidebar */}
            <div className="lg:col-span-1">
              {/* Impacting factors */}
              {simulationResults && simulationResults.impactingFactors && (
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 mb-6">
                  <h2 className="text-lg font-medium p-4 border-b border-gray-200">
                    Key Factors
                  </h2>
                  <div className="p-4">
                    <ImpactingFactors factors={simulationResults.impactingFactors} />
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default GameDetails;