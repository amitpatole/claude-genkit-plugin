#!/bin/bash
set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}   Genkit Test Generator${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════${NC}"
echo ""

# Check if we're in a Genkit project
if [ ! -f "package.json" ]; then
    echo -e "${RED}❌ Error: No package.json found${NC}"
    echo "Please run this command from your Genkit project directory"
    exit 1
fi

# Check for Genkit dependency
if ! grep -q "@genkit-ai" package.json; then
    echo -e "${RED}❌ Error: Not a Genkit project${NC}"
    echo "No @genkit-ai dependencies found in package.json"
    exit 1
fi

# Detect project language
if grep -q "\"typescript\"" package.json || [ -f "tsconfig.json" ]; then
    LANGUAGE="typescript"
    TEST_FRAMEWORK="jest"
    FILE_EXT="ts"
else
    LANGUAGE="javascript"
    TEST_FRAMEWORK="jest"
    FILE_EXT="js"
fi

echo -e "${BLUE}Project Language:${NC} $LANGUAGE"
echo ""

# Find all flow files
echo -e "${BLUE}Scanning for Genkit flows...${NC}"
FLOW_FILES=$(find src -type f \( -name "*.ts" -o -name "*.js" \) -exec grep -l "defineFlow" {} \; 2>/dev/null || echo "")

if [ -z "$FLOW_FILES" ]; then
    echo -e "${YELLOW}⚠️  No flows found${NC}"
    echo "Looking for files with 'defineFlow' in src/ directory"
    exit 0
fi

echo -e "${GREEN}Found flows:${NC}"
echo "$FLOW_FILES" | while read -r file; do
    echo "  • $file"
done
echo ""

# Ask user which test type to generate
echo -e "${BLUE}Select test type:${NC}"
echo "1. Unit tests (test individual flows in isolation)"
echo "2. Integration tests (test flows with dependencies)"
echo "3. End-to-end tests (test complete workflows)"
echo "4. All of the above"
echo ""
read -p "Enter choice (1-4): " TEST_TYPE

# Ask for test coverage preference
echo ""
echo -e "${BLUE}Test coverage level:${NC}"
echo "1. Basic (happy path only)"
echo "2. Standard (happy path + error cases)"
echo "3. Comprehensive (happy path + edge cases + error handling)"
echo ""
read -p "Enter choice (1-3): " COVERAGE_LEVEL

# Create test directory structure
echo ""
echo -e "${BLUE}Creating test directory structure...${NC}"
mkdir -p tests/{unit,integration,e2e}
mkdir -p tests/__mocks__

# Install test dependencies if not present
echo ""
echo -e "${BLUE}Checking test dependencies...${NC}"
MISSING_DEPS=""

if ! grep -q "jest" package.json; then
    MISSING_DEPS="$MISSING_DEPS jest @types/jest"
fi

if ! grep -q "@jest/globals" package.json; then
    MISSING_DEPS="$MISSING_DEPS @jest/globals"
fi

if [ -n "$MISSING_DEPS" ]; then
    echo -e "${YELLOW}Installing missing test dependencies...${NC}"
    npm install --save-dev $MISSING_DEPS
    echo -e "${GREEN}✓ Dependencies installed${NC}"
fi

# Generate test files
echo ""
echo -e "${BLUE}Generating test files...${NC}"

GENERATED_COUNT=0

echo "$FLOW_FILES" | while read -r flow_file; do
    # Extract flow name from file
    FLOW_NAME=$(basename "$flow_file" .$FILE_EXT)

    # Generate unit test
    if [ "$TEST_TYPE" = "1" ] || [ "$TEST_TYPE" = "4" ]; then
        TEST_FILE="tests/unit/${FLOW_NAME}.test.$FILE_EXT"

        cat > "$TEST_FILE" << EOF
import { describe, it, expect, beforeEach, jest } from '@jest/globals';

describe('${FLOW_NAME} Flow', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('Happy Path', () => {
    it('should execute flow successfully with valid input', async () => {
      // TODO: Add test implementation
      // 1. Prepare test data
      // 2. Execute flow
      // 3. Assert expected results
      expect(true).toBe(true);
    });
  });

$(if [ "$COVERAGE_LEVEL" != "1" ]; then
cat << 'INNER_EOF'
  describe('Error Handling', () => {
    it('should handle invalid input gracefully', async () => {
      // TODO: Test error handling
      expect(true).toBe(true);
    });

    it('should handle API failures', async () => {
      // TODO: Test API failure scenarios
      expect(true).toBe(true);
    });
  });
INNER_EOF
fi)

$(if [ "$COVERAGE_LEVEL" = "3" ]; then
cat << 'INNER_EOF'
  describe('Edge Cases', () => {
    it('should handle empty input', async () => {
      // TODO: Test edge cases
      expect(true).toBe(true);
    });

    it('should handle large inputs', async () => {
      // TODO: Test performance with large data
      expect(true).toBe(true);
    });
  });
INNER_EOF
fi)
});
EOF
        echo -e "${GREEN}✓ Created unit test:${NC} $TEST_FILE"
        GENERATED_COUNT=$((GENERATED_COUNT + 1))
    fi

    # Generate integration test
    if [ "$TEST_TYPE" = "2" ] || [ "$TEST_TYPE" = "4" ]; then
        TEST_FILE="tests/integration/${FLOW_NAME}.integration.test.$FILE_EXT"

        cat > "$TEST_FILE" << EOF
