FROM python:3.12-slim

WORKDIR /app

# Install Node.js for Reflex
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Initialize Reflex
RUN reflex init

# Expose port
EXPOSE 3000

# Run Reflex
CMD ["./start.sh"]
