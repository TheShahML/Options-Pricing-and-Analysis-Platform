# options.py routes

"""
Options API Routes

FastAPI routes for option pricing calculations.
"""

from fastapi import APIRouter, HTTPException
from app.schemas.option_request import (
    OptionPricingRequest,
    OptionPricingResponse,
    GreeksResponse,
    ImpliedVolatilityRequest,
    ImpliedVolatilityResponse
)
from app.models.black_scholes import BlackScholesModel
from app.models.greeks import Greeks
from app.services.volatility import VolatilityService

router = APIRouter(prefix="/api/options", tags=["options"])


@router.post("/price", response_model=OptionPricingResponse)
async def calculate_option_price(request: OptionPricingRequest):
    """
    Calculate option price and Greeks using Black-Scholes model.
    
    Args:
        request: Option pricing parameters
        
    Returns:
        Option price and all Greeks
    """
    try:
        # Calculate option price
        bs_model = BlackScholesModel(
            S=request.S,
            K=request.K,
            T=request.T,
            r=request.r,
            sigma=request.sigma
        )
        
        option_price = bs_model.price(request.option_type)
        
        # Calculate Greeks
        greeks_calculator = Greeks(
            S=request.S,
            K=request.K,
            T=request.T,
            r=request.r,
            sigma=request.sigma,
            option_type=request.option_type
        )
        
        greeks_dict = greeks_calculator.all_greeks()
        
        return OptionPricingResponse(
            option_price=option_price,
            greeks=GreeksResponse(**greeks_dict),
            inputs=request
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error calculating option price: {str(e)}")


@router.post("/implied-volatility", response_model=ImpliedVolatilityResponse)
async def calculate_implied_volatility(request: ImpliedVolatilityRequest):
    """
    Calculate implied volatility from market price.
    
    Args:
        request: Market price and option parameters
        
    Returns:
        Implied volatility and model price comparison
    """
    try:
        iv = VolatilityService.calculate_implied_volatility(
            market_price=request.market_price,
            S=request.S,
            K=request.K,
            T=request.T,
            r=request.r,
            option_type=request.option_type
        )
        
        if iv is None:
            return ImpliedVolatilityResponse(
                implied_volatility=None,
                market_price=request.market_price,
                model_price=None,
                difference=None
            )
        
        # Calculate model price with found IV
        bs_model = BlackScholesModel(request.S, request.K, request.T, request.r, iv)
        model_price = bs_model.price(request.option_type)
        
        return ImpliedVolatilityResponse(
            implied_volatility=iv,
            market_price=request.market_price,
            model_price=model_price,
            difference=abs(model_price - request.market_price)
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error calculating implied volatility: {str(e)}")


@router.post("/greeks-surface")
async def calculate_greeks_surface(request: OptionPricingRequest):
    """
    Calculate Greeks across a range of spot prices for visualization.
    
    Args:
        request: Base option parameters
        
    Returns:
        Greeks values across spot price range
    """
    try:
        spot_range = []
        delta_values = []
        gamma_values = []
        theta_values = []
        vega_values = []
        
        # Calculate Greeks for spot prices from 50% to 150% of current price
        min_spot = request.S * 0.5
        max_spot = request.S * 1.5
        step = (max_spot - min_spot) / 50
        
        current_spot = min_spot
        while current_spot <= max_spot:
            greeks_calc = Greeks(
                S=current_spot,
                K=request.K,
                T=request.T,
                r=request.r,
                sigma=request.sigma,
                option_type=request.option_type
            )
            
            greeks = greeks_calc.all_greeks()
            
            spot_range.append(round(current_spot, 2))
            delta_values.append(round(greeks['delta'], 4))
            gamma_values.append(round(greeks['gamma'], 6))
            theta_values.append(round(greeks['theta'], 4))
            vega_values.append(round(greeks['vega'], 4))
            
            current_spot += step
        
        return {
            "spot_prices": spot_range,
            "delta": delta_values,
            "gamma": gamma_values,
            "theta": theta_values,
            "vega": vega_values,
            "strike": request.K,
            "option_type": request.option_type
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error calculating Greeks surface: {str(e)}")