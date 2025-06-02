# Lab Instructions for LAB06: Secrets Management in GitOps with ArgoCD

This document provides detailed step-by-step instructions for securely managing secrets in GitOps workflows. You'll understand the security challenges, implement Sealed Secrets, and learn best practices for production environments.

We will start by examining the problem of secrets in GitOps, then implement a secure solution using Sealed Secrets.

---

## 🚀 Lab Steps

### Phase 1: Understanding the Secrets Problem in GitOps

**1. Prepare Your Git Repository:**
   a. Use your existing Git repository from previous labs, or create a new public repository named `secrets-gitops-demo`
   b. In your local clone of the repository, create an `app` directory:
      ```bash
      mkdir app
      cd app
      ```

**2. Copy the Demo Application Files:**
   a. Copy all the secrets demo files from the lab materials:
      ```bash
      # Copy deployment file
      cp ../path-to-cicd-labs/ArgoCD/LAB06-Secrets-Integration/secrets-app/deployment.yaml ./deployment.yaml
      
      # Copy service file
      cp ../path-to-cicd-labs/ArgoCD/LAB06-Secrets-Integration/secrets-app/service.yaml ./service.yaml
      
      # Copy the insecure secret example (for demonstration)
      cp ../path-to-cicd-labs/ArgoCD/LAB06-Secrets-Integration/secrets-app/regular-secret.yaml ./regular-secret.yaml
      ```
   b. Review the files - the deployment demonstrates different ways secrets can be used in applications
   c. **Important**: Do NOT commit the regular-secret.yaml yet - we'll use it to understand the security problem first

**3. Examine the Security Problem:**
   a. Open `regular-secret.yaml` and examine its contents
   b. Notice the base64 encoded values in the `data` section
   c. Decode one of the secrets to see the problem:
      ```bash
      echo "cGFzc3dvcmQxMjM=" | base64 -d
      ```
   d. You should see "password123" - this demonstrates that base64 is NOT encryption!
   e. **This is why we cannot store regular Kubernetes secrets in Git repositories**

**4. Create Kubernetes Namespace:**
   ```bash
   kubectl create namespace secrets-demo-app
   ```

### Phase 2: Install and Configure Sealed Secrets

**5. Install Sealed Secrets Controller:**
   a. Install the Sealed Secrets controller in your cluster:
      ```bash
      kubectl apply -f https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.24.0/controller.yaml
      ```
   b. Wait for the controller to be ready:
      ```bash
      kubectl get pods -n kube-system | grep sealed-secrets-controller
      ```
   c. The pod should be in `Running` state

**6. Install kubeseal CLI Tool:**
   a. For Linux/macOS:
      ```bash
      # Download kubeseal CLI
      KUBESEAL_VERSION='0.24.0'
      curl -OL "https://github.com/bitnami-labs/sealed-secrets/releases/download/v${KUBESEAL_VERSION}/kubeseal-${KUBESEAL_VERSION}-linux-amd64.tar.gz"
      tar -xvzf kubeseal-${KUBESEAL_VERSION}-linux-amd64.tar.gz kubeseal
      sudo install -m 755 kubeseal /usr/local/bin/kubeseal
      ```
   b. For Windows (using PowerShell):
      ```powershell
      # Download and extract kubeseal for Windows
      $version = "0.24.0"
      Invoke-WebRequest -Uri "https://github.com/bitnami-labs/sealed-secrets/releases/download/v$version/kubeseal-$version-windows-amd64.tar.gz" -OutFile "kubeseal.tar.gz"
      # Extract and move to PATH (you may need to do this manually)
      ```
   c. Verify installation:
      ```bash
      kubeseal --version
      ```

