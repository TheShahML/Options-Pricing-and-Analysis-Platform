# option_inputs.py

"""
Option Inputs Component
Form for entering option parameters and displaying results.
"""
import reflex as rx
from options_pricing_ui.state.app_state import AppState
from options_pricing_ui.state.options_chain_state import OptionsChainState


def input_field(
    label: str,
    value: str,
    on_change: callable,
    placeholder: str = "",
    type: str = "number",
) -> rx.Component:
    """Input field with label."""
    return rx.vstack(
        rx.text(label, size="3", weight="medium", color="#F5F5F5"),
        rx.input(
            value=value,
            on_change=on_change,
            placeholder=placeholder,
            type=type,
            size="3",
            width="100%",
            background="#F5F5F5",
            color="#0A192F",
            border="1px solid rgba(46, 196, 182, 0.3)",
            _focus={"border": "1px solid #2EC4B6"},
        ),
        spacing="2",
        align="start",
        width="100%",
    )


def option_inputs() -> rx.Component:
    """Option parameters input form with results."""
    return rx.box(
        rx.vstack(
            # Header
            rx.heading("Black-Scholes Calculator", size="6", weight="bold", color="#F5F5F5"),
            rx.text(
                "Click any option on the left to auto-fill, or enter custom values",
                size="2",
                color="#9CA3AF",
                font_style="italic",
            ),
            rx.divider(border_color="rgba(46, 196, 182, 0.2)"),
            
            # Selected option indicator with load button
            rx.cond(
                OptionsChainState.selected_strike != "",
                rx.hstack(
                    rx.callout(
                        rx.text(
                            f"Selected: {OptionsChainState.selected_strike} - Strike: {OptionsChainState.selected_option['strike_raw']}, IV: {OptionsChainState.selected_option['iv_raw']}",
                            weight="bold",
                            size="1",
                        ),
                        icon="check",
                        color_scheme="teal",
                        size="1",
                    ),
                    rx.button(
                        "Use These Values",
                        size="1",
                        on_click=OptionsChainState.load_selected_to_inputs,
                        background="#2EC4B6",
                        color="#0A192F",
                    ),
                    spacing="2",
                    align="center",
                    width="100%",
                ),
                rx.fragment(),
            ),
            
            # Option type selector
            rx.vstack(
                rx.text("Option Type", size="3", weight="medium", color="#F5F5F5"),
                rx.box(
                    rx.radio(
                        ["Call", "Put"],
                        default_value="Call",
                        on_change=lambda v: AppState.set_option_type(v.lower()),
                        size="2",
                        direction="row",
                        color_scheme="teal",
                    ),
                    style={"color": "#F5F5F5"},
                ),
                spacing="2",
                align="start",
                width="100%",
            ),
            
            # Strike Price and Time to Expiration
            rx.grid(
                input_field(
                    "Strike Price ($)",
                    AppState.strike_price.to(str),
                    AppState.set_strike_price,
                    "105.00",
                ),
                input_field(
                    "Time to Expiration (years)",
                    AppState.time_to_expiration.to(str),
                    AppState.set_time_to_expiration,
                    "0.25",
                ),
                columns="2",
                spacing="4",
                width="100%",
            ),
            
            # Volatility and Risk-Free Rate
            rx.grid(
                input_field(
                    "Volatility (σ)",
                    AppState.volatility.to(str),
                    AppState.set_volatility,
                    "0.20",
                ),
                input_field(
                    "Risk-Free Rate (r)",
                    AppState.risk_free_rate.to(str),
                    AppState.set_risk_free_rate,
                    "0.045",
                ),
                columns="2",
                spacing="4",
                width="100%",
            ),
            
            # Tips box
            rx.box(
                rx.vstack(
                    rx.text("💡 Tips:", weight="bold", color="#2EC4B6", size="2"),
                    rx.text("• Click options on left for quick calculations", color="#9CA3AF", size="1"),
                    rx.text("• Stock price and volatility auto-fill from market data", color="#9CA3AF", size="1"),
                    rx.text("• Adjust any value for custom scenarios", color="#9CA3AF", size="1"),
                    spacing="1",
                    align="start",
                ),
                padding="3",
                border_radius="8px",
                background="#1A1A1A",
                border="1px solid rgba(46, 196, 182, 0.2)",
            ),
            
            # Calculate button
            rx.button(
                rx.cond(
                    AppState.calculation_loading,
                    rx.hstack(
                        rx.spinner(size="3"),
                        rx.text("Calculating..."),
                        spacing="2",
                    ),
                    "Calculate Option Price & Greeks",
                ),
                on_click=AppState.validate_and_calculate,
                disabled=AppState.calculation_loading,
                size="3",
                width="100%",
                background="#2EC4B6",
                color="#0A192F",
                font_weight="600",
                _hover={"background": "#3DD5C7"},
            ),
            
            # Validation error message
            rx.cond(
                AppState.validation_error != "",
                rx.callout(
                    AppState.validation_error,
                    icon="alert-circle",
                    color_scheme="red",
                    size="1",
                ),
                rx.fragment(),
            ),
            
            # Results section
            rx.cond(
                AppState.show_results,
                rx.vstack(
                    rx.divider(border_color="rgba(46, 196, 182, 0.2)"),
                    
                    # Option Price Result
                    rx.heading("Calculated Results", size="5", weight="bold", color="#F5F5F5"),
                    rx.text(
                        "Based on Black-Scholes model with your custom inputs",
                        size="1",
                        color="#9CA3AF",
                        font_style="italic",
                    ),
                    
                    rx.box(
                        rx.vstack(
                            rx.text("Option Price", size="2", color="#9CA3AF"),
                            rx.heading(
                                f"${AppState.option_price:.4f}",
                                size="8",
                                weight="bold",
                                color="#2EC4B6",
                            ),
                            rx.text(
                                rx.cond(
                                    AppState.option_type == "call",
                                    "Call Option",
                                    "Put Option"
                                ),
                                size="2",
                                color="#9CA3AF",
                            ),
                            spacing="1",
                            align="center",
                        ),
                        padding="5",
                        border_radius="8px",
                        background="#1A1A1A",
                        border="2px solid #2EC4B6",
                        width="100%",
                    ),
                    
                    # Calculated Greeks
                    rx.heading("Calculated Greeks", size="4", weight="bold", color="#F5F5F5"),
                    rx.text(
                        "Note: These are calculated Greeks from your custom inputs, not the market Greeks shown in the Greeks tab",
                        size="1",
                        color="#9CA3AF",
                        font_style="italic",
                    ),
                    
                    rx.vstack(
                        rx.grid(
                            rx.vstack(
                                rx.text("Delta (Δ)", size="2", color="#9CA3AF", weight="medium"),
                                rx.text(f"{AppState.greeks.get('delta', 0):.4f}", size="4", weight="bold", color="#F5F5F5"),
                                rx.text("Price sensitivity", size="1", color="#6B7280"),
                                spacing="1",
                                align="start",
                            ),
                            rx.vstack(
                                rx.text("Gamma (Γ)", size="2", color="#9CA3AF", weight="medium"),
                                rx.text(f"{AppState.greeks.get('gamma', 0):.4f}", size="4", weight="bold", color="#F5F5F5"),
                                rx.text("Delta change rate", size="1", color="#6B7280"),
                                spacing="1",
                                align="start",
                            ),
                            rx.vstack(
                                rx.text("Theta (Θ)", size="2", color="#9CA3AF", weight="medium"),
                                rx.text(f"{AppState.greeks.get('theta', 0):.4f}", size="4", weight="bold", color="#F5F5F5"),
                                rx.text("Time decay/day", size="1", color="#6B7280"),
                                spacing="1",
                                align="start",
                            ),
                            columns="3",
                            spacing="4",
                            width="100%",
                        ),
                        rx.grid(
                            rx.vstack(
                                rx.text("Vega (ν)", size="2", color="#9CA3AF", weight="medium"),
                                rx.text(f"{AppState.greeks.get('vega', 0):.4f}", size="4", weight="bold", color="#F5F5F5"),
                                rx.text("Vol sensitivity", size="1", color="#6B7280"),
                                spacing="1",
                                align="start",
                            ),
                            rx.vstack(
                                rx.text("Rho (ρ)", size="2", color="#9CA3AF", weight="medium"),
                                rx.text(f"{AppState.greeks.get('rho', 0):.4f}", size="4", weight="bold", color="#F5F5F5"),
                                rx.text("Rate sensitivity", size="1", color="#6B7280"),
                                spacing="1",
                                align="start",
                            ),
                            columns="2",
                            spacing="4",
                            width="100%",
                        ),
                        spacing="3",
                        padding="4",
                        border_radius="8px",
                        background="#1A1A1A",
                        border="1px solid rgba(46, 196, 182, 0.2)",
                        width="100%",
                    ),
                    
                    spacing="4",
                    width="100%",
                ),
                rx.fragment(),
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