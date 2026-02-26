# Phase 4: Cloud-Native DevOps Testing Guide

## Overview
This guide provides comprehensive instructions for testing the implemented cloud-native components of the AI-ready full-stack todo app. Follow these steps to validate containerization, Kubernetes deployment, Helm packaging, and AI DevOps tools.

## Prerequisites
Before testing, ensure you have the following tools installed:
- Docker Desktop (with Kubernetes enabled) OR Minikube
- Helm 3.x
- kubectl
- Node.js (for building frontend if needed)
- Git (for cloning repositories if needed)

## 1. Containerization Testing

### 1.1 Build Docker Images
```bash
# Navigate to frontend directory
cd C:\Users\USER\Desktop\agentic-todo-system\phase-4\frontend

# Build frontend container
docker build -t todo-frontend:latest .

# Navigate to backend directory
cd C:\Users\USER\Desktop\agentic-todo-system\phase-4\backend

# Build backend container
docker build -t todo-backend:latest .
```

### 1.2 Verify Images Were Built
```bash
# List Docker images to confirm they were created
docker images | findstr todo-
```

### 1.3 Test Containers Locally
```bash
# Test frontend container (note: requires backend to be available)
docker run -p 3000:3000 todo-frontend:latest

# Test backend container (requires database connection)
docker run -p 8000:8000 -e DATABASE_URL="postgresql://user:password@host:5432/dbname" todo-backend:latest
```

### 1.4 Verify Container Functionality
- Check container logs: `docker logs <container-id>`
- Verify health check endpoints work
- Ensure non-root execution
- Confirm security features are active

## 2. Kubernetes Deployment Testing

### 2.1 Start Kubernetes Environment
```bash
# Option A: Using Minikube
minikube start

# Option B: Using Docker Desktop Kubernetes
# Ensure Kubernetes is enabled in Docker Desktop settings
```

### 2.2 Apply Kubernetes Resources
```bash
# Create namespace
kubectl apply -f k8s/namespace.yaml

# Create ConfigMaps
kubectl apply -f k8s/configmaps.yaml --namespace todo-app-prod

# Create secrets (for testing purposes)
kubectl create secret generic db-secret --from-literal=url="postgresql://user:password@localhost:5432/todo_db" --namespace todo-app-prod
kubectl create secret generic auth-secret --from-literal=secret="your_test_auth_secret" --namespace todo-app-prod

# Apply network policies
kubectl apply -f k8s/network-policies.yaml --namespace todo-app-prod

# Apply deployments
kubectl apply -f k8s/backend-deployment.yaml --namespace todo-app-prod
kubectl apply -f k8s/frontend-deployment.yaml --namespace todo-app-prod

# Apply services
kubectl apply -f k8s/backend-service.yaml --namespace todo-app-prod
kubectl apply -f k8s/frontend-service.yaml --namespace todo-app-prod

# Apply ingress (if using ingress controller)
kubectl apply -f k8s/ingress.yaml --namespace todo-app-prod
```

### 2.3 Verify Kubernetes Deployment
```bash
# Check all resources
kubectl get all --namespace todo-app-prod

# Check pods status
kubectl get pods --namespace todo-app-prod

# Check services
kubectl get svc --namespace todo-app-prod

# Check deployments
kubectl get deployments --namespace todo-app-prod

# Check logs for each component
kubectl logs -l app=backend --namespace todo-app-prod
kubectl logs -l app=frontend --namespace todo-app-prod
```

### 2.4 Wait for Resources to be Ready
```bash
# Wait for backend pods to be ready
kubectl wait --for=condition=ready pod -l app=backend --timeout=300s --namespace todo-app-prod

# Wait for frontend pods to be ready
kubectl wait --for=condition=ready pod -l app=frontend --timeout=300s --namespace todo-app-prod
```

## 3. Helm Chart Testing

### 3.1 Load Images into Kubernetes (for local testing)
If using Minikube:
```bash
# Load images into Minikube
minikube image load todo-frontend:latest
minikube image load todo-backend:latest
```

If using Docker Desktop Kubernetes:
```bash
# Ensure images are available in the Kubernetes cluster
# Docker Desktop shares the same image store with Kubernetes
```

