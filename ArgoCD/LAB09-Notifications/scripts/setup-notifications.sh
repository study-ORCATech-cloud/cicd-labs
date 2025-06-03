#!/bin/bash

set -e

echo "Setting up ArgoCD Notifications..."

# Apply RBAC
echo "1. Applying RBAC..."
kubectl apply -f notification-controller/argocd-notifications-rbac.yaml

# Deploy controller
echo "2. Deploying notifications controller..."
kubectl apply -f notification-controller/argocd-notifications-controller.yaml

# Apply secrets
echo "3. Applying secrets..."
kubectl apply -f secrets/slack-webhook-secret.yaml

# Apply notifications configuration
echo "4. Applying notifications configuration..."
kubectl apply -f notification-configs/master-notifications-config.yaml

# Wait for controller to be ready
echo "5. Waiting for controller to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/argocd-notifications-controller -n argocd

echo "✅ ArgoCD Notifications setup complete!"
echo "💡 Deploy test applications to verify notifications:"
echo "   kubectl apply -f test-scenarios/" 