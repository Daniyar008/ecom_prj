# =============================================================================
# Terraform Variables for E-commerce Deployment
# =============================================================================

# Environment
environment = "production"

# Kubernetes
namespace = "ecommerce"

# Application
domain           = "ecommerce.example.com"
image_repository = "ghcr.io/your-org/ecommerce"
image_tag        = "v1.0.0"
replicas         = 3
