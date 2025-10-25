# risk_free_rate.py

"""
Risk-Free Rate Service

This module fetches current Treasury rates to use as risk-free rate in pricing.
"""

import yfinance as yf
from typing import Optional


class RiskFreeRateService:
    """Service for fetching risk-free interest rates."""
    
    # Treasury ETF tickers as proxies for different maturities
    TREASURY_TICKERS = {
        "1M": "^IRX",    # 13-week Treasury Bill
        "3M": "^IRX",    # 13-week Treasury Bill
        "1Y": "^IRX",    # 13-week Treasury Bill
        "5Y": "^FVX",    # 5-year Treasury
        "10Y": "^TNX",   # 10-year Treasury Note
        "30Y": "^TYX",   # 30-year Treasury Bond
    }
    
    @staticmethod
    def get_treasury_rate(maturity: str = "10Y") -> Optional[float]:
        """
        Get current Treasury rate for specified maturity.
        
        Args:
            maturity: Maturity period ("1M", "3M", "1Y", "5Y", "10Y", "30Y")
            
        Returns:
            Annual rate as decimal (e.g., 0.045 for 4.5%) or None
        """
        try:
            ticker = RiskFreeRateService.TREASURY_TICKERS.get(maturity, "^TNX")
            treasury = yf.Ticker(ticker)
            data = treasury.history(period="5d")
            
            if not data.empty:
                # Treasury yield is already in percentage, convert to decimal
                rate = float(data['Close'].iloc[-1]) / 100
                return rate
            return None
        except Exception as e:
            print(f"Error fetching Treasury rate for {maturity}: {e}")
            return None
    
    @staticmethod
    def get_risk_free_rate_for_maturity(time_to_expiration_years: float) -> float:
        """
        Get appropriate risk-free rate based on option time to expiration.
        
        Args:
            time_to_expiration_years: Time to expiration in years
            
        Returns:
            Risk-free rate as decimal, defaults to 0.045 (4.5%) if fetch fails
        """
        # Default fallback rate
        default_rate = 0.030
        
        try:
            # Map time to expiration to appropriate Treasury maturity
            if time_to_expiration_years <= 0.25:  # <= 3 months
                rate = RiskFreeRateService.get_treasury_rate("3M")
            elif time_to_expiration_years <= 1.0:  # <= 1 year
                rate = RiskFreeRateService.get_treasury_rate("1Y")
            elif time_to_expiration_years <= 5.0:  # <= 5 years
                rate = RiskFreeRateService.get_treasury_rate("5Y")
            else:  # > 5 years
                rate = RiskFreeRateService.get_treasury_rate("10Y")
            
            return rate if rate is not None else default_rate
        except:
            return default_rate
    
    @staticmethod
    def get_all_rates() -> dict:
        """
        Get all available Treasury rates.
        
        Returns:
            Dictionary with all maturity rates
        """
        rates = {}
        for maturity in RiskFreeRateService.TREASURY_TICKERS.keys():
            rate = RiskFreeRateService.get_treasury_rate(maturity)
            if rate is not None:
                rates[maturity] = rate
        return rates