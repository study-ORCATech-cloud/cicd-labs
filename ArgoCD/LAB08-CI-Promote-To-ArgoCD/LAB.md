# Lab Instructions for LAB08: CI/CD Integration with GitOps Promotion Workflows

This document provides detailed step-by-step instructions for building complete CI/CD pipelines that integrate with GitOps workflows. You'll learn how to automate application builds, testing, image creation, and promotion through environments using GitHub Actions and ArgoCD.

We will start by creating a repository structure and copying the sample application, then build CI/CD pipelines that automatically promote changes through staging to production.

---

## 🚀 Lab Steps

### Phase 1: Copy Lab Materials and Create Repository Structure

**1. Prepare Your GitHub Repository:**
   * Create a new public GitHub repository named `cicd-gitops-demo` (or reuse existing repository from previous labs)
   * Clone the repository locally:
      ```bash
      git clone https://github.com/YOUR_USERNAME/cicd-gitops-demo.git
      cd cicd-gitops-demo
      ```
   * Create the complete directory structure:
      ```bash
      mkdir -p app/tests
      mkdir -p .github/workflows
      mkdir -p gitops-repo/{environments/{staging,production},argocd-apps}
      mkdir -p scripts
      ```

**2. Copy Sample Python Flask Application:**
   * Copy the main application files from the lab materials:
      ```bash
      # Copy the Flask application
      cp ../path-to-cicd-labs/ArgoCD/LAB08-CI-Promote-To-ArgoCD/app/main.py ./app/main.py
      
      # Copy application dependencies
      cp ../path-to-cicd-labs/ArgoCD/LAB08-CI-Promote-To-ArgoCD/app/requirements.txt ./app/requirements.txt
      
      # Copy Dockerfile
      cp ../path-to-cicd-labs/ArgoCD/LAB08-CI-Promote-To-ArgoCD/app/Dockerfile ./app/Dockerfile
      ```
   * Examine the Flask application structure:
      ```bash
      # Review the main application
      cat app/main.py
      
      # Check the dependencies
      cat app/requirements.txt
      
      # Review the Dockerfile
      cat app/Dockerfile
      ```
   * Notice the application provides multiple endpoints: `/`, `/health`, and `/version`

**3. Copy Unit Tests:**
   * Copy the test files from the lab materials:
      ```bash
      # Copy test dependencies
      cp ../path-to-cicd-labs/ArgoCD/LAB08-CI-Promote-To-ArgoCD/app/tests/test_requirements.txt ./app/tests/test_requirements.txt
      
      # Copy unit tests
      cp ../path-to-cicd-labs/ArgoCD/LAB08-CI-Promote-To-ArgoCD/app/tests/test_app.py ./app/tests/test_app.py
      ```
   * Review the test structure:
      ```bash
      # Check test dependencies
      cat app/tests/test_requirements.txt
      
      # Review the unit tests
      cat app/tests/test_app.py
      ```
   * The tests cover all endpoints and environment variable handling

### Phase 2: Copy GitOps Repository Structure

**4. Copy Staging Environment Configuration:**
   * Copy staging deployment:
      ```bash
      cp gitops-repo/environments/staging/deployment.yaml ./
      ```
   
   * Review staging deployment:
      ```bash
      cat gitops-repo/environments/staging/deployment.yaml
      ```

   * Copy staging kustomization:
      ```bash
      cp gitops-repo/environments/staging/kustomization.yaml ./
      ```
   
   * Review staging kustomization:
      ```bash
      cat gitops-repo/environments/staging/kustomization.yaml
      ```

**5. Copy Production Environment Configuration:**
   * Copy production deployment:
      ```bash
      cp gitops-repo/environments/production/deployment.yaml ./
      ```
   
   * Review production deployment:
      ```bash
      cat gitops-repo/environments/production/deployment.yaml
      ```

   * Copy production kustomization:
      ```bash
      cp gitops-repo/environments/production/kustomization.yaml ./
      ```
   
   * Review production kustomization:
      ```bash
      cat gitops-repo/environments/production/kustomization.yaml
      ```

**6. Update Docker Hub Username:**
   * Replace `YOUR_DOCKERHUB_USERNAME` with your actual Docker Hub username:
      ```bash
      # Replace with your actual Docker Hub username
      DOCKERHUB_USERNAME="your-dockerhub-username"
      
      find gitops-repo/ -name "*.yaml" -exec sed -i "s/YOUR_DOCKERHUB_USERNAME/$DOCKERHUB_USERNAME/g" {} \;
      ```

### Phase 3: Copy ArgoCD Applications

