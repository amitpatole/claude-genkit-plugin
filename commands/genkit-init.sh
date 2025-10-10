#!/bin/bash
set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔥 Firebase Genkit Project Initialization${NC}"
echo ""

# Check Node.js version
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed${NC}"
    echo "Please install Node.js 18+ from https://nodejs.org/"
    exit 1
fi

NODE_VERSION=$(node -v | cut -d 'v' -f 2 | cut -d '.' -f 1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo -e "${RED}❌ Node.js version must be 18 or higher (current: $(node -v))${NC}"
    exit 1
fi

# Check if genkit CLI is installed globally
if ! command -v genkit &> /dev/null; then
    echo -e "${YELLOW}⚠️  Genkit CLI not found globally${NC}"
    read -p "Would you like to install it globally? (y/n): " install_global

    if [[ $install_global == "y" || $install_global == "Y" ]]; then
        echo -e "${BLUE}Installing Genkit CLI globally...${NC}"
        npm install -g genkit-cli
        echo -e "${GREEN}✓ Genkit CLI installed${NC}"
    fi
fi

# Get project details
read -p "Project name (default: genkit-app): " PROJECT_NAME
PROJECT_NAME=${PROJECT_NAME:-genkit-app}

read -p "Project directory (default: ./$PROJECT_NAME): " PROJECT_DIR
PROJECT_DIR=${PROJECT_DIR:-"./$PROJECT_NAME"}

# Select language
echo ""
echo "Select language:"
echo "  1. TypeScript (recommended)"
echo "  2. JavaScript"
echo "  3. Go"
echo "  4. Python"
read -p "Choose (1-4): " LANG_CHOICE

case $LANG_CHOICE in
    1)
        LANG="typescript"
        ;;
    2)
        LANG="javascript"
        ;;
    3)
        LANG="go"
        ;;
    4)
        LANG="python"
        ;;
    *)
        echo -e "${YELLOW}Invalid choice, defaulting to TypeScript${NC}"
        LANG="typescript"
        ;;
esac

# Select AI model provider
echo ""
echo "Select primary AI model provider:"
echo "  1. Anthropic Claude (recommended)"
echo "  2. Google Gemini"
echo "  3. OpenAI GPT"
echo "  4. Multiple providers"
read -p "Choose (1-4): " MODEL_CHOICE

case $MODEL_CHOICE in
    1)
        MODEL_PROVIDER="anthropic"
        ;;
    2)
        MODEL_PROVIDER="gemini"
        ;;
    3)
        MODEL_PROVIDER="openai"
        ;;
    4)
        MODEL_PROVIDER="all"
        ;;
    *)
        echo -e "${YELLOW}Invalid choice, defaulting to Claude${NC}"
        MODEL_PROVIDER="anthropic"
        ;;
esac

# Create project directory
echo ""
echo -e "${BLUE}Creating project at $PROJECT_DIR...${NC}"
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

# Initialize based on language
if [ "$LANG" = "typescript" ] || [ "$LANG" = "javascript" ]; then
    # Initialize npm project
    npm init -y

    # Update package.json name
    npm pkg set name="$PROJECT_NAME"
    npm pkg set type="module"

    # Install Genkit core
    echo -e "${BLUE}Installing Genkit core packages...${NC}"
    npm install @genkit-ai/core @genkit-ai/ai @genkit-ai/flow zod

    # Install model providers
    case $MODEL_PROVIDER in
        anthropic)
            npm install @genkit-ai/anthropic
            ;;
        gemini)
            npm install @genkit-ai/googleai
            ;;
        openai)
            npm install @genkit-ai/openai
            ;;
        all)
            npm install @genkit-ai/anthropic @genkit-ai/googleai @genkit-ai/openai
            ;;
    esac

    # Install dev dependencies
    if [ "$LANG" = "typescript" ]; then
        npm install -D typescript @types/node tsx

        # Create tsconfig.json
        cat > tsconfig.json << 'EOF'
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "esModuleInterop": true,
    "strict": true,
    "skipLibCheck": true,
    "outDir": "dist",
    "rootDir": "src"
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
EOF
    fi

    # Create src directory
    mkdir -p src/flows

    # Create genkit config
    if [ "$LANG" = "typescript" ]; then
        cat > src/genkit.config.ts << 'EOF'
import { configureGenkit } from '@genkit-ai/core';
import { claude } from '@genkit-ai/anthropic';

