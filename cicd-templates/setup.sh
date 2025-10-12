#!/bin/bash

# CI/CD Pipeline Setup Script for Genkit Applications
# This script helps set up CI/CD pipelines for your Genkit project

set -e

echo "🚀 Genkit CI/CD Pipeline Setup"
echo "================================"
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo -e "${RED}❌ Error: Not a git repository${NC}"
    echo "Please run this script from the root of your git repository"
    exit 1
fi

# Check if running from cicd-templates directory
if [ "$(basename "$(pwd)")" = "cicd-templates" ]; then
    echo -e "${YELLOW}⚠️  Running from cicd-templates directory${NC}"
    echo "Switching to repository root..."
    cd ..
fi

# Function to print section headers
print_header() {
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

# Function to print success messages
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Function to print error messages
print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Function to print info messages
print_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

# Select CI/CD platform
print_header "Step 1: Select CI/CD Platform"
echo "Available platforms:"
echo "1. GitHub Actions (recommended)"
echo "2. GitLab CI"
echo "3. Azure Pipelines"
echo "4. CircleCI"
echo "5. Jenkins"
echo ""
read -p "Choose platform (1-5): " platform_choice

case $platform_choice in
    1) PLATFORM="github-actions" ;;
    2) PLATFORM="gitlab-ci" ;;
    3) PLATFORM="azure-pipelines" ;;
    4) PLATFORM="circleci" ;;
    5) PLATFORM="jenkins" ;;
    *)
        print_error "Invalid choice"
        exit 1
        ;;
esac

print_success "Selected: $PLATFORM"

# Select deployment target
print_header "Step 2: Select Deployment Target"
echo "Available deployment targets:"
echo "1. Firebase Cloud Functions"
echo "2. Google Cloud Run"
echo "3. Vercel"
echo "4. AWS Lambda (coming soon)"
echo "5. Docker/Kubernetes"
echo ""
read -p "Choose target (1-5): " target_choice

case $target_choice in
    1) TARGET="firebase-functions" ;;
    2) TARGET="cloud-run" ;;
    3) TARGET="vercel" ;;
    4) TARGET="aws-lambda" ;;
    5) TARGET="docker" ;;
    *)
        print_error "Invalid choice"
        exit 1
        ;;
esac

print_success "Selected: $TARGET"

# Copy template files
print_header "Step 3: Copy Template Files"

# Create necessary directories
if [ "$PLATFORM" = "github-actions" ]; then
    mkdir -p .github/workflows
    DEST_DIR=".github/workflows"
    TEMPLATE_FILE="${TARGET}.yml"
    DEST_FILE="$DEST_DIR/deploy.yml"

    if [ -f "cicd-templates/$PLATFORM/$TEMPLATE_FILE" ]; then
        cp "cicd-templates/$PLATFORM/$TEMPLATE_FILE" "$DEST_FILE"
        print_success "Copied workflow template to $DEST_FILE"
    else
        print_error "Template file not found: cicd-templates/$PLATFORM/$TEMPLATE_FILE"
        exit 1
    fi

    # Copy Dockerfile if Cloud Run
    if [ "$TARGET" = "cloud-run" ]; then
        if [ -f "cicd-templates/$PLATFORM/Dockerfile.template" ]; then
            cp "cicd-templates/$PLATFORM/Dockerfile.template" "./Dockerfile"
            print_success "Copied Dockerfile to ./Dockerfile"
        fi
    fi
fi

# Create .env.example
print_header "Step 4: Create Environment Template"

cat > .env.example << 'EOF'
# AI Model API Keys
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GOOGLE_AI_API_KEY=your_google_ai_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Application Configuration
NODE_ENV=development
LOG_LEVEL=debug
PORT=3000

# Firebase Configuration (if using Firebase)
FIREBASE_PROJECT_ID=your_firebase_project_id
FIREBASE_API_KEY=your_firebase_api_key

# Google Cloud Configuration (if using GCP)
GCP_PROJECT_ID=your_gcp_project_id
GCP_REGION=us-central1

# Vercel Configuration (if using Vercel)
VERCEL_TOKEN=your_vercel_token
VERCEL_ORG_ID=your_vercel_org_id
VERCEL_PROJECT_ID=your_vercel_project_id
EOF

print_success "Created .env.example"

# Print required secrets
print_header "Step 5: Configure Secrets"

echo "You need to configure the following secrets in your repository:"
echo ""

if [ "$PLATFORM" = "github-actions" ]; then
    echo -e "${YELLOW}GitHub Secrets Location:${NC}"
    echo "Settings → Secrets and variables → Actions → New repository secret"
    echo ""
fi

echo "Common secrets:"
echo "  - ANTHROPIC_API_KEY_DEV"
echo "  - ANTHROPIC_API_KEY_STAGING"
echo "  - ANTHROPIC_API_KEY_PROD"
echo "  - GOOGLE_AI_API_KEY_DEV"
echo "  - GOOGLE_AI_API_KEY_STAGING"
echo "  - GOOGLE_AI_API_KEY_PROD"
echo ""

