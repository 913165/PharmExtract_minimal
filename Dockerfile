# Use a base image with Python
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
# RUN apt-get update && apt-get install -y --no-install-recommends git procps libmagic1 curl \
#    && rm -rf /var/lib/apt/lists/*

# Copy the project configuration
COPY pyproject.toml /app/

# Environment variables
ENV HOME=/tmp
ENV APP_MODULE=app:app

# Install dependencies
RUN pip install --no-cache-dir -e .

# Copy all application files
COPY . /app/

# Expose the ports
EXPOSE 7870

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:7870/cache/stats || exit 1

# Copy and use the startup script
COPY start.sh /app/
RUN chmod +x /app/start.sh

# Name the image
LABEL org.opencontainers.image.title="PharmExtract"

CMD ["/app/start.sh"]
