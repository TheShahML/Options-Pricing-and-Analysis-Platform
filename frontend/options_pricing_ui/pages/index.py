# index.py
"""Options Explorer - Main Landing Page"""
import reflex as rx
from options_pricing_ui.components.navbar import navbar
from options_pricing_ui.components.info_panel import info_panel
from options_pricing_ui.components.top_panel import top_panel
from options_pricing_ui.components.left_panel import left_panel
from options_pricing_ui.components.right_panel import right_panel


def index() -> rx.Component:
    """Options Explorer page with responsive layout."""
    return rx.fragment(
        navbar(),
       
        rx.box(
            rx.vstack(
                info_panel(),
                top_panel(),
               
                # Responsive layout - stacks on mobile, side-by-side on desktop
                rx.box(
                    # Left panel - options table
                    rx.box(
                        left_panel(),
                        width=["100%", "100%", "100%", "50%"],  # Mobile: 100%, Desktop: 50%
                        margin_bottom=["4", "4", "4", "0"],  # Add margin on mobile
                    ),
                    # Right panel - tabs
                    rx.box(
                        right_panel(),
                        width=["100%", "100%", "100%", "50%"],  # Mobile: 100%, Desktop: 50%
                    ),
                    display="flex",
                    flex_direction=["column", "column", "column", "row"],  # Stack on mobile, row on desktop
                    gap="5",
                    width="100%",
                    align_items="start",
                ),
               
                spacing="4",
                width=["100%", "100%", "98%", "98%"],
                padding_x=["2", "2", "1%", "1%"],
                padding_y="4",
            ),
            background="#1A1A1A",
            min_height="100vh",
            width="100%",
        ),
    )