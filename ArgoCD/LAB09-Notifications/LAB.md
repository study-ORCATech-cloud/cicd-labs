# Lab Instructions for LAB09: ArgoCD Notifications - Comprehensive Monitoring and Alerting

This document provides detailed step-by-step instructions for setting up comprehensive ArgoCD notifications across multiple channels including Slack, email, webhooks, and Microsoft Teams. You'll learn how to create intelligent alerting that keeps your team informed without causing alert fatigue.

We will start by setting up the notifications controller, then configure multiple notification channels, create custom templates, and test various notification scenarios.

---

## 🚀 Lab Steps

### Phase 1: Copy Lab Materials and Install ArgoCD Notifications Controller

**1. Create Directory Structure:**
   ```bash
   mkdir -p notification-controller notification-configs/{notifiers,templates,triggers} secrets test-scenarios scripts
   ```

**2. Copy ArgoCD Notifications Controller Configuration:**
   a. Copy the notifications controller deployment:
      ```bash
      cp notification-controller/argocd-notifications-controller.yaml ./
      ```
   
   b. Review the controller configuration:
      ```bash
      cat notification-controller/argocd-notifications-controller.yaml
      ```

   c. Copy RBAC for notifications controller:
      ```bash
      cp notification-controller/argocd-notifications-rbac.yaml ./
      ```
   
   d. Review the RBAC configuration:
      ```bash
      cat notification-controller/argocd-notifications-rbac.yaml
      ```

**3. Deploy Notifications Controller:**
   ```bash
   kubectl apply -f notification-controller/argocd-notifications-rbac.yaml
   kubectl apply -f notification-controller/argocd-notifications-controller.yaml
   ```

**4. Verify Installation:**
   ```bash
   kubectl get pods -n argocd | grep notifications
   kubectl logs -n argocd deployment/argocd-notifications-controller
   ```

### Phase 2: Set Up Slack Integration

