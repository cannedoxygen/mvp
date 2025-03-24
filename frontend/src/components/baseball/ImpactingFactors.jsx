import React from 'react';
import { AlertTriangle, Thermometer, Wind, Users, Gauge } from 'lucide-react';

/**
 * ImpactingFactors component
 * Displays key factors affecting the game prediction
 */
const ImpactingFactors = ({ factors }) => {
  // Handle missing or empty factors
  if (!factors || factors.length === 0) {
    return (
      <div className="text-center text-gray-500 py-4">
        No significant factors identified for this game.
      </div>
    );
  }
  
  // Helper function to get appropriate icon for factor type
  const getFactorIcon = (factor) => {
    const factorText = factor.toLowerCase();
    
    if (factorText.includes('weather') || 
        factorText.includes('temperature') || 
        factorText.includes('cold') || 
        factorText.includes('hot')) {
      return <Thermometer size={18} className="text-gray-500" />;
    }
    
    if (factorText.includes('wind')) {
      return <Wind size={18} className="text-gray-500" />;
    }
    
    if (factorText.includes('injury') || 
        factorText.includes('lineup') || 
        factorText.includes('player')) {
      return <Users size={18} className="text-gray-500" />;
    }
    
    if (factorText.includes('fatigue') || 
        factorText.includes('bullpen') || 
        factorText.includes('stamina')) {
      return <Gauge size={18} className="text-gray-500" />;
    }
    
    return <AlertTriangle size={18} className="text-gray-500" />;
  };
  
  // Helper to determine if factor is positive, negative or neutral for betting
  const getFactorImpact = (factor) => {
    const factorText = factor.toLowerCase();
    // Look for indicators in the factor text
    if (factor.includes('+') || 
        factorText.includes('favor') || 
        factorText.includes('advantage') ||
        factorText.includes('strength')) {
      return 'text-green-600';
    }
    
    if (factor.includes('-') || 
        factorText.includes('against') || 
        factorText.includes('disadvantage') ||
        factorText.includes('out') ||
        factorText.includes('injury')) {
      return 'text-red-600';
    }
    
    return 'text-gray-800';
  };
  
  return (
    <div>
      <p className="text-sm text-gray-600 mb-4">
        Key factors that could impact game outcomes and betting value.
      </p>
      
      <ul className="space-y-4">
        {factors.map((factor, index) => (
          <li 
            key={index} 
            className="flex items-start space-x-3 pb-3 border-b border-gray-100 last:border-0"
          >
            <div className="mt-0.5">
              {getFactorIcon(factor)}
            </div>
            <p className={`text-sm ${getFactorImpact(factor)}`}>
              {factor}
            </p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ImpactingFactors;