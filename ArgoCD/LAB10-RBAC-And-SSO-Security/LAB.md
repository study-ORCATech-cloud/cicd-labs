# Lab Instructions for LAB10: ArgoCD Security - RBAC and Single Sign-On Integration

This document provides detailed step-by-step instructions for implementing comprehensive security in ArgoCD including role-based access control (RBAC), single sign-on (SSO) integration, project-level security, and enterprise-grade security policies.

We will start by setting up basic RBAC, then configure multiple SSO providers, create secure projects, and implement advanced security features for production environments.

---

## 🚀 Lab Steps

### Phase 1: Copy Lab Materials and Prepare Security Configuration Structure

**1. Create Directory Structure:**
   ```bash
   mkdir -p rbac-configs sso-configs security-configs projects test-scenarios scripts
   ```

**2. Backup Current ArgoCD Configuration:**
   ```bash
   # Backup existing configuration
   kubectl get configmap argocd-cm -n argocd -o yaml > backup-argocd-cm.yaml
   kubectl get configmap argocd-rbac-cm -n argocd -o yaml > backup-argocd-rbac-cm.yaml 2>/dev/null || echo "No existing RBAC config"
   ```

**3. Get Current ArgoCD Admin Password:**
   ```bash
   # Save admin password for fallback
   ADMIN_PASSWORD=$(kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d)
   echo "Admin password: $ADMIN_PASSWORD"
   echo "Save this password for emergency access!"
   ```

### Phase 2: Copy and Implement Basic RBAC Configuration

**4. Copy Basic RBAC Policy:**
   ```bash
   cp rbac-configs/basic-rbac.yaml ./
   ```

**5. Review Basic RBAC Configuration:**
   ```bash
   cat rbac-configs/basic-rbac.yaml
   ```

**6. Apply Basic RBAC Configuration:**
   ```bash
   kubectl apply -f rbac-configs/basic-rbac.yaml
   ```

**7. Verify RBAC Configuration:**
   ```bash
   # Check RBAC configuration
   kubectl get configmap argocd-rbac-cm -n argocd -o yaml
   
   # Check ArgoCD server logs for RBAC loading
   kubectl logs -n argocd deployment/argocd-server | grep -i rbac
   ```

### Phase 3: Copy and Configure GitHub SSO Integration

**8. Create GitHub OAuth Application:**
   a. Go to GitHub → Settings → Developer settings → OAuth Apps
   b. Click "New OAuth App"
   c. Fill in the details:
      - Application name: `ArgoCD Lab10`
      - Homepage URL: `http://localhost:8080` (or your ArgoCD URL)
      - Authorization callback URL: `http://localhost:8080/api/dex/callback`
   d. Save the Client ID and Client Secret

**9. Copy GitHub SSO Configuration:**
   ```bash
   cp sso-configs/github-sso.yaml ./
   ```

**10. Review GitHub SSO Configuration:**
   ```bash
   cat sso-configs/github-sso.yaml
   ```

**11. Update GitHub Configuration with Your Credentials:**
   ```bash
   # Replace with your actual GitHub OAuth credentials
   GITHUB_CLIENT_ID="your-github-client-id"
   GITHUB_CLIENT_SECRET="your-github-client-secret"
   GITHUB_ORG="your-github-org"
   
   sed -i "s/YOUR_GITHUB_CLIENT_ID/$GITHUB_CLIENT_ID/g" sso-configs/github-sso.yaml
   sed -i "s/YOUR_GITHUB_CLIENT_SECRET/$GITHUB_CLIENT_SECRET/g" sso-configs/github-sso.yaml
   sed -i "s/YOUR_GITHUB_ORG/$GITHUB_ORG/g" sso-configs/github-sso.yaml
   ```

**12. Apply GitHub SSO Configuration:**
   ```bash
   kubectl apply -f sso-configs/github-sso.yaml
   
   # Restart ArgoCD server to pick up new configuration
   kubectl rollout restart deployment/argocd-server -n argocd
   kubectl rollout restart deployment/argocd-dex-server -n argocd
   ```

### Phase 4: Copy and Configure Advanced RBAC with Custom Roles

**13. Copy Advanced RBAC Configuration:**
   ```bash
   cp rbac-configs/advanced-rbac.yaml ./
   ```

**14. Review Advanced RBAC Configuration:**
   ```bash
   cat rbac-configs/advanced-rbac.yaml
   ```

