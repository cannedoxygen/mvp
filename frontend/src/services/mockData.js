/**
 * Mock data for development and testing
 * This provides static test data when not connected to the backend
 */

// Mock team data
export const teams = {
    LAD: {
      id: 'lad',
      name: 'Los Angeles Dodgers',
      abbreviation: 'LAD',
      league: 'NL',
      division: 'West'
    },
    SF: {
      id: 'sf',
      name: 'San Francisco Giants',
      abbreviation: 'SF',
      league: 'NL',
      division: 'West'
    },
    NYY: {
      id: 'nyy',
      name: 'New York Yankees',
      abbreviation: 'NYY',
      league: 'AL',
      division: 'East'
    },
    BOS: {
      id: 'bos',
      name: 'Boston Red Sox',
      abbreviation: 'BOS',
      league: 'AL',
      division: 'East'
    },
    HOU: {
      id: 'hou',
      name: 'Houston Astros',
      abbreviation: 'HOU',
      league: 'AL',
      division: 'West'
    },
    TEX: {
      id: 'tex',
      name: 'Texas Rangers',
      abbreviation: 'TEX',
      league: 'AL',
      division: 'West'
    }
  };
  
  // Mock games for today
  export const todaysGames = [
    {
      id: "mlb-2025-03-23-lad-sf",
      awayTeam: teams.LAD,
      homeTeam: teams.SF,
      startTime: "2025-03-23T19:05:00.000Z",
      stadium: "Oracle Park",
      status: "scheduled",
      simulationResults: {
        homeWinProbability: 0.42,
        awayWinProbability: 0.58,
        averageHomeScore: 3.2,
        averageAwayScore: 4.5,
        averageTotalRuns: 7.7,
        bettingInsight: "Value on LAD moneyline"
      }
    },
    {
      id: "mlb-2025-03-23-nyy-bos",
      awayTeam: teams.NYY,
      homeTeam: teams.BOS,
      startTime: "2025-03-23T17:10:00.000Z",
      stadium: "Fenway Park",
      status: "scheduled",
      simulationResults: null // No simulation yet
    },
    {
      id: "mlb-2025-03-23-hou-tex",
      awayTeam: teams.HOU,
      homeTeam: teams.TEX,
      startTime: "2025-03-23T20:05:00.000Z",
      stadium: "Globe Life Field",
      status: "scheduled",
      simulationResults: {
        homeWinProbability: 0.51,
        awayWinProbability: 0.49,
        averageHomeScore: 4.8,
        averageAwayScore: 4.6,
        averageTotalRuns: 9.4,
        bettingInsight: "Value on OVER 8.5 runs"
      }
    }
  ];
  
  // Mock game details
  export const gameDetails = {
    "mlb-2025-03-23-lad-sf": {
      id: "mlb-2025-03-23-lad-sf",
      awayTeam: teams.LAD,
      homeTeam: teams.SF,
      startTime: "2025-03-23T19:05:00.000Z",
      stadium: "Oracle Park",
      status: "scheduled",
      weather: {
        temperature: 68,
        condition: "Clear",
        windSpeed: 12,
        windDirection: "out to center",
        precipitation: 0,
        cloudCover: 15
      },
      bettingOdds: {
        homeTeam: "San Francisco Giants",
        awayTeam: "Los Angeles Dodgers",
        homeMoneyline: 160,
        awayMoneyline: -180,
        totalRuns: 8.5,
        overOdds: -110,
        underOdds: -110
      }
    },
    
    "mlb-2025-03-23-nyy-bos": {
      id: "mlb-2025-03-23-nyy-bos",
      awayTeam: teams.NYY,
      homeTeam: teams.BOS,
      startTime: "2025-03-23T17:10:00.000Z",
      stadium: "Fenway Park",
      status: "scheduled",
      weather: {
        temperature: 54,
        condition: "Partly Cloudy",
        windSpeed: 8,
        windDirection: "in from right",
        precipitation: 0,
        cloudCover: 40
      },
      bettingOdds: {
        homeTeam: "Boston Red Sox",
        awayTeam: "New York Yankees",
        homeMoneyline: 130,
        awayMoneyline: -150,
        totalRuns: 9,
        overOdds: -105,
        underOdds: -115
      }
    },
    
    "mlb-2025-03-23-hou-tex": {
      id: "mlb-2025-03-23-hou-tex",
      awayTeam: teams.HOU,
      homeTeam: teams.TEX,
      startTime: "2025-03-23T20:05:00.000Z",
      stadium: "Globe Life Field",
      status: "scheduled",
      weather: {
        temperature: 72,
        condition: "Clear",
        windSpeed: 0,
        windDirection: "none",
        precipitation: 0,
        cloudCover: 10,
        roofClosed: true
      },
      bettingOdds: {
        homeTeam: "Texas Rangers",
        awayTeam: "Houston Astros",
        homeMoneyline: -105,
        awayMoneyline: -115,
        totalRuns: 8.5,
        overOdds: -120,
        underOdds: 100
      }
    }
  };
  
  // Mock simulation results
  export const simulationResults = {
    "mlb-2025-03-23-lad-sf": {
      gameId: "mlb-2025-03-23-lad-sf",
      simulationCount: 10000,
      homeTeamName: "San Francisco Giants",
      awayTeamName: "Los Angeles Dodgers",
      homeWinProbability: 0.42,
      awayWinProbability: 0.58,
      averageHomeScore: 3.2,
      averageAwayScore: 4.5,
      averageTotalRuns: 7.7,
      bettingInsights: {
        homeMoneyline: -210,
        awayMoneyline: 175,
        overOdds: -135,
        underOdds: 115
      },
      propBetInsights: [
        {
          playerName: "Mookie Betts",
          betType: "home_run",
          line: 0.5,
          recommendation: "over",
          confidence: 0.72,
          reasoning: "Favorable wind conditions and strong recent power numbers"
        },
        {
          playerName: "Clayton Kershaw",
          betType: "strikeouts",
          line: 6.5,
          recommendation: "over",
          confidence: 0.68,
          reasoning: "Consistent K rate vs Giants lineup"
        },
        {
          playerName: "Shohei Ohtani",
          betType: "hits",
          line: 1.5,
          recommendation: "over",
          confidence: 0.77,
          reasoning: "Strong performance against right-handed pitching"
        }
      ],
      impactingFactors: [
        "Freddie Freeman mild back tightness (-10% hitting effectiveness)",
        "Giants' bullpen fatigue, Closer Camilo Doval out",
        "Strong winds blowing out (favor hitters)"
      ]
    },
    
    "mlb-2025-03-23-nyy-bos": {
      gameId: "mlb-2025-03-23-nyy-bos",
      simulationCount: 10000,
      homeTeamName: "Boston Red Sox",
      awayTeamName: "New York Yankees",
      homeWinProbability: 0.46,
      awayWinProbability: 0.54,
      averageHomeScore: 4.3,
      averageAwayScore: 4.8,
      averageTotalRuns: 9.1,
      bettingInsights: {
        homeMoneyline: 120,
        awayMoneyline: -140,
        overOdds: -125,
        underOdds: 105
      },
      propBetInsights: [
        {
          playerName: "Aaron Judge",
          betType: "home_run",
          line: 0.5,
          recommendation: "over",
          confidence: 0.65,
          reasoning: "Strong history at Fenway Park"
        },
        {
          playerName: "Gerrit Cole",
          betType: "strikeouts",
          line: 7.5,
          recommendation: "under",
          confidence: 0.71,
          reasoning: "Recently returning from injury, likely limited pitch count"
        }
      ],
      impactingFactors: [
        "Yankees starting 3rd string catcher (affects pitching)",
        "Rain expected in later innings",
        "Red Sox playing day game after night game (fatigue factor)"
      ]
    },
    
    "mlb-2025-03-23-hou-tex": {
      gameId: "mlb-2025-03-23-hou-tex",
      simulationCount: 10000,
      homeTeamName: "Texas Rangers",
      awayTeamName: "Houston Astros",
      homeWinProbability: 0.51,
      awayWinProbability: 0.49,
      averageHomeScore: 4.8,
      averageAwayScore: 4.6,
      averageTotalRuns: 9.4,
      bettingInsights: {
        homeMoneyline: -105,
        awayMoneyline: -115,
        overOdds: -145,
        underOdds: 125
      },
      propBetInsights: [
        {
          playerName: "Yordan Alvarez",
          betType: "total_bases",
          line: 1.5,
          recommendation: "over",
          confidence: 0.82,
          reasoning: "Excellent matchup vs Rangers starter"
        },
        {
          playerName: "Corey Seager",
          betType: "home_run",
          line: 0.5,
          recommendation: "over",
          confidence: 0.69,
          reasoning: "Power surge in last 10 games"
        },
        {
          playerName: "José Altuve",
          betType: "hits",
          line: 1.5,
          recommendation: "under",
          confidence: 0.61,
          reasoning: "Struggling against left-handed pitching recently"
        }
      ],
      impactingFactors: [
        "Globe Life Field roof closed (neutral conditions)",
        "Astros missing key bullpen arms due to workload",
        "Rangers lineup at full strength for first time in two weeks"
      ]
    }
  };