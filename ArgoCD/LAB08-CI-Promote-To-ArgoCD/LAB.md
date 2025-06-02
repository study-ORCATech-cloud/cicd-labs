# Lab Instructions for LAB08: CI/CD Integration with GitOps Promotion Workflows

This document provides detailed step-by-step instructions for building complete CI/CD pipelines that integrate with GitOps workflows. You'll learn how to automate application builds, testing, image creation, and promotion through environments using GitHub Actions and ArgoCD.

We will start by creating a repository structure and copying the sample application, then build CI/CD pipelines that automatically promote changes through staging to production.

---

## 🚀 Lab Steps

### Phase 1: Create Repository Structure and Copy Sample Application

**1. Prepare Your GitHub Repository:**
   a. Create a new public GitHub repository named `cicd-gitops-demo` (or reuse existing repository from previous labs)
   b. Clone the repository locally:
      ```bash
      git clone https://github.com/YOUR_USERNAME/cicd-gitops-demo.git
      cd cicd-gitops-demo
      ```
   c. Create the complete directory structure:
      ```bash
      mkdir -p app/tests
      mkdir -p .github/workflows
      mkdir -p gitops-repo/{environments/{staging,production},argocd-apps}
      mkdir -p scripts
      ```

**2. Copy Sample Python Flask Application:**
   a. Copy the main application files from the lab materials:
      ```bash
      # Copy the Flask application
      cp ../path-to-cicd-labs/ArgoCD/LAB08-CI-Promote-To-ArgoCD/app/main.py ./app/main.py
      
      # Copy application dependencies
      cp ../path-to-cicd-labs/ArgoCD/LAB08-CI-Promote-To-ArgoCD/app/requirements.txt ./app/requirements.txt
      
      # Copy Dockerfile
      cp ../path-to-cicd-labs/ArgoCD/LAB08-CI-Promote-To-ArgoCD/app/Dockerfile ./app/Dockerfile
      ```
   b. Examine the Flask application structure:
      ```bash
      # Review the main application
      cat app/main.py
      
      # Check the dependencies
      cat app/requirements.txt
      
      # Review the Dockerfile
      cat app/Dockerfile
      ```
   c. Notice the application provides multiple endpoints: `/`, `/health`, and `/version`

**3. Copy Unit Tests:**
   a. Copy the test files from the lab materials:
      ```bash
      # Copy test dependencies
      cp ../path-to-cicd-labs/ArgoCD/LAB08-CI-Promote-To-ArgoCD/app/tests/test_requirements.txt ./app/tests/test_requirements.txt
      
      # Copy unit tests
      cp ../path-to-cicd-labs/ArgoCD/LAB08-CI-Promote-To-ArgoCD/app/tests/test_app.py ./app/tests/test_app.py
      ```
   b. Review the test structure:
      ```bash
      # Check test dependencies
      cat app/tests/test_requirements.txt
      
      # Review the unit tests
      cat app/tests/test_app.py
      ```
   c. The tests cover all endpoints and environment variable handling

### Phase 2: Create GitOps Repository Structure

