#!/bin/bash
# =============================================================================
# CI/CD Pipeline Helper Script
# =============================================================================

set -e

# =============================================================================
# GitHub Actions / GitLab CI Integration
# =============================================================================

# Build Docker image with caching
build_docker() {
    local tag="${1:-latest}"
    
    echo "Building Docker image with tag: ${tag}"
    
    docker build \
        --cache-from "${DOCKER_REGISTRY}/ecommerce:latest" \
        --build-arg BUILDKIT_INLINE_CACHE=1 \
        -t "${DOCKER_REGISTRY}/ecommerce:${tag}" \
        -t "${DOCKER_REGISTRY}/ecommerce:latest" \
        -f Dockerfile \
        .
}

# Run tests in Docker
run_tests() {
    echo "Running tests..."
    
    docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit
    local exit_code=$?
    
    docker-compose -f docker-compose.test.yml down -v
    
    return $exit_code
}

# Security scan
security_scan() {
    local image="${1:-${DOCKER_REGISTRY}/ecommerce:latest}"
    
    echo "Running security scan on ${image}..."
    
    # Trivy scan
    if command -v trivy &> /dev/null; then
        trivy image --severity HIGH,CRITICAL --exit-code 1 "$image"
    else
        echo "Trivy not installed, skipping security scan"
    fi
}

# Push to registry
push_image() {
    local tag="${1:-latest}"
    
    echo "Pushing image to registry..."
    
    docker push "${DOCKER_REGISTRY}/ecommerce:${tag}"
    docker push "${DOCKER_REGISTRY}/ecommerce:latest"
}

# Deploy to Kubernetes
deploy_k8s() {
    local environment="${1:-production}"
    local tag="${2:-latest}"
    
    echo "Deploying to ${environment} with tag ${tag}..."
    
    export IMAGE_TAG="${tag}"
    ./deploy.sh "${environment}" apply
}

# Rollback deployment
rollback() {
    local environment="${1:-production}"
    
    local namespace="ecommerce"
    if [ "$environment" == "development" ]; then
        namespace="ecommerce-dev"
    fi
    
    echo "Rolling back deployment in ${namespace}..."
    kubectl rollout undo deployment/ecommerce-web -n "$namespace"
}

# Main entry point
case "${1}" in
    build)
        build_docker "${2}"
        ;;
    test)
        run_tests
        ;;
    scan)
        security_scan "${2}"
        ;;
    push)
        push_image "${2}"
        ;;
    deploy)
        deploy_k8s "${2}" "${3}"
        ;;
    rollback)
        rollback "${2}"
        ;;
    full)
        # Full CI/CD pipeline
        build_docker "${2}"
        run_tests
        security_scan
        push_image "${2}"
        deploy_k8s production "${2}"
        ;;
    *)
        echo "Usage: $0 {build|test|scan|push|deploy|rollback|full} [args...]"
        exit 1
        ;;
esac
