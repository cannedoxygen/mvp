import React, { useState } from 'react';
import { useQuery } from 'react-query';
import GameCard from '../../components/baseball/GameCard';
import Loader from '../../components/common/Loader';
import ErrorMessage from '../../components/common/ErrorMessage';
import { formatDate } from '../../utils/dateUtils';
import useGames from '../../hooks/useGames';

/**
 * Baseball games index page
 * Shows today's MLB matchups and allows running simulations
 */
const BaseballIndex = () => {
  const [selectedDate, setSelectedDate] = useState(new Date());
  
  // Use our custom hook to fetch games
  const { 
    games, 
    isLoading, 
    isError, 
    error, 
    runSimulation, 
    isSimulating 
  } = useGames(selectedDate);

  // Format date for display
  const formattedDate = formatDate(selectedDate, 'long');

  return (
    <div>
      {/* Page header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">MLB Game Predictions</h1>
        <p className="text-gray-600 mt-2">
          AI-powered analysis and betting insights for today's baseball matchups
        </p>
      </div>

      {/* Date display */}
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-medium text-gray-800">{formattedDate}</h2>
      </div>

      {/* Loading state */}
      {isLoading && (
        <div className="text-center py-12">
          <Loader text="Loading today's games..." />
        </div>
      )}

      {/* Error state */}
      {isError && (
        <ErrorMessage 
          message={error?.message || "Unable to load games. Please try again later."} 
          type="error" 
        />
      )}

      {/* No games scheduled */}
      {games?.length === 0 && !isLoading && !isError && (
        <div className="text-center py-12">
          <p className="text-gray-600">No games scheduled for today.</p>
        </div>
      )}

      {/* Games list */}
      {games?.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {games.map(game => (
            <GameCard 
              key={game.id}
              gameId={game.id}
              awayTeam={game.awayTeam}
              homeTeam={game.homeTeam}
              startTime={game.startTime}
              stadium={game.stadium}
              simulationResults={game.simulationResults}
              onRunSimulation={() => runSimulation(game.id)}
              isSimulating={isSimulating}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default BaseballIndex;