**4. Create Staging Environment Configuration:**
   a. Create staging deployment:
      ```bash
      cat > gitops-repo/environments/staging/deployment.yaml << 'EOF'
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: cicd-demo-app
        namespace: cicd-staging
        labels:
          app: cicd-demo
          environment: staging
          version: v1.0.0
      spec:
        replicas: 2
        selector:
          matchLabels:
            app: cicd-demo
            environment: staging
        template:
          metadata:
            labels:
              app: cicd-demo
              environment: staging
              version: v1.0.0
          spec:
            containers:
            - name: app
              image: YOUR_DOCKERHUB_USERNAME/cicd-demo:v1.0.0
              ports:
              - containerPort: 5000
              env:
              - name: APP_VERSION
                value: "v1.0.0"
              - name: ENVIRONMENT
                value: "staging"
              - name: BUILD_DATE
                value: "2024-01-01T00:00:00Z"
              - name: GIT_COMMIT
                value: "unknown"
              resources:
                requests:
                  memory: "128Mi"
                  cpu: "100m"
                limits:
                  memory: "256Mi"
                  cpu: "200m"
              livenessProbe:
                httpGet:
                  path: /health
                  port: 5000
                initialDelaySeconds: 30
                periodSeconds: 10
              readinessProbe:
                httpGet:
                  path: /health
                  port: 5000
                initialDelaySeconds: 10
                periodSeconds: 5
      ---
      apiVersion: v1
      kind: Service
      metadata:
        name: cicd-demo-service
        namespace: cicd-staging
        labels:
          app: cicd-demo
          environment: staging
      spec:
        type: NodePort
        selector:
          app: cicd-demo
          environment: staging
        ports:
        - port: 5000
          targetPort: 5000
          nodePort: 30100
          protocol: TCP
          name: http
      EOF
      ```

   b. Create staging kustomization:
      ```bash
      cat > gitops-repo/environments/staging/kustomization.yaml << 'EOF'
      apiVersion: kustomize.config.k8s.io/v1beta1
      kind: Kustomization
      
      resources:
      - deployment.yaml
      
      namespace: cicd-staging
      
      commonLabels:
        app: cicd-demo
        environment: staging
        managed-by: argocd
      
      images:
      - name: YOUR_DOCKERHUB_USERNAME/cicd-demo
        newTag: v1.0.0
      EOF
      ```

**5. Create Production Environment Configuration:**
   a. Create production deployment:
      ```bash
      cat > gitops-repo/environments/production/deployment.yaml << 'EOF'
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: cicd-demo-app
        namespace: cicd-production
        labels:
          app: cicd-demo
          environment: production
          version: v1.0.0
      spec:
        replicas: 3
        selector:
          matchLabels:
            app: cicd-demo
            environment: production
        template:
          metadata:
            labels:
              app: cicd-demo
              environment: production
              version: v1.0.0
          spec:
            containers:
            - name: app
              image: YOUR_DOCKERHUB_USERNAME/cicd-demo:v1.0.0
              ports:
              - containerPort: 5000
              env:
              - name: APP_VERSION
                value: "v1.0.0"
              - name: ENVIRONMENT
                value: "production"
              - name: BUILD_DATE
                value: "2024-01-01T00:00:00Z"
              - name: GIT_COMMIT
                value: "unknown"
              resources:
                requests:
                  memory: "256Mi"
                  cpu: "200m"
                limits:
                  memory: "512Mi"
                  cpu: "500m"
              livenessProbe:
                httpGet:
                  path: /health
                  port: 5000
                initialDelaySeconds: 30
                periodSeconds: 10
              readinessProbe:
                httpGet:
                  path: /health
                  port: 5000
                initialDelaySeconds: 10
                periodSeconds: 5
      ---
      apiVersion: v1
      kind: Service
      metadata:
        name: cicd-demo-service
        namespace: cicd-production
        labels:
          app: cicd-demo
          environment: production
      spec:
        type: NodePort
        selector:
          app: cicd-demo
          environment: production
        ports:
        - port: 5000
          targetPort: 5000
          nodePort: 30200
          protocol: TCP
          name: http
      EOF
      ```

   b. Create production kustomization:
      ```bash
      cat > gitops-repo/environments/production/kustomization.yaml << 'EOF'
      apiVersion: kustomize.config.k8s.io/v1beta1
      kind: Kustomization
      
      resources:
      - deployment.yaml
      
      namespace: cicd-production
      
      commonLabels:
        app: cicd-demo
        environment: production
        managed-by: argocd
      
      images:
      - name: YOUR_DOCKERHUB_USERNAME/cicd-demo
        newTag: v1.0.0
      EOF
      ```

