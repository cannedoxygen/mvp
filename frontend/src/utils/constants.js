/**
 * Application-wide constants
 */

// Game types
export const GAME_TYPES = {
    BASEBALL: 'baseball',
    FOOTBALL: 'football',
    BASKETBALL: 'basketball',
  };
  
  // Game statuses
  export const GAME_STATUS = {
    SCHEDULED: 'scheduled',
    INPROGRESS: 'inProgress',
    FINAL: 'final',
    POSTPONED: 'postponed',
    CANCELED: 'canceled',
  };
  
  // Bet types
  export const BET_TYPES = {
    MONEYLINE: 'moneyline',
    SPREAD: 'spread',
    TOTAL: 'total',
    PROP: 'prop',
  };
  
  // Prop bet categories
  export const PROP_BET_TYPES = {
    STRIKEOUTS: 'strikeouts',
    HOME_RUNS: 'home_run',
    HITS: 'hits',
    RUNS_BATTED_IN: 'runs_batted_in',
    TOTAL_BASES: 'total_bases',
  };
  
  // Value ratings
  export const VALUE_RATINGS = {
    STRONG_VALUE: 'strong_value',
    VALUE: 'value',
    FAIR: 'fair',
    POOR: 'poor',
  };
  
  // API endpoints (for reference)
  export const API_ENDPOINTS = {
    GAMES: '/games',
    SIMULATIONS: '/simulations',
    ODDS: '/odds',
  };
  
  // Default simulation settings
  export const SIMULATION_DEFAULTS = {
    COUNT: 1000,
    MIN_CONFIDENCE: 0.55,
  };
  
  // Path to team logos
  export const TEAM_LOGO_PATH = '/images/logos/mlb';
  
  // Color scheme for teams (for visualizations)
  export const TEAM_COLORS = {
    // American League
    BAL: { primary: '#df4601', secondary: '#000000' }, // Baltimore Orioles
    BOS: { primary: '#bd3039', secondary: '#0c2340' }, // Boston Red Sox
    NYY: { primary: '#003087', secondary: '#e4002c' }, // New York Yankees
    TB: { primary: '#092c5c', secondary: '#8fbce6' },  // Tampa Bay Rays
    TOR: { primary: '#134a8e', secondary: '#e8291c' }, // Toronto Blue Jays
    CWS: { primary: '#27251f', secondary: '#c4ced4' }, // Chicago White Sox
    CLE: { primary: '#e31937', secondary: '#00385d' }, // Cleveland Guardians
    DET: { primary: '#0c2340', secondary: '#fa4616' }, // Detroit Tigers
    KC: { primary: '#004687', secondary: '#bd9b60' },  // Kansas City Royals
    MIN: { primary: '#002b5c', secondary: '#d31145' }, // Minnesota Twins
    HOU: { primary: '#002d62', secondary: '#eb6e1f' }, // Houston Astros
    LAA: { primary: '#ba0021', secondary: '#003263' }, // Los Angeles Angels
    OAK: { primary: '#003831', secondary: '#efb21e' }, // Oakland Athletics
    SEA: { primary: '#0c2c56', secondary: '#005c5c' }, // Seattle Mariners
    TEX: { primary: '#003278', secondary: '#c0111f' }, // Texas Rangers
    
    // National League
    ATL: { primary: '#ce1141', secondary: '#13274f' }, // Atlanta Braves
    MIA: { primary: '#00a3e0', secondary: '#ff6600' }, // Miami Marlins
    NYM: { primary: '#002d72', secondary: '#ff5910' }, // New York Mets
    PHI: { primary: '#e81828', secondary: '#002d72' }, // Philadelphia Phillies
    WSH: { primary: '#ab0003', secondary: '#14225a' }, // Washington Nationals
    CHC: { primary: '#0e3386', secondary: '#cc3433' }, // Chicago Cubs
    CIN: { primary: '#c6011f', secondary: '#000000' }, // Cincinnati Reds
    MIL: { primary: '#0a2351', secondary: '#b6922e' }, // Milwaukee Brewers
    PIT: { primary: '#27251f', secondary: '#fdb827' }, // Pittsburgh Pirates
    STL: { primary: '#c41e3a', secondary: '#0c2340' }, // St. Louis Cardinals
    ARI: { primary: '#a71930', secondary: '#e3d4ad' }, // Arizona Diamondbacks
    COL: { primary: '#33006f', secondary: '#c4ced4' }, // Colorado Rockies
    LAD: { primary: '#005a9c', secondary: '#e71d35' }, // Los Angeles Dodgers
    SD: { primary: '#2f241d', secondary: '#ffc425' },  // San Diego Padres
    SF: { primary: '#fd5a1e', secondary: '#27251f' },  // San Francisco Giants
  };