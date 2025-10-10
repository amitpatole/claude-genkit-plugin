#!/bin/bash
set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}   Genkit Monitor Setup${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════${NC}"
echo ""

# Check project
if [ ! -f "package.json" ]; then
    echo -e "${RED}❌ Error: No package.json found${NC}"
    exit 1
fi

echo -e "${BLUE}Select monitoring setup:${NC}"
echo "1. Basic logging (console + file)"
echo "2. Advanced telemetry (OpenTelemetry)"
echo "3. Cloud monitoring (Google Cloud/Firebase)"
echo "4. Full observability stack (logs + metrics + traces)"
echo ""
read -p "Enter choice (1-4): " SETUP_TYPE

# Install dependencies
echo ""
echo -e "${BLUE}Installing monitoring dependencies...${NC}"

case $SETUP_TYPE in
    1)
        npm install --save winston
        ;;
    2|4)
        npm install --save @opentelemetry/api @opentelemetry/sdk-node @opentelemetry/auto-instrumentations-node
        ;;
    3)
        npm install --save @google-cloud/logging @google-cloud/monitoring
        ;;
esac

# Create monitoring configuration
mkdir -p src/monitoring

cat > src/monitoring/logger.ts << 'EOF'
import winston from 'winston';

export const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  transports: [
    new winston.transports.File({ filename: 'logs/error.log', level: 'error' }),
    new winston.transports.File({ filename: 'logs/combined.log' }),
    new winston.transports.Console({
      format: winston.format.combine(
        winston.format.colorize(),
        winston.format.simple()
      )
    })
  ],
});

export function logFlowExecution(flowName: string, input: any, result: any, duration: number) {
  logger.info('Flow execution', {
    flow: flowName,
    input,
    result,
    duration,
    timestamp: new Date().toISOString()
  });
}
EOF

mkdir -p logs
echo -e "${GREEN}✓ Monitoring setup complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Import logger in your flows"
echo "2. Add logging calls"
echo "3. Run /genkit-monitor-dashboard to view logs"