**6. Update Docker Hub Username:**
   a. Replace `YOUR_DOCKERHUB_USERNAME` with your actual Docker Hub username:
      ```bash
      # Replace with your actual Docker Hub username
      DOCKERHUB_USERNAME="your-dockerhub-username"
      
      find gitops-repo/ -name "*.yaml" -exec sed -i "s/YOUR_DOCKERHUB_USERNAME/$DOCKERHUB_USERNAME/g" {} \;
      ```

### Phase 3: Create ArgoCD Applications

**7. Create ArgoCD Application for Staging:**
   ```bash
   cat > gitops-repo/argocd-apps/staging-app.yaml << 'EOF'
   apiVersion: argoproj.io/v1alpha1
   kind: Application
   metadata:
     name: cicd-demo-staging
     namespace: argocd
     labels:
       environment: staging
   spec:
     project: default
     source:
       repoURL: https://github.com/YOUR_GITHUB_USERNAME/cicd-gitops-demo.git
       targetRevision: HEAD
       path: gitops-repo/environments/staging
     destination:
       server: https://kubernetes.default.svc
       namespace: cicd-staging
     syncPolicy:
       automated:
         prune: true
         selfHeal: true
       syncOptions:
       - CreateNamespace=true
       retry:
         limit: 5
         backoff:
           duration: 5s
           factor: 2
           maxDuration: 3m
   EOF
   ```

**8. Create ArgoCD Application for Production:**
   ```bash
   cat > gitops-repo/argocd-apps/production-app.yaml << 'EOF'
   apiVersion: argoproj.io/v1alpha1
   kind: Application
   metadata:
     name: cicd-demo-production
     namespace: argocd
     labels:
       environment: production
   spec:
     project: default
     source:
       repoURL: https://github.com/YOUR_GITHUB_USERNAME/cicd-gitops-demo.git
       targetRevision: HEAD
       path: gitops-repo/environments/production
     destination:
       server: https://kubernetes.default.svc
       namespace: cicd-production
     syncPolicy:
       manual: {}
       syncOptions:
       - CreateNamespace=true
       retry:
         limit: 3
         backoff:
           duration: 10s
           factor: 2
           maxDuration: 5m
   EOF
   ```

**9. Update GitHub Username:**
   ```bash
   # Replace with your actual GitHub username
   GITHUB_USERNAME="your-github-username"
   
   sed -i "s/YOUR_GITHUB_USERNAME/$GITHUB_USERNAME/g" gitops-repo/argocd-apps/staging-app.yaml
   sed -i "s/YOUR_GITHUB_USERNAME/$GITHUB_USERNAME/g" gitops-repo/argocd-apps/production-app.yaml
   ```

### Phase 4: Create CI/CD Workflows