### 3.2 Install Helm Chart
```bash
# Navigate to project root
cd C:\Users\USER\Desktop\agentic-todo-system\phase-4

# Install the Helm chart (first update values.yaml for local testing)
# For local testing, you may need to update the image pull policy
helm install todo-app ./helm/todo-app --namespace todo-app-prod --create-namespace --set frontend.image.pullPolicy=Never --set backend.image.pullPolicy=Never

# Or install with custom values
helm install todo-app ./helm/todo-app --namespace todo-app-prod --create-namespace --set frontend.image.tag=latest --set backend.image.tag=latest --set frontend.image.pullPolicy=Never --set backend.image.pullPolicy=Never
```

### 3.3 Verify Helm Installation
```bash
# List Helm releases
helm list --namespace todo-app-prod

# Check all resources created by Helm
kubectl get all --namespace todo-app-prod

# Check Helm status
helm status todo-app --namespace todo-app-prod
```

### 3.4 Test Helm Operations
```bash
# Upgrade the release
helm upgrade todo-app ./helm/todo-app --namespace todo-app-prod --set frontend.image.pullPolicy=Never --set backend.image.pullPolicy=Never

# Rollback if needed
helm rollback todo-app --namespace todo-app-prod

# Uninstall when done testing
helm uninstall todo-app --namespace todo-app-prod
```

## 4. AI DevOps Tools Testing

### 4.1 kubectl-ai Configuration and Testing
```bash
# Install kubectl-ai plugin (follow official documentation)
# Copy the configuration file to appropriate location
# On Windows, typically goes to %USERPROFILE%\.kubectl-ai\config.ini

# Test kubectl-ai commands
kubectl ai "show me the pods in todo-app-prod namespace"
kubectl ai "scale the frontend deployment to 3 replicas" --namespace todo-app-prod
```

### 4.2 kagent Deployment and Testing
```bash
# Apply kagent configuration
kubectl apply -f ai-devops/kagent-config.yaml

# Apply kagent deployment
kubectl apply -f ai-devops/kagent-deployment.yaml

# Check if kagent is running
kubectl get pods -l app=kagent --namespace todo-app-prod

# Check kagent logs
kubectl logs -l app=kagent --namespace todo-app-prod

# Check kagent status
kubectl describe pod -l app=kagent --namespace todo-app-prod
```

### 4.3 Monitoring and Observability Testing
```bash
# Apply monitoring configuration
kubectl apply -f ai-devops/monitoring-config.yaml

# Check if ServiceMonitors are created
kubectl get servicemonitors --namespace todo-app-prod

# If using Prometheus Operator, verify targets
kubectl get prometheus --namespace todo-app-prod
```

## 5. End-to-End Application Testing

### 5.1 Port Forwarding for Local Testing
```bash
# Forward frontend service (in separate terminals)
kubectl port-forward svc/todo-app-frontend-service 3000:80 --namespace todo-app-prod

# Forward backend service
kubectl port-forward svc/todo-app-backend-service 8000:80 --namespace todo-app-prod
```

### 5.2 Access Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Health check: http://localhost:8000/health

### 5.3 Functional Testing
- Verify basic application functionality
- Test API endpoints
- Check authentication flows
- Validate task operations

## 6. Automated Testing Script

Create a test script to automate validation:

