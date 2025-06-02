#!/bin/bash

# Script to update image tags in GitOps repository
# Usage: ./update-image-tag.sh <environment> <new-tag>

set -e

ENVIRONMENT=$1
NEW_TAG=$2
DOCKER_USERNAME=${DOCKER_HUB_USERNAME:-"your-dockerhub-username"}

if [ -z "$ENVIRONMENT" ] || [ -z "$NEW_TAG" ]; then
    echo "Usage: $0 <environment> <new-tag>"
    echo "Example: $0 staging v20240101-abc1234"
    exit 1
fi

if [ "$ENVIRONMENT" != "staging" ] && [ "$ENVIRONMENT" != "production" ]; then
    echo "Error: Environment must be 'staging' or 'production'"
    exit 1
fi

ENV_PATH="gitops-repo/environments/$ENVIRONMENT"

if [ ! -d "$ENV_PATH" ]; then
    echo "Error: Environment directory $ENV_PATH not found"
    exit 1
fi

echo "Updating $ENVIRONMENT environment to use image tag: $NEW_TAG"

# Update deployment.yaml
sed -i "s|image: $DOCKER_USERNAME/cicd-demo:.*|image: $DOCKER_USERNAME/cicd-demo:$NEW_TAG|g" "$ENV_PATH/deployment.yaml"

# Update kustomization.yaml
sed -i "s|newTag: .*|newTag: $NEW_TAG|g" "$ENV_PATH/kustomization.yaml"

# Update version labels
sed -i "s|version: v.*|version: $NEW_TAG|g" "$ENV_PATH/deployment.yaml"

# Update APP_VERSION environment variable
sed -i "s|value: \"v.*\"|value: \"$NEW_TAG\"|g" "$ENV_PATH/deployment.yaml"

echo "✅ Successfully updated $ENVIRONMENT environment to $NEW_TAG"
echo "Files modified:"
echo "  - $ENV_PATH/deployment.yaml"
echo "  - $ENV_PATH/kustomization.yaml" 