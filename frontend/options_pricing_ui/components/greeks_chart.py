# greeks_chart.py Greeks Chart Component
"""
Greeks Chart Component
Displays Greeks for the selected option from the options chain.
"""
import reflex as rx
from options_pricing_ui.state.options_chain_state import OptionsChainState


def greek_card(name: str, symbol: str, value: str, description: str, color: str = "#2EC4B6") -> rx.Component:
    """Display individual Greek metric card."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text(f"{name} ({symbol})", size="3", weight="bold", color="#F5F5F5"),
                spacing="2",
                align="center",
            ),
            rx.heading(
                value,
                size="7",
                weight="bold",
                color=color,
            ),
            rx.text(description, size="1", color="#9CA3AF"),
            spacing="2",
            align="start",
        ),
        padding="4",
        border_radius="8px",
        background="#1A1A1A",
        border=f"1px solid {color}",
        width="100%",
    )


def greeks_chart() -> rx.Component:
    """Greeks display for selected option."""
    return rx.box(
        rx.vstack(
            rx.heading("Market Greeks", size="6", weight="bold", color="#F5F5F5"),
            rx.text(
                "Click any option on the left to view its Greeks from real market data",
                size="2",
                color="#9CA3AF",
                font_style="italic",
            ),
            rx.divider(border_color="rgba(46, 196, 182, 0.2)"),
            
            # Educational callout
            rx.box(
                rx.vstack(
                    rx.text("Understanding Greeks", weight="bold", color="#2EC4B6", size="2"),
                    rx.text("Delta: Price sensitivity to underlying movement", color="#9CA3AF", size="1"),
                    rx.text("Gamma: Rate of change of Delta", color="#9CA3AF", size="1"),
                    rx.text("Theta: Time decay per day", color="#9CA3AF", size="1"),
                    rx.text("Vega: Volatility sensitivity", color="#9CA3AF", size="1"),
                    rx.text("Rho: Interest rate sensitivity", color="#9CA3AF", size="1"),
                    spacing="1",
                    align="start",
                ),
                padding="3",
                border_radius="8px",
                background="#1A1A1A",
                border="1px solid rgba(46, 196, 182, 0.2)",
            ),
            
            # Greeks display - only show if option is selected
            rx.cond(
                OptionsChainState.selected_strike != "",
                rx.vstack(
                    rx.callout(
                        rx.text(
                            f"Showing Greeks for {OptionsChainState.selected_strike}",
                            weight="bold",
                        ),
                        icon="check-circle",
                        color_scheme="teal",
                        size="1",
                    ),
                    
                    # Greeks grid
                    rx.grid(
                        greek_card(
                            "Delta",
                            "Δ",
                            rx.cond(
                                OptionsChainState.selected_option.get("has_greeks"),
                                OptionsChainState.selected_option.get('delta', 0),
                                "N/A"
                            ),
                            "Price sensitivity to $1 stock move",
                            "#3B82F6",
                        ),
                        greek_card(
                            "Gamma",
                            "Γ",
                            rx.cond(
                                OptionsChainState.selected_option.get("has_greeks"),
                                OptionsChainState.selected_option.get('gamma', 0),
                                "N/A"
                            ),
                            "Delta change rate",
                            "#8B5CF6",
                        ),
                        greek_card(
                            "Theta",
                            "Θ",
                            rx.cond(
                                OptionsChainState.selected_option.get("has_greeks"),
                                OptionsChainState.selected_option.get('theta', 0),
                                "N/A"
                            ),
                            "Daily time decay",
                            "#EF4444",
                        ),
                        columns="3",
                        spacing="4",
                        width="100%",
                    ),
                    
                    rx.grid(
                        greek_card(
                            "Vega",
                            "ν",
                            rx.cond(
                                OptionsChainState.selected_option.get("has_greeks"),
                                OptionsChainState.selected_option.get('vega', 0),
                                "N/A"
                            ),
                            "Volatility sensitivity",
                            "#F59E0B",
                        ),
                        greek_card(
                            "Rho",
                            "ρ",
                            rx.cond(
                                OptionsChainState.selected_option.get("has_greeks"),
                                OptionsChainState.selected_option.get('rho', 0),
                                "N/A"
                            ),
                            "Interest rate sensitivity",
                            "#2EC4B6",
                        ),
                        columns="2",
                        spacing="4",
                        width="100%",
                    ),
                    
                    rx.box(
                        rx.text(
                            "Note: Market-derived Greeks from real options data",
                            size="1",
                            color="#9CA3AF",
                            font_style="italic",
                        ),
                        padding="3",
                        border_radius="8px",
                        background="#1A1A1A",
                        border="1px solid rgba(46, 196, 182, 0.2)",
                    ),
                    
                    spacing="4",
                    width="100%",
                ),
                # Message when no option selected
                rx.box(
                    rx.vstack(
                        rx.text(
                            "No Option Selected",
                            size="4",
                            weight="bold",
                            color="#F5F5F5",
                        ),
                        rx.text(
                            "Select an option from the table to view its Greeks",
                            size="2",
                            color="#9CA3AF",
                        ),
                        spacing="2",
                        align="center",
                    ),
                    padding="8",
                    border_radius="8px",
                    background="#1A1A1A",
                    border="2px dashed rgba(46, 196, 182, 0.3)",
                    width="100%",
                ),
            ),
            
            spacing="5",
            align="start",
            width="100%",
        ),
        padding="6",
        border_radius="12px",
        background="#0A192F",
        width="100%",
        border="1px solid rgba(46, 196, 182, 0.3)",
    )