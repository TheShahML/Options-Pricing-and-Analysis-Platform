# Options Pricing Platform

Real-time options analysis with Black-Scholes pricing, Greeks calculation, and live market data.

🔗 **[Visit Live Site](https://theshahml.com)**

## Features

- **Options Chain Viewer** - Real-time options data with bid/ask spreads
- **Black-Scholes Calculator** - Custom pricing with adjustable parameters
- **Greeks Analysis** - Live Delta, Gamma, Theta, Vega, Rho for any option
- **Market Data** - Stock quotes and historical volatility
- **Dynamic Risk-Free Rate** - Auto-fetched US Treasury yields

## Tech Stack

**Backend:** FastAPI, NumPy/SciPy, yfinance, TwelveData API, Pydantic

**Frontend:** Reflex (Python-based web framework), Radix UI

**Deployment:** AWS EC2, Nginx, Let's Encrypt SSL

## Screenshots

TBA

## How It Works

Uses Black-Scholes-Merton model for theoretical pricing and Greeks calculation. Market data from Yahoo Finance and TwelveData. Risk-free rates dynamically fetched from US Treasury yields.

## Upcoming Features

- **Fix Implied Volatility Display** - Currently shows calculation issues for some options
- **Mobile Responsive Design** - Optimize UI for mobile devices
- **Historical Volatility Charts** - Visual analysis of past volatility
- **Additional Option Strategies** - Straddles, strangles, iron condors, butterflies, and more
- **Advanced Analytics** - Profit/loss diagrams, breakeven analysis

*Note: Future updates depend on user demand and feedback. If you'd like to see specific features prioritized, please reach out!*

## Contact & Feedback

**Discord:** TheShah

For feature requests, bug reports, or general feedback, feel free to reach out on Discord. Always looking to improve the platform based on user needs!

## License

Apache 2.0

---

*Educational purposes only. Not financial advice.*
