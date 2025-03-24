import React from 'react';
import { formatPercent, formatNumber } from '../../utils/formatters';

/**
 * SimulationResult component
 * Displays the core simulation results and predictions
 */
const SimulationResult = ({ results }) => {
  // Handle missing data
  if (!results) {
    return (
      <div className="text-center text-gray-500 py-4">
        No simulation results available
      </div>
    );
  }
  
  // Calculate home and away win percentages
  const homeWinPercent = formatPercent(results.homeWinProbability);
  const awayWinPercent = formatPercent(results.awayWinProbability);
  
  // Determine which team is favored
  const favoredTeam = results.homeWinProbability > results.awayWinProbability
    ? 'home'
    : 'away';
  
  // Format average scores
  const homeScore = formatNumber(results.averageHomeScore, 1);
  const awayScore = formatNumber(results.averageAwayScore, 1);
  const totalRuns = formatNumber(results.averageTotalRuns, 1);
  
  // Get team names 
  const homeTeamName = results.homeTeamName || 'Home Team';
  const awayTeamName = results.awayTeamName || 'Away Team';
  
  // Ensure we have a simulation count
  const simulationCount = results.simulationCount || 1000;
  
  return (
    <div>
      {/* Win probability display */}
      <div className="flex flex-col mb-6">
        <div className="text-sm text-gray-500 mb-2">
          Win Probability ({simulationCount.toLocaleString()} simulations)
        </div>
        
        {/* Win probability bar */}
        <div className="h-8 flex rounded-md overflow-hidden mb-2">
          <div 
            className="bg-blue-500 flex items-center justify-start pl-2"
            style={{ width: `${results.homeWinProbability * 100}%` }}
          >
            {results.homeWinProbability >= 0.15 && (
              <span className="text-white text-sm font-medium">
                {homeWinPercent}
              </span>
            )}
          </div>
          <div 
            className="bg-red-500 flex items-center justify-end pr-2"
            style={{ width: `${results.awayWinProbability * 100}%` }}
          >
            {results.awayWinProbability >= 0.15 && (
              <span className="text-white text-sm font-medium">
                {awayWinPercent}
              </span>
            )}
          </div>
        </div>
        
        {/* Team labels */}
        <div className="flex justify-between text-sm">
          <div>{homeTeamName}</div>
          <div>{awayTeamName}</div>
        </div>
      </div>
      
      {/* Projected score */}
      <div className="mb-6">
        <div className="text-sm text-gray-500 mb-2">Projected Score</div>
        <div className="flex justify-center items-center">
          <div className="text-center">
            <div className="text-xl font-bold">{homeScore}</div>
            <div className="text-sm">{homeTeamName}</div>
          </div>
          <div className="mx-4 text-gray-400">vs</div>
          <div className="text-center">
            <div className="text-xl font-bold">{awayScore}</div>
            <div className="text-sm">{awayTeamName}</div>
          </div>
        </div>
        <div className="text-center text-sm text-gray-500 mt-2">
          Projected Total: {totalRuns} runs
        </div>
      </div>
      
      {/* Confidence indicator */}
      <div className="rounded-md bg-gray-50 p-4 border border-gray-200">
        <div className="text-center font-medium">
          {favoredTeam === 'home' ? homeTeamName : awayTeamName} 
          <span className="text-gray-700"> projected to win with </span>
          {favoredTeam === 'home' ? homeWinPercent : awayWinPercent} confidence
        </div>
      </div>
    </div>
  );
};

export default SimulationResult;