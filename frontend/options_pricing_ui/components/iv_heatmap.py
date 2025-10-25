# iv_heatmap.py

"""Implied Volatility Heatmap Component"""

import reflex as rx
from options_pricing_ui.state.options_chain_state import OptionsChainState
from options_pricing_ui.components.left_panel import LeftPanelState


def heatmap_cell(strike: str, iv: str, color: str) -> rx.Component:
    """Single cell in the heatmap."""
    return rx.box(
        rx.vstack(
            rx.text(strike, size="2", weight="bold", color="white"),
            rx.text(iv, size="1", color="white"),
            spacing="1",
            align="center",
        ),
        padding="3",
        border_radius="6px",
        background=color,
        width="100%",
        min_height="70px",
        display="flex",
        align_items="center",
        justify_content="center",
        box_shadow="0 2px 4px rgba(0,0,0,0.1)",
        transition="all 0.2s",
        _hover={
            "transform": "scale(1.05)",
            "box_shadow": "0 4px 8px rgba(0,0,0,0.2)",
        }
    )


def iv_heatmap() -> rx.Component:
    """Implied volatility heatmap visualization."""
    return rx.cond(
        (OptionsChainState.calls.length() > 0) | (OptionsChainState.puts.length() > 0),
        rx.box(
            rx.vstack(
                rx.heading(
                    rx.cond(
                        LeftPanelState.option_type == "calls",
                        "Call Options - Implied Volatility",
                        "Put Options - Implied Volatility"
                    ),
                    size="6", 
                    weight="bold", 
                    color=rx.cond(
                        LeftPanelState.option_type == "calls",
                        "#22c55e",
                        "#ef4444"
                    )
                ),
                
                rx.hstack(
                    rx.text("Low IV", size="1", color="#F5F5F5"),
                    rx.box(width="30px", height="20px", background="#1e3a8a", border_radius="4px"),
                    rx.box(width="30px", height="20px", background="#3b82f6", border_radius="4px"),
                    rx.box(width="30px", height="20px", background="#06b6d4", border_radius="4px"),
                    rx.box(width="30px", height="20px", background="#22c55e", border_radius="4px"),
                    rx.box(width="30px", height="20px", background="#eab308", border_radius="4px"),
                    rx.box(width="30px", height="20px", background="#f97316", border_radius="4px"),
                    rx.box(width="30px", height="20px", background="#dc2626", border_radius="4px"),
                    rx.text("High IV", size="1", color="#F5F5F5"),
                    spacing="2",
                    padding="3",
                    justify="center",
                ),
                
                rx.divider(border_color="rgba(46, 196, 182, 0.2)"),
                
                rx.cond(
                    LeftPanelState.option_type == "calls",
                    rx.grid(
                        rx.foreach(
                            OptionsChainState.calls,
                            lambda opt: heatmap_cell(
                                opt["strike_price"], 
                                opt["implied_volatility"],
                                opt["iv_color"]
                            )
                        ),
                        columns="6",
                        spacing="3",
                        width="100%",
                    ),
                    rx.grid(
                        rx.foreach(
                            OptionsChainState.puts,
                            lambda opt: heatmap_cell(
                                opt["strike_price"],
                                opt["implied_volatility"],
                                opt["iv_color"]
                            )
                        ),
                        columns="6",
                        spacing="3",
                        width="100%",
                    ),
                ),

                spacing="5",
                width="100%",
            ),
            padding="6",
            border_radius="12px",
            background="#0A192F",
            width="100%",
        ),
        rx.box(
            rx.text("Load options data to see IV heatmap", color="#9CA3AF", size="3"),
            padding="6",
        ),
    )