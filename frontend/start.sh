#!/bin/bash

# Initialize Reflex (generates .web folder)
reflex init

# Patch vite.config.js to allow our domain
sed -i 's/server: {/server: {\n    allowedHosts: ["theshahml.com", "www.theshahml.com", "localhost", ".theshahml.com"],/' .web/vite.config.js

# Start Reflex
reflex run --loglevel info