**15. Update Advanced RBAC with Your GitHub Organization:**
   ```bash
   sed -i "s/YOUR_GITHUB_ORG/$GITHUB_ORG/g" rbac-configs/advanced-rbac.yaml
   ```

### Phase 5: Copy and Create ArgoCD Projects for Multi-Tenancy

**16. Copy Development Project:**
   ```bash
   cp projects/dev-project.yaml ./
   ```

**17. Review Development Project:**
   ```bash
   cat projects/dev-project.yaml
   ```

**18. Copy Staging Project:**
   ```bash
   cp projects/staging-project.yaml ./
   ```

**19. Review Staging Project:**
   ```bash
   cat projects/staging-project.yaml
   ```

**20. Copy Production Project:**
   ```bash
   cp projects/production-project.yaml ./
   ```

**21. Review Production Project:**
   ```bash
   cat projects/production-project.yaml
   ```

**22. Update Projects with GitHub Organization:**
   ```bash
   sed -i "s/YOUR_GITHUB_ORG/$GITHUB_ORG/g" projects/*.yaml
   ```

**23. Apply Project Configurations:**
   ```bash
   kubectl apply -f projects/dev-project.yaml
   kubectl apply -f projects/staging-project.yaml
   kubectl apply -f projects/production-project.yaml
   ```

### Phase 6: Copy and Configure Additional SSO Providers

**24. Copy Google SSO Configuration (Optional):**
   ```bash
   cp sso-configs/google-sso.yaml ./
   ```

**25. Copy Local Users Configuration:**
   ```bash
   cp sso-configs/local-users.yaml ./
   ```

**26. Review Additional SSO Configurations:**
   ```bash
   cat sso-configs/google-sso.yaml
   cat sso-configs/local-users.yaml
   ```

### Phase 7: Copy and Configure Security Policies and Audit Logging

**27. Copy Security Policies Configuration:**
   ```bash
   cp security-configs/security-policies.yaml ./
   ```

**28. Review Security Policies:**
   ```bash
   cat security-configs/security-policies.yaml
   ```

**29. Copy Audit Logging Configuration:**
   ```bash
   cp security-configs/audit-logging.yaml ./
   ```

**30. Review Audit Logging Configuration:**
   ```bash
   cat security-configs/audit-logging.yaml
   ```

### Phase 8: Copy and Create Test Applications for Access Validation

**31. Copy Test Applications:**
   ```bash
   cp test-scenarios/test-applications.yaml ./
   ```

**32. Review Test Applications:**
   ```bash
   cat test-scenarios/test-applications.yaml
   ```

**33. Apply Test Applications:**
   ```bash
   kubectl apply -f test-scenarios/test-applications.yaml
   ```

### Phase 9: Apply Advanced Security Configuration

**34. Apply Advanced RBAC Configuration:**
   ```bash
   kubectl apply -f rbac-configs/advanced-rbac.yaml
   
   # Restart ArgoCD components to pick up RBAC changes
   kubectl rollout restart deployment/argocd-server -n argocd
   kubectl rollout restart deployment/argocd-application-controller -n argocd
   ```

**35. Use Setup Script (Optional):**
   ```bash
   cp scripts/setup-security.sh ./
   chmod +x scripts/setup-security.sh
   
   # Set admin password for scripts
   export ARGOCD_ADMIN_PASSWORD=$(kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d)
   
   # Run security setup
   ./scripts/setup-security.sh
   ```

### Phase 10: Testing and Validation

**36. Test ArgoCD UI Access:**
   a. Port forward ArgoCD server:
      ```bash
      kubectl port-forward svc/argocd-server -n argocd 8080:443 &
      ```
   b. Open browser to `http://localhost:8080`
   c. You should see SSO login options (GitHub) alongside local login

**37. Test SSO Login:**
   a. Click "Login via GitHub"
   b. Complete OAuth flow
   c. Verify you're logged in with appropriate permissions based on GitHub org/team membership

**38. Use RBAC Testing Script:**
   ```bash
   cp scripts/test-rbac.sh ./
   chmod +x scripts/test-rbac.sh
   ./scripts/test-rbac.sh
   ```

**39. Test Project-Level Access:**
   a. Log in as different users (if configured)
   b. Verify project-specific access controls
   c. Test application creation in different projects

