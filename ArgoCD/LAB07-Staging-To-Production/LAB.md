# Lab Instructions for LAB07: Multi-Environment GitOps - Staging to Production

This document provides detailed step-by-step instructions for implementing robust multi-environment GitOps workflows. You'll learn how to structure environments, configure environment-specific settings, and implement safe promotion workflows from staging to production.

We will start with understanding multi-environment strategies, then implement both folder-based and branch-based approaches.

---

## 🚀 Lab Steps

### Phase 1: Understanding Multi-Environment Architecture

**1. Prepare Your Git Repository:**
   a. Use your existing Git repository from previous labs, or create a new public repository named `multi-env-gitops-demo`
   b. In your local clone of the repository, create the directory structure:
      ```bash
      mkdir -p environments/{staging,production,common}
      mkdir -p argocd-apps
      ```
   c. This structure separates environment-specific configurations while maintaining common resources

**2. Create Kubernetes Namespaces:**
   a. Create staging namespace definition:
      ```bash
      cat > environments/common/namespace-staging.yaml << 'EOF'
      apiVersion: v1
      kind: Namespace
      metadata:
        name: webapp-staging
        labels:
          environment: staging
          managed-by: argocd
      EOF
      ```
   b. Create production namespace definition:
      ```bash
      cat > environments/common/namespace-production.yaml << 'EOF'
      apiVersion: v1
      kind: Namespace
      metadata:
        name: webapp-production
        labels:
          environment: production
          managed-by: argocd
      EOF
      ```
   c. Apply the namespaces to your cluster:
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

### Phase 2: Create Environment-Specific Configurations

**4. Create Staging Environment Configuration:**
   a. Create staging deployment:
      ```bash
      cat > environments/staging/deployment.yaml << 'EOF'
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: webapp
        namespace: webapp-staging
        labels:
          app: webapp
          environment: staging
          version: v1.0.0
      spec:
        replicas: 2
        selector:
          matchLabels:
            app: webapp
            environment: staging
        template:
          metadata:
            labels:
              app: webapp
              environment: staging
              version: v1.0.0
          spec:
            containers:
            - name: webapp
              image: nginx:1.21
              ports:
              - containerPort: 80
              env:
              - name: ENVIRONMENT
                valueFrom:
                  configMapKeyRef:
                    name: webapp-config
                    key: environment
              - name: LOG_LEVEL
                valueFrom:
                  configMapKeyRef:
                    name: webapp-config
                    key: log_level
              - name: MAX_CONNECTIONS
                valueFrom:
                  configMapKeyRef:
                    name: webapp-config
                    key: max_connections
              resources:
                requests:
                  memory: "128Mi"
                  cpu: "100m"
                limits:
                  memory: "256Mi"
                  cpu: "200m"
              livenessProbe:
                httpGet:
                  path: /
                  port: 80
                initialDelaySeconds: 10
                periodSeconds: 10
              readinessProbe:
                httpGet:
                  path: /
                  port: 80
                initialDelaySeconds: 5
                periodSeconds: 5
      EOF
      ```

   b. Create staging service:
      ```bash
      cat > environments/staging/service.yaml << 'EOF'
      apiVersion: v1
      kind: Service
      metadata:
        name: webapp-service
        namespace: webapp-staging
        labels:
          app: webapp
          environment: staging
      spec:
        type: NodePort
        selector:
          app: webapp
          environment: staging
        ports:
        - port: 80
          targetPort: 80
          nodePort: 30080
          protocol: TCP
          name: http
      EOF
      ```

   c. Create staging configuration:
      ```bash
      cat > environments/staging/configmap.yaml << 'EOF'
      apiVersion: v1
      kind: ConfigMap
      metadata:
        name: webapp-config
        namespace: webapp-staging
        labels:
          app: webapp
          environment: staging
      data:
        environment: "staging"
        log_level: "debug"
        max_connections: "100"
        database_url: "staging-db.example.com"
        cache_ttl: "300"
        feature_flags: "feature_a=true,feature_b=true,feature_c=false"
      EOF
      ```

   d. Create staging horizontal pod autoscaler:
      ```bash
      cat > environments/staging/hpa.yaml << 'EOF'
      apiVersion: autoscaling/v2
      kind: HorizontalPodAutoscaler
      metadata:
        name: webapp-hpa
        namespace: webapp-staging
        labels:
          app: webapp
          environment: staging
      spec:
        scaleTargetRef:
          apiVersion: apps/v1
          kind: Deployment
          name: webapp
        minReplicas: 2
        maxReplicas: 5
        metrics:
        - type: Resource
          resource:
            name: cpu
            target:
              type: Utilization
              averageUtilization: 70
        - type: Resource
          resource:
            name: memory
            target:
              type: Utilization
              averageUtilization: 80
      EOF
      ```