import { describe, it, expect, beforeAll, afterAll } from '@jest/globals';

describe('${FLOW_NAME} Integration Tests', () => {
  beforeAll(async () => {
    // TODO: Setup test environment
    // - Initialize database connections
    // - Setup test data
    // - Configure test environment variables
  });

  afterAll(async () => {
    // TODO: Cleanup test environment
  });

  it('should integrate with external services', async () => {
    // TODO: Test integration with real or mocked services
    expect(true).toBe(true);
  });

  it('should handle database operations', async () => {
    // TODO: Test database interactions
    expect(true).toBe(true);
  });
});
EOF
        echo -e "${GREEN}✓ Created integration test:${NC} $TEST_FILE"
        GENERATED_COUNT=$((GENERATED_COUNT + 1))
    fi
done

# Generate jest config if not exists
if [ ! -f "jest.config.js" ] && [ ! -f "jest.config.json" ]; then
    echo ""
    echo -e "${BLUE}Creating Jest configuration...${NC}"

    cat > "jest.config.js" << EOF
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/tests'],
  testMatch: ['**/*.test.ts', '**/*.test.js'],
  collectCoverageFrom: [
    'src/**/*.{ts,js}',
    '!src/**/*.d.ts',
  ],
  coverageThreshold: {
    global: {
      branches: 70,
      functions: 70,
      lines: 70,
      statements: 70,
    },
  },
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/\$1',
  },
};
EOF
    echo -e "${GREEN}✓ Created jest.config.js${NC}"
fi

# Update package.json with test scripts
echo ""
echo -e "${BLUE}Updating package.json with test scripts...${NC}"

if ! grep -q "\"test\"" package.json; then
    # Add test scripts using node to safely update JSON
    node -e "
    const fs = require('fs');
    const pkg = JSON.parse(fs.readFileSync('package.json', 'utf8'));
    pkg.scripts = pkg.scripts || {};
    pkg.scripts.test = 'jest';
    pkg.scripts['test:watch'] = 'jest --watch';
    pkg.scripts['test:coverage'] = 'jest --coverage';
    pkg.scripts['test:unit'] = 'jest tests/unit';
    pkg.scripts['test:integration'] = 'jest tests/integration';
    pkg.scripts['test:e2e'] = 'jest tests/e2e';
    fs.writeFileSync('package.json', JSON.stringify(pkg, null, 2));
    "
    echo -e "${GREEN}✓ Added test scripts to package.json${NC}"
fi

# Summary
echo ""
echo -e "${GREEN}════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}   ✓ Test Generation Complete!${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${BLUE}Generated:${NC}"
echo "  • Test files created in tests/ directory"
echo "  • Jest configuration added"
echo "  • npm test scripts configured"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo ""
echo "1. Review generated test files in tests/ directory"
echo "2. Fill in TODO sections with actual test logic"
echo "3. Run tests:"
echo "   npm test              # Run all tests"
echo "   npm run test:watch    # Watch mode"
echo "   npm run test:coverage # With coverage report"
echo ""
echo -e "${BLUE}Pro Tips:${NC}"
echo "  • Use @genkit-assistant for help writing test logic"
echo "  • Run tests before deploying"
echo "  • Aim for >80% code coverage"
echo ""
