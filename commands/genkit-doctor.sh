#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🏥 Genkit Health Check${NC}"
echo ""

ISSUES_FOUND=0

# Function to check and report
check_item() {
    local name=$1
    local status=$2
    local message=$3

    if [ "$status" = "ok" ]; then
        echo -e "  ${GREEN}✓${NC} $name"
    elif [ "$status" = "warn" ]; then
        echo -e "  ${YELLOW}⚠${NC} $name"
        if [ -n "$message" ]; then
            echo -e "    ${YELLOW}$message${NC}"
        fi
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    else
        echo -e "  ${RED}✗${NC} $name"
        if [ -n "$message" ]; then
            echo -e "    ${RED}$message${NC}"
        fi
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    fi
}

echo -e "${BLUE}System Requirements:${NC}"

# Check Node.js
if command -v node &> /dev/null; then
    NODE_VERSION=$(node -v | cut -d 'v' -f 2 | cut -d '.' -f 1)
    if [ "$NODE_VERSION" -ge 18 ]; then
        check_item "Node.js $(node -v)" "ok"
    else
        check_item "Node.js $(node -v)" "error" "Version 18+ required"
    fi
else
    check_item "Node.js" "error" "Not installed"
fi

# Check npm
if command -v npm &> /dev/null; then
    check_item "npm $(npm -v)" "ok"
else
    check_item "npm" "error" "Not installed"
fi

# Check Genkit CLI
if command -v genkit &> /dev/null; then
    check_item "Genkit CLI" "ok"
else
    check_item "Genkit CLI" "warn" "Not installed globally (optional)"
fi

echo ""
echo -e "${BLUE}Project Check:${NC}"

