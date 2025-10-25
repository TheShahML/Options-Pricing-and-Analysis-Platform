# options_pricing_ui.py

"""
Options Pricing UI - Main Application

Black-Scholes options pricing calculator with real-time market data.
"""

import reflex as rx
from options_pricing_ui.pages import index, chain


# Create the app
app = rx.App(
    theme=rx.theme(
        appearance="light",
        accent_color="blue",
        radius="large",
    ),
)

# Add pages
app.add_page(
    index.index,
    route="/",
    title="Options Pricing Tool",
    description="Black-Scholes options pricing with real-time market data",
)

app.add_page(
    chain.chain,
    route="/chain",
    title="Options Chain Analysis",
    description="Analyze real options chains with Black-Scholes comparison",
)