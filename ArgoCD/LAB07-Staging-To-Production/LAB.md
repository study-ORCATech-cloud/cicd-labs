# Lab Instructions for LAB07: Multi-Environment GitOps - Staging to Production

This document provides detailed step-by-step instructions for implementing robust multi-environment GitOps workflows. You'll learn how to structure environments, configure environment-specific settings, and implement safe promotion workflows from staging to production.

We will start with understanding multi-environment strategies, then implement both folder-based and branch-based approaches.

---

## 🚀 Lab Steps

### Phase 1: Copy Lab Materials and Understand Multi-Environment Architecture

**1. Prepare Your Git Repository:**
   * Use your existing Git repository from previous labs, or create a new public repository named `multi-env-gitops-demo`
   * In your local clone of the repository, create the directory structure:
      ```bash
      mkdir -p environments/{staging,production,common}
      mkdir -p argocd-apps
      ```
   * This structure separates environment-specific configurations while maintaining common resources

**2. Copy Kubernetes Namespaces:**
   * Copy staging namespace definition:
      ```bash
      cp ../path-to-cicd-labs/ArgoCD/LAB07-Staging-To-Production/environments/common/namespace-staging.yaml ./environments/common/namespace-staging.yaml
      ```
   
   * Review staging namespace:
      ```bash
      cat environments/common/namespace-staging.yaml
      ```
   
   * Copy production namespace definition:
      ```bash
      cp ../path-to-cicd-labs/ArgoCD/LAB07-Staging-To-Production/environments/common/namespace-production.yaml ./environments/common/namespace-production.yaml
      ```
   
   * Review production namespace:
      ```bash
      cat environments/common/namespace-production.yaml
      ```
   
   * Apply the namespaces to your cluster:
      ```bash
      kubectl apply -f environments/common/namespace-staging.yaml
      kubectl apply -f environments/common/namespace-production.yaml
      ```

**3. Verify Namespace Creation:**
   ```bash
   kubectl get namespaces | grep webapp
   kubectl describe namespace webapp-staging
   kubectl describe namespace webapp-production
   ```

### Phase 2: Copy Environment-Specific Configurations

**4. Copy Staging Environment Configuration:**
   * Copy staging deployment:
      ```bash
      cp ../path-to-cicd-labs/ArgoCD/LAB07-Staging-To-Production/environments/staging/deployment.yaml ./environments/staging/deployment.yaml
      ```
   
   * Review staging deployment:
      ```bash
      cat environments/staging/deployment.yaml
      ```

   * Copy staging service:
      ```bash
      cp ../path-to-cicd-labs/ArgoCD/LAB07-Staging-To-Production/environments/staging/service.yaml ./environments/staging/service.yaml
      ```
   
   * Review staging service:
      ```bash
      cat environments/staging/service.yaml
      ```

   * Copy staging configuration:
      ```bash
      cp ../path-to-cicd-labs/ArgoCD/LAB07-Staging-To-Production/environments/staging/configmap.yaml ./environments/staging/configmap.yaml
      ```
   
   * Review staging configuration:
      ```bash
      cat environments/staging/configmap.yaml
      ```

   * Copy staging horizontal pod autoscaler:
      ```bash
      cp ../path-to-cicd-labs/ArgoCD/LAB07-Staging-To-Production/environments/staging/hpa.yaml ./environments/staging/hpa.yaml
      ```
   
   * Review staging HPA:
      ```bash
      cat environments/staging/hpa.yaml
      ```

**5. Copy Production Environment Configuration:**
   * Copy production deployment (with higher resources and replicas):
      ```bash
      cp ../path-to-cicd-labs/ArgoCD/LAB07-Staging-To-Production/environments/production/deployment.yaml ./environments/production/deployment.yaml
      ```
   
   * Review production deployment:
      ```bash
      cat environments/production/deployment.yaml
      ```

   * Copy production service:
      ```bash
      cp ../path-to-cicd-labs/ArgoCD/LAB07-Staging-To-Production/environments/production/service.yaml ./environments/production/service.yaml
      ```
   
   * Review production service:
      ```bash
      cat environments/production/service.yaml
      ```

   * Copy production configuration (with production-specific settings):
      ```bash
      cp ../path-to-cicd-labs/ArgoCD/LAB07-Staging-To-Production/environments/production/configmap.yaml ./environments/production/configmap.yaml
      ```
   
   * Review production configuration:
      ```bash
      cat environments/production/configmap.yaml
      ```

   * Copy production horizontal pod autoscaler (more aggressive scaling):
      ```bash
      cp ../path-to-cicd-labs/ArgoCD/LAB07-Staging-To-Production/environments/production/hpa.yaml ./environments/production/hpa.yaml
      ```
   
   * Review production HPA:
      ```bash
      cat environments/production/hpa.yaml
      ```