**7. Test Sealed Secrets Setup:**
   a. Create a test secret locally (do not apply to cluster):
      ```bash
      kubectl create secret generic test-secret \
        --from-literal=username=testuser \
        --from-literal=password=testpass \
        --dry-run=client -o yaml > test-secret.yaml
      ```
   b. Seal the secret:
      ```bash
      kubeseal --format=yaml --controller-namespace=kube-system < test-secret.yaml > test-sealed-secret.yaml
      ```
   c. Examine the sealed secret:
      ```bash
      cat test-sealed-secret.yaml
      ```
   d. Notice the `encryptedData` section with encrypted values
   e. Clean up test files:
      ```bash
      rm test-secret.yaml test-sealed-secret.yaml
      ```

### Phase 3: Create and Deploy Sealed Secrets

**8. Create Application Secrets Using kubeseal:**
   a. Create the first secret (for database credentials):
      ```bash
      kubectl create secret generic database-credentials \
        --from-literal=password=production-db-password-2024 \
        --from-literal=api-key=prod-api-key-abc123xyz \
        --namespace=secrets-demo-app \
        --dry-run=client -o yaml > temp-db-secret.yaml
      ```
   b. Seal the database secret:
      ```bash
      kubeseal --format=yaml --controller-namespace=kube-system < temp-db-secret.yaml > database-sealed-secret.yaml
      ```
   c. Create the second secret (for application secrets):
      ```bash
      kubectl create secret generic app-secrets \
        --from-literal=secret-token=jwt-secret-token-2024-secure \
        --from-literal=encryption-key=aes256-encryption-key-super-secure \
        --namespace=secrets-demo-app \
        --dry-run=client -o yaml > temp-app-secret.yaml
      ```
   d. Seal the application secret:
      ```bash
      kubeseal --format=yaml --controller-namespace=kube-system < temp-app-secret.yaml > app-sealed-secret.yaml
      ```
   e. Clean up temporary files:
      ```bash
      rm temp-db-secret.yaml temp-app-secret.yaml
      ```

**9. Commit Sealed Secrets to Git:**
   a. Add the sealed secrets and application files to Git:
      ```bash
      git add deployment.yaml service.yaml database-sealed-secret.yaml app-sealed-secret.yaml
      git commit -m "Add secrets demo app with sealed secrets"
      git push origin main
      ```
   b. **Important**: Notice we did NOT commit the regular-secret.yaml file
   c. The sealed secrets are now safely stored in Git with encryption

### Phase 4: Deploy with ArgoCD

