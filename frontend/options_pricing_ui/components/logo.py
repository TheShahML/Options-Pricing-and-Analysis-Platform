# logo.py

"""TheShahML Logo Component"""

import reflex as rx


def logo() -> rx.Component:
    """TheShahML text logo with teal to purple gradient."""
    return rx.link(
        rx.text(
            "TheShahML",
            font_family="'Inter', 'SF Pro Display', system-ui, sans-serif",
            font_size="28px",
            font_weight="700",
            letter_spacing="-0.5px",
            style={
                "background": "linear-gradient(135deg, #2EC4B6 0%, #764ba2 100%)",
                "-webkit-background-clip": "text",
                "-webkit-text-fill-color": "transparent",
                "background-clip": "text",
            }
        ),
        href="/",
        _hover={"opacity": "0.8"},
        transition="opacity 0.2s",
    )