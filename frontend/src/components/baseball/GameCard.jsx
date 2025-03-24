import React from 'react';
import { Link } from 'react-router-dom';
import { ChevronRight } from 'lucide-react';
import { formatGameTime } from '../../utils/dateUtils';
import Button from '../common/Button';

/**
 * GameCard component for displaying baseball game matchup information
 * and a summary of simulation results
 */
const GameCard = ({ 
  gameId, 
  awayTeam, 
  homeTeam, 
  startTime, 
  stadium, 
  simulationResults,
  onRunSimulation,
  isSimulating = false
}) => {
  // Format the game time
  const formattedTime = formatGameTime(startTime);
  
  // Determine winner and confidence based on simulation results
  const getWinnerInfo = () => {
    if (!simulationResults) return { winner: null, confidence: 0 };
    
    const homeWinProb = simulationResults.homeWinProbability * 100;
    const awayWinProb = simulationResults.awayWinProbability * 100;
    
    if (homeWinProb > awayWinProb) {
      return { 
        winner: 'home',
        teamName: homeTeam.name,
        confidence: homeWinProb.toFixed(0)
      };
    } else {
      return { 
        winner: 'away',
        teamName: awayTeam.name,
        confidence: awayWinProb.toFixed(0)
      };
    }
  };
  
  const { winner, teamName, confidence } = getWinnerInfo();
  
  return (
    <div className="bg-white border border-gray-200 rounded-lg shadow-sm overflow-hidden">
      {/* Game info header */}
      <div className="p-4 border-b border-gray-200">
        <div className="text-sm text-gray-500 mb-2">{formattedTime} • {stadium}</div>
        
        {/* Team matchup */}
        <div className="flex justify-between items-center">
          <div className="text-center">
            <div className="font-bold text-lg">{awayTeam.abbreviation}</div>
            <div className="text-sm">{awayTeam.name}</div>
          </div>
          
          <div className="text-gray-500 font-bold">@</div>
          
          <div className="text-center">
            <div className="font-bold text-lg">{homeTeam.abbreviation}</div>
            <div className="text-sm">{homeTeam.name}</div>
          </div>
        </div>
      </div>
      
      {/* Simulation results */}
      <div className="p-4">
        {simulationResults ? (
          <div>
            <div className="mb-3">
              <div className="text-sm text-gray-500 mb-1">Prediction</div>
              <div className="font-medium">
                {teamName} Win ({confidence}% confidence)
              </div>
              <div className="text-sm text-gray-600">
                Projected: {simulationResults.averageHomeScore.toFixed(1)} - {simulationResults.averageAwayScore.toFixed(1)}
              </div>
            </div>
            
            {simulationResults.bettingInsights && (
              <div className="text-sm">
                <span className="text-betting-value font-medium">
                  {simulationResults.bettingInsight}
                </span>
              </div>
            )}
          </div>
        ) : (
          <div className="text-center py-2">
            <Button 
              variant="link" 
              onClick={onRunSimulation}
              disabled={isSimulating}
            >
              {isSimulating ? 'Running Simulation...' : 'Run Simulation'}
            </Button>
          </div>
        )}
      </div>
      
      {/* View details link */}
      <Link 
        to={`/baseball/${gameId}`} 
        className="block bg-gray-50 px-4 py-3 text-sm font-medium text-primary-600 hover:bg-gray-100 transition-colors border-t border-gray-200"
      >
        <div className="flex justify-between items-center">
          <span>View detailed analysis</span>
          <ChevronRight size={16} />
        </div>
      </Link>
    </div>
  );
};

export default GameCard;