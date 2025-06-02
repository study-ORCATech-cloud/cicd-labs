# Lab Instructions for LAB05: ArgoCD Sync Policies and Automation

This document provides detailed step-by-step instructions for learning ArgoCD sync policies. You'll experience the difference between manual and automated sync, implement self-healing, and understand the various automation options available in ArgoCD.

We will start with manual sync (the default), then gradually introduce automation features to understand their benefits and use cases.

---

## 🚀 Lab Steps

### Phase 1: Setup with Manual Sync (Baseline)

**1. Prepare Your Git Repository:**
   a. Use your existing Git repository from previous labs, or create a new public repository named `sync-policy-demo`
   b. In your local clone of the repository, create an `app` directory:
      ```bash
      mkdir app
      cd app
      ```

**2. Copy the Demo Application Files:**
   a. Copy all the sync demo files from the lab materials:
      ```bash
      # Copy deployment file
      cp ../path-to-cicd-labs/ArgoCD/LAB05-Sync-Policy-Auto-Sync/sync-demo-app/deployment.yaml ./deployment.yaml
      
      # Copy service file
      cp ../path-to-cicd-labs/ArgoCD/LAB05-Sync-Policy-Auto-Sync/sync-demo-app/service.yaml ./service.yaml
      
      # Copy configmap file
      cp ../path-to-cicd-labs/ArgoCD/LAB05-Sync-Policy-Auto-Sync/sync-demo-app/configmap.yaml ./configmap.yaml
      ```
   b. Review the files - they create a simple nginx deployment with configurable settings
   c. Commit and push the initial version:
      ```bash
      git add .
      git commit -m "Initial sync demo app - manual sync policy"
      git push origin main
      ```

**3. Create Kubernetes Namespace:**
   ```bash
   kubectl create namespace sync-demo-app
   ```

**4. Create ArgoCD Application (Manual Sync):**
   a. Open the ArgoCD UI in your browser
   b. Click **"+ NEW APP"**
   c. Fill in the application details:
      - **Application Name:** `sync-policy-demo`
      - **Project Name:** `default`
      - **SYNC POLICY:** `Manual` (this is the default)
      - **SOURCE Repository URL:** Your Git repository URL
      - **SOURCE Revision:** `HEAD`
      - **SOURCE Path:** `app`
      - **DESTINATION Cluster URL:** `https://kubernetes.default.svc`
      - **DESTINATION Namespace:** `sync-demo-app`
   d. Click **"CREATE"**

**5. Test Manual Sync Behavior:**
   a. Your application should appear as `Missing` and `OutOfSync`
   b. Notice that nothing happens automatically - this is manual sync behavior
   c. Click **"SYNC"** and **"SYNCHRONIZE"** to deploy
   d. Wait for the application to become `Healthy` and `Synced`
   e. Verify the deployment:
      ```bash
      kubectl get all -n sync-demo-app
      ```

**6. Test Manual Sync with Changes:**
   a. Make a change to the ConfigMap in your local repository:
      ```bash
      # Edit configmap.yaml and change the message
      sed -i 's/Manual Mode/Manual Mode - Updated/g' configmap.yaml
      ```
   b. Commit and push the change:
      ```bash
      git add configmap.yaml
      git commit -m "Update ConfigMap message for manual sync test"
      git push origin main
      ```
   c. Go back to ArgoCD UI - after a few minutes, the application should show `OutOfSync`
   d. **Important:** Notice that the change is NOT automatically applied
   e. You must manually click **"SYNC"** to apply the change

### Phase 2: Enable Auto Sync

**7. Configure Auto Sync via ArgoCD UI:**
   a. In the ArgoCD UI, click on your `sync-policy-demo` application
   b. Click on **"APP DETAILS"** (top-left area or details button)
   c. In the summary section, click **"EDIT"** 
   d. Scroll down to find **"SYNC POLICY"**
   e. Toggle **"AUTOMATED"** to enable auto-sync
   f. Click **"SAVE"**
   g. You should see the sync policy now shows as **"Automated"**

**8. Test Auto Sync Behavior:**
   a. Make another change to test auto-sync:
      ```bash
      # Change the replica count in deployment.yaml
      sed -i 's/replicas: 2/replicas: 3/g' deployment.yaml
      ```
   b. Commit and push:
      ```bash
      git add deployment.yaml
      git commit -m "Scale to 3 replicas - testing auto-sync"
      git push origin main
      ```
   c. Watch the ArgoCD UI - within 1-3 minutes, you should see:
      - Application briefly shows `OutOfSync`
      - ArgoCD automatically starts synchronization
      - Application returns to `Synced` state
   d. Verify the change was applied:
      ```bash
      kubectl get pods -n sync-demo-app
      ```
   e. You should now see 3 pods running!

