"""
Navbar Component
"""
import reflex as rx
from options_pricing_ui.components.logo import logo


def navbar() -> rx.Component:
    """Navigation bar component."""
    return rx.box(
        rx.hstack(
            logo(),
            rx.spacer(),
            rx.hstack(
                rx.link(
                    rx.hstack(
                        rx.icon("github", size=20),
                        rx.text("GitHub", size="2", color="#F5F5F5"),
                        spacing="2",
                        align="center",
                    ),
                    href="https://github.com/TheShahML",
                    target="_blank",
                    _hover={"color": "#2EC4B6"},
                ),
                rx.link(
                    rx.hstack(
                        rx.icon("linkedin", size=20),
                        rx.text("LinkedIn", size="2", color="#F5F5F5"),
                        spacing="2",
                        align="center",
                    ),
                    href="https://linkedin.com/in/shahmirjaved",
                    target="_blank",
                    _hover={"color": "#2EC4B6"},
                ),
                spacing="4",
                align="center",
            ),
            justify="between",
            align="center",
            width=["100%", "100%", "98%", "98%"],
            padding_x=["2", "2", "1%", "1%"],
        ),
        position="sticky",
        top="0",
        z_index="50",
        padding_y="6",
        padding_x="6",
        background="#0A192F",
        border_bottom="1px solid rgba(46, 196, 182, 0.1)",
        width="100%",
        box_shadow="0 4px 6px -1px rgb(0 0 0 / 0.3)",
    )