**5. Create Production Environment Configuration:**
   a. Create production deployment (with higher resources and replicas):
      ```bash
      cat > environments/production/deployment.yaml << 'EOF'
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: webapp
        namespace: webapp-production
        labels:
          app: webapp
          environment: production
          version: v1.0.0
      spec:
        replicas: 3
        selector:
          matchLabels:
            app: webapp
            environment: production
        template:
          metadata:
            labels:
              app: webapp
              environment: production
              version: v1.0.0
          spec:
            containers:
            - name: webapp
              image: nginx:1.21
              ports:
              - containerPort: 80
              env:
              - name: ENVIRONMENT
                valueFrom:
                  configMapKeyRef:
                    name: webapp-config
                    key: environment
              - name: LOG_LEVEL
                valueFrom:
                  configMapKeyRef:
                    name: webapp-config
                    key: log_level
              - name: MAX_CONNECTIONS
                valueFrom:
                  configMapKeyRef:
                    name: webapp-config
                    key: max_connections
              resources:
                requests:
                  memory: "256Mi"
                  cpu: "200m"
                limits:
                  memory: "512Mi"
                  cpu: "500m"
              livenessProbe:
                httpGet:
                  path: /
                  port: 80
                initialDelaySeconds: 15
                periodSeconds: 10
              readinessProbe:
                httpGet:
                  path: /
                  port: 80
                initialDelaySeconds: 10
                periodSeconds: 5
      EOF
      ```

   b. Create production service:
      ```bash
      cat > environments/production/service.yaml << 'EOF'
      apiVersion: v1
      kind: Service
      metadata:
        name: webapp-service
        namespace: webapp-production
        labels:
          app: webapp
          environment: production
      spec:
        type: NodePort
        selector:
          app: webapp
          environment: production
        ports:
        - port: 80
          targetPort: 80
          nodePort: 30090
          protocol: TCP
          name: http
      EOF
      ```

   c. Create production configuration (with production-specific settings):
      ```bash
      cat > environments/production/configmap.yaml << 'EOF'
      apiVersion: v1
      kind: ConfigMap
      metadata:
        name: webapp-config
        namespace: webapp-production
        labels:
          app: webapp
          environment: production
      data:
        environment: "production"
        log_level: "info"
        max_connections: "500"
        database_url: "prod-db.example.com"
        cache_ttl: "3600"
        feature_flags: "feature_a=true,feature_b=false,feature_c=false"
      EOF
      ```

   d. Create production horizontal pod autoscaler (more aggressive scaling):
      ```bash
      cat > environments/production/hpa.yaml << 'EOF'
      apiVersion: autoscaling/v2
      kind: HorizontalPodAutoscaler
      metadata:
        name: webapp-hpa
        namespace: webapp-production
        labels:
          app: webapp
          environment: production
      spec:
        scaleTargetRef:
          apiVersion: apps/v1
          kind: Deployment
          name: webapp
        minReplicas: 3
        maxReplicas: 10
        metrics:
        - type: Resource
          resource:
            name: cpu
            target:
              type: Utilization
              averageUtilization: 60
        - type: Resource
          resource:
            name: memory
            target:
              type: Utilization
              averageUtilization: 70
      EOF
      ```