**40. Validate Security Policies:**
   ```bash
   # Check audit logs
   kubectl logs -n argocd deployment/argocd-server | grep -i audit
   
   # Check session timeout settings
   kubectl get configmap argocd-cm-security -n argocd -o yaml
   
   # Verify RBAC enforcement
   kubectl get configmap argocd-rbac-cm -n argocd -o yaml
   ```

**41. Test Emergency Admin Access:**
   ```bash
   # Ensure admin access still works for emergency
   argocd login localhost:8080 --username admin --password $ARGOCD_ADMIN_PASSWORD --insecure
   argocd app list
   ```

**42. Advanced Security Testing:**
   a. Test API access with different authentication methods:
      ```bash
      # Test with bearer token
      ARGOCD_TOKEN=$(argocd account generate-token --account admin)
      curl -H "Authorization: Bearer $ARGOCD_TOKEN" http://localhost:8080/api/v1/applications
      ```
   b. Test unauthorized access attempts
   c. Verify session timeouts work correctly
   d. Test password policy enforcement (if using local accounts)

---

## ✅ Validation Checklist

- [ ] Successfully configured basic and advanced RBAC policies
- [ ] Implemented GitHub SSO integration with OAuth application
- [ ] Created multi-tenant projects with environment-specific access controls
- [ ] Applied security policies including session timeouts and audit logging
- [ ] Successfully tested SSO login with GitHub authentication
- [ ] Verified RBAC enforcement with different user roles and permissions
- [ ] Tested project-level access restrictions for development, staging, and production
- [ ] Confirmed team-based access controls work correctly with GitHub org/team mappings
- [ ] Validated security policies are enforced (session timeouts, rate limiting)
- [ ] Successfully tested emergency admin access for fallback authentication
- [ ] Verified audit logging captures user actions and authentication events
- [ ] Tested API access with different authentication methods and permissions
- [ ] Confirmed proper cleanup and restoration of default configuration
- [ ] Validated all security configurations work in a production-like environment

---

## 🧹 Cleanup

**43. Use Cleanup Script:**
   ```bash
   cp scripts/cleanup-security.sh ./
   chmod +x scripts/cleanup-security.sh
   ./scripts/cleanup-security.sh
   ```

**44. Manual Cleanup (Alternative):**
   a. Stop port forwarding:
      ```bash
      pkill -f "port-forward"
      ```
   b. Remove any remaining security configurations:
      ```bash
      kubectl delete configmap -n argocd -l "app.kubernetes.io/part-of=argocd-security"
      ```

**45. Verify Default State:**
   ```bash
   # Check that default configuration is restored
   kubectl get configmap argocd-cm -n argocd -o yaml
   kubectl get configmap argocd-rbac-cm -n argocd 2>/dev/null || echo "RBAC config removed"
   ```

**46. Reset GitHub OAuth Application:**
   a. Go to GitHub → Settings → Developer settings → OAuth Apps
   b. Delete or disable the OAuth application created for this lab

**47. Clean Up Local Files:**
   ```bash
   rm -rf backup-*.yaml
   ```

---

## 🎯 Key Learning Outcomes

By completing this lab, you have learned:

1. **ArgoCD Security Architecture**: Understanding RBAC, SSO, and multi-tenant security patterns
2. **RBAC Implementation**: Creating granular permission policies with custom roles and team mappings
3. **SSO Integration**: Configuring external authentication providers with OAuth and OIDC
4. **Project-Level Security**: Implementing multi-tenant isolation with environment-specific controls
5. **Security Policies**: Enforcing session timeouts, audit logging, and enterprise security standards
6. **Production Readiness**: Implementing security controls suitable for enterprise environments
7. **Compliance Support**: Setting up audit trails and access controls for regulatory requirements

This comprehensive security implementation ensures your ArgoCD instance meets enterprise-grade security standards while maintaining usability for development teams.

---

## 📚 Additional Resources

- [ArgoCD RBAC Documentation](https://argo-cd.readthedocs.io/en/stable/operator-manual/rbac/)
- [ArgoCD SSO Configuration](https://argo-cd.readthedocs.io/en/stable/operator-manual/user-management/)
- [GitHub OAuth Apps](https://docs.github.com/en/developers/apps/building-oauth-apps)
- [ArgoCD Projects](https://argo-cd.readthedocs.io/en/stable/user-guide/projects/)
- [Enterprise Security Best Practices](https://argo-cd.readthedocs.io/en/stable/operator-manual/security/) 