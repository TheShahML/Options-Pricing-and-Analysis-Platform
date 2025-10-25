# formatters.py

"""
Formatters

Utility functions for formatting numbers, dates, and financial data.
"""

from typing import Optional


def format_currency(value: Optional[float], decimals: int = 2) -> str:
    """
    Format number as currency.
    
    Args:
        value: Number to format
        decimals: Number of decimal places
        
    Returns:
        Formatted currency string
    """
    if value is None:
        return "N/A"
    return f"${value:,.{decimals}f}"


def format_percentage(value: Optional[float], decimals: int = 2) -> str:
    """
    Format number as percentage.
    
    Args:
        value: Number to format (0.05 = 5%)
        decimals: Number of decimal places
        
    Returns:
        Formatted percentage string
    """
    if value is None:
        return "N/A"
    return f"{value * 100:.{decimals}f}%"


def format_large_number(value: Optional[float]) -> str:
    """
    Format large numbers with K, M, B, T suffixes.
    
    Args:
        value: Number to format
        
    Returns:
        Formatted number string
    """
    if value is None:
        return "N/A"
    
    if abs(value) >= 1e12:
        return f"${value / 1e12:.2f}T"
    elif abs(value) >= 1e9:
        return f"${value / 1e9:.2f}B"
    elif abs(value) >= 1e6:
        return f"${value / 1e6:.2f}M"
    elif abs(value) >= 1e3:
        return f"${value / 1e3:.2f}K"
    else:
        return f"${value:,.2f}"


def format_volume(value: Optional[int]) -> str:
    """
    Format trading volume.
    
    Args:
        value: Volume to format
        
    Returns:
        Formatted volume string
    """
    if value is None:
        return "N/A"
    return f"{value:,}"


def format_greek(value: Optional[float], decimals: int = 4) -> str:
    """
    Format Greek value.
    
    Args:
        value: Greek value to format
        decimals: Number of decimal places
        
    Returns:
        Formatted Greek string
    """
    if value is None:
        return "N/A"
    return f"{value:.{decimals}f}"