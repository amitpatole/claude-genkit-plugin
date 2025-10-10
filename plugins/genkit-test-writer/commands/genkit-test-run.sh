#!/bin/bash
set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}   Genkit Test Runner${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════${NC}"
echo ""

# Check if we're in a Genkit project
if [ ! -f "package.json" ]; then
    echo -e "${RED}❌ Error: No package.json found${NC}"
    exit 1
fi

# Check if tests exist
if [ ! -d "tests" ]; then
    echo -e "${YELLOW}⚠️  No tests directory found${NC}"
    echo "Run /genkit-test-generate first to create tests"
    exit 0
fi

# Menu
echo -e "${BLUE}Select test mode:${NC}"
echo "1. Run all tests"
echo "2. Run unit tests only"
echo "3. Run integration tests only"
echo "4. Run with coverage report"
echo "5. Watch mode (auto-rerun on changes)"
echo ""
read -p "Enter choice (1-5): " MODE

case $MODE in
    1)
        echo -e "${BLUE}Running all tests...${NC}"
        npm test
        ;;
    2)
        echo -e "${BLUE}Running unit tests...${NC}"
        npm run test:unit
        ;;
    3)
        echo -e "${BLUE}Running integration tests...${NC}"
        npm run test:integration
        ;;
    4)
        echo -e "${BLUE}Running tests with coverage...${NC}"
        npm run test:coverage

        # Display coverage summary
        if [ -d "coverage" ]; then
            echo ""
            echo -e "${GREEN}Coverage report generated in coverage/ directory${NC}"
            echo "Open coverage/lcov-report/index.html in a browser to view detailed report"
        fi
        ;;
    5)
        echo -e "${BLUE}Starting watch mode...${NC}"
        npm run test:watch
        ;;
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}✓ Test run complete!${NC}"