if [ "$TARGET" = "firebase-functions" ]; then
    echo "Firebase-specific secrets:"
    echo "  - FIREBASE_SERVICE_ACCOUNT_DEV"
    echo "  - FIREBASE_SERVICE_ACCOUNT_STAGING"
    echo "  - FIREBASE_SERVICE_ACCOUNT_PROD"
    echo "  - FIREBASE_PROJECT_ID_DEV"
    echo "  - FIREBASE_PROJECT_ID_STAGING"
    echo "  - FIREBASE_PROJECT_ID_PROD"
fi

if [ "$TARGET" = "cloud-run" ]; then
    echo "Google Cloud-specific secrets:"
    echo "  - GCP_SERVICE_ACCOUNT_KEY"
    echo "  - GCP_PROJECT_ID"
fi

if [ "$TARGET" = "vercel" ]; then
    echo "Vercel-specific secrets:"
    echo "  - VERCEL_TOKEN"
    echo "  - VERCEL_ORG_ID"
    echo "  - VERCEL_PROJECT_ID"
    echo "  - VERCEL_PRODUCTION_URL"
fi

echo ""
echo "Optional secrets:"
echo "  - SLACK_WEBHOOK_URL (for notifications)"
echo ""

# Create health check endpoint
print_header "Step 6: Create Health Check Endpoint"

mkdir -p src

if [ ! -f "src/health.ts" ]; then
    cat > src/health.ts << 'EOF'
import { defineFlow } from '@genkit-ai/flow';
import { z } from 'zod';

export const healthFlow = defineFlow({
  name: 'health',
  inputSchema: z.object({}),
  outputSchema: z.object({
    status: z.enum(['healthy', 'degraded', 'unhealthy']),
    version: z.string(),
    timestamp: z.string(),
  }),
}, async () => {
  return {
    status: 'healthy',
    version: process.env.APP_VERSION || '1.0.0',
    timestamp: new Date().toISOString(),
  };
});
EOF
    print_success "Created src/health.ts"
else
    print_info "src/health.ts already exists, skipping"
fi

# Update package.json scripts
print_header "Step 7: Update Package Scripts"

if [ -f "package.json" ]; then
    print_info "Please ensure your package.json includes these scripts:"
    echo ""
    echo "  \"scripts\": {"
    echo "    \"build\": \"tsc\","
    echo "    \"test\": \"jest\","
    echo "    \"lint\": \"eslint src/\","
    echo "    \"format:check\": \"prettier --check src/\","
    echo "    \"test:integration\": \"jest --testMatch='**/*.integration.test.ts'\","
    echo "    \"test:smoke\": \"jest --testMatch='**/*.smoke.test.ts'\""
    echo "  }"
    echo ""
fi

# Create README section
print_header "Step 8: Documentation"

cat > CI-CD-SETUP.md << EOF
# CI/CD Pipeline Setup

This project uses $PLATFORM for continuous integration and deployment.

## Deployment Target

**Target:** $TARGET

## Quick Start

1. Configure secrets (see below)
2. Push to your branch:
   - \`develop\` → deploys to development/staging
   - \`main\` → deploys to production

## Required Secrets

See the list above in the setup output, or refer to:
- [GitHub Actions README](cicd-templates/github-actions/README.md)

## Deployment Workflow

\`\`\`
Pull Request → Tests → Code Quality → Security Scan
     ↓
Merge to develop → Deploy to Staging
     ↓
Merge to main → Deploy to Production
\`\`\`

## Health Checks

The pipeline includes automated health checks at:
- \`/health\` endpoint

## Rollback

If deployment fails, the pipeline automatically rolls back to the previous version.

## Manual Deployment

You can trigger manual deployment from the Actions tab in GitHub.

## Support

For issues, see [Troubleshooting Guide](cicd-templates/github-actions/README.md#troubleshooting)
EOF

print_success "Created CI-CD-SETUP.md"

# Final summary
print_header "✅ Setup Complete!"

echo "Next steps:"
echo ""
echo "1. Review and customize the workflow file:"
echo "   ${DEST_FILE}"
echo ""
echo "2. Configure secrets in your repository"
echo ""
echo "3. Commit and push the changes:"
echo "   git add ."
echo "   git commit -m 'chore: add CI/CD pipeline'"
echo "   git push origin $(git branch --show-current)"
echo ""
echo "4. Watch your workflow run in the Actions tab!"
echo ""
echo -e "${GREEN}🎉 Your CI/CD pipeline is ready!${NC}"
echo ""
print_info "For detailed documentation, see:"
echo "  - CI-CD-SETUP.md (project-specific)"
echo "  - cicd-templates/$PLATFORM/README.md (platform guide)"
echo ""
