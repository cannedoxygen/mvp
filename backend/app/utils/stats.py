# backend/app/utils/stats.py
import numpy as np
from typing import List, Dict, Any, Tuple, Optional

def calculate_average(values: List[float]) -> float:
    """
    Calculate the average of a list of values
    
    Args:
        values: List of numeric values
        
    Returns:
        Average value
    """
    if not values:
        return 0.0
    return sum(values) / len(values)

def calculate_median(values: List[float]) -> float:
    """
    Calculate the median of a list of values
    
    Args:
        values: List of numeric values
        
    Returns:
        Median value
    """
    if not values:
        return 0.0
    sorted_values = sorted(values)
    n = len(sorted_values)
    if n % 2 == 0:
        return (sorted_values[n//2 - 1] + sorted_values[n//2]) / 2
    else:
        return sorted_values[n//2]

def calculate_standard_deviation(values: List[float]) -> float:
    """
    Calculate the standard deviation of a list of values
    
    Args:
        values: List of numeric values
        
    Returns:
        Standard deviation
    """
    if not values or len(values) < 2:
        return 0.0
    return np.std(values, ddof=1)

def calculate_win_probability(home_score: float, away_score: float, 
                              home_variance: float, away_variance: float,
                              simulations: int = 10000) -> Tuple[float, float]:
    """
    Calculate win probability using Monte Carlo simulation
    
    Args:
        home_score: Expected home team score
        away_score: Expected away team score
        home_variance: Variance in home team score
        away_variance: Variance in away team score
        simulations: Number of simulations to run
        
    Returns:
        Tuple of (home_win_probability, away_win_probability)
    """
    # Generate random scores based on normal distribution
    home_scores = np.random.normal(home_score, np.sqrt(home_variance), simulations)
    away_scores = np.random.normal(away_score, np.sqrt(away_variance), simulations)
    
    # Count wins
    home_wins = np.sum(home_scores > away_scores)
    
    # Handle ties (50/50 split)
    ties = np.sum(home_scores == away_scores)
    home_wins += ties / 2
    
    # Calculate probabilities
    home_win_probability = home_wins / simulations
    away_win_probability = 1 - home_win_probability
    
    return home_win_probability, away_win_probability

def calculate_over_under_probability(total_score: float, line: float, 
                                    variance: float, simulations: int = 10000) -> Tuple[float, float]:
    """
    Calculate over/under probability using Monte Carlo simulation
    
    Args:
        total_score: Expected total score
        line: Over/under line
        variance: Variance in total score
        simulations: Number of simulations to run
        
    Returns:
        Tuple of (over_probability, under_probability)
    """
    # Generate random total scores based on normal distribution
    total_scores = np.random.normal(total_score, np.sqrt(variance), simulations)
    
    # Count overs
    overs = np.sum(total_scores > line)
    
    # Handle pushes (refund scenario)
    pushes = np.sum(total_scores == line)
    total_non_push = simulations - pushes
    
    # Calculate probabilities
    over_probability = overs / total_non_push if total_non_push > 0 else 0.5
    under_probability = 1 - over_probability
    
    return over_probability, under_probability

def calculate_expected_value(probability: float, odds: int) -> float:
    """
    Calculate the expected value of a bet
    
    Args:
        probability: Probability of winning (0-1)
        odds: American odds (e.g., -110, +120)
        
    Returns:
        Expected value per dollar wagered
    """
    if odds > 0:
        return probability * (odds / 100) - (1 - probability)
    else:
        return probability * (100 / abs(odds)) - (1 - probability)