### Phase 3: Create ArgoCD Applications for Multi-Environment

**6. Create ArgoCD Application for Staging:**
   ```bash
   cat > argocd-apps/staging-app.yaml << 'EOF'
   apiVersion: argoproj.io/v1alpha1
   kind: Application
   metadata:
     name: webapp-staging
     namespace: argocd
     labels:
       environment: staging
   spec:
     project: default
     source:
       repoURL: YOUR_GIT_REPO_URL_HERE
       targetRevision: HEAD
       path: environments/staging
     destination:
       server: https://kubernetes.default.svc
       namespace: webapp-staging
     syncPolicy:
       automated:
         prune: true
         selfHeal: true
       syncOptions:
       - CreateNamespace=false
       retry:
         limit: 5
         backoff:
           duration: 5s
           factor: 2
           maxDuration: 3m
   EOF
   ```

**7. Create ArgoCD Application for Production:**
   ```bash
   cat > argocd-apps/production-app.yaml << 'EOF'
   apiVersion: argoproj.io/v1alpha1
   kind: Application
   metadata:
     name: webapp-production
     namespace: argocd
     labels:
       environment: production
   spec:
     project: default
     source:
       repoURL: YOUR_GIT_REPO_URL_HERE
       targetRevision: HEAD
       path: environments/production
     destination:
       server: https://kubernetes.default.svc
       namespace: webapp-production
     syncPolicy:
       manual: {}
       syncOptions:
       - CreateNamespace=false
       retry:
         limit: 3
         backoff:
           duration: 10s
           factor: 2
           maxDuration: 5m
   EOF
   ```

**8. Update ArgoCD Applications with Your Git Repository URL:**
   a. Replace `YOUR_GIT_REPO_URL_HERE` with your actual Git repository URL:
      ```bash
      # Replace with your actual Git repository URL
      GIT_REPO_URL="https://github.com/YOUR_USERNAME/multi-env-gitops-demo.git"
      
      sed -i "s|YOUR_GIT_REPO_URL_HERE|$GIT_REPO_URL|g" argocd-apps/staging-app.yaml
      sed -i "s|YOUR_GIT_REPO_URL_HERE|$GIT_REPO_URL|g" argocd-apps/production-app.yaml
      ```

### Phase 4: Deploy Multi-Environment Setup

**9. Commit Initial Environment Configurations:**
   ```bash
   git add environments/ argocd-apps/
   git commit -m "Add multi-environment configuration with staging and production"
   git push origin main
   ```

**10. Deploy ArgoCD Applications:**
   a. Apply the staging application:
      ```bash
      kubectl apply -f argocd-apps/staging-app.yaml
      ```
   b. Apply the production application:
      ```bash
      kubectl apply -f argocd-apps/production-app.yaml
      ```
   c. Verify applications were created:
      ```bash
      kubectl get applications -n argocd
      ```

**11. Monitor Initial Synchronization:**
   a. Open the ArgoCD UI in your browser
   b. You should see two applications: `webapp-staging` and `webapp-production`
   c. The staging application should sync automatically (due to auto-sync policy)
   d. The production application should be "OutOfSync" and require manual sync
   e. Manually sync the production application by clicking "SYNC" in the UI

**12. Verify Environment Deployments:**
   a. Check staging deployment:
      ```bash
      kubectl get all -n webapp-staging
      kubectl get configmap -n webapp-staging
      kubectl get hpa -n webapp-staging
      ```
   b. Check production deployment:
      ```bash
      kubectl get all -n webapp-production
      kubectl get configmap -n webapp-production
      kubectl get hpa -n webapp-production
      ```
   c. Notice the differences in replica counts and resource limits

