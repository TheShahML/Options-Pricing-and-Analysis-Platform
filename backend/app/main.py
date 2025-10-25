# main.py

"""
FastAPI Main Application

Entry point for the Options Pricing Tool backend API.
"""

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import options, market_data, options_chain

# Create FastAPI app
app = FastAPI(
    title="Options Pricing Tool API",
    description="Black-Scholes options pricing with real market data from Yahoo Finance",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(options.router)
app.include_router(market_data.router)
app.include_router(options_chain.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Options Pricing Tool API",
        "docs": "/api/docs",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)