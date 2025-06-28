#!/bin/bash

set -e

echo "Testing ArgoCD Notifications..."

# Deploy test applications
echo "1. Deploying test applications..."
kubectl apply -f test-scenarios/test-app-healthy.yaml
kubectl apply -f test-scenarios/test-app-production.yaml

# Wait a moment for applications to be created
sleep 10

# Check application status
echo "2. Checking application status..."
kubectl get applications -n argocd | grep test-notifications

# Trigger sync for production app (should send notification)
echo "3. Triggering sync for production app..."
kubectl patch app test-notifications-production -n argocd --type merge -p '{"operation":{"sync":{}}}'

# Deploy failing app to test failure notifications
echo "4. Deploying failing app to test failure notifications..."
kubectl apply -f test-scenarios/test-app-sync-failed.yaml

echo "✅ Test applications deployed!"
echo "💡 Check your email inbox for notifications"
echo "💡 Monitor with: kubectl logs -n argocd deployment/argocd-notifications-controller" 