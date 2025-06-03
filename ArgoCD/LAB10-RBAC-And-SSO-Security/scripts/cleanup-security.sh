#!/bin/bash

set -e

echo "Cleaning up ArgoCD Security Configuration..."

# Remove test applications
echo "1. Removing test applications..."
kubectl delete -f test-scenarios/test-applications.yaml --ignore-not-found=true

# Remove projects
echo "2. Removing projects..."
kubectl delete -f projects/ --ignore-not-found=true

# Remove security configurations
echo "3. Removing security configurations..."
kubectl delete configmap argocd-rbac-cm -n argocd --ignore-not-found=true
kubectl delete configmap argocd-cm-security -n argocd --ignore-not-found=true
kubectl delete configmap argocd-audit-cm -n argocd --ignore-not-found=true

# Restore original configuration if backup exists
echo "4. Restoring original configuration..."
if [ -f "backup-argocd-cm.yaml" ]; then
    kubectl apply -f backup-argocd-cm.yaml
    echo "Original argocd-cm restored"
else
    echo "No backup found, skipping restore"
fi

# Restart ArgoCD components
echo "5. Restarting ArgoCD components..."
kubectl rollout restart deployment/argocd-server -n argocd
kubectl rollout restart deployment/argocd-dex-server -n argocd
kubectl rollout restart deployment/argocd-application-controller -n argocd

# Clean up test namespaces
echo "6. Cleaning up test namespaces..."
kubectl delete namespace dev-test staging-test production-test --ignore-not-found=true

echo "✅ Cleanup complete!"
echo "🔓 ArgoCD restored to default security configuration." 