### Phase 5: Implement Promotion Workflow

**13. Test Staging Environment:**
   a. Get your Minikube IP:
      ```bash
      minikube ip
      ```
   b. Test staging application:
      ```bash
      curl http://<MINIKUBE_IP>:30080
      ```
   c. Check staging configuration:
      ```bash
      kubectl exec -n webapp-staging deployment/webapp -- env | grep -E "(ENVIRONMENT|LOG_LEVEL|MAX_CONNECTIONS)"
      ```

**14. Make a Change in Staging:**
   a. Update the staging application image version:
      ```bash
      sed -i 's/nginx:1.21/nginx:1.22/g' environments/staging/deployment.yaml
      ```
   b. Update the version label:
      ```bash
      sed -i 's/version: v1.0.0/version: v1.1.0/g' environments/staging/deployment.yaml
      ```
   c. Add a new configuration to staging:
      ```bash
      cat >> environments/staging/configmap.yaml << 'EOF'
        new_feature: "enabled"
      EOF
      ```

**15. Deploy Change to Staging:**
   a. Commit the staging changes:
      ```bash
      git add environments/staging/
      git commit -m "Update staging to nginx 1.22 and add new feature"
      git push origin main
      ```
   b. The staging application should auto-sync and deploy the changes
   c. Verify the update in ArgoCD UI and kubectl:
      ```bash
      kubectl describe deployment webapp -n webapp-staging | grep Image
      kubectl get configmap webapp-config -n webapp-staging -o yaml | grep new_feature
      ```

**16. Test and Validate Staging Changes:**
   a. Test the updated staging application:
      ```bash
      curl http://<MINIKUBE_IP>:30080
      ```
   b. Monitor application health:
      ```bash
      kubectl get pods -n webapp-staging -w
      ```
   c. Check application logs for any issues:
      ```bash
      kubectl logs -n webapp-staging deployment/webapp
      ```

**17. Promote Changes to Production:**
   a. Once satisfied with staging, promote the changes to production:
      ```bash
      # Copy the image update
      sed -i 's/nginx:1.21/nginx:1.22/g' environments/production/deployment.yaml
      sed -i 's/version: v1.0.0/version: v1.1.0/g' environments/production/deployment.yaml
      
      # Copy the configuration update
      cat >> environments/production/configmap.yaml << 'EOF'
        new_feature: "enabled"
      EOF
      ```
   b. Commit the production changes:
      ```bash
      git add environments/production/
      git commit -m "Promote nginx 1.22 and new feature to production"
      git push origin main
      ```

**18. Deploy to Production (Manual Approval):**
   a. In the ArgoCD UI, the production application should show as "OutOfSync"
   b. Review the differences in the ArgoCD UI
   c. Manually click "SYNC" to deploy to production
   d. Monitor the production deployment carefully:
      ```bash
      kubectl get pods -n webapp-production -w
      ```

### Phase 6: Advanced Environment Management

**19. Implement Environment-Specific Rollback:**
   a. If there's an issue in production, roll back by reverting the Git commit:
      ```bash
      # Revert only the production changes
      git log --oneline -5  # Find the commit hash
      git revert COMMIT_HASH_OF_PRODUCTION_PROMOTION
      git push origin main
      ```
   b. The production application will auto-detect the change and show "OutOfSync"
   c. Manually sync to apply the rollback

**20. Test Blue-Green Deployment Simulation:**
   a. Create a temporary "blue" version in production:
      ```bash
      # Scale up production temporarily
      kubectl scale deployment webapp --replicas=6 -n webapp-production
      ```
   b. Update to a new version:
      ```bash
      sed -i 's/nginx:1.22/nginx:1.23/g' environments/production/deployment.yaml
      git add environments/production/deployment.yaml
      git commit -m "Update production to nginx 1.23 (blue-green test)"
      git push origin main
      ```
   c. Sync in ArgoCD and monitor the rolling update
   d. The old pods will be terminated gradually as new ones come online

