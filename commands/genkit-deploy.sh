#!/bin/bash
set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Deploy Genkit Application${NC}"
echo ""

# Check if we're in a project
if [ ! -f "package.json" ]; then
    echo -e "${RED}❌ No package.json found${NC}"
    echo "Please run this command from your project directory"
    exit 1
fi

# Check if Genkit is installed
if ! grep -q "@genkit-ai/core" package.json; then
    echo -e "${RED}❌ This doesn't appear to be a Genkit project${NC}"
    exit 1
fi

echo "Select deployment target:"
echo ""
echo "  1. Firebase Cloud Functions"
echo "  2. Google Cloud Run"
echo "  3. Google Cloud Functions (2nd gen)"
echo "  4. Vercel"
echo "  5. Custom Docker deployment"
echo "  6. Local build only"
echo ""
read -p "Choose (1-6): " DEPLOY_TARGET

case $DEPLOY_TARGET in
    1)
        # Firebase Cloud Functions
        echo -e "${BLUE}Deploying to Firebase Cloud Functions...${NC}"

        # Check if firebase-tools is installed
        if ! command -v firebase &> /dev/null; then
            echo -e "${YELLOW}Firebase CLI not found${NC}"
            read -p "Install Firebase CLI? (y/n): " install_firebase
            if [[ $install_firebase == "y" || $install_firebase == "Y" ]]; then
                npm install -g firebase-tools
            else
                exit 1
            fi
        fi

        # Check if Firebase is initialized
        if [ ! -f "firebase.json" ]; then
            echo -e "${YELLOW}Firebase not initialized${NC}"
            echo "Initializing Firebase..."
            firebase init functions
        fi

        # Build project
        if grep -q '"build"' package.json; then
            echo -e "${BLUE}Building project...${NC}"
            npm run build
        fi

        # Deploy
        echo -e "${BLUE}Deploying to Firebase...${NC}"
        firebase deploy --only functions

        echo -e "${GREEN}✅ Deployment complete!${NC}"
        ;;

    2)
        # Google Cloud Run
        echo -e "${BLUE}Deploying to Google Cloud Run...${NC}"

        # Check if gcloud is installed
        if ! command -v gcloud &> /dev/null; then
            echo -e "${RED}❌ Google Cloud SDK not found${NC}"
            echo "Install from: https://cloud.google.com/sdk/docs/install"
            exit 1
        fi

        read -p "Project ID: " GCP_PROJECT
        read -p "Service name (default: genkit-app): " SERVICE_NAME
        SERVICE_NAME=${SERVICE_NAME:-genkit-app}
        read -p "Region (default: us-central1): " REGION
        REGION=${REGION:-us-central1}

        # Create Dockerfile if it doesn't exist
        if [ ! -f "Dockerfile" ]; then
            echo -e "${BLUE}Creating Dockerfile...${NC}"
            cat > Dockerfile << 'EOF'
FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy application files
COPY . .

# Build if needed
RUN if grep -q '"build"' package.json; then npm run build; fi

# Expose port
EXPOSE 8080

# Start application
CMD ["npm", "start"]
EOF
        fi

        # Create .dockerignore if it doesn't exist
        if [ ! -f ".dockerignore" ]; then
            cat > .dockerignore << 'EOF'