**10. Create CI Build and Test Workflow:**
   ```bash
   cat > .github/workflows/ci-build-test.yml << 'EOF'
   name: CI - Build and Test
   
   on:
     push:
       branches: [ main, develop ]
       paths: [ 'app/**' ]
     pull_request:
       branches: [ main ]
       paths: [ 'app/**' ]
   
   env:
     DOCKER_HUB_USERNAME: ${{ secrets.DOCKER_HUB_USERNAME }}
     DOCKER_HUB_TOKEN: ${{ secrets.DOCKER_HUB_TOKEN }}
     IMAGE_NAME: ${{ secrets.DOCKER_HUB_USERNAME }}/cicd-demo
   
   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
       - name: Checkout code
         uses: actions/checkout@v4
   
       - name: Set up Python
         uses: actions/setup-python@v4
         with:
           python-version: '3.9'
   
       - name: Install dependencies
         run: |
           cd app
           pip install -r requirements.txt
           pip install -r tests/test_requirements.txt
   
       - name: Run unit tests
         run: |
           cd app
           python -m pytest tests/ -v --tb=short
   
       - name: Test application startup
         run: |
           cd app
           python main.py &
           sleep 5
           curl -f http://localhost:5000/health
           pkill -f python
   
     build:
       needs: test
       runs-on: ubuntu-latest
       if: github.ref == 'refs/heads/main'
       outputs:
         version: ${{ steps.version.outputs.version }}
         image-tag: ${{ steps.version.outputs.version }}
       steps:
       - name: Checkout code
         uses: actions/checkout@v4
   
       - name: Generate version
         id: version
         run: |
           # Generate version based on timestamp and short commit hash
           VERSION="v$(date +'%Y%m%d')-${GITHUB_SHA::7}"
           echo "version=$VERSION" >> $GITHUB_OUTPUT
           echo "Generated version: $VERSION"
   
       - name: Set up Docker Buildx
         uses: docker/setup-buildx-action@v3
   
       - name: Login to Docker Hub
         uses: docker/login-action@v3
         with:
           username: ${{ env.DOCKER_HUB_USERNAME }}
           password: ${{ env.DOCKER_HUB_TOKEN }}
   
       - name: Build and push Docker image
         uses: docker/build-push-action@v5
         with:
           context: ./app
           file: ./app/Dockerfile
           push: true
           tags: |
             ${{ env.IMAGE_NAME }}:${{ steps.version.outputs.version }}
             ${{ env.IMAGE_NAME }}:latest
           build-args: |
             BUILD_DATE=${{ github.event.head_commit.timestamp }}
             GIT_COMMIT=${{ github.sha }}
           cache-from: type=gha
           cache-to: type=gha,mode=max
   
       - name: Run security scan
         uses: docker/scout-action@v1
         with:
           command: cves
           image: ${{ env.IMAGE_NAME }}:${{ steps.version.outputs.version }}
           only-severities: critical,high
         continue-on-error: true
   EOF
   ```

**11. Create Staging Promotion Workflow:**
   ```bash
   cat > .github/workflows/promote-to-staging.yml << 'EOF'
   name: Promote to Staging
   
   on:
     workflow_run:
       workflows: ["CI - Build and Test"]
       types:
         - completed
   
   env:
     DOCKER_HUB_USERNAME: ${{ secrets.DOCKER_HUB_USERNAME }}
   
   jobs:
     promote-staging:
       runs-on: ubuntu-latest
       if: ${{ github.event.workflow_run.conclusion == 'success' && github.event.workflow_run.head_branch == 'main' }}
       steps:
       - name: Checkout code
         uses: actions/checkout@v4
         with:
           token: ${{ secrets.GITHUB_TOKEN }}
   
       - name: Get latest image tag
         id: get-tag
         run: |
           # Get the latest tag from Docker Hub
           LATEST_TAG=$(curl -s "https://registry.hub.docker.com/v2/repositories/${{ env.DOCKER_HUB_USERNAME }}/cicd-demo/tags/" | jq -r '.results[0].name')
           echo "latest-tag=$LATEST_TAG" >> $GITHUB_OUTPUT
           echo "Latest tag: $LATEST_TAG"
   
       - name: Update staging deployment
         run: |
           # Update the image tag in staging deployment
           sed -i "s|image: ${{ env.DOCKER_HUB_USERNAME }}/cicd-demo:.*|image: ${{ env.DOCKER_HUB_USERNAME }}/cicd-demo:${{ steps.get-tag.outputs.latest-tag }}|g" gitops-repo/environments/staging/deployment.yaml
           
           # Update kustomization
           sed -i "s|newTag: .*|newTag: ${{ steps.get-tag.outputs.latest-tag }}|g" gitops-repo/environments/staging/kustomization.yaml
           
           # Update version in deployment metadata
           sed -i "s|version: v.*|version: ${{ steps.get-tag.outputs.latest-tag }}|g" gitops-repo/environments/staging/deployment.yaml
           
           # Update APP_VERSION environment variable
           sed -i "s|value: \"v.*\"|value: \"${{ steps.get-tag.outputs.latest-tag }}\"|g" gitops-repo/environments/staging/deployment.yaml
   
       - name: Commit and push changes
         run: |
           git config --local user.email "action@github.com"
           git config --local user.name "GitHub Action"
           git add gitops-repo/environments/staging/
           git commit -m "🚀 Promote ${{ steps.get-tag.outputs.latest-tag }} to staging" || exit 0
           git push
   
       - name: Create staging deployment comment
         run: |
           echo "## 🚀 Staging Deployment" >> $GITHUB_STEP_SUMMARY
           echo "Successfully promoted **${{ steps.get-tag.outputs.latest-tag }}** to staging environment." >> $GITHUB_STEP_SUMMARY
           echo "- **Image:** \`${{ env.DOCKER_HUB_USERNAME }}/cicd-demo:${{ steps.get-tag.outputs.latest-tag }}\`" >> $GITHUB_STEP_SUMMARY
           echo "- **Environment:** staging" >> $GITHUB_STEP_SUMMARY
           echo "- **ArgoCD Application:** cicd-demo-staging" >> $GITHUB_STEP_SUMMARY
   EOF
   ```

