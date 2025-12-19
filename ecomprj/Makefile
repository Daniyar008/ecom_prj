# =============================================================================
# Makefile for Project Management
# =============================================================================

.PHONY: help build run test deploy clean

# Variables
DOCKER_REGISTRY ?= ghcr.io/your-org
IMAGE_NAME ?= ecommerce
IMAGE_TAG ?= latest
ENVIRONMENT ?= development

# Colors
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[1;33m
NC := \033[0m

# Default target
help:
	@echo "$(BLUE)E-commerce Project Management$(NC)"
	@echo ""
	@echo "$(GREEN)Development:$(NC)"
	@echo "  make dev           - Start development environment"
	@echo "  make dev-down      - Stop development environment"
	@echo "  make shell         - Open Django shell"
	@echo "  make migrate       - Run database migrations"
	@echo "  make makemigrations - Create new migrations"
	@echo "  make static        - Collect static files"
	@echo "  make createsuperuser - Create admin user"
	@echo ""
	@echo "$(GREEN)Testing:$(NC)"
	@echo "  make test          - Run tests"
	@echo "  make test-cov      - Run tests with coverage"
	@echo "  make lint          - Run linting"
	@echo ""
	@echo "$(GREEN)Docker:$(NC)"
	@echo "  make build         - Build Docker image"
	@echo "  make push          - Push Docker image"
	@echo "  make run           - Run with Docker Compose"
	@echo "  make logs          - View container logs"
	@echo ""
	@echo "$(GREEN)Kubernetes:$(NC)"
	@echo "  make k8s-dev       - Deploy to development"
	@echo "  make k8s-prod      - Deploy to production"
	@echo "  make k8s-status    - Show deployment status"
	@echo ""
	@echo "$(GREEN)Database:$(NC)"
	@echo "  make db-backup     - Backup database"
	@echo "  make db-restore    - Restore database"

# =============================================================================
# Development
# =============================================================================
dev:
	docker-compose up -d
	@echo "$(GREEN)Development environment started$(NC)"
	@echo "Access at: http://localhost:8000"

dev-down:
	docker-compose down

dev-logs:
	docker-compose logs -f

shell:
	docker-compose exec web python manage.py shell

migrate:
	docker-compose exec web python manage.py migrate

makemigrations:
	docker-compose exec web python manage.py makemigrations

static:
	docker-compose exec web python manage.py collectstatic --noinput

createsuperuser:
	docker-compose exec web python manage.py createsuperuser

# =============================================================================
# Testing
# =============================================================================
test:
	docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit
	docker-compose -f docker-compose.test.yml down -v

test-cov:
	docker-compose exec web pytest --cov=. --cov-report=html
	@echo "$(GREEN)Coverage report: htmlcov/index.html$(NC)"

lint:
	docker-compose exec web flake8 .
	docker-compose exec web black --check .

format:
	docker-compose exec web black .
	docker-compose exec web isort .

# =============================================================================
# Docker
# =============================================================================
build:
	docker build -t $(DOCKER_REGISTRY)/$(IMAGE_NAME):$(IMAGE_TAG) .
	@echo "$(GREEN)Image built: $(DOCKER_REGISTRY)/$(IMAGE_NAME):$(IMAGE_TAG)$(NC)"

push: build
	docker push $(DOCKER_REGISTRY)/$(IMAGE_NAME):$(IMAGE_TAG)
	@echo "$(GREEN)Image pushed$(NC)"

run:
	docker-compose -f docker-compose.prod.yml up -d

logs:
	docker-compose logs -f web

# =============================================================================
# Kubernetes
# =============================================================================
k8s-dev:
	./deploy.sh development apply

k8s-prod:
	./deploy.sh production apply

k8s-status:
	./deploy.sh production status

k8s-diff:
	./deploy.sh production diff

# =============================================================================
# Helm
# =============================================================================
helm-install:
	helm upgrade --install ecommerce ./helm/ecommerce \
		--namespace ecommerce \
		--create-namespace \
		-f ./helm/ecommerce/values.yaml

helm-uninstall:
	helm uninstall ecommerce --namespace ecommerce

helm-template:
	helm template ecommerce ./helm/ecommerce

# =============================================================================
# Database
# =============================================================================
db-backup:
	@echo "$(YELLOW)Creating database backup...$(NC)"
	docker-compose exec db pg_dump -U postgres ecommerce > backup_$$(date +%Y%m%d_%H%M%S).sql
	@echo "$(GREEN)Backup created$(NC)"

db-restore:
	@echo "$(YELLOW)Restoring database from $(BACKUP_FILE)...$(NC)"
	docker-compose exec -T db psql -U postgres ecommerce < $(BACKUP_FILE)
	@echo "$(GREEN)Database restored$(NC)"

# =============================================================================
# Cleanup
# =============================================================================
clean:
	docker-compose down -v --remove-orphans
	docker system prune -f
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

clean-all: clean
	docker-compose down -v --rmi all
