/**
 * Utility functions for betting odds calculations and formatting
 */

/**
 * Convert American odds to implied probability
 * @param {number} americanOdds - Odds in American format (e.g., -150, +130)
 * @returns {number} - Implied probability as decimal (0-1)
 */
export const americanToImpliedProbability = (americanOdds) => {
    if (americanOdds > 0) {
      return 100 / (americanOdds + 100);
    } else {
      return Math.abs(americanOdds) / (Math.abs(americanOdds) + 100);
    }
  };
  
  /**
   * Convert implied probability to American odds
   * @param {number} probability - Decimal probability (0-1)
   * @returns {number} - Odds in American format (rounded to nearest 5)
   */
  export const impliedProbabilityToAmerican = (probability) => {
    if (probability <= 0 || probability >= 1) {
      throw new Error('Probability must be between 0 and 1');
    }
    
    let odds;
    if (probability > 0.5) {
      odds = -100 * probability / (1 - probability);
    } else {
      odds = 100 * (1 - probability) / probability;
    }
    
    // Round to nearest 5 for conventional formatting
    return Math.round(odds / 5) * 5;
  };
  
  /**
   * Format American odds with + or - sign
   * @param {number} odds - Odds in American format
   * @returns {string} - Formatted odds string
   */
  export const formatAmericanOdds = (odds) => {
    return odds > 0 ? `+${odds}` : `${odds}`;
  };
  
  /**
   * Calculate expected value of a bet
   * @param {number} americanOdds - Odds in American format
   * @param {number} impliedProbability - True probability as decimal (0-1)
   * @returns {number} - Expected value (positive means +EV bet)
   */
  export const calculateExpectedValue = (americanOdds, impliedProbability) => {
    const decimalOdds = americanToDecimalOdds(americanOdds);
    return ((decimalOdds - 1) * impliedProbability) - (1 - impliedProbability);
  };
  
  /**
   * Convert American odds to decimal odds
   * @param {number} americanOdds - Odds in American format
   * @returns {number} - Odds in decimal format
   */
  export const americanToDecimalOdds = (americanOdds) => {
    if (americanOdds > 0) {
      return 1 + (americanOdds / 100);
    } else {
      return 1 + (100 / Math.abs(americanOdds));
    }
  };
  
  /**
   * Calculate Kelly criterion stake size
   * @param {number} probability - True probability as decimal (0-1)
   * @param {number} americanOdds - Odds in American format
   * @returns {number} - Optimal stake as fraction of bankroll (0-1)
   */
  export const calculateKellyStake = (probability, americanOdds) => {
    const decimalOdds = americanToDecimalOdds(americanOdds);
    const q = 1 - probability;
    
    // Kelly formula: (bp - q) / b where b = decimal odds - 1
    const b = decimalOdds - 1;
    const stake = (b * probability - q) / b;
    
    // Kelly can sometimes recommend negative stakes; cap at 0
    return Math.max(0, stake);
  };