```bash
#!/bin/bash
# automated-test.sh

echo "Starting automated Phase 4 cloud-native deployment test..."

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "kubectl could not be found. Please install kubectl."
    exit 1
fi

# Check if helm is available
if ! command -v helm &> /dev/null; then
    echo "helm could not be found. Please install helm."
    exit 1
fi

# Check if docker is available
if ! command -v docker &> /dev/null; then
    echo "docker could not be found. Please install docker."
    exit 1
fi

echo "Building Docker images..."
cd ../frontend
docker build -t todo-frontend:latest .
cd ../backend
docker build -t todo-backend:latest .

echo "Verifying Kubernetes cluster connection..."
kubectl cluster-info

echo "Checking for todo-app-prod namespace..."
NAMESPACE_EXISTS=$(kubectl get namespace todo-app-prod --ignore-not-found=true)
if [ -z "$NAMESPACE_EXISTS" ]; then
    echo "Creating todo-app-prod namespace..."
    kubectl apply -f ../k8s/namespace.yaml
fi

echo "Loading images into cluster (if using Minikube)..."
if command -v minikube &> /dev/null; then
    minikube image load todo-frontend:latest
    minikube image load todo-backend:latest
fi

echo "Checking deployments status..."
FRONTEND_DEPLOYMENT=$(kubectl get deployment todo-app-frontend -n todo-app-prod --ignore-not-found=true)
BACKEND_DEPLOYMENT=$(kubectl get deployment todo-app-backend -n todo-app-prod --ignore-not-found=true)

if [ -z "$FRONTEND_DEPLOYMENT" ] || [ -z "$BACKEND_DEPLOYMENT" ]; then
    echo "Deployments not found. Applying manifests..."
    kubectl apply -f ../k8s/configmaps.yaml -n todo-app-prod
    kubectl apply -f ../k8s/backend-deployment.yaml -n todo-app-prod
    kubectl apply -f ../k8s/frontend-deployment.yaml -n todo-app-prod
    kubectl apply -f ../k8s/backend-service.yaml -n todo-app-prod
    kubectl apply -f ../k8s/frontend-service.yaml -n todo-app-prod
    kubectl apply -f ../k8s/network-policies.yaml -n todo-app-prod
fi

echo "Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app=backend --timeout=300s -n todo-app-prod
kubectl wait --for=condition=ready pod -l app=frontend --timeout=300s -n todo-app-prod

echo "Checking service endpoints..."
kubectl get svc -n todo-app-prod

echo "Test completed successfully!"
echo "Access the application:"
echo "- Frontend: kubectl port-forward svc/todo-app-frontend-service 3000:80 -n todo-app-prod"
echo "- Backend: kubectl port-forward svc/todo-app-backend-service 8000:80 -n todo-app-prod"
```

## 7. Cleanup Procedures

### 7.1 Clean Up Kubernetes Resources
```bash
# Uninstall Helm release
helm uninstall todo-app --namespace todo-app-prod

# Or delete all resources manually
kubectl delete namespace todo-app-prod

# Or delete specific resources
kubectl delete -f k8s/ --namespace todo-app-prod
```

### 7.2 Clean Up Docker Images (Optional)
```bash
# Remove Docker images
docker rmi todo-frontend:latest
docker rmi todo-backend:latest

# Clean up unused Docker resources
docker system prune -f
```

## 8. Troubleshooting Common Issues

### 8.1 Image Build Issues
```bash
# Ensure you're in the correct directory when building
cd C:\Users\USER\Desktop\agentic-todo-system\phase-4\frontend
docker build -t todo-frontend:latest .

cd C:\Users\USER\Desktop\agentic-todo-system\phase-4\backend
docker build -t todo-backend:latest .
```

### 8.2 Pod Not Starting
```bash
# Check pod status and events
kubectl describe pod <pod-name> --namespace todo-app-prod

# Check pod logs
kubectl logs <pod-name> --namespace todo-app-prod
```

### 8.3 Service Not Accessible
```bash
# Check service configuration
kubectl describe svc <service-name> --namespace todo-app-prod

# Check endpoints
kubectl get endpoints <service-name> --namespace todo-app-prod
```

### 8.4 Helm Installation Issues
```bash
# Check Helm status
helm status <release-name> --namespace todo-app-prod

# Check Helm history
helm history <release-name> --namespace todo-app-prod
```

## 9. Production Considerations

When deploying to production, ensure:
- Proper database setup and connection
- Valid TLS certificates for ingress
- Secure secret management (consider HashiCorp Vault)
- Proper resource limits and requests
- Monitoring and alerting configuration
- Backup and recovery procedures
- Security scanning integration

## 10. Validation Checklist

Before declaring the deployment successful, verify:
- [ ] All Docker images built successfully
- [ ] All pods are running and healthy
- [ ] Services are accessible
- [ ] Ingress routes are working
- [ ] Health checks pass
- [ ] Application functionality works
- [ ] Security policies are enforced
- [ ] Resource limits are appropriate
- [ ] Monitoring is collecting data
- [ ] Logs are accessible
- [ ] AI DevOps tools are operational