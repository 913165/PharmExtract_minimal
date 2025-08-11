#!/bin/bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}Setting up radextract with Docker${NC}"

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo -e "${RED}Error: Docker is not running. Please start Docker Desktop.${NC}"
    exit 1
fi

# Check if env.list exists
if [ ! -f "env.list" ]; then
    echo -e "${RED}Error: env.list file not found!${NC}"
    echo "Please create env.list with your API keys and configuration."
    exit 1
fi

# Stop and remove existing container if it exists
echo -e "${YELLOW}Cleaning up existing containers...${NC}"
docker stop radiology-report-app 2>/dev/null || true
docker rm radiology-report-app 2>/dev/null || true

# Build the Docker image
echo -e "${YELLOW}Building Docker image...${NC}"
docker build -t radiology-report-app .

# Run the container
echo -e "${YELLOW}Starting application in Docker container...${NC}"
docker run -d \
    --name radiology-report-app \
    --env-file env.list \
    -p 7870:7870 \
    -v "$(pwd)/cache:/app/cache" \
    radiology-report-app

# Wait for the application to start
echo -e "${YELLOW}Waiting for application to start...${NC}"
sleep 5

# Check if the application is running
if curl -s http://localhost:7870/ >/dev/null; then
    echo -e "${GREEN}Application is running at http://localhost:7870/${NC}"
    echo ""
    echo "To view logs: docker logs -f radiology-report-app"
    echo "To stop: docker stop radiology-report-app"
    echo "To restart: docker restart radiology-report-app"
else
    echo -e "${RED}Application failed to start. Check logs with: docker logs radiology-report-app${NC}"
    exit 1
fi 