# pricing_results.py Pricing Results Display Component

"""
Pricing Results Component

Displays calculated option price and Greeks.
"""

import reflex as rx
from options_pricing_ui.state.app_state import AppState


def greek_card(name: str, value: float, description: str, color: str = "blue") -> rx.Component:
    """Display individual Greek metric."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text(name, size="4", weight="bold"),
                rx.badge(f"{value:.4f}", color_scheme=color, size="2"),
                spacing="2",
                align="center",
            ),
            rx.text(description, size="2", color="gray"),
            spacing="2",
            align="start",
        ),
        padding="4",
        border_radius="8px",
        border=f"1px solid var(--{color}-6)",
        background=f"var(--{color}-2)",
        width="100%",
    )


def pricing_results() -> rx.Component:
    """Pricing results display."""
    return rx.cond(
        AppState.show_results,
        rx.box(
            rx.vstack(
                rx.heading("Results", size="6", weight="bold"),
                rx.divider(),
                
                # Option Price - Large Display
                rx.box(
                    rx.vstack(
                        rx.text("Option Price", size="3", color="gray"),
                        rx.heading(
                            f"${AppState.option_price:.4f}",
                            size="9",
                            weight="bold",
                            color="green",
                        ),
                        rx.text(
                            rx.cond(
                                AppState.option_type == "call",
                                "Call Option",
                                "Put Option"
                            ),
                            size="3",
                            color="gray",
                        ),
                        spacing="2",
                        align="center",
                    ),
                    padding="6",
                    border_radius="12px",
                    background="linear-gradient(135deg, var(--green-2) 0%, var(--green-3) 100%)",
                    border="2px solid var(--green-6)",
                    width="100%",
                ),
                
                # Greeks Section
                rx.heading("The Greeks", size="5", weight="bold"),
                
                rx.grid(
                    greek_card(
                        "Delta (Δ)",
                        AppState.greeks.get("delta", 0),
                        "Rate of change of option price with respect to underlying price",
                        "blue",
                    ),
                    greek_card(
                        "Gamma (Γ)",
                        AppState.greeks.get("gamma", 0),
                        "Rate of change of delta with respect to underlying price",
                        "purple",
                    ),
                    greek_card(
                        "Theta (Θ)",
                        AppState.greeks.get("theta", 0),
                        "Time decay per day (typically negative)",
                        "red",
                    ),
                    greek_card(
                        "Vega (ν)",
                        AppState.greeks.get("vega", 0),
                        "Sensitivity to volatility (per 1% change)",
                        "orange",
                    ),
                    greek_card(
                        "Rho (ρ)",
                        AppState.greeks.get("rho", 0),
                        "Sensitivity to interest rate (per 1% change)",
                        "teal",
                    ),
                    columns="2",
                    spacing="4",
                    width="100%",
                ),
                
                rx.callout(
                    rx.vstack(
                        rx.text("Understanding the Greeks:", weight="bold"),
                        rx.text("• Delta: How much option price changes when stock moves $1"),
                        rx.text("• Gamma: How much delta changes when stock moves $1"),
                        rx.text("• Theta: How much value option loses per day"),
                        rx.text("• Vega: How much option price changes per 1% volatility change"),
                        rx.text("• Rho: How much option price changes per 1% interest rate change"),
                        spacing="1",
                        align="start",
                    ),
                    icon="info",
                    color_scheme="gray",
                    size="1",
                ),
                
                spacing="5",
                align="start",
                width="100%",
            ),
            padding="6",
            border_radius="12px",
            background="white",
            box_shadow="0 4px 6px -1px rgb(0 0 0 / 0.1)",
            width="100%",
        ),
        rx.fragment(),
    )