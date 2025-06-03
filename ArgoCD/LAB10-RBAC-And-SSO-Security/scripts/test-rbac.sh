#!/bin/bash

set -e

echo "Testing ArgoCD RBAC Configuration..."

# Deploy test applications
echo "1. Deploying test applications..."
kubectl apply -f test-scenarios/test-applications.yaml

# Wait for applications to be created
sleep 10

# Check applications were created
echo "2. Checking test applications..."
kubectl get applications -n argocd | grep test-app

# Test basic RBAC policies
echo "3. Testing RBAC policies..."

# Check that RBAC config is applied
kubectl get configmap argocd-rbac-cm -n argocd -o yaml

# Check projects are created
echo "4. Verifying projects..."
kubectl get appprojects -n argocd

# Check ArgoCD server logs for RBAC messages
echo "5. Checking ArgoCD server logs for RBAC..."
kubectl logs -n argocd deployment/argocd-server --tail=20 | grep -i rbac || echo "No recent RBAC logs"

# Test project-specific access
echo "6. Testing project access controls..."
echo "✅ Development project: dev"
kubectl get appproject dev -n argocd -o yaml | grep -A 10 "spec:"

echo "✅ Staging project: staging"
kubectl get appproject staging -n argocd -o yaml | grep -A 10 "spec:"

echo "✅ Production project: production"
kubectl get appproject production -n argocd -o yaml | grep -A 10 "spec:"

echo "✅ RBAC testing complete!"
echo "💡 Login via SSO to test user-specific permissions"
echo "💡 Check audit logs: kubectl logs -n argocd deployment/argocd-server | grep -i audit" 