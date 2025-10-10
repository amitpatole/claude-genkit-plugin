#!/bin/bash
set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Starting Genkit Development Server${NC}"
echo ""

# Check if we're in a Genkit project
if [ ! -f "package.json" ]; then
    echo -e "${RED}❌ No package.json found${NC}"
    echo "Please run this command from a Node.js project directory"
    echo "Or run /genkit-init to create a new Genkit project"
    exit 1
fi

# Check if Genkit is installed in the project
if ! grep -q "@genkit-ai/core" package.json; then
    echo -e "${RED}❌ Genkit not found in package.json${NC}"
    echo "This doesn't appear to be a Genkit project"
    echo ""
    read -p "Would you like to add Genkit to this project? (y/n): " add_genkit

    if [[ $add_genkit == "y" || $add_genkit == "Y" ]]; then
        echo -e "${BLUE}Installing Genkit packages...${NC}"
        npm install @genkit-ai/core @genkit-ai/ai @genkit-ai/flow zod

        echo ""
        echo "Select AI provider to install:"
        echo "  1. Anthropic Claude"
        echo "  2. Google Gemini"
        echo "  3. OpenAI"
        echo "  4. All providers"
        read -p "Choose (1-4): " provider_choice

        case $provider_choice in
            1)
                npm install @genkit-ai/anthropic
                ;;
            2)
                npm install @genkit-ai/googleai
                ;;
            3)
                npm install @genkit-ai/openai
                ;;
            4)
                npm install @genkit-ai/anthropic @genkit-ai/googleai @genkit-ai/openai
                ;;
            *)
                npm install @genkit-ai/anthropic
                ;;
        esac

        echo -e "${GREEN}✓ Genkit packages installed${NC}"
    else
        exit 1
    fi
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  No .env file found${NC}"

    if [ -f ".env.example" ]; then
        read -p "Copy .env.example to .env? (y/n): " copy_env
        if [[ $copy_env == "y" || $copy_env == "Y" ]]; then
            cp .env.example .env
            echo -e "${GREEN}✓ Created .env from .env.example${NC}"
            echo -e "${YELLOW}⚠️  Please edit .env and add your API keys${NC}"
        fi
    else
        echo -e "${YELLOW}Creating basic .env file...${NC}"
        cat > .env << 'EOF'
# Add your API keys here
ANTHROPIC_API_KEY=
GOOGLE_AI_API_KEY=
OPENAI_API_KEY=
EOF
        echo -e "${GREEN}✓ Created .env file${NC}"
        echo -e "${YELLOW}⚠️  Please add your API keys to .env${NC}"
    fi

    echo ""
    read -p "Press Enter to continue or Ctrl+C to exit..."
fi

# Check if dev script exists in package.json
if ! grep -q '"dev"' package.json; then
    echo -e "${YELLOW}⚠️  No 'dev' script found in package.json${NC}"

    # Detect if TypeScript or JavaScript
    if [ -f "tsconfig.json" ] || grep -q "typescript" package.json; then
        echo -e "${BLUE}Detected TypeScript project${NC}"

        # Check for src/index.ts
        if [ -f "src/index.ts" ]; then
            ENTRY_FILE="src/index.ts"
        elif [ -f "index.ts" ]; then
            ENTRY_FILE="index.ts"
        else
            ENTRY_FILE="src/index.ts"
            echo -e "${YELLOW}Creating default entry file at $ENTRY_FILE${NC}"
            mkdir -p src
            cat > "$ENTRY_FILE" << 'EOF'
import './genkit.config';

console.log('Genkit server ready');
EOF
        fi

        # Install tsx if not present
        if ! grep -q "tsx" package.json; then
            npm install -D tsx
        fi

        npm pkg set scripts.dev="genkit start -- tsx --watch $ENTRY_FILE"
        echo -e "${GREEN}✓ Added dev script for TypeScript${NC}"
    else
        echo -e "${BLUE}Detected JavaScript project${NC}"

        # Check for src/index.js
        if [ -f "src/index.js" ]; then
            ENTRY_FILE="src/index.js"
        elif [ -f "index.js" ]; then
            ENTRY_FILE="index.js"
        else
            ENTRY_FILE="src/index.js"
            echo -e "${YELLOW}Creating default entry file at $ENTRY_FILE${NC}"
            mkdir -p src
            cat > "$ENTRY_FILE" << 'EOF'
import './genkit.config.js';

console.log('Genkit server ready');
EOF
        fi

        npm pkg set scripts.dev="genkit start -- node --watch $ENTRY_FILE"
        echo -e "${GREEN}✓ Added dev script for JavaScript${NC}"
    fi
fi

# Check if port 4000 is already in use
if command -v lsof &> /dev/null; then
    if lsof -Pi :4000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        echo -e "${YELLOW}⚠️  Port 4000 is already in use${NC}"
        read -p "Kill the existing process? (y/n): " kill_process
        if [[ $kill_process == "y" || $kill_process == "Y" ]]; then
            lsof -ti:4000 | xargs kill -9 2>/dev/null || true
            echo -e "${GREEN}✓ Cleared port 4000${NC}"
        fi
    fi
fi

echo ""
echo -e "${GREEN}Starting Genkit development server...${NC}"
echo -e "${BLUE}Developer UI will be available at: http://localhost:4000${NC}"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
echo ""

# Run the dev server
npm run dev
