#!/bin/bash

set -e

echo "Cleaning up ArgoCD Notifications..."

# Remove test applications
echo "1. Removing test applications..."
kubectl delete -f test-scenarios/ --ignore-not-found=true

# Remove notifications configuration
echo "2. Removing notifications configuration..."
kubectl delete -f notification-configs/master-notifications-config.yaml --ignore-not-found=true

# Remove secrets
echo "3. Removing secrets..."
kubectl delete -f secrets/email-credentials-secret.yaml --ignore-not-found=true
kubectl delete -f secrets/slack-webhook-secret.yaml --ignore-not-found=true

# Remove controller
echo "4. Removing notifications controller..."
kubectl delete -f notification-controller/argocd-notifications-controller.yaml --ignore-not-found=true

# Remove RBAC
echo "5. Removing RBAC..."
kubectl delete -f notification-controller/argocd-notifications-rbac.yaml --ignore-not-found=true

# Clean up test namespaces
echo "6. Cleaning up test namespaces..."
kubectl delete namespace test-notifications test-notifications-fail test-notifications-prod --ignore-not-found=true

echo "✅ ArgoCD Notifications cleanup complete!" 