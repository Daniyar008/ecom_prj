# =============================================================================
# E-commerce Django Application - Infrastructure Documentation
# =============================================================================

## 🏗️ Architecture Overview

```
                                    ┌─────────────────┐
                                    │   CloudFlare    │
                                    │   (CDN/WAF)     │
                                    └────────┬────────┘
                                             │
                                    ┌────────▼────────┐
                                    │ Nginx Ingress   │
                                    │  Controller     │
                                    └────────┬────────┘
                                             │
                    ┌────────────────────────┼────────────────────────┐
                    │                        │                        │
           ┌────────▼────────┐     ┌─────────▼────────┐     ┌────────▼────────┐
           │  Django Web     │     │   Django Web     │     │   Django Web    │
           │  (Gunicorn)     │     │   (Gunicorn)     │     │   (Gunicorn)    │
           │   Pod 1         │     │    Pod 2         │     │    Pod 3        │
           └────────┬────────┘     └─────────┬────────┘     └────────┬────────┘
                    │                        │                        │
                    └────────────────────────┼────────────────────────┘
                                             │
                    ┌────────────────────────┼────────────────────────┐
                    │                        │                        │
           ┌────────▼────────┐     ┌─────────▼────────┐     ┌────────▼────────┐
           │   PostgreSQL    │     │      Redis       │     │  Celery Worker  │
           │  StatefulSet    │     │   StatefulSet    │     │   Deployment    │
           └─────────────────┘     └──────────────────┘     └─────────────────┘
```

## 📦 Quick Start

### Development Environment
```bash
# Start development environment
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Access at http://localhost:8000
```

### Production with Docker Swarm
```bash
# Deploy to Docker Swarm
docker stack deploy -c docker-compose.prod.yml ecommerce

# Scale services
docker service scale ecommerce_web=5
```

---

## 🐳 Docker Configuration

### Images
- **Web Application**: Python 3.11 + Gunicorn
- **Database**: PostgreSQL 15 Alpine
- **Cache**: Redis 7 Alpine
- **Reverse Proxy**: Nginx 1.25 Alpine

### Build
```bash
# Build image
docker build -t ghcr.io/your-org/ecommerce:latest .

# Build with specific tag
docker build -t ghcr.io/your-org/ecommerce:v1.0.0 .

# Multi-platform build
docker buildx build --platform linux/amd64,linux/arm64 -t ghcr.io/your-org/ecommerce:latest --push .
```

---

## ☸️ Kubernetes Deployment

### Prerequisites
- Kubernetes cluster (1.25+)
- kubectl configured
- Nginx Ingress Controller
- cert-manager (for TLS)

### Directory Structure
```
k8s/
├── base/                    # Base Kustomize configuration
│   ├── kustomization.yaml
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── secrets.yaml
│   ├── deployment.yaml
│   ├── celery-deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── statefulsets.yaml
│   ├── pvc.yaml
│   ├── hpa.yaml
│   ├── rbac.yaml
│   ├── certificate.yaml
│   ├── cronjobs.yaml
│   ├── jobs.yaml
│   ├── monitoring.yaml
│   ├── grafana-dashboard.yaml
│   └── external-secrets.yaml
├── overlays/
│   ├── development/         # Development-specific patches
│   └── production/          # Production-specific patches
```

### Deploy with Kustomize
```bash
# Development
kubectl apply -k k8s/overlays/development

# Production
kubectl apply -k k8s/overlays/production

# Preview changes
kubectl diff -k k8s/overlays/production
```

### Deploy with Helm
```bash
# Install/upgrade
helm upgrade --install ecommerce ./helm/ecommerce \
    --namespace ecommerce \
    --create-namespace \
    -f ./helm/ecommerce/values.yaml

# With custom values
helm upgrade --install ecommerce ./helm/ecommerce \
    --set image.tag=v1.0.0 \
    --set ingress.hosts[0].host=mystore.com
```

