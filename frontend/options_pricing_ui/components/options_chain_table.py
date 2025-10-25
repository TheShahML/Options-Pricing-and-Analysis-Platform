# options_chain_table.py Options Chain Table Display Component

"""
Options Chain Table Component

Displays real options data with Black-Scholes comparison.
"""

import reflex as rx
from options_pricing_ui.state.options_chain_state import OptionsChainState


def options_search_bar() -> rx.Component:
    """Search bar for options chain."""
    return rx.box(
        rx.vstack(
            rx.heading("Real Options Chain Analysis", size="8", weight="bold"),
            rx.text(
                "Compare market prices with Black-Scholes theoretical values",
                size="4",
                color="gray",
            ),
            
            rx.hstack(
                rx.input(
                    placeholder="Enter ticker (e.g., AAPL)",
                    value=OptionsChainState.ticker,
                    on_change=OptionsChainState.set_ticker,
                    size="3",
                    width="250px",
                ),
                rx.button(
                    rx.cond(
                        OptionsChainState.loading_expirations | OptionsChainState.loading_chain,
                        rx.spinner(size="3"),
                        "Load Options Chain"
                    ),
                    on_click=OptionsChainState.search_and_load,
                    disabled=OptionsChainState.loading_expirations | OptionsChainState.loading_chain,
                    size="3",
                    color_scheme="blue",
                ),
                spacing="3",
            ),
            
            rx.cond(
                OptionsChainState.available_expirations != [],
                rx.hstack(
                    rx.text("Expiration:", size="3", weight="medium"),
                    rx.select(
                        OptionsChainState.available_expirations,
                        value=OptionsChainState.selected_expiration,
                        on_change=OptionsChainState.set_expiration,
                        size="2",
                    ),
                    rx.button(
                        "Reload Chain",
                        on_click=OptionsChainState.load_options_chain,
                        size="2",
                        variant="soft",
                    ),
                    spacing="3",
                    align="center",
                ),
                rx.fragment(),
            ),
            
            rx.cond(
                OptionsChainState.error_message != "",
                rx.callout(
                    OptionsChainState.error_message,
                    icon="alert-triangle",
                    color_scheme="red",
                    size="2",
                ),
                rx.fragment(),
            ),
            
            spacing="4",
            align="start",
        ),
        padding="6",
        border_radius="12px",
        background="white",
        box_shadow="0 4px 6px -1px rgb(0 0 0 / 0.1)",
        width="100%",
    )


def option_row(option: dict, option_type: str) -> rx.Component:
    """Single row in options table."""
    return rx.table.row(
        rx.table.cell(option["strike_price"]),
        rx.table.cell(option["bid"]),
        rx.table.cell(option["ask"]),
        rx.table.cell(option["last_price"]),
        rx.table.cell(option["bs_price"]),
        rx.table.cell(
            option["difference"],
            color=rx.cond(
                option["difference_color"] == "green",
                "var(--green-11)",
                rx.cond(
                    option["difference_color"] == "red",
                    "var(--red-11)",
                    "inherit"
                )
            ),
            weight="bold",
        ),
        rx.table.cell(option["volume"]),
        rx.table.cell(option["implied_volatility"]),
    )


def options_table(options: list, title: str) -> rx.Component:
    """Options table display."""
    return rx.box(
        rx.vstack(
            rx.heading(title, size="6", weight="bold"),
            
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Strike"),
                        rx.table.column_header_cell("Bid"),
                        rx.table.column_header_cell("Ask"),
                        rx.table.column_header_cell("Last"),
                        rx.table.column_header_cell("BS Price"),
                        rx.table.column_header_cell("Diff"),
                        rx.table.column_header_cell("Volume"),
                        rx.table.column_header_cell("Implied Vol"),
                    ),
                ),
                rx.table.body(
                    rx.foreach(
                        options,
                        lambda opt: option_row(opt, title.lower())
                    )
                ),
                width="100%",
                variant="surface",
            ),
            
            spacing="4",
            width="100%",
        ),
        padding="6",
        border_radius="12px",
        background="white",
        box_shadow="0 4px 6px -1px rgb(0 0 0 / 0.1)",
        width="100%",
    )


def options_chain_display() -> rx.Component:
    """Main options chain display."""
    return rx.cond(
        (OptionsChainState.calls != []) | (OptionsChainState.puts != []),
        rx.vstack(
            rx.callout(
                rx.hstack(
                    rx.text(f"Current Stock Price: ${OptionsChainState.current_price:.2f}", weight="bold"),
                    rx.text(f"Expiration: {OptionsChainState.selected_expiration}"),
                    spacing="4",
                ),
                icon="info",
                color_scheme="blue",
                size="2",
            ),
            
            # Full width tables (no grid, stacked vertically)
            rx.vstack(
                options_table(OptionsChainState.calls, "Call Options"),
                options_table(OptionsChainState.puts, "Put Options"),
                spacing="6",
                width="100%",
            ),
            
            spacing="6",
            width="100%",
        ),
        rx.cond(
            OptionsChainState.loading_chain,
            rx.box(
                rx.vstack(
                    rx.spinner(size="3"),
                    rx.text("Loading options chain...", size="3"),
                    spacing="3",
                    align="center",
                ),
                padding="12",
                width="100%",
            ),
            rx.fragment(),
        ),
    )