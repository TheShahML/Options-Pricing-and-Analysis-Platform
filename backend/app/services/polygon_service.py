# polygon_service.py 

"""
Polygon.io Options Service

This module fetches real options chain data from Polygon.io API.
"""

from polygon import RESTClient
from typing import Optional, List, Dict
from datetime import datetime, timedelta
import os


class PolygonOptionsService:
    """Service for fetching options data from Polygon.io."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Polygon client.
        
        Args:
            api_key: Polygon.io API key. If None, reads from POLYGON_API_KEY env var
        """
        self.api_key = api_key or os.getenv("POLYGON_API_KEY")
        if not self.api_key:
            raise ValueError("Polygon.io API key not found. Set POLYGON_API_KEY environment variable.")
        self.client = RESTClient(self.api_key)
    
    def get_options_chain(
        self, 
        ticker: str,
        expiration_date: Optional[str] = None,
        strike_price: Optional[float] = None,
        contract_type: Optional[str] = None
    ) -> List[Dict]:
        """
        Get options chain for a ticker.
        
        Args:
            ticker: Underlying ticker symbol (e.g., "AAPL")
            expiration_date: Filter by expiration date (YYYY-MM-DD)
            strike_price: Filter by strike price
            contract_type: Filter by "call" or "put"
            
        Returns:
            List of option contracts with details
        """
        try:
            # Get options contracts
            contracts = self.client.list_options_contracts(
                underlying_ticker=ticker,
                expiration_date=expiration_date,
                strike_price=strike_price,
                contract_type=contract_type,
                limit=1000
            )
            
            options_list = []
            for contract in contracts:
                options_list.append({
                    "ticker": contract.ticker,
                    "strike_price": contract.strike_price,
                    "expiration_date": contract.expiration_date,
                    "contract_type": contract.contract_type,
                    "underlying_ticker": contract.underlying_ticker,
                    "shares_per_contract": contract.shares_per_contract,
                })
            
            return options_list
            
        except Exception as e:
            print(f"Error fetching options chain for {ticker}: {e}")
            return []
    
    def get_option_quote(self, option_ticker: str) -> Optional[Dict]:
        """
        Get current quote for a specific option contract.
        
        Args:
            option_ticker: Option contract ticker (e.g., "O:AAPL251219C00150000")
            
        Returns:
            Dictionary with bid, ask, last price, volume, etc.
        """
        try:
            quote = self.client.get_snapshot_option(
                underlying_asset=option_ticker.split(":")[1][:4],  # Extract ticker
                option_contract=option_ticker
            )
            
            if quote:
                return {
                    "ticker": option_ticker,
                    "bid": quote.last_quote.bid if hasattr(quote, 'last_quote') else None,
                    "ask": quote.last_quote.ask if hasattr(quote, 'last_quote') else None,
                    "last_price": quote.day.close if hasattr(quote, 'day') else None,
                    "volume": quote.day.volume if hasattr(quote, 'day') else None,
                    "open_interest": quote.open_interest if hasattr(quote, 'open_interest') else None,
                    "implied_volatility": quote.implied_volatility if hasattr(quote, 'implied_volatility') else None,
                }
            return None
            
        except Exception as e:
            print(f"Error fetching option quote for {option_ticker}: {e}")
            return None
    
    def get_options_chain_with_quotes(
        self,
        ticker: str,
        expiration_date: Optional[str] = None,
        limit: int = 50
    ) -> Dict[str, List[Dict]]:
        """
        Get options chain with current market quotes.
        
        Args:
            ticker: Underlying ticker symbol
            expiration_date: Filter by expiration date (YYYY-MM-DD)
            limit: Maximum number of contracts to fetch per type
            
        Returns:
            Dictionary with 'calls' and 'puts' lists
        """
        try:
            # Get calls
            calls = self.get_options_chain(
                ticker=ticker,
                expiration_date=expiration_date,
                contract_type="call"
            )[:limit]
            
            # Get puts
            puts = self.get_options_chain(
                ticker=ticker,
                expiration_date=expiration_date,
                contract_type="put"
            )[:limit]
            
            # Enrich with quotes (sample first 10 to avoid rate limits)
            calls_with_quotes = []
            for i, call in enumerate(calls[:10]):
                quote = self.get_option_quote(call['ticker'])
                if quote:
                    calls_with_quotes.append({**call, **quote})
                else:
                    calls_with_quotes.append(call)
            
            puts_with_quotes = []
            for i, put in enumerate(puts[:10]):
                quote = self.get_option_quote(put['ticker'])
                if quote:
                    puts_with_quotes.append({**put, **quote})
                else:
                    puts_with_quotes.append(put)
            
            return {
                "calls": calls_with_quotes,
                "puts": puts_with_quotes,
                "expiration_date": expiration_date or "multiple",
                "underlying_ticker": ticker
            }
            
        except Exception as e:
            print(f"Error fetching options chain with quotes for {ticker}: {e}")
            return {"calls": [], "puts": [], "expiration_date": "", "underlying_ticker": ticker}
    
    def get_available_expirations(self, ticker: str, limit: int = 20) -> List[str]:
        """
        Get list of available expiration dates for a ticker.
        
        Args:
            ticker: Underlying ticker symbol
            limit: Maximum number of expiration dates to return
            
        Returns:
            List of expiration dates (YYYY-MM-DD)
        """
        try:
            # Get all contracts and extract unique expiration dates
            contracts = self.get_options_chain(ticker=ticker)
            
            expirations = sorted(list(set(
                contract['expiration_date'] 
                for contract in contracts 
                if 'expiration_date' in contract
            )))
            
            return expirations[:limit]
            
        except Exception as e:
            print(f"Error fetching expirations for {ticker}: {e}")
            return []


# Create a singleton instance
_instance = None

def get_polygon_service(api_key: Optional[str] = None) -> PolygonOptionsService:
    """
    Get or create PolygonOptionsService singleton instance.
    
    Args:
        api_key: Optional API key, otherwise uses environment variable
        
    Returns:
        PolygonOptionsService instance
    """
    global _instance
    if _instance is None:
        _instance = PolygonOptionsService(api_key=api_key)
    return _instance