**7. Copy ArgoCD Application for Staging:**
   ```bash
   cp gitops-repo/argocd-apps/staging-app.yaml ./
   ```

**8. Review Staging Application:**
   ```bash
   cat gitops-repo/argocd-apps/staging-app.yaml
   ```

**9. Copy ArgoCD Application for Production:**
   ```bash
   cp gitops-repo/argocd-apps/production-app.yaml ./
   ```

**10. Review Production Application:**
   ```bash
   cat gitops-repo/argocd-apps/production-app.yaml
   ```

**11. Update GitHub Username:**
   ```bash
   # Replace with your actual GitHub username
   GITHUB_USERNAME="your-github-username"
   
   sed -i "s/YOUR_GITHUB_USERNAME/$GITHUB_USERNAME/g" gitops-repo/argocd-apps/staging-app.yaml
   sed -i "s/YOUR_GITHUB_USERNAME/$GITHUB_USERNAME/g" gitops-repo/argocd-apps/production-app.yaml
   ```

### Phase 4: Copy CI/CD Workflows

**12. Copy CI Build and Test Workflow:**
   ```bash
   cp .github/workflows/ci-build-test.yml ./
   ```

**13. Review CI Build and Test Workflow:**
   ```bash
   cat .github/workflows/ci-build-test.yml
   ```

**14. Copy Staging Promotion Workflow:**
   ```bash
   cp .github/workflows/promote-to-staging.yml ./
   ```

**15. Review Staging Promotion Workflow:**
   ```bash
   cat .github/workflows/promote-to-staging.yml
   ```

**16. Copy Production Promotion Workflow:**
   ```bash
   cp .github/workflows/promote-to-production.yml ./
   ```

**17. Review Production Promotion Workflow:**
   ```bash
   cat .github/workflows/promote-to-production.yml
   ```

### Phase 5: Copy Helper Scripts

**18. Copy Helper Scripts from Lab Materials:**
   * Copy the image tag update script:
      ```bash
      # Copy the image tag update script
      cp ../path-to-cicd-labs/ArgoCD/LAB08-CI-Promote-To-ArgoCD/scripts/update-image-tag.sh ./scripts/update-image-tag.sh
      chmod +x scripts/update-image-tag.sh
      ```
   * Copy the environment promotion script:
      ```bash
      # Copy the environment promotion script
      cp ../path-to-cicd-labs/ArgoCD/LAB08-CI-Promote-To-ArgoCD/scripts/promote-environment.sh ./scripts/promote-environment.sh
      chmod +x scripts/promote-environment.sh
      ```
   * Review the helper scripts:
      ```bash
      # Review the update script
      cat scripts/update-image-tag.sh
      
      # Review the promotion script
      cat scripts/promote-environment.sh
      ```

**19. Test Local Application (Optional):**
   * Test the Flask application locally:
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
   * Run the unit tests:
      ```bash
      cd app
      pip install -r tests/test_requirements.txt
      python -m pytest tests/ -v
      cd ..
      ```

### Phase 6: Set Up GitHub Secrets and Deploy

**20. Commit Initial Code:**
   ```bash
   git add .
   git commit -m "Initial CI/CD GitOps demo setup"
   git push origin main
   ```

**21. Set Up GitHub Secrets:**
   * Go to your GitHub repository settings → Secrets and variables → Actions
   * Add the following repository secrets:
      - `DOCKER_HUB_USERNAME`: Your Docker Hub username
      - `DOCKER_HUB_TOKEN`: Your Docker Hub access token
   * To create a Docker Hub access token:
      - Go to Docker Hub → Account Settings → Security
      - Click "New Access Token"
      - Give it a descriptive name like "GitHub Actions"
      - Copy the token and add it as `DOCKER_HUB_TOKEN` secret

**22. Deploy ArgoCD Applications:**
   ```bash
   kubectl apply -f gitops-repo/argocd-apps/staging-app.yaml
   kubectl apply -f gitops-repo/argocd-apps/production-app.yaml
   ```

**23. Verify ArgoCD Applications:**
   * Open ArgoCD UI
   * You should see two applications: `cicd-demo-staging` and `cicd-demo-production`
   * The staging application should auto-sync
   * The production application should be manual sync

### Phase 7: Test Complete CI/CD Pipeline

**24. Trigger Initial CI/CD Pipeline:**
   * Make a small change to the application:
      ```bash
      sed -i 's/Hello from CI\/CD GitOps Demo!/Hello from Automated CI\/CD Pipeline!/' app/main.py
      git add app/main.py
      git commit -m "Update welcome message"
      git push origin main
      ```
   * This will trigger the CI build workflow
   * Watch the workflow in GitHub Actions tab

