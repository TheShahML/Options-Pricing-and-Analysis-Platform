# volatility.py

"""
Volatility Calculation Service

This module calculates historical volatility and provides methods
for implied volatility calculation.
"""

import numpy as np
import pandas as pd
from scipy.optimize import brentq
from typing import Optional, Literal
from app.models.black_scholes import BlackScholesModel


class VolatilityService:
    """Service for calculating historical and implied volatility."""
    
    @staticmethod
    def calculate_historical_volatility(prices: pd.Series, window: int = 30) -> float:
        """
        Calculate historical volatility using log returns.
        
        Args:
            prices: Series of historical prices
            window: Number of days for calculation (default 30)
            
        Returns:
            Annualized historical volatility
        """
        if len(prices) < 2:
            return 0.0
        
        # Calculate log returns
        log_returns = np.log(prices / prices.shift(1))
        
        # Drop NaN values
        log_returns = log_returns.dropna()
        
        if len(log_returns) < 2:
            return 0.0
        
        # Use last 'window' days if available
        if len(log_returns) > window:
            log_returns = log_returns.tail(window)
        
        # Calculate standard deviation and annualize (252 trading days)
        volatility = log_returns.std() * np.sqrt(252)
        
        return float(volatility)
    
    @staticmethod
    def calculate_implied_volatility(
        market_price: float,
        S: float,
        K: float,
        T: float,
        r: float,
        option_type: Literal["call", "put"],
        initial_guess: float = 0.3,
        max_iterations: int = 100,
        tolerance: float = 1e-6
    ) -> Optional[float]:
        """
        Calculate implied volatility using Newton-Raphson method.
        
        Args:
            market_price: Observed market price of the option
            S: Current stock price
            K: Strike price
            T: Time to expiration (years)
            r: Risk-free rate
            option_type: "call" or "put"
            initial_guess: Starting volatility guess
            max_iterations: Maximum iterations
            tolerance: Convergence tolerance
            
        Returns:
            Implied volatility or None if not found
        """
        if T <= 0 or market_price <= 0:
            return None
        
        # Check if price is within valid bounds
        intrinsic_value = max(0, S - K) if option_type == "call" else max(0, K - S)
        if market_price < intrinsic_value:
            return None
        
        def objective(sigma):
            """Objective function: difference between model and market price."""
            try:
                bs = BlackScholesModel(S, K, T, r, sigma)
                model_price = bs.price(option_type)
                return model_price - market_price
            except:
                return float('inf')
        
        try:
            # Use Brent's method to find root
            implied_vol = brentq(objective, 0.001, 5.0, maxiter=max_iterations, xtol=tolerance)
            return float(implied_vol)
        except:
            # If Brent's method fails, try Newton-Raphson
            try:
                sigma = initial_guess
                for _ in range(max_iterations):
                    bs = BlackScholesModel(S, K, T, r, sigma)
                    price_diff = bs.price(option_type) - market_price
                    
                    if abs(price_diff) < tolerance:
                        return float(sigma)
                    
                    # Calculate vega for Newton-Raphson step
                    from app.models.greeks import Greeks
                    greeks = Greeks(S, K, T, r, sigma, option_type)
                    vega = greeks.vega() * 100  # Convert back to decimal
                    
                    if vega < 1e-10:
                        break
                    
                    # Newton-Raphson update
                    sigma = sigma - price_diff / vega
                    
                    # Keep sigma in reasonable bounds
                    sigma = max(0.001, min(sigma, 5.0))
                
                return None
            except:
                return None
    
    @staticmethod
    def calculate_volatility_surface(
        option_chain: pd.DataFrame,
        S: float,
        r: float,
        option_type: Literal["call", "put"]
    ) -> pd.DataFrame:
        """
        Calculate implied volatility surface from option chain.
        
        Args:
            option_chain: DataFrame with option data (strike, lastPrice, etc.)
            S: Current stock price
            r: Risk-free rate
            option_type: "call" or "put"
            
        Returns:
            DataFrame with strikes, implied volatilities, and time to expiration
        """
        results = []
        
        for _, row in option_chain.iterrows():
            try:
                strike = row.get('strike')
                market_price = row.get('lastPrice')
                
                # Calculate time to expiration from DTE if available
                # Otherwise estimate from expiration date
                T = 30 / 365  # Default 30 days if not available
                
                if pd.notna(strike) and pd.notna(market_price) and market_price > 0:
                    iv = VolatilityService.calculate_implied_volatility(
                        market_price, S, strike, T, r, option_type
                    )
                    
                    if iv is not None:
                        results.append({
                            'strike': strike,
                            'implied_volatility': iv,
                            'time_to_expiration': T,
                            'market_price': market_price
                        })
            except:
                continue
        
        return pd.DataFrame(results)