### Phase 3: Configuration Drift and Self-Healing

**9. Enable Self-Healing:**
   a. Go back to your application in ArgoCD UI
   b. Click **"APP DETAILS"** → **"EDIT"**
   c. In the **"SYNC POLICY"** section, enable **"SELF HEAL"**
   d. Click **"SAVE"**

**10. Test Configuration Drift (Manual Changes):**
   a. Manually scale the deployment using kubectl:
      ```bash
      kubectl scale deployment sync-demo-app --replicas=5 -n sync-demo-app
      ```
   b. Check the pods immediately:
      ```bash
      kubectl get pods -n sync-demo-app
      ```
   c. You should see 5 pods for a short time
   d. Watch the ArgoCD UI - within 1-3 minutes, you should see:
      - ArgoCD detects the drift
      - Self-healing kicks in automatically
      - Pods are scaled back to 3 (the Git-defined state)
   e. Verify self-healing worked:
      ```bash
      kubectl get pods -n sync-demo-app
      ```

**11. Test Manual Resource Deletion:**
   a. Delete the ConfigMap manually:
      ```bash
      kubectl delete configmap sync-demo-config -n sync-demo-app
      ```
   b. Check that it's gone:
      ```bash
      kubectl get configmap -n sync-demo-app
      ```
   c. Wait 1-3 minutes and check again:
      ```bash
      kubectl get configmap -n sync-demo-app
      ```
   d. The ConfigMap should be automatically recreated by self-healing!

### Phase 4: Automated Pruning

**12. Enable Automated Pruning:**
   a. In ArgoCD UI, edit your application again
   b. In the **"SYNC POLICY"** section, enable **"PRUNE RESOURCES"**
   c. Click **"SAVE"**

**13. Test Automated Pruning:**
   a. Add a temporary resource to your Git repository:
      ```bash
      # Create a temporary ConfigMap
      cat > temp-config.yaml << EOF
      apiVersion: v1
      kind: ConfigMap
      metadata:
        name: temp-config
        labels:
          app: sync-demo
      data:
        temp: "This will be removed to test pruning"
      EOF
      ```
   b. Commit and push:
      ```bash
      git add temp-config.yaml
      git commit -m "Add temporary resource for pruning test"
      git push origin main
      ```
   c. Wait for auto-sync to deploy the new resource:
      ```bash
      kubectl get configmap -n sync-demo-app
      ```
   d. You should see both `sync-demo-config` and `temp-config`
   e. Now remove the temporary resource from Git:
      ```bash
      git rm temp-config.yaml
      git commit -m "Remove temporary resource - test pruning"
      git push origin main
      ```
   f. Wait for auto-sync and check:
      ```bash
      kubectl get configmap -n sync-demo-app
      ```
   g. The `temp-config` ConfigMap should be automatically removed (pruned)!

### Phase 5: Sync Options and Advanced Configuration

**14. Configure Sync Options:**
   a. Edit your application in ArgoCD UI one more time
   b. Look for **"SYNC OPTIONS"** (may be in an advanced section)
   c. Enable these options if available:
      - **"REPLACE RESOURCE"** (for force updates)
      - **"RETRY"** (for automatic retry on failure)
   d. Click **"SAVE"**

**15. Test Complete Automation Workflow:**
   a. Make multiple changes simultaneously:
      ```bash
      # Update multiple values
      sed -i 's/replicas: 3/replicas: 4/g' deployment.yaml
      sed -i 's/development/production/g' configmap.yaml
      sed -i 's/MANUAL/AUTO/g' deployment.yaml
      ```
   b. Commit and push all changes:
      ```bash
      git add .
      git commit -m "Multi-change update: scale to 4 replicas, switch to production mode"
      git push origin main
      ```
   c. Watch the ArgoCD UI for automatic synchronization
   d. Verify all changes were applied:
      ```bash
      kubectl get pods -n sync-demo-app
      kubectl describe configmap sync-demo-config -n sync-demo-app
      ```

### Phase 6: Understanding Sync Policy Trade-offs

**16. Compare Manual vs Auto Sync:**
   a. Temporarily disable auto-sync to compare:
      - Edit application → SYNC POLICY → Turn off **"AUTOMATED"**
      - Make a change and observe it requires manual sync
   b. Re-enable auto-sync:
      - Edit application → SYNC POLICY → Turn on **"AUTOMATED"**

