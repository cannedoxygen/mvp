import React from 'react';
import { CheckCircle, XCircle, AlertTriangle } from 'lucide-react';

/**
 * PropBetsList component
 * Displays player-specific prop bet recommendations
 */
const PropBetsList = ({ propBets }) => {
  // Skip rendering if no prop bets
  if (!propBets || propBets.length === 0) {
    return (
      <div className="text-center text-gray-500 py-4">
        No prop bet recommendations available for this game.
      </div>
    );
  }
  
  // Format confidence as percentage
  const formatConfidence = (confidence) => {
    return `${(confidence * 100).toFixed(0)}%`;
  };
  
  // Get confidence color class based on confidence level
  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.75) return 'text-green-600';
    if (confidence >= 0.6) return 'text-green-500';
    if (confidence >= 0.5) return 'text-blue-500';
    return 'text-gray-500';
  };
  
  // Get appropriate icon for recommendation
  const getRecommendationIcon = (recommendation) => {
    if (recommendation === 'over') {
      return <CheckCircle size={16} className="text-green-500" />;
    } else if (recommendation === 'under') {
      return <XCircle size={16} className="text-red-500" />;
    }
    return <AlertTriangle size={16} className="text-amber-500" />;
  };
  
  // Format bet type for display
  const formatBetType = (betType) => {
    // Handle different API response formats
    const type = typeof betType === 'string' ? betType : betType?.name || 'unknown';
    
    // Map to readable format
    switch (type.toLowerCase()) {
      case 'strikeouts':
        return 'Strikeouts';
      case 'home_run':
      case 'home_runs':
        return 'Home Run';
      case 'hits':
        return 'Hits';
      case 'runs_batted_in':
      case 'rbi':
        return 'RBIs';
      case 'total_bases':
        return 'Total Bases';
      default:
        // Try to make it look nice if it's unknown
        return type.split('_').map(word => 
          word.charAt(0).toUpperCase() + word.slice(1)
        ).join(' ');
    }
  };
  
  // Group prop bets by type for better organization
  const groupedPropBets = propBets.reduce((groups, bet) => {
    // Handle different API response formats
    const betType = typeof bet.betType === 'string' 
      ? bet.betType 
      : bet.betType?.name || 'unknown';
    
    if (!groups[betType]) {
      groups[betType] = [];
    }
    groups[betType].push(bet);
    return groups;
  }, {});
  
  return (
    <div>
      <p className="text-sm text-gray-600 mb-4">
        Player prop bets with highest value based on recent performance and matchup analysis.
      </p>
      
      {/* Display each type of prop bet */}
      {Object.entries(groupedPropBets).map(([betType, bets]) => (
        <div key={betType} className="mb-6">
          <h3 className="font-medium mb-2 capitalize">{formatBetType(betType)}</h3>
          
          <div className="space-y-3">
            {bets.map((bet, index) => (
              <div 
                key={`${bet.playerName}-${betType}-${index}`} 
                className="flex items-center justify-between pb-2 border-b border-gray-100"
              >
                <div className="flex items-center">
                  <span className="font-medium text-gray-800">{bet.playerName}</span>
                  <span className="mx-2 text-gray-500">·</span>
                  <span className="text-sm text-gray-600">
                    {formatBetType(betType)}
                    {' '}
                    {bet.line && `${bet.recommendation.toUpperCase()} ${bet.line}`}
                    {!bet.line && bet.recommendation.toUpperCase()}
                  </span>
                </div>
                
                <div className="flex items-center space-x-4">
                  {/* Confidence indicator */}
                  <div className={`text-sm font-medium ${getConfidenceColor(bet.confidence)}`}>
                    {formatConfidence(bet.confidence)} confidence
                  </div>
                  
                  {/* Recommendation icon */}
                  <div className="flex items-center">
                    {getRecommendationIcon(bet.recommendation)}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
};

export default PropBetsList;