# input_validation.py

"""
Validation Utilities

Helper functions for validating option pricing inputs.
"""

from datetime import datetime, timedelta
from typing import Tuple


class ValidationError(Exception):
    """Custom validation error."""
    pass


def validate_option_inputs(S: float, K: float, T: float, r: float, sigma: float) -> Tuple[bool, str]:
    """
    Validate option pricing inputs.
    
    Args:
        S: Current stock price
        K: Strike price
        T: Time to expiration (years)
        r: Risk-free rate
        sigma: Volatility
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if S <= 0:
        return False, "Stock price must be positive"
    
    if K <= 0:
        return False, "Strike price must be positive"
    
    if T < 0:
        return False, "Time to expiration cannot be negative"
    
    if T > 10:
        return False, "Time to expiration too large (max 10 years)"
    
    if r < 0 or r > 1:
        return False, "Risk-free rate must be between 0 and 1 (0% to 100%)"
    
    if sigma <= 0:
        return False, "Volatility must be positive"
    
    if sigma > 5:
        return False, "Volatility too high (max 500%)"
    
    return True, ""


def validate_ticker(ticker: str) -> Tuple[bool, str]:
    """
    Validate ticker symbol format.
    
    Args:
        ticker: Stock ticker symbol
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not ticker:
        return False, "Ticker cannot be empty"
    
    ticker = ticker.strip().upper()
    
    if len(ticker) > 10:
        return False, "Ticker too long (max 10 characters)"
    
    if not ticker.replace('.', '').replace('-', '').isalnum():
        return False, "Ticker contains invalid characters"
    
    return True, ""


def calculate_time_to_expiration(expiration_date: str) -> float:
    """
    Calculate time to expiration in years from date string.
    
    Args:
        expiration_date: Date in YYYY-MM-DD format
        
    Returns:
        Time to expiration in years
        
    Raises:
        ValidationError: If date format is invalid
    """
    try:
        exp_date = datetime.strptime(expiration_date, "%Y-%m-%d")
        today = datetime.now()
        
        if exp_date < today:
            raise ValidationError("Expiration date is in the past")
        
        days_to_expiration = (exp_date - today).days
        years_to_expiration = days_to_expiration / 365.0
        
        return years_to_expiration
        
    except ValueError:
        raise ValidationError("Invalid date format. Use YYYY-MM-DD")


def validate_date_format(date_string: str) -> Tuple[bool, str]:
    """
    Validate date string format.
    
    Args:
        date_string: Date string to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True, ""
    except ValueError:
        return False, "Invalid date format. Use YYYY-MM-DD"


def round_to_trading_precision(value: float, precision: int = 2) -> float:
    """
    Round value to standard trading precision.
    
    Args:
        value: Value to round
        precision: Number of decimal places
        
    Returns:
        Rounded value
    """
    return round(value, precision)


def check_arbitrage_bounds(option_price: float, S: float, K: float, 
                          option_type: str, T: float, r: float) -> Tuple[bool, str]:
    """
    Check if option price violates arbitrage bounds.
    
    Args:
        option_price: Calculated option price
        S: Stock price
        K: Strike price
        option_type: "call" or "put"
        T: Time to expiration
        r: Risk-free rate
        
    Returns:
        Tuple of (is_valid, warning_message)
    """
    import math
    
    if option_type.lower() == "call":
        # Call lower bound: max(0, S - K*e^(-rT))
        lower_bound = max(0, S - K * math.exp(-r * T))
        # Call upper bound: S
        upper_bound = S
        
        if option_price < lower_bound - 0.01:  # Small tolerance
            return False, f"Call price below arbitrage lower bound ({lower_bound:.2f})"
        if option_price > upper_bound:
            return False, f"Call price above arbitrage upper bound ({upper_bound:.2f})"
            
    else:  # put
        # Put lower bound: max(0, K*e^(-rT) - S)
        lower_bound = max(0, K * math.exp(-r * T) - S)
        # Put upper bound: K*e^(-rT)
        upper_bound = K * math.exp(-r * T)
        
        if option_price < lower_bound - 0.01:
            return False, f"Put price below arbitrage lower bound ({lower_bound:.2f})"
        if option_price > upper_bound:
            return False, f"Put price above arbitrage upper bound ({upper_bound:.2f})"
    
    return True, ""