**10. Create ArgoCD Application:**
   a. Open the ArgoCD UI in your browser
   b. Click **"+ NEW APP"**
   c. Fill in the application details:
      - **Application Name:** `secrets-demo`
      - **Project Name:** `default`
      - **SYNC POLICY:** `Manual` (we'll sync manually to observe the process)
      - **SOURCE Repository URL:** Your Git repository URL
      - **SOURCE Revision:** `HEAD`
      - **SOURCE Path:** `app`
      - **DESTINATION Cluster URL:** `https://kubernetes.default.svc`
      - **DESTINATION Namespace:** `secrets-demo-app`
   d. Click **"CREATE"**

**11. Synchronize and Observe Sealed Secrets:**
   a. Click **"SYNC"** and **"SYNCHRONIZE"**
   b. Watch the synchronization process in ArgoCD UI
   c. Check what resources were created:
      ```bash
      kubectl get all -n secrets-demo-app
      kubectl get sealedsecrets -n secrets-demo-app
      kubectl get secrets -n secrets-demo-app
      ```
   d. You should see:
      - SealedSecret resources (encrypted)
      - Regular Secret resources (automatically created by the controller)
      - Deployment and Service resources

**12. Verify Secret Decryption:**
   a. Check that the Sealed Secrets controller decrypted the secrets:
      ```bash
      kubectl get secret database-credentials -n secrets-demo-app -o yaml
      kubectl get secret app-secrets -n secrets-demo-app -o yaml
      ```
   b. The secrets should exist with base64 encoded data
   c. Verify the application can access the secrets:
      ```bash
      kubectl describe pod -l app=secrets-demo -n secrets-demo-app
      ```
   d. Look for the environment variables being set from secrets

**13. Test Application Access:**
   a. Get your Minikube IP:
      ```bash
      minikube ip
      ```
   b. Access the application:
      ```bash
      curl http://<MINIKUBE_IP>:30100
      ```
   c. The nginx welcome page should load (indicating the application started successfully with secrets)

### Phase 5: Secrets Management Best Practices

**14. Test Secret Updates:**
   a. Create a new version of one of the secrets:
      ```bash
      kubectl create secret generic app-secrets \
        --from-literal=secret-token=jwt-secret-token-2024-updated \
        --from-literal=encryption-key=aes256-encryption-key-updated-v2 \
        --namespace=secrets-demo-app \
        --dry-run=client -o yaml > temp-updated-secret.yaml
      ```
   b. Seal the updated secret:
      ```bash
      kubeseal --format=yaml --controller-namespace=kube-system < temp-updated-secret.yaml > app-sealed-secret-updated.yaml
      ```
   c. Replace the old sealed secret:
      ```bash
      mv app-sealed-secret-updated.yaml app-sealed-secret.yaml
      rm temp-updated-secret.yaml
      ```
   d. Commit and push the updated secret:
      ```bash
      git add app-sealed-secret.yaml
      git commit -m "Update app secrets with new values"
      git push origin main
      ```
   e. Sync in ArgoCD and verify the secret was updated

**15. Verify Secret File Mounting:**
   a. Check that secrets are also mounted as files:
      ```bash
      kubectl exec -it deployment/secrets-demo-app -n secrets-demo-app -- ls -la /etc/secrets/
      ```
   b. You should see the secret files mounted
   c. View the content of a secret file:
      ```bash
      kubectl exec -it deployment/secrets-demo-app -n secrets-demo-app -- cat /etc/secrets/secret-token
      ```

**16. Understand Sealed Secrets Security:**
   a. Try to decrypt a sealed secret without the controller:
      ```bash
      # This will fail - demonstrating the security
      echo "AgBy3i4OJSWK..." | base64 -d  # (use actual encrypted data from your sealed secret)
      ```
   b. Only the controller in the cluster can decrypt sealed secrets
   c. Even if someone gets access to your Git repository, they cannot decrypt the secrets

### Phase 6: Alternative Approaches and Production Considerations

**17. Explore Production Alternatives:**
   a. Research External Secrets Operator (brief overview):
      - Integrates with external secret stores (Vault, AWS Secrets Manager, Azure Key Vault)
      - Secrets never stored in Git at all
      - More complex setup but more enterprise-ready
   
   b. Consider other approaches:
      - Helm with encrypted values (helm-secrets plugin)
      - GitOps-specific tools (SOPS, age encryption)
      - Cloud-native secret managers

**18. Security Best Practices Review:**
   a. **Do's:**
      - Use Sealed Secrets or external secret operators
      - Rotate secrets regularly
      - Limit access to sealing keys
      - Monitor secret access
      - Use namespace-scoped secrets when possible
   
   b. **Don'ts:**
      - Never commit plain-text secrets to Git
      - Don't use base64 encoding as security
      - Avoid storing secrets in ConfigMaps
      - Don't share sealing keys unnecessarily

---

## ✅ Validation Checklist

- [ ] Successfully installed Sealed Secrets controller
- [ ] Installed and verified kubeseal CLI tool
- [ ] Created and sealed multiple secrets using kubeseal
- [ ] Committed sealed secrets to Git repository (encrypted)
- [ ] Created ArgoCD application for secrets demo
- [ ] Successfully deployed application with sealed secrets
- [ ] Verified that Sealed Secrets controller decrypted secrets automatically
- [ ] Confirmed application can access secrets via environment variables
- [ ] Verified secrets are mounted as files in containers
- [ ] Tested secret updates through GitOps workflow
- [ ] Understand the security model of Sealed Secrets
- [ ] Learned about alternative approaches for production environments

---

## 🧹 Cleanup

**1. Delete the Application from ArgoCD:**
   a. In the ArgoCD UI, click on your `secrets-demo` application
   b. Click the **"DELETE"** button
   c. Check the option to **"Delete resources"** to remove Kubernetes resources
   d. Confirm the deletion

**2. Delete the Namespace:**
   ```bash
   kubectl delete namespace secrets-demo-app
   ```

**3. Remove Sealed Secrets Controller (Optional):**
   ```bash
   kubectl delete -f https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.24.0/controller.yaml
   ```

**4. Clean Up Git Repository (Optional):**
   a. You can keep the repository for future experiments
   b. Or clean up the sealed secrets if desired:
      ```bash
      git rm database-sealed-secret.yaml app-sealed-secret.yaml
      git commit -m "Clean up sealed secrets demo"
      git push origin main
      ```

**5. Stop Minikube (If Done):**
   ```bash
   minikube stop
   ```

---

## 🎓 Key Learnings Summary

### **The Secrets Problem in GitOps:**
- ❌ **Plain-text secrets**: Never store in Git repositories
- ❌ **Base64 encoding**: Is NOT encryption, anyone can decode
- ❌ **ConfigMaps for secrets**: Not designed for sensitive data
- ✅ **Encryption required**: Must encrypt before storing in Git

### **Sealed Secrets Solution:**
- ✅ **Encryption at rest**: Secrets encrypted before Git storage
- ✅ **Controller-based decryption**: Only cluster controller can decrypt
- ✅ **GitOps compatible**: Encrypted secrets can be safely stored in Git
- ✅ **Kubernetes native**: Works with standard Kubernetes Secret resources
- ❌ **Single point of failure**: Controller holds the decryption key
- ❌ **Cluster coupling**: Sealed secrets tied to specific cluster

### **Production Considerations:**
- **Key rotation**: Regular rotation of sealing keys for enhanced security
- **Backup/Recovery**: Plan for sealing key backup and recovery procedures
- **Multi-cluster**: Consider challenges when managing multiple clusters
- **External integrations**: May need external secret stores for complex scenarios

### **Alternative Approaches:**
1. **External Secrets Operator**: Integrates with external secret stores
2. **SOPS**: Mozilla's solution for encrypting files with Git
3. **Helm Secrets**: Helm plugin for encrypted values files
4. **Cloud-native**: Use cloud provider secret management services

### **Best Practices:**
1. **Never commit plain-text secrets** to any repository
2. **Use encryption** for any secrets stored in Git
3. **Rotate secrets regularly** following security policies
4. **Monitor secret access** and usage patterns
5. **Limit sealing key access** to essential personnel only
6. **Test secret recovery procedures** before production incidents
7. **Consider external secret stores** for enterprise environments

---

## 🔐 Security Model Deep Dive

### **How Sealed Secrets Work:**
1. **Public-Key Cryptography**: Uses asymmetric encryption
2. **Cluster-Specific Keys**: Each cluster has its own key pair
3. **Controller Decryption**: Only the controller can decrypt sealed secrets
4. **Automatic Secret Creation**: Controller creates Kubernetes secrets automatically

### **Security Guarantees:**
- ✅ **Git Safety**: Encrypted secrets safe to store in Git
- ✅ **Access Control**: Secrets only accessible within the target cluster
- ✅ **Namespace Isolation**: Can scope secrets to specific namespaces
- ✅ **Audit Trail**: Git provides complete change history

### **Security Limitations:**
- ❌ **Key Compromise**: If sealing key is compromised, all secrets are at risk
- ❌ **Cluster Access**: Anyone with cluster access can read decrypted secrets
- ❌ **Controller Dependency**: Controller failure affects secret decryption

---

End of Lab Instructions. Return to the main `README.md` for Key Concepts and Next Steps. 