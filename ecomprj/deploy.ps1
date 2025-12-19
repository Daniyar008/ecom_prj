#!/usr/bin/env pwsh
# =============================================================================
# Windows PowerShell Deployment Script
# =============================================================================

param(
    [Parameter(Position=0)]
    [ValidateSet("development", "production")]
    [string]$Environment = "development",
    
    [Parameter(Position=1)]
    [ValidateSet("apply", "delete", "diff", "dry-run", "build", "status")]
    [string]$Action = "apply"
)

# Configuration
$DOCKER_REGISTRY = if ($env:DOCKER_REGISTRY) { $env:DOCKER_REGISTRY } else { "ghcr.io/your-org" }
$IMAGE_TAG = if ($env:IMAGE_TAG) { $env:IMAGE_TAG } else { "latest" }
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$K8S_DIR = Join-Path $SCRIPT_DIR "k8s"

# Colors
function Write-Info { param($Message) Write-Host "[INFO] $Message" -ForegroundColor Blue }
function Write-Success { param($Message) Write-Host "[SUCCESS] $Message" -ForegroundColor Green }
function Write-Warning { param($Message) Write-Host "[WARNING] $Message" -ForegroundColor Yellow }
function Write-Error { param($Message) Write-Host "[ERROR] $Message" -ForegroundColor Red }

# Check prerequisites
function Test-Prerequisites {
    Write-Info "Checking prerequisites..."
    
    if (-not (Get-Command kubectl -ErrorAction SilentlyContinue)) {
        Write-Error "kubectl is not installed"
        exit 1
    }
    
    try {
        kubectl cluster-info 2>&1 | Out-Null
    } catch {
        Write-Error "Cannot connect to Kubernetes cluster"
        exit 1
    }
    
    Write-Success "Prerequisites check passed"
}

# Build Docker image
function Build-Image {
    Write-Info "Building Docker image..."
    
    docker build -t "${DOCKER_REGISTRY}/ecommerce:${IMAGE_TAG}" .
    
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Image built: ${DOCKER_REGISTRY}/ecommerce:${IMAGE_TAG}"
    } else {
        Write-Error "Build failed"
        exit 1
    }
}

# Deploy to Kubernetes
function Deploy-App {
    $OverlayPath = Join-Path $K8S_DIR "overlays" $Environment
    
    if (-not (Test-Path $OverlayPath)) {
        Write-Error "Environment overlay not found: $OverlayPath"
        exit 1
    }
    
    Write-Info "Deploying to $Environment environment..."
    
    $env:DOCKER_REGISTRY = $DOCKER_REGISTRY
    $env:IMAGE_TAG = $IMAGE_TAG
    
    switch ($Action) {
        "apply" {
            kubectl apply -k $OverlayPath
        }
        "delete" {
            kubectl delete -k $OverlayPath
        }
        "diff" {
            kubectl diff -k $OverlayPath
        }
        "dry-run" {
            kubectl apply -k $OverlayPath --dry-run=client
        }
    }
    
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Deployment action '$Action' completed for $Environment"
    }
}

# Show status
function Show-Status {
    Write-Info "Deployment Status:"
    
    $Namespace = if ($Environment -eq "development") { "ecommerce-dev" } else { "ecommerce" }
    
    Write-Host "`n=== Pods ===" -ForegroundColor Cyan
    kubectl get pods -n $Namespace
    
    Write-Host "`n=== Services ===" -ForegroundColor Cyan
    kubectl get svc -n $Namespace
    
    Write-Host "`n=== Ingress ===" -ForegroundColor Cyan
    kubectl get ingress -n $Namespace
    
    Write-Host "`n=== HPA ===" -ForegroundColor Cyan
    kubectl get hpa -n $Namespace
}

# Main execution
switch ($Action) {
    "build" {
        Build-Image
    }
    "status" {
        Show-Status
    }
    default {
        Test-Prerequisites
        Deploy-App
        if ($Action -eq "apply") {
            Write-Info "Waiting for deployment to be ready..."
            $Namespace = if ($Environment -eq "development") { "ecommerce-dev" } else { "ecommerce" }
            kubectl rollout status deployment/ecommerce-web -n $Namespace --timeout=300s
            Show-Status
        }
    }
}