**12. Create Production Promotion Workflow:**
   ```bash
   cat > .github/workflows/promote-to-production.yml << 'EOF'
   name: Promote to Production
   
   on:
     workflow_dispatch:
       inputs:
         version:
           description: 'Version to promote to production'
           required: true
           type: string
         confirm:
           description: 'Type "promote" to confirm production deployment'
           required: true
           type: string
   
   env:
     DOCKER_HUB_USERNAME: ${{ secrets.DOCKER_HUB_USERNAME }}
   
   jobs:
     validate-input:
       runs-on: ubuntu-latest
       steps:
       - name: Validate confirmation
         if: ${{ github.event.inputs.confirm != 'promote' }}
         run: |
           echo "❌ Production promotion cancelled. Please type 'promote' to confirm."
           exit 1
   
     promote-production:
       needs: validate-input
       runs-on: ubuntu-latest
       environment: production
       steps:
       - name: Checkout code
         uses: actions/checkout@v4
         with:
           token: ${{ secrets.GITHUB_TOKEN }}
   
       - name: Verify image exists
         run: |
           # Check if the specified version exists in Docker Hub
           VERSION="${{ github.event.inputs.version }}"
           curl -f "https://registry.hub.docker.com/v2/repositories/${{ env.DOCKER_HUB_USERNAME }}/cicd-demo/tags/$VERSION/" || {
             echo "❌ Image tag $VERSION not found in Docker Hub"
             exit 1
           }
           echo "✅ Image tag $VERSION verified in Docker Hub"
   
       - name: Update production deployment
         run: |
           VERSION="${{ github.event.inputs.version }}"
           
           # Update the image tag in production deployment
           sed -i "s|image: ${{ env.DOCKER_HUB_USERNAME }}/cicd-demo:.*|image: ${{ env.DOCKER_HUB_USERNAME }}/cicd-demo:$VERSION|g" gitops-repo/environments/production/deployment.yaml
           
           # Update kustomization
           sed -i "s|newTag: .*|newTag: $VERSION|g" gitops-repo/environments/production/kustomization.yaml
           
           # Update version in deployment metadata
           sed -i "s|version: v.*|version: $VERSION|g" gitops-repo/environments/production/deployment.yaml
           
           # Update APP_VERSION environment variable
           sed -i "s|value: \"v.*\"|value: \"$VERSION\"|g" gitops-repo/environments/production/deployment.yaml
   
       - name: Commit and push changes
         run: |
           VERSION="${{ github.event.inputs.version }}"
           git config --local user.email "action@github.com"
           git config --local user.name "GitHub Action"
           git add gitops-repo/environments/production/
           git commit -m "🚀 Promote $VERSION to production" || exit 0
           git push
   
       - name: Create production deployment summary
         run: |
           VERSION="${{ github.event.inputs.version }}"
           echo "## 🚀 Production Deployment" >> $GITHUB_STEP_SUMMARY
           echo "Successfully promoted **$VERSION** to production environment." >> $GITHUB_STEP_SUMMARY
           echo "- **Image:** \`${{ env.DOCKER_HUB_USERNAME }}/cicd-demo:$VERSION\`" >> $GITHUB_STEP_SUMMARY
           echo "- **Environment:** production" >> $GITHUB_STEP_SUMMARY
           echo "- **ArgoCD Application:** cicd-demo-production" >> $GITHUB_STEP_SUMMARY
           echo "- **Promoted by:** ${{ github.actor }}" >> $GITHUB_STEP_SUMMARY
           echo "" >> $GITHUB_STEP_SUMMARY
           echo "⚠️ **Remember to manually sync the ArgoCD application for production deployment.**" >> $GITHUB_STEP_SUMMARY
   EOF
   ```