### Phase 3: Copy ArgoCD Applications for Multi-Environment

**6. Copy ArgoCD Application for Staging:**
   ```bash
   cp ../path-to-cicd-labs/ArgoCD/LAB07-Staging-To-Production/argocd-apps/staging-app.yaml ./argocd-apps/staging-app.yaml
   ```

**7. Review Staging Application:**
   ```bash
   cat argocd-apps/staging-app.yaml
   ```

**8. Copy ArgoCD Application for Production:**
   ```bash
   cp ../path-to-cicd-labs/ArgoCD/LAB07-Staging-To-Production/argocd-apps/production-app.yaml ./argocd-apps/production-app.yaml
   ```

**9. Review Production Application:**
   ```bash
   cat argocd-apps/production-app.yaml
   ```

**10. Update Git Repository URLs:**
   * Update the repository URL in both ArgoCD applications:
      ```bash
      # Replace with your actual Git repository URL
      GIT_REPO_URL="https://github.com/YOUR_USERNAME/multi-env-gitops-demo.git"
      
      sed -i "s|YOUR_GIT_REPO_URL_HERE|$GIT_REPO_URL|g" argocd-apps/staging-app.yaml
      sed -i "s|YOUR_GIT_REPO_URL_HERE|$GIT_REPO_URL|g" argocd-apps/production-app.yaml
      ```
   * Verify the URLs were updated correctly:
      ```bash
      grep "repoURL" argocd-apps/*.yaml
      ```

### Phase 4: Deploy and Test Environment Separation

**11. Commit and Push Initial Configuration:**
   ```bash
   git add .
   git commit -m "Add multi-environment GitOps configuration"
   git push origin main
   ```

**12. Deploy ArgoCD Applications:**
   * Apply the staging application:
      ```bash
      kubectl apply -f argocd-apps/staging-app.yaml
      ```
   * Apply the production application:
      ```bash
      kubectl apply -f argocd-apps/production-app.yaml
      ```

**13. Monitor Application Deployment:**
   * Open ArgoCD UI and verify both applications appear
   * Check that staging syncs automatically
   * Verify production requires manual sync (safety measure)
   * Monitor the sync status:
      ```bash
      kubectl get applications -n argocd
      kubectl describe application webapp-staging -n argocd
      kubectl describe application webapp-production -n argocd
      ```

**14. Verify Environment Separation:**
   * Check staging deployment:
      ```bash
      kubectl get pods -n webapp-staging
      kubectl get services -n webapp-staging
      kubectl get configmaps -n webapp-staging
      kubectl get hpa -n webapp-staging
      ```
   * Check production deployment:
      ```bash
      kubectl get pods -n webapp-production
      kubectl get services -n webapp-production
      kubectl get configmaps -n webapp-production
      kubectl get hpa -n webapp-production
      ```
   * Notice the different resource allocations and replica counts

**15. Test Applications:**
   * Test staging application:
      ```bash
      minikube ip  # Get Minikube IP
      curl http://<MINIKUBE_IP>:30080/
      ```
   * Test production application:
      ```bash
      curl http://<MINIKUBE_IP>:30090/
      ```

### Phase 5: Implement Environment Promotion Workflow

**16. Test Configuration Differences:**
   * Check staging configuration:
      ```bash
      kubectl get configmap webapp-config -n webapp-staging -o yaml
      ```
   * Check production configuration:
      ```bash
      kubectl get configmap webapp-config -n webapp-production -o yaml
      ```
   * Notice the different values for log_level, max_connections, and feature_flags

**17. Simulate Configuration Update in Staging:**
   * Update staging configuration:
      ```bash
      kubectl patch configmap webapp-config -n webapp-staging --patch '{"data":{"feature_flags":"feature_a=true,feature_b=true,feature_c=true"}}'
      ```
   * Restart staging deployment to pick up changes:
      ```bash
      kubectl rollout restart deployment webapp -n webapp-staging
      ```
   * Monitor rollout:
      ```bash
      kubectl rollout status deployment webapp -n webapp-staging
      ```

