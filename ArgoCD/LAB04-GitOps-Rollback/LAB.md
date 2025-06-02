# Lab Instructions for LAB04: GitOps Rollback Strategies with Argo CD

This document provides detailed step-by-step instructions for learning and practicing GitOps rollback strategies using ArgoCD. You'll deploy multiple versions of an application, encounter issues, and learn different rollback approaches.

We will simulate a real-world scenario where a deployment goes wrong and needs to be rolled back safely using GitOps principles.

---

## 🚀 Lab Steps

### Phase 1: Setup the Rollback Demo Application

**1. Prepare Your Git Repository:**
   a. Use your existing Git repository from previous labs, or create a new public repository named `rollback-demo`
   b. In your local clone of the repository, create an `app` directory:
      ```bash
      mkdir app
      cd app
      ```

**2. Deploy Version 1 (Stable Release):**
   a. Copy the v1 deployment file from the lab materials:
      ```bash
      # Copy from the lab materials directory
      cp ../path-to-cicd-labs/ArgoCD/LAB04-GitOps-Rollback/app-versions/v1-deployment.yaml ./deployment.yaml
      ```
   b. Review the v1 deployment file - it's a stable nginx deployment with 2 replicas
   c. Commit and push this initial version:
      ```bash
      git add deployment.yaml
      git commit -m "Deploy v1.0.0 - Initial stable release"
      git push origin main
      ```

**3. Create Kubernetes Namespace:**
   ```bash
   kubectl create namespace rollback-demo-app
   ```

**4. Create the ArgoCD Application:**
   a. Open the ArgoCD UI in your browser
   b. Click **"+ NEW APP"**
   c. Fill in the application details:
      - **Application Name:** `rollback-demo`
      - **Project Name:** `default`
      - **SYNC POLICY:** `Manual`
      - **SOURCE Repository URL:** Your Git repository URL
      - **SOURCE Revision:** `HEAD`
      - **SOURCE Path:** `app`
      - **DESTINATION Cluster URL:** `https://kubernetes.default.svc`
      - **DESTINATION Namespace:** `rollback-demo-app`
   d. Click **"CREATE"**

**5. Synchronize Version 1:**
   a. Click on your `rollback-demo` application in ArgoCD
   b. Click **"SYNC"** and then **"SYNCHRONIZE"**
   c. Wait for the application to become `Healthy` and `Synced`
   d. Verify the deployment:
      ```bash
      kubectl get pods -n rollback-demo-app
      kubectl get svc -n rollback-demo-app
      ```
   e. You should see 2 nginx pods running

**6. Access Version 1:**
   a. Get your Minikube IP:
      ```bash
      minikube ip
      ```
   b. Open your browser and navigate to: `http://<MINIKUBE_IP>:30090`
   c. You should see the nginx welcome page (this represents v1.0.0)

### Phase 2: Deploy a Problematic Version (Version 2)

**7. Update to Version 2 (Problematic Version):**
   a. Copy the v2 deployment file:
      ```bash
      cp ../path-to-cicd-labs/ArgoCD/LAB04-GitOps-Rollback/app-versions/v2-deployment.yaml ./deployment.yaml
      ```
   b. Review the changes in v2:
      - Uses excessive resource requests (2Gi memory, 1 CPU per pod)
      - Increased replicas to 5 (requiring 10Gi total memory)
      - This will likely cause scheduling issues on Minikube
   c. Commit and push this problematic version:
      ```bash
      git add deployment.yaml
      git commit -m "Deploy v2.0.0 - New features with performance improvements"
      git push origin main
      ```

**8. Synchronize Version 2:**
   a. Go back to ArgoCD UI - your application should show `OutOfSync`
   b. Click **"SYNC"** and **"SYNCHRONIZE"**
   c. Watch the deployment process
   d. Notice that some pods might remain in `Pending` state due to resource constraints

**9. Observe the Problem:**
   a. Check the pod status:
      ```bash
      kubectl get pods -n rollback-demo-app
      ```
   b. You should see some pods in `Pending` state due to insufficient cluster resources
   c. Describe a pending pod to see the scheduling error:
      ```bash
      kubectl describe pod <POD_NAME> -n rollback-demo-app
      ```
   d. Look for events showing `Insufficient memory` or `Insufficient cpu`
   e. Your application is having performance issues and needs to be rolled back!

### Phase 3: ArgoCD UI Rollback

**10. View Application History:**
   a. In the ArgoCD UI, click on your `rollback-demo` application
   b. Click on the **"HISTORY AND ROLLBACK"** tab (or **"History"** button)
   c. You should see at least 2 revisions:
      - Revision 1: Your initial v1.0.0 deployment
      - Revision 2: Your current broken v2.0.0 deployment
   d. Note the Git commit IDs and sync timestamps

**11. Perform UI-Based Rollback:**
   a. In the History view, find Revision 1 (the working version)
   b. Click the **"ROLLBACK"** button next to Revision 1
   c. Confirm the rollback operation
   d. ArgoCD will automatically sync back to the previous working state
   e. Wait for the application to become `Healthy` and `Synced` again

**12. Verify the Rollback:**
   a. Check that the pods are running correctly:
      ```bash
      kubectl get pods -n rollback-demo-app
      ```
   b. You should see 2 pods (back to v1 configuration) and they should be `Running`
   c. Access the application again via browser to confirm it's working
   d. Check the ArgoCD UI - it should show `Synced` and `Healthy`

### Phase 4: Git-Based Rollback Approach

