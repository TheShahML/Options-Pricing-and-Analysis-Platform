# payoff_diagram.py

"""
Payoff Diagram Component

Visualizes option payoff at expiration.
"""

import reflex as rx
from options_pricing_ui.state.app_state import AppState


def payoff_diagram() -> rx.Component:
    """Option payoff diagram."""
    return rx.cond(
        AppState.show_results,
        rx.box(
            rx.vstack(
                rx.heading("Payoff Diagram at Expiration", size="6", weight="bold"),
                rx.text(
                    "Profit/Loss at different spot prices at expiration",
                    size="3",
                    color="gray",
                ),
                rx.divider(),
                
                rx.callout(
                    rx.vstack(
                        rx.text("Payoff Diagram Explanation:", weight="bold"),
                        rx.cond(
                            AppState.option_type == "call",
                            rx.vstack(
                                rx.text("• Call Option: Profit when spot price > strike price"),
                                rx.text(f"• Maximum Loss: ${AppState.option_price:.2f} (premium paid)"),
                                rx.text(f"• Breakeven: ${AppState.strike_price + AppState.option_price:.2f}"),
                                rx.text(f"• Current Strike: ${AppState.strike_price:.2f}"),
                                spacing="1",
                                align="start",
                            ),
                            rx.vstack(
                                rx.text("• Put Option: Profit when spot price < strike price"),
                                rx.text(f"• Maximum Loss: ${AppState.option_price:.2f} (premium paid)"),
                                rx.text(f"• Breakeven: ${AppState.strike_price - AppState.option_price:.2f}"),
                                rx.text(f"• Current Strike: ${AppState.strike_price:.2f}"),
                                spacing="1",
                                align="start",
                            ),
                        ),
                        spacing="2",
                        align="start",
                    ),
                    icon="info",
                    color_scheme="blue",
                    size="1",
                ),
                
                spacing="4",
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