# info_panel.py Info Panel Component
"""
Info Panel Component
Educational information about options and how to use the platform.
"""
import reflex as rx


def info_panel() -> rx.Component:
    """Information panel explaining options and platform usage."""
    return rx.box(
        rx.vstack(
            # Main heading
            rx.heading(
                "Options Pricing & Analysis Platform",
                size="8",
                weight="bold",
                color="#F5F5F5",
            ),
            
            # Subtitle
            rx.text(
                "Real-time options data with Black-Scholes pricing and Greeks analysis",
                size="3",
                color="#9CA3AF",
            ),
            
            rx.divider(border_color="rgba(46, 196, 182, 0.2)"),
            
            # Two column layout - stacks on mobile
            rx.grid(
                # Left column - What are options
                rx.box(
                    rx.vstack(
                        rx.text(
                            "What are Options?",
                            size="4",
                            weight="bold",
                            color="#2EC4B6",
                        ),
                        rx.text(
                            "Options are financial derivatives that give buyers the right, but not the obligation, to buy or sell an underlying asset at a predetermined price (strike price) before a specific expiration date.",
                            size="2",
                            color="#D1D5DB",
                            line_height="1.6",
                        ),
                        rx.text(
                            "Call options grant the right to buy, while put options grant the right to sell. Options are used for hedging risk, speculation, and income generation.",
                            size="2",
                            color="#D1D5DB",
                            line_height="1.6",
                        ),
                        spacing="2",
                        align="start",
                    ),
                    padding="4",
                    border_radius="8px",
                    background="#1A1A1A",
                    border="1px solid rgba(46, 196, 182, 0.2)",
                ),
                
                # Right column - How to use platform
                rx.box(
                    rx.vstack(
                        rx.text(
                            "How to Use This Platform",
                            size="4",
                            weight="bold",
                            color="#2EC4B6",
                        ),
                        rx.text(
                            "1. Enter a ticker symbol to load real-time options chain data",
                            size="2",
                            color="#D1D5DB",
                        ),
                        rx.text(
                            "2. Select an expiration date and view available options with market prices",
                            size="2",
                            color="#D1D5DB",
                        ),
                        rx.text(
                            "3. Analyze market Greeks to understand how options respond to changes",
                            size="2",
                            color="#D1D5DB",
                        ),
                        rx.text(
                            "4. View IV Heatmap to identify volatility patterns across strikes",
                            size="2",
                            color="#D1D5DB",
                        ),
                        rx.text(
                            "5. Use Calculator for custom Black-Scholes pricing with theoretical Greeks",
                            size="2",
                            color="#D1D5DB",
                        ),
                        spacing="2",
                        align="start",
                    ),
                    padding="4",
                    border_radius="8px",
                    background="#1A1A1A",
                    border="1px solid rgba(46, 196, 182, 0.2)",
                ),
                
                columns=rx.breakpoints(initial="1", md="2"),  # 1 column on mobile, 2 on desktop
                spacing="4",
                width="100%",
            ),
            
            # Disclaimer
            rx.box(
                rx.text(
                    "Disclaimer: This platform is for educational and informational purposes only. Options trading involves substantial risk and is not suitable for all investors. Past performance does not guarantee future results. This is not financial advice. Please consult with a licensed financial advisor before making investment decisions.",
                    size="1",
                    color="#9CA3AF",
                    font_style="italic",
                    text_align="center",
                ),
                padding="3",
                border_radius="8px",
                background="#1A1A1A",
                border="1px solid rgba(239, 68, 68, 0.3)",
                width="100%",
            ),
            
            spacing="4",
            align="start",
            width="100%",
        ),
        padding="6",
        border_radius="12px",
        background="#0A192F",
        width="100%",
        border="1px solid rgba(46, 196, 182, 0.3)",
        margin_bottom="4",
    )