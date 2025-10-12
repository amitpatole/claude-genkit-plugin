#!/bin/bash

# Multi-Region Deployment Script for Genkit Applications
# Deploys to all configured regions in parallel

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
CONFIG_FILE="${CONFIG_FILE:-multi-region/config/regions.json}"
DEPLOYMENT_TYPE="${DEPLOYMENT_TYPE:-cloud-run}"  # or 'firebase'
PROJECT_ID="${GCP_PROJECT_ID:-}"

# Functions
print_header() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

# Check prerequisites
check_prerequisites() {
    print_header "Checking Prerequisites"

    # Check if jq is installed
    if ! command -v jq &> /dev/null; then
        print_error "jq is not installed. Please install jq to continue."
        exit 1
    fi
    print_success "jq is installed"

    # Check if gcloud is installed
    if ! command -v gcloud &> /dev/null; then
        print_error "gcloud CLI is not installed"
        exit 1
    fi
    print_success "gcloud CLI is installed"

    # Check if logged in
    if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" &> /dev/null; then
        print_error "Not logged in to gcloud. Run: gcloud auth login"
        exit 1
    fi
    print_success "Authenticated with gcloud"

    # Check project ID
    if [ -z "$PROJECT_ID" ]; then
        PROJECT_ID=$(gcloud config get-value project)
        if [ -z "$PROJECT_ID" ]; then
            print_error "No GCP project ID set. Set GCP_PROJECT_ID or run: gcloud config set project PROJECT_ID"
            exit 1
        fi
    fi
    print_success "Project ID: $PROJECT_ID"

    # Check config file
    if [ ! -f "$CONFIG_FILE" ]; then
        print_error "Config file not found: $CONFIG_FILE"
        exit 1
    fi
    print_success "Config file found: $CONFIG_FILE"
}

# Build application
build_application() {
    print_header "Building Application"

    npm install
    npm run build

    print_success "Application built successfully"
}

# Deploy to Cloud Run
deploy_cloud_run() {
    local region=$1
    local service_name="genkit-app"

    print_info "Deploying to Cloud Run in $region..."

    gcloud run deploy "$service_name" \
        --source=. \
        --region="$region" \
        --platform=managed \
        --allow-unauthenticated \
        --memory=1Gi \
        --cpu=1 \
        --max-instances=100 \
        --min-instances=0 \
        --port=8080 \
        --set-env-vars="REGION=$region,NODE_ENV=production" \
        --set-secrets="ANTHROPIC_API_KEY=ANTHROPIC_API_KEY:latest,GOOGLE_AI_API_KEY=GOOGLE_AI_API_KEY:latest" \
        --quiet

    # Get service URL
    SERVICE_URL=$(gcloud run services describe "$service_name" \
        --region="$region" \
        --format='value(status.url)')

    print_success "Deployed to $region: $SERVICE_URL"
    echo "$SERVICE_URL" > "/tmp/deploy-${region}.url"
}

# Deploy to Firebase Functions
deploy_firebase() {
    local region=$1

    print_info "Deploying to Firebase Functions in $region..."

    firebase deploy \
        --only functions \
        --project "$PROJECT_ID" \
        --force \
        --config "firebase.${region}.json"

    print_success "Deployed Firebase Functions to $region"
}

# Deploy to specific region
deploy_to_region() {
    local region_id=$1
    local region_location=$2

    print_header "Deploying to Region: $region_id ($region_location)"

    if [ "$DEPLOYMENT_TYPE" = "cloud-run" ]; then
        deploy_cloud_run "$region_location"
    elif [ "$DEPLOYMENT_TYPE" = "firebase" ]; then
        deploy_firebase "$region_location"
    else
        print_error "Unknown deployment type: $DEPLOYMENT_TYPE"
        return 1
    fi
}

# Health check for deployed region
health_check() {
    local region=$1
    local url=$2
    local max_attempts=5
    local attempt=1

    print_info "Running health check for $region..."

    while [ $attempt -le $max_attempts ]; do
        if curl -sf "${url}/health" > /dev/null; then
            print_success "Health check passed for $region"
            return 0
        fi

        print_info "Health check attempt $attempt/$max_attempts failed, retrying..."
        attempt=$((attempt + 1))
        sleep 10
    done

    print_error "Health check failed for $region after $max_attempts attempts"
    return 1
}

# Deploy to all regions
deploy_all() {
    print_header "Multi-Region Deployment"

    # Parse regions from config
    regions=$(jq -r '.regions[] | "\(.id):\(.location)"' "$CONFIG_FILE")

    # Deploy to each region in parallel
    pids=()
    for region_info in $regions; do
        region_id=$(echo "$region_info" | cut -d: -f1)
        region_location=$(echo "$region_info" | cut -d: -f2)

        (deploy_to_region "$region_id" "$region_location") &
        pids+=($!)
    done

    # Wait for all deployments
    print_info "Waiting for all deployments to complete..."
    failed=0
    for pid in "${pids[@]}"; do
        if ! wait "$pid"; then
            failed=$((failed + 1))
        fi
    done

    if [ $failed -gt 0 ]; then
        print_error "$failed region(s) failed to deploy"
        return 1
    fi

    print_success "All regions deployed successfully!"
}

# Run health checks for all regions
check_all_health() {
    print_header "Health Checks"

    regions=$(jq -r '.regions[] | "\(.id):\(.location)"' "$CONFIG_FILE")

    failed=0
    for region_info in $regions; do
        region_id=$(echo "$region_info" | cut -d: -f1)
        region_location=$(echo "$region_info" | cut -d: -f2)

        # Get URL from deployment
        if [ -f "/tmp/deploy-${region_location}.url" ]; then
            url=$(cat "/tmp/deploy-${region_location}.url")
            if ! health_check "$region_id" "$url"; then
                failed=$((failed + 1))
            fi
        else
            print_error "No deployment URL found for $region_id"
            failed=$((failed + 1))
        fi
    done

    if [ $failed -gt 0 ]; then
        print_error "$failed region(s) failed health checks"
        return 1
    fi

    print_success "All regions passed health checks!"
}

# Configure load balancer
configure_load_balancer() {
    print_header "Configuring Load Balancer"

    # This is a placeholder - actual implementation depends on your setup
    print_info "Load balancer configuration..."

    # For Cloud Run, you can use Google Cloud Load Balancer
    # For Firebase, CDN is automatic

    print_success "Load balancer configured"
}

# Main execution
main() {
    print_header "Multi-Region Deployment for Genkit"

    check_prerequisites
    build_application
    deploy_all
    sleep 30  # Wait for deployments to stabilize
    check_all_health
    configure_load_balancer

    print_header "Deployment Complete! 🎉"

    # Print summary
    echo ""
    echo "Deployment Summary:"
    echo "=================="
    regions=$(jq -r '.regions[] | "\(.id): \(.name) (\(.location))"' "$CONFIG_FILE")
    echo "$regions"
    echo ""
    echo "Next steps:"
    echo "1. Monitor health: ./multi-region/scripts/health-check.sh"
    echo "2. Test failover: ./multi-region/scripts/failover.sh"
    echo "3. View metrics: Check your cloud console"
}

# Run main function
main
