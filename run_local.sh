#!/bin/bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}Setting up radextract development environment${NC}"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
if [ "$1" = "dev" ]; then
    echo -e "${YELLOW}Installing with development dependencies...${NC}"
    pip install -e ".[dev]"
else
    pip install -e .
fi

# Check if env.list exists
if [ ! -f "env.list" ]; then
    echo -e "${RED}Error: env.list file not found!${NC}"
    echo -e "${YELLOW}Please create env.list with required environment variables${NC}"
    exit 1
fi

# Load environment variables
echo -e "${YELLOW}Loading environment variables...${NC}"
export $(cat env.list | xargs)

# Start the application
echo -e "${GREEN}Starting radextract application on http://localhost:7870${NC}"
python app.py