**13. Deploy Version 3 (Fixed Version):**
   a. Copy the v3 deployment file:
      ```bash
      cp ../path-to-cicd-labs/ArgoCD/LAB04-GitOps-Rollback/app-versions/v3-deployment.yaml ./deployment.yaml
      ```
   b. Review v3 improvements:
      - Uses a stable nginx image (`nginx:1.22`)
      - 3 replicas (balanced)
      - Added health checks
   c. Commit and push version 3:
      ```bash
      git add deployment.yaml
      git commit -m "Deploy v3.0.0 - Fixed issues and added health checks"
      git push origin main
      ```

**14. Sync Version 3:**
   a. In ArgoCD UI, sync the new version
   b. Verify the deployment is healthy with 3 replicas
   c. Check that the health checks are working:
      ```bash
      kubectl describe deployment rollback-demo-app -n rollback-demo-app
      ```

**15. Simulate Another Problem (Git Rollback Method):**
   a. Let's say v3.0.0 has a critical issue that wasn't caught immediately
   b. Instead of using ArgoCD rollback, we'll use Git to revert
   c. Use Git to revert to the previous commit:
      ```bash
      git log --oneline  # See your commit history
      git revert HEAD    # This creates a new commit that undoes the last commit
      ```
   d. Edit the revert commit message to be descriptive:
      ```
      Revert "Deploy v3.0.0 - Fixed issues and added health checks"
      
      This reverts commit <commit-hash> due to critical issues discovered in production.
      Rolling back to v2.0.0 while we investigate the problems.
      ```
   e. Push the revert commit:
      ```bash
      git push origin main
      ```

**16. Observe Git-Based Rollback:**
   a. In ArgoCD UI, your application should show `OutOfSync` 
   b. Click **"SYNC"** and **"SYNCHRONIZE"**
   c. ArgoCD will now deploy the reverted state
   d. However, you'll notice we're back to the broken v2 (this is intentional to show the difference)

**17. Fix with Proper Git Rollback:**
   a. Since v2 was also broken, let's revert to v1 properly:
      ```bash
      git revert HEAD    # Revert the revert (which gets us back to v3)
      git revert HEAD~2  # Revert the v2 commit
      ```
   b. Or alternatively, use Git reset to go back to v1:
      ```bash
      git log --oneline  # Find the v1 commit hash
      git reset --hard <v1-commit-hash>
      git push --force-with-lease origin main
      ```
   c. Sync in ArgoCD to get back to the stable v1 state

### Phase 5: ArgoCD CLI Rollback (Optional)

**18. Install ArgoCD CLI (If Not Already Installed):**
   a. Download ArgoCD CLI for your OS from: https://argo-cd.readthedocs.io/en/stable/cli_installation/
   b. For Linux/macOS:
      ```bash
      curl -sSL -o argocd-linux-amd64 https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
      sudo install -m 555 argocd-linux-amd64 /usr/local/bin/argocd
      ```

**19. Login to ArgoCD CLI:**
   a. Get your ArgoCD admin password:
      ```bash
      kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
      ```
   b. Login via CLI:
      ```bash
      argocd login <ARGOCD_SERVER_IP>:30080 --username admin --password <PASSWORD> --insecure
      ```

**20. CLI-Based Rollback:**
   a. View application history:
      ```bash
      argocd app history rollback-demo
      ```
   b. Rollback to a specific revision:
      ```bash
      argocd app rollback rollback-demo <REVISION_NUMBER>
      ```
   c. Verify the rollback:
      ```bash
      argocd app get rollback-demo
      ```

---

## ✅ Validation Checklist

- [ ] Created Git repository with `app` directory
- [ ] Successfully deployed v1.0.0 (stable version) with 2 replicas
- [ ] Created ArgoCD application pointing to your Git repository 
- [ ] Successfully accessed working application via browser
- [ ] Deployed v2.0.0 (broken version) and observed ImagePullError
- [ ] Used ArgoCD UI to view application history and revisions
- [ ] Performed successful rollback via ArgoCD UI from v2 to v1
- [ ] Verified application is working after UI rollback
- [ ] Deployed v3.0.0 (fixed version) with health checks
- [ ] Performed Git-based rollback using `git revert` command
- [ ] Observed ArgoCD detecting Git changes and syncing automatically
- [ ] (Optional) Installed ArgoCD CLI and performed CLI-based rollback
- [ ] Understand the difference between ArgoCD rollbacks and Git reverts

---

## 🧹 Cleanup

**1. Delete the Application from ArgoCD:**
   a. In the ArgoCD UI, click on your `rollback-demo` application
   b. Click the **"DELETE"** button
   c. Check the option to **"Delete resources"** to remove Kubernetes resources
   d. Confirm the deletion

**2. Delete the Namespace:**
   ```bash
   kubectl delete namespace rollback-demo-app
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

**ArgoCD UI Rollback:**
- ✅ Fast and visual
- ✅ Shows clear revision history
- ✅ Good for quick recovery
- ❌ Doesn't change Git state (can lead to confusion)

**Git-Based Rollback:**
- ✅ Maintains audit trail in Git
- ✅ True GitOps approach
- ✅ Team can see what happened
- ❌ Requires Git knowledge
- ❌ Takes longer than UI rollback

**Best Practices:**
1. Always test deployments in staging first
2. Use Git-based rollbacks for transparency
3. ArgoCD UI rollbacks are good for emergencies
4. Monitor applications after rollbacks
5. Learn from incidents and improve processes

---

End of Lab Instructions. Return to the main `README.md` for Key Concepts and Next Steps. 