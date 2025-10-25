# options_chain_state.py Options Chain State Management

"""
Options Chain State

State management for real options chain display and analysis.
"""

import reflex as rx
from typing import Dict, List, Any
from datetime import datetime
from options_pricing_ui.services import api_client


class OptionsChainState(rx.State):
    """State for options chain page."""
    
    # Ticker and expiration selection
    ticker: str = ""
    selected_expiration: str = ""
    available_expirations: List[str] = []
    
    # Options chain data
    calls: List[Dict[str, Any]] = []
    puts: List[Dict[str, Any]] = []
    
    # Loading states
    loading_expirations: bool = False
    loading_chain: bool = False
    
    # Error handling
    error_message: str = ""
    
    # Current stock price (for BS calculations)
    current_price: float = 0.0
    
    # Risk-free rate used in calculations
    risk_free_rate: float = 0.0
    treasury_maturity: str = "3M"  # Which Treasury is being used
    
    # NEW: Selected option for calculator/greeks
    selected_option: Dict[str, Any] = {}
    selected_strike: str = ""  # Track which row is selected
    copy_to_calculator: bool = False  # Flag to copy values
    
    def select_option(self, option: Dict[str, Any]):
        """Select an option from the table."""
        self.selected_option = option
        self.selected_strike = option.get("strike_price", "")
    
    def load_selected_to_inputs(self):
        """Load selected option values into calculator."""
        if not self.selected_option:
            return
        
        strike = float(self.selected_option.get("strike_raw", 0))
        vol = float(self.selected_option.get("iv_raw", 0.25))
        opt_type = self.selected_option.get("option_type", "call")
        
        # Calculate time to expiration
        time_to_exp = 0.25  # Default
        if self.selected_expiration:
            try:
                from datetime import datetime
                exp_date = datetime.strptime(self.selected_expiration, "%Y-%m-%d")
                today = datetime.now()
                days_to_exp = (exp_date - today).days
                time_to_exp = max(days_to_exp / 365.0, 0.01)
            except:
                pass
        
        # Call AppState method to load values
        from options_pricing_ui.state.app_state import AppState
        return AppState.load_from_selected_option(
            strike=strike,
            vol=vol,
            time=time_to_exp,
            opt_type=opt_type,
            current=self.current_price
        )
    
    def clear_selection(self):
        """Clear the selected option."""
        self.selected_option = {}
        self.selected_strike = ""
    
    async def load_expirations(self):
        """Load available expiration dates for ticker."""
        if not self.ticker:
            self.error_message = "Please enter a ticker symbol"
            return
        
        self.loading_expirations = True
        self.error_message = ""
        self.available_expirations = []
        
        try:
            # Use Yahoo Finance for expirations
            result = await api_client.get_yahoo_expirations(self.ticker.upper())
            
            if result:
                self.available_expirations = result.get("expirations", [])
                if self.available_expirations:
                    self.selected_expiration = self.available_expirations[0]
                    # Also fetch stock price
                    stock_info = await api_client.get_stock_info(self.ticker.upper())
                    if stock_info:
                        self.current_price = stock_info.get("current_price", 0.0)
            else:
                self.error_message = f"No expiration dates found for {self.ticker}"
                
        except Exception as e:
            self.error_message = f"Error loading expirations: {str(e)}"
        finally:
            self.loading_expirations = False
    
    async def load_options_chain(self):
        """Load options chain with quotes for selected expiration."""
        if not self.ticker or not self.selected_expiration:
            self.error_message = "Please select a ticker and expiration date"
            return
        
        self.loading_chain = True
        self.error_message = ""
        self.calls = []
        self.puts = []
        self.selected_option = {}  # Clear selection when loading new chain
        self.selected_strike = ""
        
        try:
            # Use Yahoo Finance for full options data
            result = await api_client.get_yahoo_options_chain(
                self.ticker.upper(),
                self.selected_expiration,
                limit=50
            )
            
            if result:
                # Format the data for display
                raw_calls = result.get("calls", [])
                raw_puts = result.get("puts", [])
                
                # Store risk-free rate from API
                self.risk_free_rate = result.get("risk_free_rate", 0.045)
                self.treasury_maturity = result.get("treasury_maturity", "3M")
                
                # Format calls
                self.calls = [
                    {
                        "strike_price": f"${c.get('strike_price', 0):.2f}",
                        "strike_raw": c.get('strike_price', 0),  # Raw strike for calculator
                        "bid": f"${c.get('bid', 0):.2f}" if c.get('bid') else "N/A",
                        "ask": f"${c.get('ask', 0):.2f}" if c.get('ask') else "N/A",
                        "last_price": f"${c.get('last_price', 0):.2f}" if c.get('last_price') else "N/A",
                        "bs_price": f"${c.get('bs_price', 0):.2f}" if c.get('bs_price') else "N/A",
                        "difference": f"${c.get('difference', 0):+.2f}" if c.get('difference') is not None else "N/A",
                        "difference_color": "green" if (c.get('difference') is not None and c.get('difference') < 0) else "red" if (c.get('difference') is not None and c.get('difference') > 0) else "gray",
                        "volume": f"{c.get('volume', 0):,}" if c.get('volume') else "N/A",
                        "implied_volatility": f"{c.get('implied_volatility', 0) * 100:.2f}%" if c.get('implied_volatility') else "N/A",
                        "iv_raw": c.get('implied_volatility', 0.25),
                        "iv_color": self.get_iv_color(c.get('implied_volatility', 0.25)),
                        "option_type": "call",  # For calculator
                        # Flatten Greeks as formatted strings
                        "delta": f"{c.get('greeks', {}).get('delta', 0):.4f}" if c.get('greeks') else "0.0000",
                        "gamma": f"{c.get('greeks', {}).get('gamma', 0):.4f}" if c.get('greeks') else "0.0000",
                        "theta": f"{c.get('greeks', {}).get('theta', 0):.4f}" if c.get('greeks') else "0.0000",
                        "vega": f"{c.get('greeks', {}).get('vega', 0):.4f}" if c.get('greeks') else "0.0000",
                        "rho": f"{c.get('greeks', {}).get('rho', 0):.4f}" if c.get('greeks') else "0.0000",
                        "has_greeks": c.get('greeks') is not None,
                    }
                    for c in raw_calls
                ]
                
                # Format puts
                self.puts = [
                    {
                        "strike_price": f"${p.get('strike_price', 0):.2f}",
                        "strike_raw": p.get('strike_price', 0),
                        "bid": f"${p.get('bid', 0):.2f}" if p.get('bid') else "N/A",
                        "ask": f"${p.get('ask', 0):.2f}" if p.get('ask') else "N/A",
                        "last_price": f"${p.get('last_price', 0):.2f}" if p.get('last_price') else "N/A",
                        "bs_price": f"${p.get('bs_price', 0):.2f}" if p.get('bs_price') else "N/A",
                        "difference": f"${p.get('difference', 0):+.2f}" if p.get('difference') is not None else "N/A",
                        "difference_color": "green" if (p.get('difference') is not None and p.get('difference') < 0) else "red" if (p.get('difference') is not None and p.get('difference') > 0) else "gray",
                        "volume": f"{p.get('volume', 0):,}" if p.get('volume') else "N/A",
                        "implied_volatility": f"{p.get('implied_volatility', 0) * 100:.2f}%" if p.get('implied_volatility') else "N/A",
                        "iv_raw": p.get('implied_volatility', 0.25),
                        "iv_color": self.get_iv_color(p.get('implied_volatility', 0.25)),
                        "option_type": "put",
                        # Flatten Greeks as formatted strings
                        "delta": f"{p.get('greeks', {}).get('delta', 0):.4f}" if p.get('greeks') else "0.0000",
                        "gamma": f"{p.get('greeks', {}).get('gamma', 0):.4f}" if p.get('greeks') else "0.0000",
                        "theta": f"{p.get('greeks', {}).get('theta', 0):.4f}" if p.get('greeks') else "0.0000",
                        "vega": f"{p.get('greeks', {}).get('vega', 0):.4f}" if p.get('greeks') else "0.0000",
                        "rho": f"{p.get('greeks', {}).get('rho', 0):.4f}" if p.get('greeks') else "0.0000",
                        "has_greeks": p.get('greeks') is not None,
                    }
                    for p in raw_puts
                ]
                
                if not self.calls and not self.puts:
                    self.error_message = "No options data found for this expiration"
            else:
                self.error_message = "Failed to load options chain"
                
        except Exception as e:
            self.error_message = f"Error loading options chain: {str(e)}"
        finally:
            self.loading_chain = False
    
    def set_ticker(self, value: str):
        """Set ticker value."""
        self.ticker = value.upper()
    
    def set_expiration(self, value: str):
        """Set selected expiration."""
        self.selected_expiration = value
    
    async def search_and_load(self):
        """Search ticker and load full chain."""
        await self.load_expirations()
        if self.available_expirations:
            await self.load_options_chain()
    
    def get_iv_color(self, iv: float) -> str:
        """Calculate color based on IV value."""
        if iv < 0.15:
            return "#1e3a8a"
        elif iv < 0.25:
            return "#3b82f6"
        elif iv < 0.35:
            return "#06b6d4"
        elif iv < 0.45:
            return "#22c55e"
        elif iv < 0.55:
            return "#eab308"
        elif iv < 0.70:
            return "#f97316"
        else:
            return "#dc2626"