### Deploy with Terraform
```bash
cd terraform
terraform init
terraform plan
terraform apply
```

### Deploy with ArgoCD (GitOps)
```bash
kubectl apply -f argocd/application.yaml
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | Required |
| `DEBUG` | Debug mode | `False` |
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `REDIS_URL` | Redis connection string | Required |
| `ALLOWED_HOSTS` | Allowed hosts | `localhost` |
| `CELERY_BROKER_URL` | Celery broker URL | Redis URL |

### Secrets Management
```bash
# Create secrets from literals
kubectl create secret generic ecommerce-secrets \
    --from-literal=SECRET_KEY='your-secret-key' \
    --from-literal=DATABASE_URL='postgresql://...' \
    -n ecommerce

# From file
kubectl create secret generic ecommerce-secrets \
    --from-env-file=.env.production \
    -n ecommerce
```

---

## 📊 Monitoring

### Prometheus Metrics
The application exposes metrics at `/metrics` endpoint.

### Grafana Dashboard
Import the dashboard from `k8s/base/grafana-dashboard.yaml`.

### Health Checks
- **Full Health**: `/health/` - DB + Cache check
- **Liveness**: `/healthz/` - Simple alive check
- **Readiness**: `/readyz/` - Ready to accept traffic

### Alerting
Prometheus rules configured in `k8s/base/monitoring.yaml`:
- High error rate (>5%)
- High response time (P95 > 2s)
- Pod not ready
- Database connection errors
- High memory usage (>90%)
- Celery queue backlog

### Logging
```bash
# View web logs
kubectl logs -f deployment/ecommerce-web -n ecommerce

# View all pods
kubectl logs -f -l app.kubernetes.io/name=ecommerce -n ecommerce
```

---

## 🚀 CI/CD Pipeline

### GitHub Actions Workflow
1. **Test**: Lint and run tests
2. **Build**: Build and push Docker image
3. **Security**: Trivy vulnerability scan
4. **Deploy Dev**: Auto-deploy to development
5. **Deploy Prod**: Manual approval for production

### Trigger Deployments
```bash
# Development (automatic on develop branch)
git push origin develop

# Production (create a release tag)
git tag v1.0.0
git push origin v1.0.0
```

---

## 🔐 Security

### Best Practices Implemented
- Non-root container execution
- Read-only root filesystem
- Resource limits and requests
- Network policies
- Pod security contexts
- HTTPS only with HSTS
- Rate limiting
- Security headers

### SSL/TLS
TLS certificates are managed by cert-manager with Let's Encrypt.

---

## 📈 Scaling

### Horizontal Pod Autoscaler
```yaml
# Automatically scales based on CPU/Memory
minReplicas: 3
maxReplicas: 10
targetCPUUtilization: 70%
```

### Manual Scaling
```bash
# Scale web deployment
kubectl scale deployment ecommerce-web --replicas=5 -n ecommerce

# Scale celery workers
kubectl scale deployment ecommerce-celery-worker --replicas=4 -n ecommerce
```

---

## 🔄 Rollback

### Kubernetes
```bash
# View rollout history
kubectl rollout history deployment/ecommerce-web -n ecommerce

# Rollback to previous version
kubectl rollout undo deployment/ecommerce-web -n ecommerce

# Rollback to specific revision
kubectl rollout undo deployment/ecommerce-web --to-revision=2 -n ecommerce
```

---

## 📁 Make Commands

```bash
make help           # Show all commands
make dev            # Start development environment
make test           # Run tests
make build          # Build Docker image
make k8s-prod       # Deploy to production
make db-backup      # Backup database
```

## 📁 PowerShell Commands (Windows)

```powershell
.\deploy.ps1 development apply    # Deploy to dev
.\deploy.ps1 production apply     # Deploy to prod
.\deploy.ps1 production status    # Show status
.\deploy.ps1 -Action build        # Build image
```

---

## 📞 Support

For issues or questions, please open a GitHub issue or contact the DevOps team.