export default configureGenkit({
  plugins: [
    claude({
      apiKey: process.env.ANTHROPIC_API_KEY,
    }),
  ],
  logLevel: 'debug',
  enableTracingAndMetrics: true,
});
EOF
    else
        cat > src/genkit.config.js << 'EOF'
import { configureGenkit } from '@genkit-ai/core';
import { claude } from '@genkit-ai/anthropic';

export default configureGenkit({
  plugins: [
    claude({
      apiKey: process.env.ANTHROPIC_API_KEY,
    }),
  ],
  logLevel: 'debug',
  enableTracingAndMetrics: true,
});
EOF
    fi

    # Create example flow
    EXT="ts"
    [ "$LANG" = "javascript" ] && EXT="js"

    cat > "src/flows/chat.$EXT" << 'EOF'
import { defineFlow } from '@genkit-ai/flow';
import { claude35Sonnet } from '@genkit-ai/anthropic';
import { z } from 'zod';

export const chatFlow = defineFlow(
  {
    name: 'chatFlow',
    inputSchema: z.object({
      message: z.string(),
    }),
    outputSchema: z.string(),
  },
  async (input) => {
    const result = await claude35Sonnet.generate({
      prompt: input.message,
    });

    return result.text;
  }
);
EOF

    # Create index file
    cat > "src/index.$EXT" << 'EOF'
import './genkit.config';
import { chatFlow } from './flows/chat';

// Export flows for Genkit to discover
export { chatFlow };

console.log('Genkit flows initialized');
EOF

    # Create .env.example
    cat > .env.example << 'EOF'
# Anthropic API Key
ANTHROPIC_API_KEY=your_api_key_here

# Google AI API Key
GOOGLE_AI_API_KEY=your_api_key_here

# OpenAI API Key
OPENAI_API_KEY=your_api_key_here
EOF

    # Create .env
    touch .env

    # Update package.json scripts
    if [ "$LANG" = "typescript" ]; then
        npm pkg set scripts.dev="genkit start -- tsx --watch src/index.ts"
        npm pkg set scripts.build="tsc"
        npm pkg set scripts.start="node dist/index.js"
    else
        npm pkg set scripts.dev="genkit start -- node --watch src/index.js"
        npm pkg set scripts.start="node src/index.js"
    fi

elif [ "$LANG" = "go" ]; then
    # Initialize Go module
    go mod init "$PROJECT_NAME"

    # Install Genkit for Go
    go get github.com/firebase/genkit/go/genkit

    echo -e "${YELLOW}⚠️  Go support is in beta. Please refer to Genkit Go docs for setup.${NC}"

elif [ "$LANG" = "python" ]; then
    # Create virtual environment
    python3 -m venv venv
    source venv/bin/activate

    # Install Genkit for Python
    pip install genkit

    echo -e "${YELLOW}⚠️  Python support is in alpha. Please refer to Genkit Python docs for setup.${NC}"
fi

# Create .gitignore
cat > .gitignore << 'EOF'
# Dependencies
node_modules/
venv/
__pycache__/

# Environment
.env
.env.local

# Build
dist/
build/
*.js (TypeScript projects)

# Genkit
.genkit/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
EOF

# Create README
cat > README.md << EOF
# $PROJECT_NAME

Firebase Genkit application built with $LANG and $MODEL_PROVIDER.

## Setup

1. Install dependencies:
   \`\`\`bash
   npm install
   \`\`\`

2. Copy \`.env.example\` to \`.env\` and add your API keys:
   \`\`\`bash
   cp .env.example .env
   \`\`\`

3. Start development server:
   \`\`\`bash
   npm run dev
   \`\`\`

4. Open Genkit Developer UI:
   \`\`\`
   http://localhost:4000
   \`\`\`

## Available Flows

- \`chatFlow\` - Simple chat flow using Claude 3.5 Sonnet

## Development

- \`npm run dev\` - Start development server with Genkit UI
- \`npm run build\` - Build for production
- \`npm start\` - Run production build

## Learn More

- [Genkit Documentation](https://firebase.google.com/docs/genkit)
- [Claude API Reference](https://docs.anthropic.com/)
EOF

echo ""
echo -e "${GREEN}✨ Project created successfully!${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo -e "  1. cd $PROJECT_DIR"
echo -e "  2. Edit .env and add your API keys"
echo -e "  3. Run ${GREEN}npm run dev${NC} to start development server"
echo -e "  4. Open ${BLUE}http://localhost:4000${NC} for Genkit Developer UI"
echo ""
echo -e "${YELLOW}💡 Tip: Use /genkit-run to start the dev server from Claude Code${NC}"