# Check if in a project
if [ -f "package.json" ]; then
    check_item "package.json found" "ok"

    # Check Genkit packages
    if grep -q "@genkit-ai/core" package.json; then
        check_item "@genkit-ai/core installed" "ok"
    else
        check_item "@genkit-ai/core" "error" "Not found in package.json"
    fi

    if grep -q "@genkit-ai/flow" package.json; then
        check_item "@genkit-ai/flow installed" "ok"
    else
        check_item "@genkit-ai/flow" "warn" "Not found in package.json"
    fi

    # Check for AI providers
    echo ""
    echo -e "${BLUE}AI Model Providers:${NC}"

    PROVIDER_FOUND=false

    if grep -q "@genkit-ai/anthropic" package.json; then
        check_item "Anthropic Claude" "ok"
        PROVIDER_FOUND=true
    fi

    if grep -q "@genkit-ai/googleai" package.json; then
        check_item "Google Gemini" "ok"
        PROVIDER_FOUND=true
    fi

    if grep -q "@genkit-ai/openai" package.json; then
        check_item "OpenAI" "ok"
        PROVIDER_FOUND=true
    fi

    if [ "$PROVIDER_FOUND" = false ]; then
        check_item "AI Provider" "warn" "No AI provider installed"
    fi

    # Check configuration files
    echo ""
    echo -e "${BLUE}Configuration:${NC}"

    if [ -f "src/genkit.config.ts" ] || [ -f "src/genkit.config.js" ] || [ -f "genkit.config.ts" ] || [ -f "genkit.config.js" ]; then
        check_item "Genkit config found" "ok"
    else
        check_item "Genkit config" "warn" "No genkit.config.ts/js found"
    fi

    if [ -f "tsconfig.json" ]; then
        check_item "TypeScript config" "ok"
    fi

    # Check environment
    echo ""
    echo -e "${BLUE}Environment:${NC}"

    if [ -f ".env" ]; then
        check_item ".env file found" "ok"

        # Check for API keys (without revealing them)
        if grep -q "ANTHROPIC_API_KEY=" .env && ! grep -q "ANTHROPIC_API_KEY=$" .env && ! grep -q "ANTHROPIC_API_KEY=your_api_key_here" .env; then
            check_item "ANTHROPIC_API_KEY configured" "ok"
        elif grep -q "@genkit-ai/anthropic" package.json; then
            check_item "ANTHROPIC_API_KEY" "warn" "Not set or using placeholder"
        fi

        if grep -q "GOOGLE_AI_API_KEY=" .env && ! grep -q "GOOGLE_AI_API_KEY=$" .env && ! grep -q "GOOGLE_AI_API_KEY=your_api_key_here" .env; then
            check_item "GOOGLE_AI_API_KEY configured" "ok"
        elif grep -q "@genkit-ai/googleai" package.json; then
            check_item "GOOGLE_AI_API_KEY" "warn" "Not set or using placeholder"
        fi

        if grep -q "OPENAI_API_KEY=" .env && ! grep -q "OPENAI_API_KEY=$" .env && ! grep -q "OPENAI_API_KEY=your_api_key_here" .env; then
            check_item "OPENAI_API_KEY configured" "ok"
        elif grep -q "@genkit-ai/openai" package.json; then
            check_item "OPENAI_API_KEY" "warn" "Not set or using placeholder"
        fi
    else
        check_item ".env file" "warn" "Not found"
    fi

    # Check scripts
    echo ""
    echo -e "${BLUE}NPM Scripts:${NC}"

    if grep -q '"dev"' package.json; then
        check_item "dev script" "ok"
    else
        check_item "dev script" "warn" "Not configured"
    fi

    if grep -q '"build"' package.json; then
        check_item "build script" "ok"
    fi

    if grep -q '"start"' package.json; then
        check_item "start script" "ok"
    fi

    # Check for flows
    echo ""
    echo -e "${BLUE}Flows:${NC}"

    FLOW_COUNT=0
    if [ -d "src/flows" ]; then
        FLOW_COUNT=$(find src/flows -name "*.ts" -o -name "*.js" | wc -l)
    elif [ -d "flows" ]; then
        FLOW_COUNT=$(find flows -name "*.ts" -o -name "*.js" | wc -l)
    fi

    if [ "$FLOW_COUNT" -gt 0 ]; then
        check_item "Flows found: $FLOW_COUNT" "ok"
    else
        check_item "Flows" "warn" "No flows found in src/flows/ or flows/"
    fi

    # Check dependencies are installed
    echo ""
    echo -e "${BLUE}Dependencies:${NC}"

    if [ -d "node_modules" ]; then
        check_item "node_modules exists" "ok"
    else
        check_item "node_modules" "error" "Run 'npm install'"
    fi

else
    check_item "package.json" "error" "Not found - not in a Node.js project"
fi

# Check network (optional tools)
echo ""
echo -e "${BLUE}Optional Tools:${NC}"

if command -v firebase &> /dev/null; then
    check_item "Firebase CLI" "ok"
else
    check_item "Firebase CLI" "warn" "Not installed (needed for Firebase deployment)"
fi

if command -v gcloud &> /dev/null; then
    check_item "Google Cloud SDK" "ok"
else
    check_item "Google Cloud SDK" "warn" "Not installed (needed for Cloud deployment)"
fi

if command -v docker &> /dev/null; then
    check_item "Docker" "ok"
else
    check_item "Docker" "warn" "Not installed (needed for container deployment)"
fi

# Summary
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ $ISSUES_FOUND -eq 0 ]; then
    echo -e "${GREEN}✅ All checks passed! Your Genkit setup looks good.${NC}"
else
    echo -e "${YELLOW}⚠️  Found $ISSUES_FOUND issue(s). Review warnings and errors above.${NC}"
fi
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo ""
echo -e "${BLUE}Quick Commands:${NC}"
echo "  /genkit-init   - Initialize new project"
echo "  /genkit-run    - Start development server"
echo "  /genkit-flow   - Create a new flow"
echo "  /genkit-deploy - Deploy to production"

exit 0
