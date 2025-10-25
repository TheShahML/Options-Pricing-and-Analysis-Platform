# black_scholes.py

"""
Black-Scholes Option Pricing Model

This module implements the Black-Scholes formula for pricing European call and put options
"""

import math
from scipy.stats import norm
from typing import Literal

class BlackScholesModel:
    """
    Black-Scholes option pricing model for European call and put options

    Attributes:
        S: Current stock price
        K: Option strike price
        T: Time to expiration (in years)
        r: Risk-free interest rate (annualized)
        sigma: Volatility of the underlying asset (annualized)
    """
    def __init__(self, S: float, K: float, T: float, r: float, sigma: float):
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
    
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

    def call_price(self) -> float:
        """
        Calculate European call option price.
        
        Returns:
            Call option price
        """
        if self.T <= 0:
            return max(0, self.S - self.K)
        
        d1 = self._d1()
        d2 = self._d2()
        
        call = (self.S * norm.cdf(d1)) - (self.K * math.exp(-self.r * self.T) * norm.cdf(d2))
        return call

    def put_price(self) -> float:
        """
        Calculate European put option price.
        
        Returns:
            Put option price
        """
        if self.T <= 0:
            return max(0, self.K - self.S)
        
        d1 = self._d1()
        d2 = self._d2()
        
        put = (self.K * math.exp(-self.r * self.T) * norm.cdf(-d2)) - (self.S * norm.cdf(-d1))
        return put

    def price(self, option_type: Literal["call", "put"]) -> float:
        """
        Calculate option price based on type.
        
        Args:
            option_type: Either "call" or "put"
            
        Returns:
            Option price
        """
        if option_type.lower() == "call":
            return self.call_price()
        elif option_type.lower() == "put":
            return self.put_price()
        else:
            raise ValueError("option_type must be 'call' or 'put'")

    def get_d1_d2(self) -> tuple[float, float]:
        """
        Get d1 and d2 values for Greeks calculations.
        
        Returns:
            Tuple of (d1, d2)
        """
        return self._d1(), self._d2()