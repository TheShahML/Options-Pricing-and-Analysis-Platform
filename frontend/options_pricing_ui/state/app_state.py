# app_state.py App state management

"""
Application State

Manages all state for the Options Pricing UI using Reflex state management.
"""

import reflex as rx
from typing import Dict, Optional, Any
from options_pricing_ui.services import api_client


class AppState(rx.State):
    """Main application state."""
    
    # Ticker search
    ticker: str = ""
    ticker_loading: bool = False
    ticker_error: str = ""
    
    # Stock data
    stock_data: Dict[str, Any] = {}
    current_price: float = 0.0
    historical_volatility: float = 0.0
    
    # Option inputs
    strike_price: float = 100.0
    time_to_expiration: float = 0.25
    risk_free_rate: float = 0.045
    volatility: float = 0.20
    option_type: str = "call"
    
    # Calculation results
    option_price: float = 0.0
    greeks: Dict[str, float] = {}
    calculation_loading: bool = False
    
    # Greeks surface data for charts
    greeks_surface: Dict[str, Any] = {}
    
    # UI state
    show_results: bool = False
    validation_error: str = ""
    
    async def search_ticker(self):
        """Search for ticker and fetch stock data."""
        if not self.ticker:
            self.ticker_error = "Please enter a ticker symbol"
            return
        
        self.ticker_loading = True
        self.ticker_error = ""
        self.stock_data = {}
        
        try:
            print(f"Searching for ticker: {self.ticker}")
            
            # Fetch stock info and historical volatility in parallel
            stock_info = await api_client.get_stock_info(self.ticker.upper())
            vol_data = await api_client.get_historical_volatility(self.ticker.upper())
            
            print(f"Stock info result: {stock_info}")
            print(f"Vol data result: {vol_data}")
            
            if stock_info:
                self.stock_data = stock_info
                self.current_price = stock_info.get("current_price", 0.0)
                self.strike_price = self.current_price  # Default strike to current price
                
                if vol_data:
                    self.historical_volatility = vol_data.get("volatility", 0.0)
                    self.volatility = self.historical_volatility  # Use as default
                
                self.ticker_error = ""
            else:
                self.ticker_error = f"Could not find data for {self.ticker}"
                
        except Exception as e:
            print(f"Exception in search_ticker: {e}")
            import traceback
            traceback.print_exc()
            self.ticker_error = f"Error connecting to backend: {str(e)}"
        finally:
            self.ticker_loading = False
    
    async def validate_and_calculate(self):
        """Validate inputs before calculating."""
        self.validation_error = ""
        self.show_results = False  # Clear previous results
        
        # Check if required values are filled
        if self.strike_price <= 0:
            self.validation_error = "Please enter a valid strike price or select an option and click 'Use These Values'"
            return
        
        if self.time_to_expiration <= 0:
            self.validation_error = "Please enter a valid time to expiration"
            return
        
        if self.volatility <= 0:
            self.validation_error = "Please enter a valid volatility or select an option and click 'Use These Values'"
            return
        
        # Debug print
        print(f"Calculating with: S={self.current_price}, K={self.strike_price}, T={self.time_to_expiration}, vol={self.volatility}, type={self.option_type}")
        
        # All valid, proceed to calculate
        await self.calculate_option()
    
    def load_from_selected_option(self, strike: float, vol: float, time: float, opt_type: str, current: float):
        """Load values from selected option."""
        self.strike_price = strike
        self.volatility = vol
        self.time_to_expiration = time
        self.option_type = opt_type
        if current > 0:
            self.current_price = current
        print(f"Loaded values: K={strike}, vol={vol}, T={time}, type={opt_type}, S={current}")
    
    
    async def calculate_option(self):
        """Calculate option price and Greeks."""
        self.calculation_loading = True
        self.show_results = False
        
        try:
            # Use current price if available, otherwise use strike
            spot_price = self.current_price if self.current_price > 0 else self.strike_price
            
            params = {
                "S": spot_price,
                "K": self.strike_price,
                "T": self.time_to_expiration,
                "r": self.risk_free_rate,
                "sigma": self.volatility,
                "option_type": self.option_type
            }
            
            result = await api_client.calculate_option_price(params)
            
            if result:
                self.option_price = result.get("option_price", 0.0)
                self.greeks = result.get("greeks", {})
                self.show_results = True
                
                # Also fetch Greeks surface for visualization
                surface_data = await api_client.get_greeks_surface(params)
                if surface_data:
                    self.greeks_surface = surface_data
            
        except Exception as e:
            print(f"Error calculating option: {e}")
        finally:
            self.calculation_loading = False
    
    def set_ticker(self, value: str):
        """Set ticker value."""
        self.ticker = value.upper()
    
    def set_strike_price(self, value: str):
        """Set strike price."""
        try:
            self.strike_price = float(value) if value else 0.0
        except:
            pass
    
    def set_time_to_expiration(self, value: str):
        """Set time to expiration."""
        try:
            self.time_to_expiration = float(value) if value else 0.0
        except:
            pass
    
    def set_risk_free_rate(self, value: str):
        """Set risk-free rate."""
        try:
            self.risk_free_rate = float(value) if value else 0.0
        except:
            pass
    
    def set_volatility(self, value: str):
        """Set volatility."""
        try:
            self.volatility = float(value) if value else 0.0
        except:
            pass
    
    def set_option_type(self, value: str):
        """Set option type."""
        self.option_type = value