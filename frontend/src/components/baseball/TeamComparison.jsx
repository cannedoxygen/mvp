import React from 'react';

/**
 * TeamComparison component
 * Displays a side-by-side comparison of two baseball teams
 */
const TeamComparison = ({ homeTeam, awayTeam, className = '' }) => {
  // Skip rendering if team data is missing
  if (!homeTeam || !awayTeam) {
    return (
      <div className="text-center text-gray-500 py-4">
        Team data not available
      </div>
    );
  }
  
  // Comparison categories and stats
  const categories = [
    {
      name: 'Batting',
      stats: [
        { label: 'Avg', home: homeTeam.batting?.average, away: awayTeam.batting?.average, precision: 3 },
        { label: 'OBP', home: homeTeam.batting?.obp, away: awayTeam.batting?.obp, precision: 3 },
        { label: 'SLG', home: homeTeam.batting?.slugging, away: awayTeam.batting?.slugging, precision: 3 },
        { label: 'HR', home: homeTeam.batting?.homeRuns, away: awayTeam.batting?.homeRuns, precision: 0 },
        { label: 'Runs/G', home: homeTeam.batting?.runsPerGame, away: awayTeam.batting?.runsPerGame, precision: 1 }
      ]
    },
    {
      name: 'Pitching',
      stats: [
        { label: 'ERA', home: homeTeam.pitching?.era, away: awayTeam.pitching?.era, precision: 2 },
        { label: 'WHIP', home: homeTeam.pitching?.whip, away: awayTeam.pitching?.whip, precision: 2 },
        { label: 'K/9', home: homeTeam.pitching?.strikeoutsPerNine, away: awayTeam.pitching?.strikeoutsPerNine, precision: 1 },
        { label: 'BB/9', home: homeTeam.pitching?.walksPerNine, away: awayTeam.pitching?.walksPerNine, precision: 1 },
        { label: 'HR/9', home: homeTeam.pitching?.homeRunsPerNine, away: awayTeam.pitching?.homeRunsPerNine, precision: 1 }
      ]
    },
    {
      name: 'Other',
      stats: [
        { label: 'Record', home: homeTeam.record, away: awayTeam.record, isText: true },
        { label: 'Last 10', home: homeTeam.last10, away: awayTeam.last10, isText: true },
        { label: 'Home/Away', home: homeTeam.homeRecord, away: awayTeam.awayRecord, isText: true }
      ]
    }
  ];
  
  // Format a numeric stat with proper precision
  const formatStat = (value, precision = 1, isText = false) => {
    if (isText) return value || '-';
    if (value === undefined || value === null) return '-';
    return parseFloat(value).toFixed(precision);
  };
  
  // Determine which value is better
  const getBetterValue = (stat, homeValue, awayValue) => {
    // Skip if either value is missing
    if (homeValue === '-' || awayValue === '-') return null;
    
    // For most stats, higher is better
    let homeBetter = parseFloat(homeValue) > parseFloat(awayValue);
    
    // For ERA, WHIP, BB/9, HR/9, lower is better
    if (['ERA', 'WHIP', 'BB/9', 'HR/9'].includes(stat)) {
      homeBetter = !homeBetter;
    }
    
    return homeBetter ? 'home' : 'away';
  };
  
  return (
    <div className={className}>
      <div className="mb-4 flex items-center justify-between">
        <div className="text-center flex-1">
          <span className="text-lg font-medium text-gray-900">
            {awayTeam.name}
          </span>
        </div>
        <div className="text-center flex-1">
          <span className="px-3 text-sm text-gray-500 uppercase">vs</span>
        </div>
        <div className="text-center flex-1">
          <span className="text-lg font-medium text-gray-900">
            {homeTeam.name}
          </span>
        </div>
      </div>
      
      {/* Categories */}
      {categories.map((category, categoryIndex) => (
        <div key={categoryIndex} className="mb-4">
          <h4 className="text-sm font-medium text-gray-700 mb-2">{category.name}</h4>
          
          <div className="border rounded-lg overflow-hidden">
            {category.stats.map((stat, statIndex) => {
              const formattedHome = formatStat(stat.home, stat.precision, stat.isText);
              const formattedAway = formatStat(stat.away, stat.precision, stat.isText);
              const better = !stat.isText ? getBetterValue(stat.label, formattedHome, formattedAway) : null;
              
              return (
                <div 
                  key={statIndex} 
                  className={`flex items-center ${statIndex !== category.stats.length - 1 ? 'border-b' : ''}`}
                >
                  {/* Away value */}
                  <div className={`flex-1 py-2 px-3 text-center ${better === 'away' ? 'font-medium text-primary-600' : ''}`}>
                    {formattedAway}
                  </div>
                  
                  {/* Stat label */}
                  <div className="flex-1 py-2 px-3 text-center bg-gray-50 text-sm text-gray-500">
                    {stat.label}
                  </div>
                  
                  {/* Home value */}
                  <div className={`flex-1 py-2 px-3 text-center ${better === 'home' ? 'font-medium text-primary-600' : ''}`}>
                    {formattedHome}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      ))}
    </div>
  );
};

export default TeamComparison;