node_modules
npm-debug.log
.env
.env.local
.git
.gitignore
README.md
.vscode
.idea
EOF
        fi

        # Deploy to Cloud Run
        echo -e "${BLUE}Deploying to Cloud Run...${NC}"
        gcloud run deploy "$SERVICE_NAME" \
            --source . \
            --project="$GCP_PROJECT" \
            --region="$REGION" \
            --platform=managed \
            --allow-unauthenticated \
            --set-env-vars="NODE_ENV=production"

        echo -e "${GREEN}✅ Deployment complete!${NC}"
        ;;

    3)
        # Google Cloud Functions 2nd gen
        echo -e "${BLUE}Deploying to Google Cloud Functions (2nd gen)...${NC}"

        if ! command -v gcloud &> /dev/null; then
            echo -e "${RED}❌ Google Cloud SDK not found${NC}"
            exit 1
        fi

        read -p "Project ID: " GCP_PROJECT
        read -p "Function name (default: genkitApp): " FUNCTION_NAME
        FUNCTION_NAME=${FUNCTION_NAME:-genkitApp}
        read -p "Region (default: us-central1): " REGION
        REGION=${REGION:-us-central1}

        # Build project
        if grep -q '"build"' package.json; then
            echo -e "${BLUE}Building project...${NC}"
            npm run build
        fi

        # Deploy
        gcloud functions deploy "$FUNCTION_NAME" \
            --gen2 \
            --runtime=nodejs18 \
            --region="$REGION" \
            --source=. \
            --entry-point=genkitApp \
            --trigger-http \
            --allow-unauthenticated \
            --project="$GCP_PROJECT"

        echo -e "${GREEN}✅ Deployment complete!${NC}"
        ;;

    4)
        # Vercel
        echo -e "${BLUE}Deploying to Vercel...${NC}"

        if ! command -v vercel &> /dev/null; then
            echo -e "${YELLOW}Vercel CLI not found${NC}"
            read -p "Install Vercel CLI? (y/n): " install_vercel
            if [[ $install_vercel == "y" || $install_vercel == "Y" ]]; then
                npm install -g vercel
            else
                exit 1
            fi
        fi

        # Deploy
        vercel --prod

        echo -e "${GREEN}✅ Deployment complete!${NC}"
        ;;

    5)
        # Docker
        echo -e "${BLUE}Building Docker image...${NC}"

        read -p "Image name (default: genkit-app): " IMAGE_NAME
        IMAGE_NAME=${IMAGE_NAME:-genkit-app}
        read -p "Image tag (default: latest): " IMAGE_TAG
        IMAGE_TAG=${IMAGE_TAG:-latest}

        # Create Dockerfile if needed
        if [ ! -f "Dockerfile" ]; then
            echo -e "${BLUE}Creating Dockerfile...${NC}"
            cat > Dockerfile << 'EOF'
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN if grep -q '"build"' package.json; then npm run build; fi

EXPOSE 8080

CMD ["npm", "start"]
EOF
        fi

        # Build Docker image
        docker build -t "$IMAGE_NAME:$IMAGE_TAG" .

        echo -e "${GREEN}✅ Docker image built: $IMAGE_NAME:$IMAGE_TAG${NC}"
        echo ""
        echo "To run locally:"
        echo "  docker run -p 8080:8080 --env-file .env $IMAGE_NAME:$IMAGE_TAG"
        echo ""
        echo "To push to registry:"
        echo "  docker tag $IMAGE_NAME:$IMAGE_TAG your-registry/$IMAGE_NAME:$IMAGE_TAG"
        echo "  docker push your-registry/$IMAGE_NAME:$IMAGE_TAG"
        ;;

    6)
        # Build only
        echo -e "${BLUE}Building project...${NC}"

        if ! grep -q '"build"' package.json; then
            echo -e "${YELLOW}No build script found in package.json${NC}"

            # Add build script
            if [ -f "tsconfig.json" ]; then
                npm pkg set scripts.build="tsc"
                npm install -D typescript
            else
                echo -e "${YELLOW}Skipping build - no TypeScript config found${NC}"
                exit 0
            fi
        fi

        npm run build

        echo -e "${GREEN}✅ Build complete!${NC}"
        echo "Output directory: dist/"
        ;;

    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${YELLOW}📝 Post-deployment checklist:${NC}"
echo "  ☐ Set environment variables (API keys) in your deployment platform"
echo "  ☐ Configure custom domain if needed"
echo "  ☐ Set up monitoring and logging"
echo "  ☐ Test your deployed endpoints"
echo "  ☐ Update CORS settings if needed"
