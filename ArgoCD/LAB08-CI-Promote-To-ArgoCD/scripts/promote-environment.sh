#!/bin/bash

# Script to promote from staging to production
# Usage: ./promote-environment.sh

set -e

STAGING_PATH="gitops-repo/environments/staging"
PRODUCTION_PATH="gitops-repo/environments/production"

if [ ! -f "$STAGING_PATH/kustomization.yaml" ]; then
    echo "Error: Staging kustomization.yaml not found"
    exit 1
fi

# Get current staging image tag
STAGING_TAG=$(grep "newTag:" "$STAGING_PATH/kustomization.yaml" | awk '{print $2}')

if [ -z "$STAGING_TAG" ]; then
    echo "Error: Could not determine staging image tag"
    exit 1
fi

echo "Current staging tag: $STAGING_TAG"
read -p "Promote $STAGING_TAG to production? (y/N): " confirm

if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo "Promotion cancelled"
    exit 0
fi

# Use the update script to promote to production
./scripts/update-image-tag.sh production "$STAGING_TAG"

echo "✅ Successfully promoted $STAGING_TAG from staging to production"
echo "Don't forget to commit and push the changes!" 