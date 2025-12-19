# =============================================================================
# Terraform Configuration for Kubernetes Infrastructure
# =============================================================================

terraform {
  required_version = ">= 1.0"
  
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.23"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.11"
    }
    # Uncomment for your cloud provider
    # aws = {
    #   source  = "hashicorp/aws"
    #   version = "~> 5.0"
    # }
    # google = {
    #   source  = "hashicorp/google"
    #   version = "~> 5.0"
    # }
    # azurerm = {
    #   source  = "hashicorp/azurerm"
    #   version = "~> 3.0"
    # }
  }
  
  # Backend configuration for state management
  # backend "s3" {
  #   bucket = "terraform-state-ecommerce"
  #   key    = "k8s/terraform.tfstate"
  #   region = "us-east-1"
  # }
}

# =============================================================================
# Variables
# =============================================================================

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "production"
}

variable "namespace" {
  description = "Kubernetes namespace"
  type        = string
  default     = "ecommerce"
}

variable "domain" {
  description = "Application domain"
  type        = string
  default     = "ecommerce.example.com"
}

variable "image_repository" {
  description = "Docker image repository"
  type        = string
  default     = "ghcr.io/your-org/ecommerce"
}

variable "image_tag" {
  description = "Docker image tag"
  type        = string
  default     = "latest"
}

variable "replicas" {
  description = "Number of web replicas"
  type        = number
  default     = 3
}

# =============================================================================
# Kubernetes Provider
# =============================================================================

provider "kubernetes" {
  # Configure based on your cluster access method
  config_path = "~/.kube/config"
  # Or use:
  # host                   = var.cluster_endpoint
  # cluster_ca_certificate = base64decode(var.cluster_ca_cert)
  # token                  = var.cluster_token
}

provider "helm" {
  kubernetes {
    config_path = "~/.kube/config"
  }
}

# =============================================================================
# Namespace
# =============================================================================

resource "kubernetes_namespace" "ecommerce" {
  metadata {
    name = var.namespace
    
    labels = {
      "app.kubernetes.io/name"       = "ecommerce"
      "app.kubernetes.io/managed-by" = "terraform"
      "environment"                  = var.environment
    }
  }
}

# =============================================================================
# Helm Releases
# =============================================================================

# Nginx Ingress Controller
resource "helm_release" "nginx_ingress" {
  name             = "nginx-ingress"
  repository       = "https://kubernetes.github.io/ingress-nginx"
  chart            = "ingress-nginx"
  namespace        = "ingress-nginx"
  create_namespace = true
  version          = "4.8.0"
  
  set {
    name  = "controller.replicaCount"
    value = "2"
  }
  
  set {
    name  = "controller.metrics.enabled"
    value = "true"
  }
}

# cert-manager for TLS certificates
resource "helm_release" "cert_manager" {
  name             = "cert-manager"
  repository       = "https://charts.jetstack.io"
  chart            = "cert-manager"
  namespace        = "cert-manager"
  create_namespace = true
  version          = "1.13.0"
  
  set {
    name  = "installCRDs"
    value = "true"
  }
}

# Prometheus Stack (optional)
resource "helm_release" "prometheus" {
  count = var.environment == "production" ? 1 : 0
  
  name             = "prometheus"
  repository       = "https://prometheus-community.github.io/helm-charts"
  chart            = "kube-prometheus-stack"
  namespace        = "monitoring"
  create_namespace = true
  version          = "52.0.0"
  
  set {
    name  = "grafana.enabled"
    value = "true"
  }
  
  set {
    name  = "grafana.adminPassword"
    value = "admin"  # Change in production
  }
}

# =============================================================================
# E-commerce Application Deployment
# =============================================================================

resource "helm_release" "ecommerce" {
  name      = "ecommerce"
  chart     = "../helm/ecommerce"
  namespace = kubernetes_namespace.ecommerce.metadata[0].name
  
  values = [
    file("../helm/ecommerce/values.yaml")
  ]
  
  set {
    name  = "image.repository"
    value = var.image_repository
  }
  
  set {
    name  = "image.tag"
    value = var.image_tag
  }
  
  set {
    name  = "replicaCount"
    value = var.replicas
  }
  
  set {
    name  = "ingress.hosts[0].host"
    value = var.domain
  }
  
  depends_on = [
    helm_release.nginx_ingress,
    helm_release.cert_manager,
  ]
}

# =============================================================================
# Outputs
# =============================================================================

output "namespace" {
  description = "Kubernetes namespace"
  value       = kubernetes_namespace.ecommerce.metadata[0].name
}

output "app_url" {
  description = "Application URL"
  value       = "https://${var.domain}"
}
