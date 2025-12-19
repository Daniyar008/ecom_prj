#!/bin/bash
# =============================================================================
# Kubernetes Deployment Script
# =============================================================================
# Usage: ./deploy.sh [environment] [action]
# Example: ./deploy.sh production apply

set -e

# =============================================================================
# Configuration
# =============================================================================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
K8S_DIR="${SCRIPT_DIR}/k8s"

# Default values
ENVIRONMENT="${1:-development}"
ACTION="${2:-apply}"
DOCKER_REGISTRY="${DOCKER_REGISTRY:-ghcr.io/your-org}"
IMAGE_TAG="${IMAGE_TAG:-latest}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# =============================================================================
# Functions
# =============================================================================
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    if ! command -v kubectl &> /dev/null; then
        log_error "kubectl is not installed"
    fi
    
    if ! command -v kustomize &> /dev/null; then
        log_warning "kustomize is not installed, using kubectl kustomize"
    fi
    
    # Check cluster connectivity
    if ! kubectl cluster-info &> /dev/null; then
        log_error "Cannot connect to Kubernetes cluster"
    fi
    
    log_success "Prerequisites check passed"
}

# Build and push Docker image
build_and_push() {
    log_info "Building Docker image..."
    
    docker build -t "${DOCKER_REGISTRY}/ecommerce:${IMAGE_TAG}" .
    
    log_info "Pushing image to registry..."
    docker push "${DOCKER_REGISTRY}/ecommerce:${IMAGE_TAG}"
    
    log_success "Image built and pushed: ${DOCKER_REGISTRY}/ecommerce:${IMAGE_TAG}"
}

# Deploy using Kustomize
deploy() {
    local overlay_path="${K8S_DIR}/overlays/${ENVIRONMENT}"
    
    if [ ! -d "$overlay_path" ]; then
        log_error "Environment overlay not found: ${overlay_path}"
    fi
    
    log_info "Deploying to ${ENVIRONMENT} environment..."
    
    # Export variables for kustomize
    export DOCKER_REGISTRY
    export IMAGE_TAG
    
    case $ACTION in
        apply)
            kubectl apply -k "$overlay_path"
            ;;
        delete)
            kubectl delete -k "$overlay_path"
            ;;
        diff)
            kubectl diff -k "$overlay_path" || true
            ;;
        dry-run)
            kubectl apply -k "$overlay_path" --dry-run=client
            ;;
        *)
            log_error "Unknown action: ${ACTION}"
            ;;
    esac
    
    log_success "Deployment action '${ACTION}' completed for ${ENVIRONMENT}"
}

# Wait for deployment to be ready
wait_for_deployment() {
    log_info "Waiting for deployment to be ready..."
    
    local namespace="ecommerce"
    if [ "$ENVIRONMENT" == "development" ]; then
        namespace="ecommerce-dev"
    fi
    
    kubectl rollout status deployment/ecommerce-web -n "$namespace" --timeout=300s
    
    log_success "Deployment is ready"
}

# Run database migrations
run_migrations() {
    log_info "Running database migrations..."
    
    local namespace="ecommerce"
    if [ "$ENVIRONMENT" == "development" ]; then
        namespace="ecommerce-dev"
    fi
    
    kubectl exec -it deployment/ecommerce-web -n "$namespace" -- python manage.py migrate
    
    log_success "Migrations completed"
}

# Collect static files
collect_static() {
    log_info "Collecting static files..."
    
    local namespace="ecommerce"
    if [ "$ENVIRONMENT" == "development" ]; then
        namespace="ecommerce-dev"
    fi
    
    kubectl exec -it deployment/ecommerce-web -n "$namespace" -- python manage.py collectstatic --noinput
    
    log_success "Static files collected"
}

# Print deployment status
print_status() {
    log_info "Deployment Status:"
    
    local namespace="ecommerce"
    if [ "$ENVIRONMENT" == "development" ]; then
        namespace="ecommerce-dev"
    fi
    
    echo ""
    echo "=== Pods ==="
    kubectl get pods -n "$namespace"
    
    echo ""
    echo "=== Services ==="
    kubectl get svc -n "$namespace"
    
    echo ""
    echo "=== Ingress ==="
    kubectl get ingress -n "$namespace"
    
    echo ""
    echo "=== HPA ==="
    kubectl get hpa -n "$namespace"
}

# Show help
show_help() {
    echo "Usage: $0 [environment] [action]"
    echo ""
    echo "Environments:"
    echo "  development   Deploy to development environment"
    echo "  production    Deploy to production environment"
    echo ""
    echo "Actions:"
    echo "  apply         Apply the deployment (default)"
    echo "  delete        Delete the deployment"
    echo "  diff          Show differences"
    echo "  dry-run       Dry run without applying"
    echo "  build         Build and push Docker image"
    echo "  migrate       Run database migrations"
    echo "  static        Collect static files"
    echo "  status        Show deployment status"
    echo ""
    echo "Environment variables:"
    echo "  DOCKER_REGISTRY   Docker registry (default: ghcr.io/your-org)"
    echo "  IMAGE_TAG         Image tag (default: latest)"
}

# =============================================================================
# Main
# =============================================================================
case $ACTION in
    help|--help|-h)
        show_help
        exit 0
        ;;
    build)
        check_prerequisites
        build_and_push
        ;;
    migrate)
        run_migrations
        ;;
    static)
        collect_static
        ;;
    status)
        print_status
        ;;
    apply|delete|diff|dry-run)
        check_prerequisites
        deploy
        if [ "$ACTION" == "apply" ]; then
            wait_for_deployment
            print_status
        fi
        ;;
    *)
        log_error "Unknown action: ${ACTION}. Use --help for usage."
        ;;
esac
