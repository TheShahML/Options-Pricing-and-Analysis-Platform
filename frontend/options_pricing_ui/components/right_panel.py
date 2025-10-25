# right_panel.py
"""Right Panel with Greeks, IV Heatmap, and Calculator tabs"""
import reflex as rx
from options_pricing_ui.components.greeks_chart import greeks_chart
from options_pricing_ui.components.option_inputs import option_inputs
from options_pricing_ui.components.iv_heatmap import iv_heatmap


class RightPanelState(rx.State):
    """State for right panel tab selection."""
    active_tab: str = "greeks"
   
    def set_greeks(self):
        self.active_tab = "greeks"
   
    def set_heatmap(self):
        self.active_tab = "heatmap"
   
    def set_calculator(self):
        self.active_tab = "calculator"


def right_panel() -> rx.Component:
    """Right panel with tabbed interface."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.button(
                    "Greeks",
                    on_click=RightPanelState.set_greeks,
                    variant="solid",
                    size="3",
                    background=rx.cond(RightPanelState.active_tab == "greeks", "#2EC4B6", "#F5F5F5"),
                    color=rx.cond(RightPanelState.active_tab == "greeks", "#0A192F", "#1A1A1A"),
                ),
                rx.button(
                    "IV Heatmap",
                    on_click=RightPanelState.set_heatmap,
                    variant="solid",
                    size="3",
                    background=rx.cond(RightPanelState.active_tab == "heatmap", "#2EC4B6", "#F5F5F5"),
                    color=rx.cond(RightPanelState.active_tab == "heatmap", "#0A192F", "#1A1A1A"),
                ),
                rx.button(
                    "Calculator",
                    on_click=RightPanelState.set_calculator,
                    variant="solid",
                    size="3",
                    background=rx.cond(RightPanelState.active_tab == "calculator", "#2EC4B6", "#F5F5F5"),
                    color=rx.cond(RightPanelState.active_tab == "calculator", "#0A192F", "#1A1A1A"),
                ),
                spacing="2",
                width="100%",
                justify="center",
            ),
           
            rx.divider(border_color="rgba(46, 196, 182, 0.2)"),
           
            rx.cond(
                RightPanelState.active_tab == "greeks",
                greeks_chart(),
                rx.cond(
                    RightPanelState.active_tab == "heatmap",
                    iv_heatmap(),
                    option_inputs(),
                ),
            ),
           
            spacing="4",
            width="100%",
            height="100%",
        ),
        background="#0A192F",
        border_radius="12px",
        padding="6",
        min_height="85vh",
        overflow_y="auto",
        border="1px solid rgba(46, 196, 182, 0.3)",
    )