# options_chain.py

"""Options Chain Page"""

import reflex as rx
from options_pricing_ui.components.navbar import navbar
from options_pricing_ui.components.options_chain_table import (
    options_search_bar,
    options_chain_display,
)
from options_pricing_ui.components.iv_heatmap import iv_heatmap


def chain() -> rx.Component:
    """Options chain analysis page."""
    return rx.fragment(
        navbar(),

        rx.box(
            rx.container(
                rx.vstack(
                    options_search_bar(),
                    options_chain_display(),
                    iv_heatmap(),

                    spacing="6",
                    width="100%",
                    padding_y="8",
                ),
                max_width="1400px",
            ),
            background="linear-gradient(135deg, var(--slate-2) 0%, var(--blue-2) 100%)",
            min_height="100vh",
            width="100%",
        ),
    )