### Phase 5: Copy Helper Scripts

**13. Copy Helper Scripts from Lab Materials:**
   a. Copy the image tag update script:
      ```bash
      # Copy the image tag update script
      cp ../path-to-cicd-labs/ArgoCD/LAB08-CI-Promote-To-ArgoCD/scripts/update-image-tag.sh ./scripts/update-image-tag.sh
      chmod +x scripts/update-image-tag.sh
      ```
   b. Copy the environment promotion script:
      ```bash
      # Copy the environment promotion script
      cp ../path-to-cicd-labs/ArgoCD/LAB08-CI-Promote-To-ArgoCD/scripts/promote-environment.sh ./scripts/promote-environment.sh
      chmod +x scripts/promote-environment.sh
      ```
   c. Review the helper scripts:
      ```bash
      # Review the update script
      cat scripts/update-image-tag.sh
      
      # Review the promotion script
      cat scripts/promote-environment.sh
      ```

**14. Test Local Application (Optional):**
   a. Test the Flask application locally:
      ```bash
      cd app
      pip install -r requirements.txt
      python main.py &
      sleep 2
      curl http://localhost:5000/
      curl http://localhost:5000/health
      curl http://localhost:5000/version
      pkill -f python
      cd ..
      ```
   b. Run the unit tests:
      ```bash
      cd app
      pip install -r tests/test_requirements.txt
      python -m pytest tests/ -v
      cd ..
      ```

### Phase 6: Set Up GitHub Secrets and Deploy

**15. Commit Initial Code:**
   ```bash
   git add .
   git commit -m "Initial CI/CD GitOps demo setup"
   git push origin main
   ```

**16. Set Up GitHub Secrets:**
   a. Go to your GitHub repository settings → Secrets and variables → Actions
   b. Add the following repository secrets:
      - `DOCKER_HUB_USERNAME`: Your Docker Hub username
      - `DOCKER_HUB_TOKEN`: Your Docker Hub access token
   c. To create a Docker Hub access token:
      - Go to Docker Hub → Account Settings → Security
      - Click "New Access Token"
      - Give it a descriptive name like "GitHub Actions"
      - Copy the token and add it as `DOCKER_HUB_TOKEN` secret

**17. Deploy ArgoCD Applications:**
   ```bash
   kubectl apply -f gitops-repo/argocd-apps/staging-app.yaml
   kubectl apply -f gitops-repo/argocd-apps/production-app.yaml
   ```

**18. Verify ArgoCD Applications:**
   a. Open ArgoCD UI
   b. You should see two applications: `cicd-demo-staging` and `cicd-demo-production`
   c. The staging application should auto-sync
   d. The production application should be manual sync

### Phase 7: Test Complete CI/CD Pipeline

**19. Trigger Initial CI/CD Pipeline:**
   a. Make a small change to the application:
      ```bash
      sed -i 's/Hello from CI\/CD GitOps Demo!/Hello from Automated CI\/CD Pipeline!/' app/main.py
      git add app/main.py
      git commit -m "Update welcome message"
      git push origin main
      ```
   b. This will trigger the CI build workflow
   c. Watch the workflow in GitHub Actions tab

**20. Monitor Staging Deployment:**
   a. After CI completes, the staging promotion workflow should run
   b. Check ArgoCD UI for staging application sync
   c. Test the staging application:
      ```bash
      minikube ip  # Get Minikube IP
      curl http://<MINIKUBE_IP>:30100/
      ```