**17. Access Your Application:**
   a. Get your Minikube IP:
      ```bash
      minikube ip
      ```
   b. Open browser to: `http://<MINIKUBE_IP>:30095`
   c. You should see the nginx welcome page

---

## ✅ Validation Checklist

- [ ] Created Git repository with sync demo application files
- [ ] Successfully deployed application with manual sync policy
- [ ] Tested manual sync behavior (changes require manual sync button)
- [ ] Enabled auto-sync policy via ArgoCD UI
- [ ] Verified auto-sync automatically deploys Git changes
- [ ] Enabled self-healing and tested configuration drift scenarios
- [ ] Confirmed self-healing reverts manual kubectl changes
- [ ] Enabled automated pruning and tested resource removal
- [ ] Verified pruning automatically removes resources deleted from Git
- [ ] Configured additional sync options (retry, replace, etc.)
- [ ] Successfully tested complete automation workflow with multiple changes
- [ ] Understand the trade-offs between manual and automated sync policies

---

## 🧹 Cleanup

**1. Delete the Application from ArgoCD:**
   a. In the ArgoCD UI, click on your `sync-policy-demo` application
   b. Click the **"DELETE"** button
   c. Check the option to **"Delete resources"** to remove Kubernetes resources
   d. Confirm the deletion

**2. Delete the Namespace:**
   ```bash
   kubectl delete namespace sync-demo-app
   ```

**3. Clean Up Git Repository (Optional):**
   a. You can keep the repository for future experiments
   b. Or clean up the commits if desired:
      ```bash
      git log --oneline  # Review your commits
      # Keep as learning reference or clean up as needed
      ```

**4. Stop Minikube (If Done):**
   ```bash
   minikube stop
   ```

---

## 🎓 Key Learnings Summary

### **Manual Sync Policy:**
- ✅ **Full control:** Every change must be explicitly approved
- ✅ **Safety:** Prevents unwanted automatic deployments
- ✅ **Review process:** Allows for manual review before deployment
- ❌ **Manual overhead:** Requires human intervention for every change
- ❌ **Slower deployment:** No continuous deployment capability

### **Auto Sync Policy:**
- ✅ **Continuous deployment:** Changes deploy automatically
- ✅ **Faster delivery:** No manual bottlenecks
- ✅ **True GitOps:** Git becomes the single source of truth
- ❌ **Less control:** Changes deploy without manual review
- ❌ **Potential risk:** Bad changes can deploy automatically

### **Self-Healing:**
- ✅ **Drift prevention:** Automatically fixes manual changes
- ✅ **Reliability:** Ensures desired state is maintained
- ✅ **Reduced incidents:** Prevents configuration drift issues
- ❌ **Can be surprising:** May revert legitimate manual fixes
- ❌ **Debugging complexity:** May interfere with troubleshooting

### **Automated Pruning:**
- ✅ **Clean environment:** Removes orphaned resources
- ✅ **GitOps compliance:** Ensures only Git-defined resources exist
- ❌ **Potential data loss:** Can remove resources unexpectedly
- ❌ **Requires careful planning:** Need to consider resource dependencies

### **Best Practices:**
1. **Start with manual sync** for new applications until stable
2. **Use auto-sync with self-healing** for stable production applications
3. **Enable pruning carefully** - test thoroughly first
4. **Monitor sync operations** especially when first enabling automation
5. **Use sync windows** for controlled deployment timing
6. **Have rollback procedures** ready when using automation
7. **Test all policies** in staging before production

---

## 🔧 When to Use Each Policy

**Manual Sync - Use When:**
- Learning ArgoCD and GitOps concepts
- Deploying critical production applications that need review
- Working with applications that have complex dependencies
- Regulatory environments requiring change approval

**Auto Sync - Use When:**
- You have mature CI/CD pipelines with proper testing
- Deploying to development/staging environments
- Applications are stable and well-tested
- You want true continuous deployment

**Self-Healing - Use When:**
- You need to prevent configuration drift
- Operating in environments where manual changes are common
- Running production workloads that must maintain desired state
- You have good monitoring and alerting in place

**Automated Pruning - Use When:**
- You want to ensure clean environments
- Resources are managed entirely through Git
- You have backup/recovery procedures for any critical data
- Operating in ephemeral or test environments

---

End of Lab Instructions. Return to the main `README.md` for Key Concepts and Next Steps. 