**5. Create Slack Webhook (Prerequisites):**
   a. Go to your Slack workspace
   b. Navigate to Apps → Incoming Webhooks
   c. Click "Add to Slack" and select a channel (e.g., #argocd-alerts)
   d. Copy the webhook URL (format: https://hooks.slack.com/services/...)

**6. Copy and Configure Slack Webhook Secret:**
   ```bash
   cp secrets/slack-webhook-secret.yaml ./
   ```

**7. Update Slack Webhook URL:**
   ```bash
   # Replace with your actual Slack webhook URL
   SLACK_WEBHOOK="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
   sed -i "s|YOUR_SLACK_WEBHOOK_URL_HERE|$SLACK_WEBHOOK|g" secrets/slack-webhook-secret.yaml
   ```

**8. Review and Apply Slack Secret:**
   ```bash
   cat secrets/slack-webhook-secret.yaml
   kubectl apply -f secrets/slack-webhook-secret.yaml
   ```

### Phase 3: Copy and Configure Notification Templates

**9. Copy Sync Event Templates:**
   ```bash
   cp notification-configs/templates/app-sync-templates.yaml ./
   ```

**10. Review Sync Templates:**
   ```bash
   cat notification-configs/templates/app-sync-templates.yaml
   ```

**11. Copy Health Event Templates:**
   ```bash
   cp notification-configs/templates/app-health-templates.yaml ./
   ```

**12. Review Health Templates:**
   ```bash
   cat notification-configs/templates/app-health-templates.yaml
   ```

**13. Copy Environment-Specific Templates:**
   ```bash
   cp notification-configs/templates/environment-templates.yaml ./
   ```

**14. Review Environment Templates:**
   ```bash
   cat notification-configs/templates/environment-templates.yaml
   ```

### Phase 4: Configure Notification Triggers

**15. Copy Production Triggers:**
   ```bash
   cp notification-configs/triggers/production-triggers.yaml ./
   ```

**16. Review Production Triggers:**
   ```bash
   cat notification-configs/triggers/production-triggers.yaml
   ```

**17. Copy Staging Triggers:**
   ```bash
   cp notification-configs/triggers/staging-triggers.yaml ./
   ```

**18. Review Staging Triggers:**
   ```bash
   cat notification-configs/triggers/staging-triggers.yaml
   ```

**19. Copy Global Triggers:**
   ```bash
   cp notification-configs/triggers/global-triggers.yaml ./
   ```

**20. Review Global Triggers:**
   ```bash
   cat notification-configs/triggers/global-triggers.yaml
   ```

### Phase 5: Deploy Master Notifications Configuration

**21. Copy Master Configuration:**
   ```bash
   cp notification-configs/master-notifications-config.yaml ./
   ```

**22. Review Master Configuration:**
   ```bash
   cat notification-configs/master-notifications-config.yaml
   ```

**23. Apply Master Configuration:**
   ```bash
   kubectl apply -f notification-configs/master-notifications-config.yaml
   ```

**24. Verify Configuration:**
   ```bash
   kubectl get configmap argocd-notifications-cm -n argocd -o yaml
   ```

### Phase 6: Configure Additional Notifiers (Optional)

**25. Copy Slack Notifier:**
   ```bash
   cp notification-configs/notifiers/slack-notifier.yaml ./
   ```

**26. Copy Email Notifier:**
   ```bash
   cp notification-configs/notifiers/email-notifier.yaml ./
   ```

**27. Copy Webhook Notifier:**
   ```bash
   cp notification-configs/notifiers/webhook-notifier.yaml ./
   ```

**28. Copy Teams Notifier:**
   ```bash
   cp notification-configs/notifiers/teams-notifier.yaml ./
   ```

**29. Review Additional Notifiers:**
   ```bash
   cat notification-configs/notifiers/slack-notifier.yaml
   cat notification-configs/notifiers/email-notifier.yaml
   cat notification-configs/notifiers/webhook-notifier.yaml
   cat notification-configs/notifiers/teams-notifier.yaml
   ```

### Phase 7: Deploy Test Applications

**30. Copy Test Applications:**
   ```bash
   cp test-scenarios/test-app-healthy.yaml ./
   cp test-scenarios/test-app-sync-failed.yaml ./
   cp test-scenarios/test-app-production.yaml ./
   ```

**31. Review Test Applications:**
   ```bash
   cat test-scenarios/test-app-healthy.yaml
   cat test-scenarios/test-app-sync-failed.yaml
   cat test-scenarios/test-app-production.yaml
   ```

**32. Deploy Test Applications:**
   ```bash
   kubectl apply -f test-scenarios/test-app-healthy.yaml
   kubectl apply -f test-scenarios/test-app-production.yaml
   ```

**33. Verify Test Applications:**
   ```bash
   kubectl get applications -n argocd | grep test-notifications
   ```

### Phase 8: Test Notification Scenarios

**34. Use Setup Script (Optional):**
   ```bash
   cp scripts/setup-notifications.sh ./
   chmod +x scripts/setup-notifications.sh
   ./scripts/setup-notifications.sh
   ```

**35. Use Test Script:**
   ```bash
   cp scripts/test-notifications.sh ./
   chmod +x scripts/test-notifications.sh
   ./scripts/test-notifications.sh
   ```

**36. Monitor Notifications:**
   ```bash
   # Watch controller logs
   kubectl logs -n argocd deployment/argocd-notifications-controller -f
   
   # Check application status
   kubectl get applications -n argocd
   
   # Trigger manual sync for production app
   kubectl patch app test-notifications-production -n argocd --type merge -p '{"operation":{"sync":{}}}'
   ```

**37. Test Failure Scenarios:**
   ```bash
   # Deploy failing application
   kubectl apply -f test-scenarios/test-app-sync-failed.yaml
   
   # Watch for failure notifications in Slack
   kubectl get applications -n argocd test-notifications-sync-fail
   ```

### Phase 9: Advanced Testing and Validation

**38. Test Environment-Based Routing:**
   ```bash
   # Check production alerts
   kubectl get app test-notifications-production -n argocd -o yaml | grep -A 10 status
   
   # Check staging notifications
   kubectl get app test-notifications-healthy -n argocd -o yaml | grep -A 10 status
   ```

**39. Validate Notification Delivery:**
   ```bash
   # Check controller metrics
   kubectl port-forward -n argocd svc/argocd-notifications-controller-metrics 9001:9001 &
   curl http://localhost:9001/metrics | grep notification
   ```

**40. Test Manual Triggers:**
   ```bash
   # Add manual notification annotation
   kubectl annotate app test-notifications-healthy -n argocd \
     notifications.argoproj.io/subscribe.on-sync-succeeded.slack=""
   
   # Trigger sync
   kubectl patch app test-notifications-healthy -n argocd --type merge -p '{"operation":{"sync":{}}}'
   ```

---

## 🧪 Validation Checklist

### ✅ **Controller Installation**
- [ ] Notifications controller pod is running
- [ ] Controller logs show no errors
- [ ] RBAC permissions are correctly applied
- [ ] Metrics endpoint is accessible

### ✅ **Slack Integration**
- [ ] Slack webhook secret is created
- [ ] Slack service configuration is applied
- [ ] Test message can be sent to Slack channel
- [ ] Slack templates render correctly

### ✅ **Template Configuration**
- [ ] Sync success templates work
- [ ] Sync failure templates work
- [ ] Health degradation templates work
- [ ] Environment-specific templates work
- [ ] Rich formatting (attachments, colors) displays correctly

### ✅ **Trigger Configuration**
- [ ] Production triggers fire for production apps
- [ ] Staging triggers fire for staging apps
- [ ] Global triggers work across environments
- [ ] Label-based filtering works correctly

### ✅ **Test Application Deployment**
- [ ] Healthy test app deploys successfully
- [ ] Production test app triggers appropriate notifications
- [ ] Failing test app triggers failure notifications
- [ ] Application annotations are correctly configured

### ✅ **Notification Delivery**
- [ ] Sync success notifications arrive in Slack
- [ ] Sync failure notifications arrive in Slack
- [ ] Health status notifications arrive in Slack
- [ ] Production alerts include @channel mentions
- [ ] Environment-specific routing works

### ✅ **Advanced Scenarios**
- [ ] Label-based notification routing
- [ ] Manual trigger annotations work
- [ ] Multiple notification channels (if configured)
- [ ] Notification escalation for production
- [ ] Template customization works

---

## 🧹 Cleanup

**41. Use Cleanup Script:**
   ```bash
   cp scripts/cleanup-notifications.sh ./
   chmod +x scripts/cleanup-notifications.sh
   ./scripts/cleanup-notifications.sh
   ```

**42. Manual Cleanup (Alternative):**
   ```bash
   # Remove test applications
   kubectl delete -f test-scenarios/ --ignore-not-found=true
   
   # Remove notifications configuration
   kubectl delete -f notification-configs/master-notifications-config.yaml --ignore-not-found=true
   
   # Remove secrets
   kubectl delete -f secrets/slack-webhook-secret.yaml --ignore-not-found=true
   
   # Remove controller
   kubectl delete -f notification-controller/ --ignore-not-found=true
   
   # Clean up test namespaces
   kubectl delete namespace test-notifications test-notifications-fail test-notifications-prod --ignore-not-found=true
   ```

**43. Verify Cleanup:**
   ```bash
   kubectl get pods -n argocd | grep notifications
   kubectl get applications -n argocd | grep test-notifications
   kubectl get configmap argocd-notifications-cm -n argocd
   ```

---

## 🎯 Key Learning Outcomes

By completing this lab, you have learned:

1. **ArgoCD Notifications Architecture**: Understanding the notifications controller, templates, triggers, and services
2. **Multi-Channel Integration**: Configuring Slack, email, webhooks, and Teams notifications
3. **Template Customization**: Creating rich, contextual notification templates with dynamic content
4. **Intelligent Triggering**: Implementing environment-based and label-based notification routing
5. **Production Readiness**: Setting up escalation, alert fatigue prevention, and monitoring
6. **Testing Strategies**: Validating notification delivery and troubleshooting issues
7. **Operational Excellence**: Implementing notifications that enhance rather than overwhelm team productivity

This comprehensive notifications system ensures your team stays informed about critical GitOps events while maintaining focus on development and operations tasks.

---

## 📚 Additional Resources

- [ArgoCD Notifications Documentation](https://argocd-notifications.readthedocs.io/)
- [Slack Incoming Webhooks](https://api.slack.com/messaging/webhooks)
- [ArgoCD Templating Guide](https://argocd-notifications.readthedocs.io/en/stable/templates/)
- [Notification Triggers Reference](https://argocd-notifications.readthedocs.io/en/stable/triggers/)
- [Production Notification Best Practices](https://argocd-notifications.readthedocs.io/en/stable/services/overview/) 