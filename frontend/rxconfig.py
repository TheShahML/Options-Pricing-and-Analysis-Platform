# rxconfig.py React configuration file

import reflex as rx

config = rx.Config(
    app_name="options_pricing_ui",
    # Frontend port
    frontend_port=3000,
    # Backend port (Reflex internal websocket server)
    backend_port=8001,
    # Disable sitemap plugin warning
    disable_plugins=["reflex.plugins.sitemap.SitemapPlugin"],
)