**21. Implement Configuration Drift Detection:**
   a. Manually change something in the cluster:
      ```bash
      kubectl patch deployment webapp -n webapp-staging -p '{"spec":{"replicas":5}}'
      ```
   b. Check ArgoCD UI - staging should show as "OutOfSync" due to self-heal being enabled
   c. ArgoCD should automatically fix the drift within a few minutes
   d. Production won't auto-heal due to manual sync policy

### Phase 7: Multi-Environment Best Practices

**22. Implement Environment Monitoring:**
   a. Check resource usage across environments:
      ```bash
      echo "=== Staging Resources ==="
      kubectl top pods -n webapp-staging
      echo "=== Production Resources ==="
      kubectl top pods -n webapp-production
      ```
   b. Compare HPA status:
      ```bash
      kubectl get hpa -n webapp-staging
      kubectl get hpa -n webapp-production
      ```

**23. Document Promotion Procedures:**
   a. Create a simple promotion checklist:
      ```bash
      cat > PROMOTION_CHECKLIST.md << 'EOF'
      # Production Promotion Checklist
      
      ## Pre-Promotion (Staging)
      - [ ] Feature tested in staging environment
      - [ ] All staging tests passing
      - [ ] Performance metrics acceptable
      - [ ] Security scan completed
      - [ ] Database migrations tested (if applicable)
      
      ## Promotion Process
      - [ ] Copy changes from staging to production configs
      - [ ] Update version numbers and labels
      - [ ] Commit with descriptive message
      - [ ] Review diff in ArgoCD UI
      - [ ] Manual sync to production
      - [ ] Monitor deployment progress
      
      ## Post-Promotion
      - [ ] Verify application functionality
      - [ ] Check monitoring and logs
      - [ ] Validate performance metrics
      - [ ] Update documentation
      - [ ] Notify stakeholders
      EOF
      ```

**24. Understanding Environment Differences:**
   a. Compare the configurations:
      ```bash
      echo "=== Staging vs Production Differences ==="
      echo "Replicas:"
      grep "replicas:" environments/staging/deployment.yaml environments/production/deployment.yaml
      echo "Resources:"
      grep -A 4 "resources:" environments/staging/deployment.yaml environments/production/deployment.yaml
      echo "Log Level:"
      grep "log_level:" environments/staging/configmap.yaml environments/production/configmap.yaml
      ```

---

## ✅ Validation Checklist

- [ ] Successfully created separate staging and production namespaces
- [ ] Created environment-specific configurations with different resource limits
- [ ] Implemented ConfigMaps with environment-specific settings
- [ ] Set up HPA with different scaling policies per environment
- [ ] Created ArgoCD applications for both environments with different sync policies
- [ ] Successfully deployed applications to both environments
- [ ] Staging environment has auto-sync enabled and working
- [ ] Production environment requires manual sync approval
- [ ] Tested promotion workflow from staging to production
- [ ] Verified environment-specific configurations are applied correctly
- [ ] Tested rollback procedures for both environments
- [ ] Implemented and tested configuration drift detection
- [ ] Compared resource usage between environments
- [ ] Understood the differences between staging and production configurations

---

## 🧹 Cleanup

**1. Delete ArgoCD Applications:**
   a. In the ArgoCD UI, delete both applications:
      - Click on `webapp-staging` → DELETE → Check "Delete resources" → Confirm
      - Click on `webapp-production` → DELETE → Check "Delete resources" → Confirm
   b. Alternatively, use kubectl:
      ```bash
      kubectl delete application webapp-staging -n argocd
      kubectl delete application webapp-production -n argocd
      ```

**2. Delete Namespaces:**
   ```bash
   kubectl delete namespace webapp-staging
   kubectl delete namespace webapp-production
   ```