**21. Promote to Production:**
   a. In GitHub, go to Actions tab
   b. Run the "Promote to Production" workflow manually
   c. Enter the version tag from staging (check staging kustomization.yaml)
   d. Type "promote" to confirm
   e. Run the workflow

**22. Manually Sync Production:**
   a. In ArgoCD UI, the production application should show "OutOfSync"
   b. Review the changes
   c. Manually click "SYNC" to deploy to production
   d. Test the production application:
      ```bash
      curl http://<MINIKUBE_IP>:30200/
      ```

### Phase 8: Advanced Testing and Validation

**23. Test Rollback Scenario:**
   a. Make a breaking change to the application:
      ```bash
      echo "import invalid_module" >> app/main.py
      git add app/main.py
      git commit -m "Introduce breaking change"
      git push origin main
      ```
   b. The CI pipeline should fail at the test stage
   c. Verify that staging is not updated with the broken version

**24. Test Manual Promotion Override:**
   a. Fix the breaking change:
      ```bash
      git revert HEAD
      git push origin main
      ```
   b. Wait for CI to complete and staging to be updated
   c. Use the promotion script locally:
      ```bash
      ./scripts/promote-environment.sh
      ```
   d. Commit and push the changes

**25. Monitor and Validate Complete Pipeline:**
   a. Check application versions across environments:
      ```bash
      echo "=== Staging Version ==="
      curl http://<MINIKUBE_IP>:30100/version
      echo ""
      echo "=== Production Version ==="
      curl http://<MINIKUBE_IP>:30200/version
      ```
   b. Verify Docker Hub contains the built images
   c. Confirm ArgoCD shows correct sync status for both applications

---

## ✅ Validation Checklist

- [ ] Successfully copied and reviewed Python Flask application with unit tests
- [ ] Created complete GitOps repository structure with staging and production environments
- [ ] Created ArgoCD applications for both environments with appropriate sync policies
- [ ] Successfully configured GitHub Actions workflows for CI, staging promotion, and production promotion
- [ ] Set up GitHub repository secrets for Docker Hub integration
- [ ] Successfully triggered automated CI/CD pipeline with code changes
- [ ] Verified automated staging deployment after successful CI build
- [ ] Successfully promoted application to production using manual workflow
- [ ] Tested rollback capabilities when CI pipeline fails
- [ ] Validated that production requires manual approval for deployments
- [ ] Confirmed image versioning and tagging works correctly
- [ ] Verified security scanning integration in CI pipeline
- [ ] Tested manual promotion scripts and helper utilities
- [ ] Validated complete end-to-end pipeline from code commit to production deployment

---

## 🧹 Cleanup

**1. Delete ArgoCD Applications:**
   a. In the ArgoCD UI, delete both applications:
      - Click on `cicd-demo-staging` → DELETE → Check "Delete resources" → Confirm
      - Click on `cicd-demo-production` → DELETE → Check "Delete resources" → Confirm
   b. Alternatively, use kubectl:
      ```bash
      kubectl delete application cicd-demo-staging -n argocd
      kubectl delete application cicd-demo-production -n argocd
      ```

**2. Delete Namespaces:**
   ```bash
   kubectl delete namespace cicd-staging
   kubectl delete namespace cicd-production
   ```

**3. Disable GitHub Actions Workflows:**
   a. In GitHub repository, go to Actions tab
   b. Click on each workflow and disable them to prevent accidental runs
   c. Or delete the workflow files:
      ```bash
      git rm .github/workflows/*.yml
      git commit -m "Remove CI/CD workflows"
      git push origin main
      ```

**4. Clean Up Docker Images (Optional):**
   a. Remove local Docker images:
      ```bash
      docker rmi $(docker images "*/cicd-demo" -q) 2>/dev/null || true
      ```
   b. Remove images from Docker Hub (manual process via Docker Hub UI)