**18. Test Environment-Specific Scaling:**
   * Generate load on staging (simulate traffic):
      ```bash
      kubectl run load-generator --image=busybox --restart=Never --rm -i --tty -- sh -c "while true; do wget -q -O- http://webapp-service.webapp-staging.svc.cluster.local:80; done"
      ```
   * In another terminal, watch HPA scaling:
      ```bash
      kubectl get hpa webapp-hpa -n webapp-staging --watch
      ```
   * Stop the load generator with Ctrl+C and watch scaling down

### Phase 6: Multi-Environment Promotion Workflow

**19. Implement Staged Rollout Process:**
   * Update the application image in staging:
      ```bash
      kubectl patch deployment webapp -n webapp-staging --patch '{"spec":{"template":{"spec":{"containers":[{"name":"webapp","image":"nginx:1.22"}]}}}}'
      ```
   * Verify the update in staging:
      ```bash
      kubectl rollout status deployment webapp -n webapp-staging
      kubectl get deployment webapp -n webapp-staging -o jsonpath='{.spec.template.spec.containers[0].image}'
      ```

**20. Test Staging After Update:**
   * Verify staging is working correctly:
      ```bash
      curl http://<MINIKUBE_IP>:30080/
      kubectl get pods -n webapp-staging
      ```
   * Check application logs:
      ```bash
      kubectl logs -l app=webapp -n webapp-staging --tail=10
      ```

**21. Promote Changes to Production:**
   * After validating staging, update production deployment:
      ```bash
      kubectl patch deployment webapp -n webapp-production --patch '{"spec":{"template":{"spec":{"containers":[{"name":"webapp","image":"nginx:1.22"}]}}}}'
      ```
   * Monitor production rollout carefully:
      ```bash
      kubectl rollout status deployment webapp -n webapp-production --timeout=300s
      ```
   * Verify production application:
      ```bash
      curl http://<MINIKUBE_IP>:30090/
      kubectl get pods -n webapp-production
      ```

**22. Implement GitOps-Based Promotion:**
   * Instead of kubectl patches, update the Git repository:
      ```bash
      # Update staging deployment file
      sed -i 's|nginx:1.21|nginx:1.22|g' environments/staging/deployment.yaml
      
      # Commit and push
      git add environments/staging/deployment.yaml
      git commit -m "Update staging to nginx:1.22"
      git push origin main
      ```
   * Watch ArgoCD sync the changes automatically
   * After staging validation, promote to production:
      ```bash
      # Update production deployment file
      sed -i 's|nginx:1.21|nginx:1.22|g' environments/production/deployment.yaml
      
      # Commit and push
      git add environments/production/deployment.yaml
      git commit -m "Promote nginx:1.22 to production"
      git push origin main
      ```
   * Manually sync production in ArgoCD UI

### Phase 7: Environment Comparison and Validation

**23. Compare Environment Configurations:**
   * Compare deployment configurations:
      ```bash
      diff environments/staging/deployment.yaml environments/production/deployment.yaml
      ```
   * Compare service configurations:
      ```bash
      diff environments/staging/service.yaml environments/production/service.yaml
      ```
   * Compare ConfigMap configurations:
      ```bash
      diff environments/staging/configmap.yaml environments/production/configmap.yaml
      ```

**24. Validate Environment Isolation:**
   * Check resource usage in staging:
      ```bash
      kubectl top pods -n webapp-staging
      kubectl describe hpa webapp-hpa -n webapp-staging
      ```
   * Check resource usage in production:
      ```bash
      kubectl top pods -n webapp-production
      kubectl describe hpa webapp-hpa -n webapp-production
      ```

**25. Test Rollback Scenarios:**
   * Simulate a bad deployment in staging:
      ```bash
      kubectl patch deployment webapp -n webapp-staging --patch '{"spec":{"template":{"spec":{"containers":[{"name":"webapp","image":"nginx:invalid-tag"}]}}}}'
      ```
   * Watch the rollout fail:
      ```bash
      kubectl rollout status deployment webapp -n webapp-staging --timeout=60s
      kubectl get pods -n webapp-staging
      ```
   * Rollback staging:
      ```bash
      kubectl rollout undo deployment webapp -n webapp-staging
      kubectl rollout status deployment webapp -n webapp-staging
      ```
   * Verify staging is back to working state:
      ```bash
      curl http://<MINIKUBE_IP>:30080/
      ```

### Phase 8: Advanced Multi-Environment Features

