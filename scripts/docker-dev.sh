#!/usr/bin/env bash
set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Paper Trail - Docker Development Environment${NC}\n"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed${NC}"
    echo "Please install Docker from https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is available
if ! docker compose version &> /dev/null; then
    echo -e "${RED}Error: Docker Compose is not available${NC}"
    echo "Please install Docker Compose or update Docker to a version with Compose V2"
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}Warning: .env file not found${NC}"
    echo "Creating .env from .env.docker template..."
    cp .env.docker .env
    echo -e "${GREEN}✓ Created .env file${NC}"
    echo -e "${YELLOW}Note: Update .env with your Congress.gov API key if needed${NC}\n"
fi

# Parse command line arguments
BUILD_FLAG=""
DETACH_FLAG=""

for arg in "$@"; do
    case $arg in
        --build)
            BUILD_FLAG="--build"
            shift
            ;;
        -d|--detach)
            DETACH_FLAG="-d"
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --build        Rebuild containers before starting"
            echo "  -d, --detach   Run in detached mode (background)"
            echo "  -h, --help     Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0              # Start services in foreground"
            echo "  $0 --build      # Rebuild and start services"
            echo "  $0 -d           # Start services in background"
            echo ""
            exit 0
            ;;
    esac
done

echo -e "${GREEN}Starting Docker Compose services...${NC}\n"

# Start Docker Compose
docker compose up $BUILD_FLAG $DETACH_FLAG

if [ -n "$DETACH_FLAG" ]; then
    echo ""
    echo -e "${GREEN}Services started successfully!${NC}"
    echo ""
    echo "Access the application:"
    echo "  Frontend:  http://localhost:5173"
    echo "  Backend:   http://localhost:5001"
    echo "  Database:  localhost:5432"
    echo ""
    echo "View logs:"
    echo "  docker compose logs -f"
    echo ""
    echo "Stop services:"
    echo "  docker compose down"
fi
