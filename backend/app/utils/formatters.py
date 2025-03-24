# backend/app/utils/formatters.py
from datetime import datetime
from typing import Dict, Any, List, Optional, Union
import json

def format_date(date_obj: Union[datetime, str], format_str: str = "%Y-%m-%d") -> str:
    """
    Format a date object or string to a specified format
    
    Args:
        date_obj: The date to format (datetime object or string)
        format_str: The format string to use
        
    Returns:
        Formatted date string
    """
    if isinstance(date_obj, str):
        # Try to parse the string as a date first
        try:
            date_obj = datetime.fromisoformat(date_obj.replace('Z', '+00:00'))
        except ValueError:
            # Return as is if parsing fails
            return date_obj
    
    # Format the datetime object
    return date_obj.strftime(format_str)

def format_currency(amount: float, currency: str = "USD", decimal_places: int = 2) -> str:
    """
    Format a monetary amount
    
    Args:
        amount: The amount to format
        currency: The currency code
        decimal_places: Number of decimal places to show
        
    Returns:
        Formatted currency string
    """
    if currency == "USD":
        return f"${amount:.{decimal_places}f}"
    else:
        return f"{amount:.{decimal_places}f} {currency}"

def format_percentage(value: float, decimal_places: int = 1) -> str:
    """
    Format a value as a percentage
    
    Args:
        value: The value to format (0-1)
        decimal_places: Number of decimal places to show
        
    Returns:
        Formatted percentage string
    """
    return f"{value * 100:.{decimal_places}f}%"

def format_american_odds(decimal_odds: float) -> int:
    """
    Convert decimal odds to American format
    
    Args:
        decimal_odds: Odds in decimal format (e.g., 1.91)
        
    Returns:
        Odds in American format (e.g., -110)
    """
    if decimal_odds >= 2.0:
        # Underdog (positive odds)
        return round((decimal_odds - 1) * 100)
    else:
        # Favorite (negative odds)
        return round(-100 / (decimal_odds - 1))

def format_decimal_odds(american_odds: int) -> float:
    """
    Convert American odds to decimal format
    
    Args:
        american_odds: Odds in American format (e.g., -110)
        
    Returns:
        Odds in decimal format (e.g., 1.91)
    """
    if american_odds > 0:
        return 1 + (american_odds / 100)
    else:
        return 1 + (100 / abs(american_odds))

def format_json_response(data: Any, pretty: bool = False) -> str:
    """
    Format data as a JSON string
    
    Args:
        data: The data to format
        pretty: Whether to pretty-print the JSON
        
    Returns:
        JSON string
    """
    if pretty:
        return json.dumps(data, indent=2, sort_keys=True)
    else:
        return json.dumps(data)