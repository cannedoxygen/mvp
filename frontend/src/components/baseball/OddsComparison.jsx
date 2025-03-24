import React from 'react';
import { ArrowUpRight, ArrowDownRight, Minus } from 'lucide-react';

/**
 * OddsComparison component
 * Compares market betting odds with simulated odds to identify value bets
 */
const OddsComparison = ({ marketOdds, simulatedOdds }) => {
  // Skip rendering if odds are missing
  if (!marketOdds || !simulatedOdds) {
    return (
      <div className="text-center text-gray-500 py-4">
        Odds data not available
      </div>
    );
  }
  
  // Helper function to convert American odds to implied probability
  const oddsToProb = (americanOdds) => {
    if (americanOdds > 0) {
      return (100 / (americanOdds + 100)).toFixed(3);
    } else {
      return (Math.abs(americanOdds) / (Math.abs(americanOdds) + 100)).toFixed(3);
    }
  };
  
  // Helper to format American odds with + or - sign
  const formatAmericanOdds = (odds) => {
    return odds > 0 ? `+${odds}` : odds;
  };
  
  // Helper to determine value indicator
  const getValueIndicator = (marketOdds, simulatedOdds) => {
    const marketProb = oddsToProb(marketOdds);
    const simulatedProb = oddsToProb(simulatedOdds);
    const difference = (simulatedProb - marketProb).toFixed(3);
    
    if (difference > 0.05) {
      return {
        text: 'Strong Value',
        icon: <ArrowUpRight size={16} className="text-green-600" />,
        color: 'text-green-600'
      };
    } else if (difference > 0.02) {
      return {
        text: 'Value',
        icon: <ArrowUpRight size={16} className="text-green-500" />,
        color: 'text-green-500'
      };
    } else if (difference < -0.05) {
      return {
        text: 'Poor Value',
        icon: <ArrowDownRight size={16} className="text-red-600" />,
        color: 'text-red-600'
      };
    } else if (difference < -0.02) {
      return {
        text: 'Below Value',
        icon: <ArrowDownRight size={16} className="text-red-500" />,
        color: 'text-red-500'
      };
    } else {
      return {
        text: 'Fair Value',
        icon: <Minus size={16} className="text-gray-500" />,
        color: 'text-gray-500'
      };
    }
  };
  
  // Extract team names from odds or use placeholders
  const homeTeamName = marketOdds.homeTeam || 'Home Team';
  const awayTeamName = marketOdds.awayTeam || 'Away Team';
  
  // Get value indicators for each bet type
  const homeMoneylineValue = getValueIndicator(marketOdds.homeMoneyline, simulatedOdds.homeMoneyline);
  const awayMoneylineValue = getValueIndicator(marketOdds.awayMoneyline, simulatedOdds.awayMoneyline);
  const overValue = getValueIndicator(marketOdds.overOdds, simulatedOdds.overOdds);
  const underValue = getValueIndicator(marketOdds.underOdds, simulatedOdds.underOdds);
  
  return (
    <div>
      <p className="text-sm text-gray-600 mb-4">
        This analysis compares market odds with simulated probabilities to identify potential betting value.
      </p>
      
      {/* Moneyline comparison */}
      <div className="mb-6">
        <h3 className="font-medium mb-2">Moneyline</h3>
        <div className="space-y-3">
          {/* Home team */}
          <div className="flex items-center justify-between pb-2 border-b border-gray-100">
            <div>
              <span className="text-sm text-gray-800">{homeTeamName}</span>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-sm text-gray-600">
                <span>Market: </span>
                <span className="font-medium">{formatAmericanOdds(marketOdds.homeMoneyline)}</span>
              </div>
              <div className="text-sm text-gray-600">
                <span>Simulated: </span>
                <span className="font-medium">{formatAmericanOdds(simulatedOdds.homeMoneyline)}</span>
              </div>
              <div className={`flex items-center text-sm font-medium ${homeMoneylineValue.color}`}>
                {homeMoneylineValue.icon}
                <span className="ml-1">{homeMoneylineValue.text}</span>
              </div>
            </div>
          </div>
          
          {/* Away team */}
          <div className="flex items-center justify-between pb-2 border-b border-gray-100">
            <div>
              <span className="text-sm text-gray-800">{awayTeamName}</span>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-sm text-gray-600">
                <span>Market: </span>
                <span className="font-medium">{formatAmericanOdds(marketOdds.awayMoneyline)}</span>
              </div>
              <div className="text-sm text-gray-600">
                <span>Simulated: </span>
                <span className="font-medium">{formatAmericanOdds(simulatedOdds.awayMoneyline)}</span>
              </div>
              <div className={`flex items-center text-sm font-medium ${awayMoneylineValue.color}`}>
                {awayMoneylineValue.icon}
                <span className="ml-1">{awayMoneylineValue.text}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      {/* Totals comparison */}
      <div>
        <h3 className="font-medium mb-2">Total Runs (Over/Under {marketOdds.totalRuns})</h3>
        <div className="space-y-3">
          {/* Over */}
          <div className="flex items-center justify-between pb-2 border-b border-gray-100">
            <div>
              <span className="text-sm text-gray-800">Over</span>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-sm text-gray-600">
                <span>Market: </span>
                <span className="font-medium">{formatAmericanOdds(marketOdds.overOdds)}</span>
              </div>
              <div className="text-sm text-gray-600">
                <span>Simulated: </span>
                <span className="font-medium">{formatAmericanOdds(simulatedOdds.overOdds)}</span>
              </div>
              <div className={`flex items-center text-sm font-medium ${overValue.color}`}>
                {overValue.icon}
                <span className="ml-1">{overValue.text}</span>
              </div>
            </div>
          </div>
          
          {/* Under */}
          <div className="flex items-center justify-between pb-2 border-b border-gray-100">
            <div>
              <span className="text-sm text-gray-800">Under</span>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-sm text-gray-600">
                <span>Market: </span>
                <span className="font-medium">{formatAmericanOdds(marketOdds.underOdds)}</span>
              </div>
              <div className="text-sm text-gray-600">
                <span>Simulated: </span>
                <span className="font-medium">{formatAmericanOdds(simulatedOdds.underOdds)}</span>
              </div>
              <div className={`flex items-center text-sm font-medium ${underValue.color}`}>
                {underValue.icon}
                <span className="ml-1">{underValue.text}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default OddsComparison;