**25. Monitor Staging Deployment:**
   * After CI completes, the staging promotion workflow should run
   * Check ArgoCD UI for staging application sync
   * Test the staging application:
      ```bash
      minikube ip  # Get Minikube IP
      curl http://<MINIKUBE_IP>:30100/
      ```

**26. Promote to Production:**
   * In GitHub, go to Actions tab
   * Run the "Promote to Production" workflow manually
   * Enter the version tag from staging (check staging kustomization.yaml)
   * Type "promote" to confirm
   * Run the workflow

**27. Manually Sync Production:**
   * In ArgoCD UI, the production application should show "OutOfSync"
   * Review the changes
   * Manually click "SYNC" to deploy to production
   * Test the production application:
      ```bash
      curl http://<MINIKUBE_IP>:30200/
      ```

### Phase 8: Advanced Testing and Validation

**28. Test Rollback Scenario:**
   * Make a breaking change to the application:
      ```bash
      echo "import invalid_module" >> app/main.py
      git add app/main.py
      git commit -m "Introduce breaking change"
      git push origin main
      ```
   * The CI pipeline should fail at the test stage
   * Verify that staging is not updated with the broken version

**29. Test Manual Promotion Override:**
   * Fix the breaking change:
      ```bash
      git revert HEAD
      git push origin main
      ```
   * Wait for CI to complete and staging to be updated
   * Use the promotion script locally:
      ```bash
      ./scripts/promote-environment.sh
      ```
   * Commit and push the changes

**30. Monitor and Validate Complete Pipeline:**
   * Check application versions across environments:
      ```bash
      echo "=== Staging Version ==="
      curl http://<MINIKUBE_IP>:30100/version
      echo ""
      echo "=== Production Version ==="
      curl http://<MINIKUBE_IP>:30200/version
      ```
   * Verify Docker Hub contains the built images
   * Confirm ArgoCD shows correct sync status for both applications

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

**31. Delete ArgoCD Applications:**
   * In the ArgoCD UI, delete both applications:
      - Click on `cicd-demo-staging` → DELETE → Check "Delete resources" → Confirm
      - Click on `cicd-demo-production` → DELETE → Check "Delete resources" → Confirm
   * Alternatively, use kubectl:
      ```bash
      kubectl delete application cicd-demo-staging -n argocd
      kubectl delete application cicd-demo-production -n argocd
      ```

**32. Delete Namespaces:**
   ```bash
   kubectl delete namespace cicd-staging
   kubectl delete namespace cicd-production
   ```

**33. Disable GitHub Actions Workflows:**
   * In GitHub repository, go to Actions tab
   * Click on each workflow and disable them to prevent accidental runs
   * Or delete the workflow files:
      ```bash
      git rm .github/workflows/*.yml
      git commit -m "Remove CI/CD workflows"
      git push origin main
      ```

**34. Clean Up Docker Images (Optional):**
   * Remove local Docker images:
      ```bash
      docker rmi $(docker images "*/cicd-demo" -q) 2>/dev/null || true
      ```
   * Remove images from Docker Hub (manual process via Docker Hub UI)

**35. Clean Up Git Repository (Optional):**
   ```bash
   git rm -r app/ gitops-repo/ scripts/ .github/
   git commit -m "Clean up CI/CD demo"
   git push origin main
   ```

**36. Stop Minikube (If Done):**
   ```bash
   minikube stop
   ```

---

## 🎯 Key Learning Outcomes

By completing this lab, you have learned:

1. **CI/CD Integration Architecture**: Understanding how CI systems integrate with GitOps workflows
2. **Automated Promotion Pipelines**: Building workflows that automatically promote through environments
3. **GitHub Actions Workflows**: Creating sophisticated CI/CD pipelines with multiple triggers and conditions
4. **GitOps Repository Management**: Structuring repositories for multi-environment deployments
5. **Container Registry Integration**: Automated image building, tagging, and security scanning
6. **Production Deployment Controls**: Implementing manual approval gates and validation steps
7. **Rollback and Recovery**: Handling failed deployments and implementing rollback strategies

This comprehensive CI/CD integration demonstrates enterprise-grade automation while maintaining proper controls and quality gates for production deployments.

---

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Build and Push Action](https://github.com/docker/build-push-action)
- [ArgoCD GitOps Best Practices](https://argo-cd.readthedocs.io/en/stable/user-guide/best_practices/)
- [Kustomize Documentation](https://kustomize.io/)
- [Container Security Scanning](https://docs.docker.com/scout/) 