**3. Clean Up Git Repository (Optional):**
   a. You can keep the repository for future experiments
   b. Or clean up if desired:
      ```bash
      git rm -r environments/ argocd-apps/ PROMOTION_CHECKLIST.md
      git commit -m "Clean up multi-environment demo"
      git push origin main
      ```

**4. Stop Minikube (If Done):**
   ```bash
   minikube stop
   ```

---

## 🎓 Key Learnings Summary

### **Multi-Environment Architecture:**
- ✅ **Environment Separation**: Use namespaces and folder structure for clear isolation
- ✅ **Configuration Management**: Environment-specific ConfigMaps and resource limits
- ✅ **Progressive Deployment**: Staging first, then production with manual approval
- ✅ **Resource Scaling**: Different replica counts and resource limits per environment
- ❌ **Complexity**: Multiple environments increase operational overhead
- ❌ **Consistency**: Need to maintain parity while allowing differences

### **GitOps Promotion Strategies:**
- ✅ **Folder-Based**: Clear separation, easy to understand and manage
- ✅ **Git-Based Workflow**: All changes tracked and auditable
- ✅ **Rollback Capability**: Easy to revert using Git history
- ✅ **Automated Staging**: Auto-sync for staging enables faster feedback
- ❌ **Manual Production**: Requires human approval, can create bottlenecks
- ❌ **Configuration Drift**: Need monitoring to detect manual changes

### **Environment-Specific Configurations:**
- **Staging Environment:**
  - Lower resource limits (faster deployment, cost-effective)
  - Debug logging enabled
  - Experimental features enabled
  - Auto-sync for rapid iteration
  - More aggressive autoscaling testing

- **Production Environment:**
  - Higher resource limits (performance and reliability)
  - Info-level logging (security and performance)
  - Stable features only
  - Manual sync for change control
  - Conservative autoscaling policies

### **Best Practices Learned:**
1. **Environment Parity**: Keep environments similar but not identical
2. **Resource Management**: Right-size resources for each environment's purpose
3. **Sync Policies**: Auto-sync for staging, manual for production
4. **Configuration Management**: Use ConfigMaps for environment-specific settings
5. **Monitoring**: Implement drift detection and resource monitoring
6. **Documentation**: Maintain promotion checklists and procedures
7. **Testing**: Validate in staging before promoting to production
8. **Rollback Plans**: Always have a rollback strategy ready

### **Advanced Concepts:**
- **Blue-Green Deployments**: Use multiple environments for zero-downtime deployments
- **Canary Releases**: Gradual rollout within environments
- **Feature Flags**: Control feature availability per environment
- **Database Migrations**: Handle schema changes across environments
- **Secret Management**: Environment-specific secrets and configurations

---

## 🏗️ Architecture Patterns Deep Dive

### **Folder-Based vs Branch-Based Strategies:**

**Folder-Based (Used in this lab):**
- ✅ **Simplicity**: All environments in one branch, clear folder structure
- ✅ **Visibility**: Easy to compare configurations across environments
- ✅ **Git Workflow**: Single branch, simpler merge conflicts
- ❌ **File Duplication**: Similar files replicated across folders
- ❌ **Bulk Changes**: Changes across environments require multiple file edits

**Branch-Based Alternative:**
- ✅ **Isolation**: Complete separation between environments
- ✅ **Release Branching**: Aligns with Git flow release strategies
- ❌ **Complexity**: Merge conflicts between branches
- ❌ **Visibility**: Harder to compare environments
- ❌ **Maintenance**: Multiple branches to maintain

### **Scaling Multi-Environment Architecture:**
For larger organizations, consider:
1. **Multiple Clusters**: Separate clusters per environment
2. **Regional Deployments**: Geographic distribution
3. **Tenant Isolation**: Multi-tenant environments
4. **GitOps Operators**: Advanced tools like Flux or ArgoCD ApplicationSets

---

End of Lab Instructions. Return to the main `README.md` for Key Concepts and Next Steps. 