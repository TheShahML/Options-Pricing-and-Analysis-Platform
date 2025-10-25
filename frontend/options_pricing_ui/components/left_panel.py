# left_panel.py

"""Left Panel with Calls/Puts toggle and options table"""

import reflex as rx
from options_pricing_ui.state.options_chain_state import OptionsChainState


class LeftPanelState(rx.State):
    """State for left panel option type selection."""
    option_type: str = "calls"
    
    def set_calls(self):
        self.option_type = "calls"
    
    def set_puts(self):
        self.option_type = "puts"


def options_table_row(option: dict) -> rx.Component:
    """Single row in options table."""
    return rx.table.row(
        rx.table.cell(option["strike_price"], color="#F5F5F5", font_weight="600"),
        rx.table.cell(option["bid"], color="#F5F5F5"),
        rx.table.cell(option["ask"], color="#F5F5F5"),
        rx.table.cell(option["last_price"], color="#F5F5F5"),
        rx.table.cell(option["volume"], color="#F5F5F5"),
        rx.table.cell(option["implied_volatility"], color="#2EC4B6", font_weight="600"),
        background=rx.cond(
            OptionsChainState.selected_strike == option["strike_price"],
            "rgba(46, 196, 182, 0.3)",
            "#0A192F"
        ),
        border_bottom="1px solid rgba(46, 196, 182, 0.1)",
        on_click=OptionsChainState.select_option(option),
        _hover={"background": "rgba(46, 196, 182, 0.15)", "cursor": "pointer"},
    )

def left_panel() -> rx.Component:
    """Left panel with options data."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.button(
                    "Calls",
                    on_click=LeftPanelState.set_calls,
                    variant="solid",
                    size="3",
                    background=rx.cond(LeftPanelState.option_type == "calls", "#22c55e", "#F5F5F5"),
                    color=rx.cond(LeftPanelState.option_type == "calls", "#0A192F", "#1A1A1A"),
                ),
                rx.button(
                    "Puts",
                    on_click=LeftPanelState.set_puts,
                    variant="solid",
                    size="3",
                    background=rx.cond(LeftPanelState.option_type == "puts", "#ef4444", "#F5F5F5"),
                    color=rx.cond(LeftPanelState.option_type == "puts", "#F5F5F5", "#1A1A1A"),
                ),
                spacing="2",
            ),
            
            rx.divider(border_color="rgba(46, 196, 182, 0.2)"),
            
            rx.cond(
                LeftPanelState.option_type == "calls",
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Strike", color="#2EC4B6", font_weight="700"),
                            rx.table.column_header_cell("Bid", color="#2EC4B6", font_weight="700"),
                            rx.table.column_header_cell("Ask", color="#2EC4B6", font_weight="700"),
                            rx.table.column_header_cell("Last", color="#2EC4B6", font_weight="700"),
                            rx.table.column_header_cell("Volume", color="#2EC4B6", font_weight="700"),
                            rx.table.column_header_cell("IV", color="#2EC4B6", font_weight="700"),
                        ),
                        background="#0A192F",
                    ),
                    rx.table.body(
                        rx.foreach(
                            OptionsChainState.calls,
                            options_table_row,
                        ),
                    ),
                    variant="surface",
                    size="2",
                    width="100%",
                    style={
                        "--table-row-background": "#0A192F",
                        "--table-row-background-hover": "rgba(46, 196, 182, 0.15)",
                    },
                ),
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Strike", color="#2EC4B6", font_weight="700"),
                            rx.table.column_header_cell("Bid", color="#2EC4B6", font_weight="700"),
                            rx.table.column_header_cell("Ask", color="#2EC4B6", font_weight="700"),
                            rx.table.column_header_cell("Last", color="#2EC4B6", font_weight="700"),
                            rx.table.column_header_cell("Volume", color="#2EC4B6", font_weight="700"),
                            rx.table.column_header_cell("IV", color="#2EC4B6", font_weight="700"),
                        ),
                        background="#0A192F",
                    ),
                    rx.table.body(
                        rx.foreach(
                            OptionsChainState.puts,
                            options_table_row,
                        ),
                    ),
                    variant="surface",
                    size="2",
                    width="100%",
                    style={"color": "#F5F5F5", "--table-row-background": "#0A192F"}
                ),
            ),
            
            spacing="4",
            width="100%",
        ),
        background="#0A192F",
        border_radius="12px",
        padding="6",
        min_height="85vh",
        overflow_y="auto",
        border="1px solid rgba(46, 196, 182, 0.3)",
    )