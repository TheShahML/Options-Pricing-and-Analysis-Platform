# greeks.py

"""
Greeks Calculations for Options

This module calculates the option Greeks (Delta, Gamma, Theta, Vega, Rho)
which measure the sensitivity of option prices to various parameters.
"""

import math
from scipy.stats import norm
from typing import Literal


class Greeks:
    """
    Calculate option Greeks for European options using Black-Scholes model.
    
    Attributes:
        S: Current stock price
        K: Strike price
        T: Time to expiration (in years)
        r: Risk-free interest rate (annual)
        sigma: Volatility (annual)
        option_type: "call" or "put"
    """
    
    def __init__(self, S: float, K: float, T: float, r: float, sigma: float, option_type: Literal["call", "put"]):
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.option_type = option_type.lower()
        
    def _d1(self) -> float:
        """Calculate d1 parameter."""
        if self.T <= 0:
            return 0.0
        return (math.log(self.S / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * math.sqrt(self.T))
    
    def _d2(self) -> float:
        """Calculate d2 parameter."""
        if self.T <= 0:
            return 0.0
        return self._d1() - self.sigma * math.sqrt(self.T)
    
    def delta(self) -> float:
        """
        Calculate Delta: rate of change of option price with respect to underlying price.
        
        Returns:
            Delta value (Call: 0 to 1, Put: -1 to 0)
        """
        if self.T <= 0:
            if self.option_type == "call":
                return 1.0 if self.S > self.K else 0.0
            else:
                return -1.0 if self.S < self.K else 0.0
        
        d1 = self._d1()
        
        if self.option_type == "call":
            return norm.cdf(d1)
        else:  # put
            return norm.cdf(d1) - 1
    
    def gamma(self) -> float:
        """
        Calculate Gamma: rate of change of Delta with respect to underlying price.
        
        Returns:
            Gamma value (same for calls and puts)
        """
        if self.T <= 0:
            return 0.0
        
        d1 = self._d1()
        return norm.pdf(d1) / (self.S * self.sigma * math.sqrt(self.T))
    
    def theta(self) -> float:
        """
        Calculate Theta: rate of change of option price with respect to time.
        Returned as decay per day (negative for long positions).
        
        Returns:
            Theta value (typically negative, per day)
        """
        if self.T <= 0:
            return 0.0
        
        d1 = self._d1()
        d2 = self._d2()
        
        term1 = -(self.S * norm.pdf(d1) * self.sigma) / (2 * math.sqrt(self.T))
        
        if self.option_type == "call":
            term2 = self.r * self.K * math.exp(-self.r * self.T) * norm.cdf(d2)
            theta_annual = term1 - term2
        else:  # put
            term2 = self.r * self.K * math.exp(-self.r * self.T) * norm.cdf(-d2)
            theta_annual = term1 + term2
        
        # Convert to per-day theta
        return theta_annual / 365
    
    def vega(self) -> float:
        """
        Calculate Vega: rate of change of option price with respect to volatility.
        Returned as change per 1% change in volatility.
        
        Returns:
            Vega value (same for calls and puts, per 1% vol change)
        """
        if self.T <= 0:
            return 0.0
        
        d1 = self._d1()
        vega_decimal = self.S * norm.pdf(d1) * math.sqrt(self.T)
        
        # Convert to per 1% change in volatility
        return vega_decimal / 100
    
    def rho(self) -> float:
        """
        Calculate Rho: rate of change of option price with respect to risk-free rate.
        Returned as change per 1% change in interest rate.
        
        Returns:
            Rho value (per 1% rate change)
        """
        if self.T <= 0:
            return 0.0
        
        d2 = self._d2()
        
        if self.option_type == "call":
            rho_decimal = self.K * self.T * math.exp(-self.r * self.T) * norm.cdf(d2)
        else:  # put
            rho_decimal = -self.K * self.T * math.exp(-self.r * self.T) * norm.cdf(-d2)
        
        # Convert to per 1% change in interest rate
        return rho_decimal / 100
    
    def all_greeks(self) -> dict:
        """
        Calculate all Greeks at once.
        
        Returns:
            Dictionary containing all Greek values
        """
        return {
            "delta": self.delta(),
            "gamma": self.gamma(),
            "theta": self.theta(),
            "vega": self.vega(),
            "rho": self.rho()
        }