**5. Clean Up Git Repository (Optional):**
   ```bash
   git rm -r app/ gitops-repo/ scripts/ .github/
   git commit -m "Clean up CI/CD demo"
   git push origin main
   ```

**6. Stop Minikube (If Done):**
   ```bash
   minikube stop
   ```

---

## 🎓 Key Learnings Summary

### **CI/CD Integration Architecture:**
- ✅ **Separation of Concerns**: CI handles build/test, ArgoCD handles deployment
- ✅ **Automated Promotion**: Staging deployments automated, production requires approval
- ✅ **Image Versioning**: Systematic tagging based on timestamps and commit hashes
- ✅ **Quality Gates**: Unit tests, security scanning, and manual approvals prevent bad deployments
- ❌ **Complexity**: Multiple moving parts require careful coordination
- ❌ **Secret Management**: Multiple systems require synchronized secret management

### **GitHub Actions Workflows:**
- **CI Build & Test**: Runs on every push, builds images, runs tests
- **Staging Promotion**: Automatically triggered after successful CI builds
- **Production Promotion**: Manual trigger with confirmation required
- **Security Integration**: Container scanning and vulnerability assessment
- **Rollback Capability**: Failed builds prevent automatic promotion

### **GitOps Repository Management:**
- ✅ **Environment Separation**: Clear folder structure for different environments
- ✅ **Kustomize Integration**: Environment-specific configurations without duplication
- ✅ **Version Tracking**: All changes tracked in Git with full audit trail
- ✅ **Automated Updates**: CI pipelines update GitOps repo programmatically
- ❌ **Repository Size**: Git history grows with automated commits
- ❌ **Merge Conflicts**: Potential conflicts with multiple automated updates

### **Production Best Practices:**
1. **Automated Testing**: Comprehensive unit tests prevent broken deployments
2. **Security Scanning**: Container vulnerability scanning in CI pipeline
3. **Manual Approval**: Production deployments require human confirmation
4. **Environment Parity**: Staging mirrors production configuration
5. **Rollback Strategy**: Git-based rollbacks and failed deployment handling
6. **Monitoring Integration**: Health checks and application monitoring
7. **Secret Management**: Secure handling of credentials and API keys

### **Advanced Concepts Demonstrated:**
- **Container Registry Integration**: Docker Hub with automated image builds
- **Multi-Environment Workflows**: Different promotion strategies per environment
- **Infrastructure as Code**: All configurations versioned in Git
- **Observability**: Application health checks and version endpoints
- **Compliance**: Audit trails and approval workflows for production changes

---

## 🏗️ Architecture Patterns Deep Dive

### **CI/CD Pipeline Stages:**

1. **Source Control Trigger**: Git push triggers CI pipeline
2. **Build & Test**: Compile, test, and validate application code
3. **Image Build**: Create container image with proper versioning
4. **Security Scan**: Vulnerability assessment of container images
5. **Staging Deployment**: Automated deployment to staging environment
6. **Manual Testing**: Human validation in staging environment
7. **Production Promotion**: Manual trigger for production deployment
8. **Production Deployment**: ArgoCD applies changes to production

### **GitOps Integration Points:**

- **CI System**: Builds and tests application, creates artifacts
- **Container Registry**: Stores versioned container images
- **GitOps Repository**: Contains deployment configurations
- **ArgoCD**: Monitors GitOps repo and applies changes to cluster
- **Kubernetes**: Runs the actual application workloads

### **Scaling Considerations:**
For larger organizations, consider:
1. **Multiple Clusters**: Separate clusters for staging and production
2. **Advanced Workflows**: Canary deployments, blue-green strategies
3. **Enterprise Tools**: Argo Workflows, Tekton, or enterprise CI/CD platforms
4. **Policy as Code**: OPA Gatekeeper for deployment policies
5. **Multi-Tenancy**: Namespace isolation and RBAC for team separation

---

End of Lab Instructions. Return to the main `README.md` for Key Concepts and Next Steps. 