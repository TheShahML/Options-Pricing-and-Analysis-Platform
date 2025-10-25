# yahoo_options_service.py

"""
Yahoo Finance Options Service

Fetches real options chain data from Yahoo Finance using yfinance.
"""

import yfinance as yf
from typing import List, Dict, Optional
import pandas as pd
from datetime import datetime
from app.models.black_scholes import BlackScholesModel
from app.models.greeks import Greeks


class YahooOptionsService:
    """Service for fetching options data from Yahoo Finance."""
    
    @staticmethod
    def get_available_expirations(ticker: str, limit: int = 20) -> List[str]:
        """
        Get available expiration dates for a ticker.
        
        Args:
            ticker: Stock ticker symbol
            limit: Maximum number of expirations to return
            
        Returns:
            List of expiration dates (YYYY-MM-DD)
        """
        try:
            stock = yf.Ticker(ticker)
            expirations = stock.options
            return list(expirations)[:limit]
        except Exception as e:
            print(f"Error fetching expirations for {ticker}: {e}")
            return []
    
    @staticmethod
    def get_options_chain(ticker: str, expiration_date: str) -> Dict[str, pd.DataFrame]:
        """
        Get options chain for a specific expiration.
        
        Args:
            ticker: Stock ticker symbol
            expiration_date: Expiration date (YYYY-MM-DD)
            
        Returns:
            Dictionary with 'calls' and 'puts' DataFrames
        """
        try:
            stock = yf.Ticker(ticker)
            chain = stock.option_chain(expiration_date)
            
            return {
                "calls": chain.calls,
                "puts": chain.puts,
                "expiration_date": expiration_date
            }
        except Exception as e:
            print(f"Error fetching options chain for {ticker}: {e}")
            return {
                "calls": pd.DataFrame(),
                "puts": pd.DataFrame(),
                "expiration_date": expiration_date
            }
    
    @staticmethod
    def format_options_for_api(df: pd.DataFrame, contract_type: str) -> List[Dict]:
        """
        Format options DataFrame for API response.
        
        Args:
            df: Options DataFrame from yfinance
            contract_type: "call" or "put"
            
        Returns:
            List of formatted option dictionaries
        """
        if df.empty:
            return []
        
        options_list = []
        for _, row in df.iterrows():
            options_list.append({
                "ticker": row.get("contractSymbol", ""),
                "strike_price": float(row.get("strike", 0)),
                "expiration_date": "",  # Will be set by caller
                "contract_type": contract_type,
                "underlying_ticker": "",  # Will be set by caller
                "shares_per_contract": 100,
                "bid": float(row.get("bid", 0)) if pd.notna(row.get("bid")) else None,
                "ask": float(row.get("ask", 0)) if pd.notna(row.get("ask")) else None,
                "last_price": float(row.get("lastPrice", 0)) if pd.notna(row.get("lastPrice")) else None,
                "volume": int(row.get("volume", 0)) if pd.notna(row.get("volume")) else None,
                "open_interest": int(row.get("openInterest", 0)) if pd.notna(row.get("openInterest")) else None,
                "implied_volatility": float(row.get("impliedVolatility", 0)) if pd.notna(row.get("impliedVolatility")) else None,
            })
        
        return options_list
    
    @staticmethod
    def calculate_time_to_expiration(expiration_date: str) -> float:
        """Calculate time to expiration in years."""
        try:
            exp_date = datetime.strptime(expiration_date, "%Y-%m-%d")
            today = datetime.now()
            days_to_expiration = (exp_date - today).days
            return max(days_to_expiration / 365.0, 0.01)
        except:
            return 0.25

    @staticmethod
    def get_options_chain_formatted(
        ticker: str, 
        expiration_date: str,
        limit: int = 50,
        current_price: Optional[float] = None,
        risk_free_rate: Optional[float] = None
    ) -> Dict[str, List[Dict]]:
        """Get formatted options chain with BS calculations and Greeks."""
        from app.models.black_scholes import BlackScholesModel
        from app.services.risk_free_rate import RiskFreeRateService
        
        chain_data = YahooOptionsService.get_options_chain(ticker, expiration_date)
        
        # Get current price if not provided
        if current_price is None:
            try:
                stock = yf.Ticker(ticker)
                current_price = stock.history(period="1d")['Close'].iloc[-1]
            except Exception as e:
                print(f"Error getting current price: {e}")
                current_price = 100.0
        
        # Get time to expiration
        T = YahooOptionsService.calculate_time_to_expiration(expiration_date)
        
        # Get risk-free rate if not provided - use appropriate rate for maturity
        if risk_free_rate is None:
            try:
                risk_free_rate = RiskFreeRateService.get_risk_free_rate_for_maturity(T)
            except Exception as e:
                print(f"Error getting risk-free rate: {e}")
                risk_free_rate = 0.045
        
        # Determine which maturity was used
        if T <= 0.25:
            treasury_maturity = "3M"
        elif T <= 1.0:
            treasury_maturity = "3M"
        elif T <= 5.0:
            treasury_maturity = "5Y"
        else:
            treasury_maturity = "10Y"
        
        calls_df = chain_data["calls"].head(limit)
        puts_df = chain_data["puts"].head(limit)
        
        # Process calls with BS and Greeks
        calls = []
        for _, row in calls_df.iterrows():
            strike = float(row.get("strike", 0))
            market_price = float(row.get("lastPrice", 0)) if pd.notna(row.get("lastPrice")) else None
            iv = float(row.get("impliedVolatility", 0.25)) if pd.notna(row.get("impliedVolatility")) else 0.25
            
            bs_price = None
            difference = None
            greeks_dict = None
            
            if iv > 0:
                try:
                    bs_model = BlackScholesModel(current_price, strike, T, risk_free_rate, iv)
                    bs_price = bs_model.call_price()
                    if market_price:
                        difference = market_price - bs_price
                    
                    # Calculate Greeks
                    greeks = Greeks(current_price, strike, T, risk_free_rate, iv, "call")
                    greeks_dict = greeks.all_greeks()
                except Exception as e:
                    print(f"Error calculating Greeks for call: {e}")
                    import traceback
                    traceback.print_exc()
            
            calls.append({
                "ticker": row.get("contractSymbol", ""),
                "strike_price": strike,
                "expiration_date": expiration_date,
                "contract_type": "call",
                "underlying_ticker": ticker.upper(),
                "shares_per_contract": 100,
                "bid": float(row.get("bid", 0)) if pd.notna(row.get("bid")) else None,
                "ask": float(row.get("ask", 0)) if pd.notna(row.get("ask")) else None,
                "last_price": market_price,
                "volume": int(row.get("volume", 0)) if pd.notna(row.get("volume")) else None,
                "open_interest": int(row.get("openInterest", 0)) if pd.notna(row.get("openInterest")) else None,
                "implied_volatility": iv,
                "bs_price": bs_price,
                "difference": difference,
                "greeks": greeks_dict,
            })
        
        # Process puts with BS and Greeks
        puts = []
        for _, row in puts_df.iterrows():
            strike = float(row.get("strike", 0))
            market_price = float(row.get("lastPrice", 0)) if pd.notna(row.get("lastPrice")) else None
            iv = float(row.get("impliedVolatility", 0.25)) if pd.notna(row.get("impliedVolatility")) else 0.25
            
            bs_price = None
            difference = None
            greeks_dict = None
            
            if iv > 0:
                try:
                    bs_model = BlackScholesModel(current_price, strike, T, risk_free_rate, iv)
                    bs_price = bs_model.put_price()
                    if market_price:
                        difference = market_price - bs_price
                    
                    # Calculate Greeks
                    greeks = Greeks(current_price, strike, T, risk_free_rate, iv, "put")
                    greeks_dict = greeks.all_greeks()
                except Exception as e:
                    print(f"Error calculating Greeks for put: {e}")
                    import traceback
                    traceback.print_exc()
            
            puts.append({
                "ticker": row.get("contractSymbol", ""),
                "strike_price": strike,
                "expiration_date": expiration_date,
                "contract_type": "put",
                "underlying_ticker": ticker.upper(),
                "shares_per_contract": 100,
                "bid": float(row.get("bid", 0)) if pd.notna(row.get("bid")) else None,
                "ask": float(row.get("ask", 0)) if pd.notna(row.get("ask")) else None,
                "last_price": market_price,
                "volume": int(row.get("volume", 0)) if pd.notna(row.get("volume")) else None,
                "open_interest": int(row.get("openInterest", 0)) if pd.notna(row.get("openInterest")) else None,
                "implied_volatility": iv,
                "bs_price": bs_price,
                "difference": difference,
                "greeks": greeks_dict,
            })
        
        return {
            "calls": calls,
            "puts": puts,
            "expiration_date": expiration_date,
            "underlying_ticker": ticker.upper(),
            "risk_free_rate": risk_free_rate,
            "treasury_maturity": treasury_maturity,
        }


# Singleton instance
_instance = None

def get_yahoo_options_service() -> YahooOptionsService:
    """Get or create YahooOptionsService singleton."""
    global _instance
    if _instance is None:
        _instance = YahooOptionsService()
    return _instance