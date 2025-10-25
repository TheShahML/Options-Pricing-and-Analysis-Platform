# top_panel.py

"""Top Panel with Stock Search and Metrics"""

import reflex as rx
from options_pricing_ui.state.options_chain_state import OptionsChainState


def top_panel() -> rx.Component:
    """Top panel with stock search and current metrics."""
    return rx.box(
        rx.center(
            rx.vstack(
                rx.hstack(
                    rx.input(
                        placeholder="Enter ticker (e.g., AAPL)",
                        value=OptionsChainState.ticker,
                        on_change=OptionsChainState.set_ticker,
                        size="3",
                        width="250px",
                        background="#F5F5F5",
                        color="#0A192F",
                        border="1px solid rgba(46, 196, 182, 0.4)",
                        _focus={"border": "1px solid #2EC4B6"},
                    ),
                    rx.button(
                        "Load Options",
                        on_click=OptionsChainState.search_and_load,
                        loading=OptionsChainState.loading_chain,
                        size="3",
                        background="#2EC4B6",
                        color="#0A192F",
                        font_weight="600",
                        _hover={"background": "#3DD5C7"},
                    ),
                    rx.cond(
                        OptionsChainState.available_expirations.length() > 0,
                        rx.select(
                            OptionsChainState.available_expirations,
                            value=OptionsChainState.selected_expiration,
                            on_change=OptionsChainState.set_expiration,
                            size="3",
                            placeholder="Select expiration",
                            background="#F5F5F5",
                            color="#0A192F",
                        ),
                        rx.fragment(),
                    ),
                    rx.cond(
                        OptionsChainState.selected_expiration != "",
                        rx.button(
                            "Reload Chain",
                            on_click=OptionsChainState.load_options_chain,
                            size="3",
                            variant="soft",
                            color_scheme="blue",
                        ),
                        rx.fragment(),
                    ),
                    spacing="3",
                    align="center",
                ),
                
                rx.cond(
                    OptionsChainState.error_message != "",
                    rx.callout(
                        OptionsChainState.error_message,
                        icon="alert-circle",
                        color_scheme="red",
                        size="2",
                    ),
                    rx.fragment(),
                ),
                
                rx.cond(
                    OptionsChainState.current_price > 0,
                    rx.hstack(
                        rx.vstack(
                            rx.text("Current Price", size="2", color="#9CA3AF"),
                            rx.text(f"${OptionsChainState.current_price:.2f}", size="5", weight="bold", color="#2EC4B6"),
                            spacing="1",
                        ),
                        rx.divider(orientation="vertical", size="4"),
                        rx.vstack(
                            rx.text("Ticker", size="2", color="#9CA3AF"),
                            rx.text(OptionsChainState.ticker, size="5", weight="bold", color="#F5F5F5"),
                            spacing="1",
                        ),
                        rx.divider(orientation="vertical", size="4"),
                        rx.vstack(
                            rx.text("Expiration", size="2", color="#9CA3AF"),
                            rx.text(OptionsChainState.selected_expiration, size="4", color="#F5F5F5"),
                            spacing="1",
                        ),
                        rx.divider(orientation="vertical", size="4"),
                        rx.vstack(
                            rx.text("Risk-Free Rate", size="2", color="#9CA3AF"),
                            rx.text(f"{OptionsChainState.risk_free_rate * 100:.2f}%", size="4", weight="bold", color="#F59E0B"),
                            rx.text(f"({OptionsChainState.treasury_maturity} Treasury)", size="1", color="#6B7280", font_style="italic"),
                            spacing="1",
                        ),
                        spacing="6",
                        padding="4",
                        border_radius="8px",
                        background="#0A192F",
                        border="1px solid rgba(46, 196, 182, 0.2)",
                    ),
                    rx.fragment(),
                ),
                
                spacing="4",
                align="center",
            ),
        ),
        background="#0A192F",
        border_radius="12px",
        padding="6",
        border="1px solid rgba(46, 196, 182, 0.3)",
        width="100%",
    )