**26. Implement Environment-Specific Secrets:**
   * Create staging secret:
      ```bash
      kubectl create secret generic webapp-secrets \
        --from-literal=api-key="staging-api-key-123" \
        --from-literal=db-password="staging-db-pass" \
        -n webapp-staging
      ```
   * Create production secret:
      ```bash
      kubectl create secret generic webapp-secrets \
        --from-literal=api-key="production-api-key-456" \
        --from-literal=db-password="production-db-pass" \
        -n webapp-production
      ```

**27. Test Environment-Specific Monitoring:**
   * Check staging metrics:
      ```bash
      kubectl get events -n webapp-staging --sort-by='.lastTimestamp'
      kubectl describe deployment webapp -n webapp-staging
      ```
   * Check production metrics:
      ```bash
      kubectl get events -n webapp-production --sort-by='.lastTimestamp'
      kubectl describe deployment webapp -n webapp-production
      ```

**28. Validate Complete Multi-Environment Setup:**
   * Verify both environments are running:
      ```bash
      kubectl get all -n webapp-staging
      kubectl get all -n webapp-production
      ```
   * Check ArgoCD application health:
      ```bash
      kubectl get applications -n argocd -o custom-columns=NAME:.metadata.name,HEALTH:.status.health.status,SYNC:.status.sync.status
      ```
   * Test both applications are accessible:
      ```bash
      echo "Testing Staging:"
      curl -s http://<MINIKUBE_IP>:30080/ | head -5
      echo "Testing Production:"
      curl -s http://<MINIKUBE_IP>:30090/ | head -5
      ```

---

## ✅ Validation Checklist

- [ ] Successfully copied and reviewed all environment configurations
- [ ] Created separate namespaces for staging and production environments
- [ ] Deployed ArgoCD applications for both environments with different sync policies
- [ ] Verified environment-specific configurations (resources, replicas, settings)
- [ ] Tested environment isolation and resource separation
- [ ] Successfully implemented staged rollout from staging to production
- [ ] Validated horizontal pod autoscaling works differently in each environment
- [ ] Tested rollback scenarios in staging environment
- [ ] Implemented environment-specific secrets and configurations
- [ ] Verified GitOps-based promotion workflow
- [ ] Confirmed production requires manual intervention while staging is automated
- [ ] Tested both kubectl-based and Git-based deployment updates
- [ ] Validated monitoring and observability for both environments

---

## 🧹 Cleanup

**29. Delete ArgoCD Applications:**
   * In the ArgoCD UI, delete both applications:
      - Click on `webapp-staging` → DELETE → Check "Delete resources" → Confirm
      - Click on `webapp-production` → DELETE → Check "Delete resources" → Confirm
   * Alternatively, use kubectl:
      ```bash
      kubectl delete application webapp-staging -n argocd
      kubectl delete application webapp-production -n argocd
      ```

**30. Delete Namespaces:**
   ```bash
   kubectl delete namespace webapp-staging
   kubectl delete namespace webapp-production
   ```

**31. Clean Up Git Repository (Optional):**
   ```bash
   git rm -r environments/ argocd-apps/
   git commit -m "Clean up multi-environment demo"
   git push origin main
   ```

**32. Stop Minikube (If Done):**
   ```bash
   minikube stop
   ```

---

## 🎯 Key Learning Outcomes

By completing this lab, you have learned:

1. **Multi-Environment Architecture**: Understanding how to structure GitOps repositories for multiple environments
2. **Environment Separation**: Implementing proper isolation between staging and production environments
3. **Configuration Management**: Managing environment-specific configurations, resources, and settings
4. **Promotion Workflows**: Implementing safe promotion processes from staging to production
5. **GitOps Best Practices**: Using Git as the source of truth for environment configurations
6. **ArgoCD Multi-App Management**: Managing multiple applications with different sync policies
7. **Rollback Strategies**: Implementing and testing rollback procedures for failed deployments

This comprehensive multi-environment setup demonstrates enterprise-grade GitOps practices for managing applications across different environments safely and efficiently.

---

## 📚 Additional Resources

- [ArgoCD Best Practices for Multi-Environment](https://argo-cd.readthedocs.io/en/stable/user-guide/best_practices/)
- [Kubernetes Multi-Tenancy](https://kubernetes.io/docs/concepts/security/multi-tenancy/)
- [GitOps Principles](https://opengitops.dev/)
- [Environment Promotion Strategies](https://www.weave.works/technologies/gitops/)
- [Horizontal Pod Autoscaling](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/) 