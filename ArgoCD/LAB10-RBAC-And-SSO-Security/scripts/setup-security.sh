#!/bin/bash

set -e

echo "Setting up ArgoCD Security Configuration..."

# Backup existing configuration
echo "1. Backing up existing configuration..."
kubectl get configmap argocd-cm -n argocd -o yaml > backup-argocd-cm.yaml
kubectl get configmap argocd-rbac-cm -n argocd -o yaml > backup-argocd-rbac-cm.yaml 2>/dev/null || echo "No existing RBAC config"

# Apply RBAC configuration
echo "2. Applying RBAC configuration..."
kubectl apply -f rbac-configs/advanced-rbac.yaml

# Apply SSO configuration
echo "3. Applying SSO configuration..."
if [ -f "sso-configs/github-sso.yaml" ]; then
    kubectl apply -f sso-configs/github-sso.yaml
    echo "GitHub SSO configuration applied"
fi

# Apply security policies
echo "4. Applying security policies..."
kubectl apply -f security-configs/security-policies.yaml
kubectl apply -f security-configs/audit-logging.yaml

# Apply projects
echo "5. Applying projects..."
kubectl apply -f projects/dev-project.yaml
kubectl apply -f projects/staging-project.yaml
kubectl apply -f projects/production-project.yaml

# Restart ArgoCD components
echo "6. Restarting ArgoCD components..."
kubectl rollout restart deployment/argocd-server -n argocd
kubectl rollout restart deployment/argocd-dex-server -n argocd
kubectl rollout restart deployment/argocd-application-controller -n argocd

# Wait for components to be ready
echo "7. Waiting for components to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/argocd-server -n argocd
kubectl wait --for=condition=available --timeout=300s deployment/argocd-dex-server -n argocd

echo "✅ ArgoCD Security setup complete!"
echo "💡 You can now test SSO login and RBAC permissions"
echo "💡 Port forward to access: kubectl port-forward svc/argocd-server -n argocd 8080:443" 